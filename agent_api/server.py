"""Local HTTP/JSON entry point for Agent calls."""

from __future__ import annotations

import argparse
import json
import signal
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .runtime import ApiError, Runtime


MAX_BODY = 16 * 1024
ROUTES = {
    "/start_hardware",
    "/check_policy",
    "/reset_to_initial",
    "/start_policy",
    "/stop_policy",
    "/stop_motion",
}


def _http_status(code: str) -> int:
    if code in ("INVALID_ARGUMENT", "DUPLICATE_EXECUTION_ID"):
        return 400
    if code == "NOT_ACTIVE":
        return 404
    if code == "RESOURCE_BUSY":
        return 409
    return 503


def make_handler(runtime: Runtime) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, format_string: str, *args: object) -> None:
            print("[agent_api] " + format_string % args, flush=True)

        def _reply(self, code: int, value: dict) -> None:
            payload = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:
            if self.path == "/health":
                self._reply(200, runtime.health())
            else:
                self._reply(404, {"error": {"code": "NOT_FOUND", "message": "Unknown route"}})

        def do_POST(self) -> None:
            if self.path not in ROUTES:
                return self._reply(404, {"error": {"code": "NOT_FOUND", "message": "Unknown route"}})
            if not self.headers.get("Content-Type", "").lower().startswith("application/json"):
                return self._reply(415, {"error": {"code": "UNSUPPORTED_MEDIA_TYPE", "message": "Use application/json"}})
            try:
                size = int(self.headers.get("Content-Length", ""))
                if not 0 < size <= MAX_BODY:
                    raise ValueError("Invalid JSON body length")
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError("JSON body must be an object")
            except (ValueError, UnicodeError) as exc:
                return self._reply(400, {"error": {"code": "INVALID_ARGUMENT", "message": str(exc)}})
            try:
                if self.path == "/start_hardware":
                    result = runtime.start_hardware(data.get("ready_timeout_s", 90))
                elif self.path == "/check_policy":
                    result = runtime.check_policy(data.get("policy_id"))
                elif self.path == "/reset_to_initial":
                    result = runtime.reset_to_initial(data.get("execution_id"), data.get("timeout_s", 60))
                elif self.path == "/start_policy":
                    result = runtime.start_policy(
                        data.get("execution_id"), data.get("policy_id"),
                        data.get("params"), data.get("max_duration_s"),
                    )
                elif self.path == "/stop_policy":
                    result = runtime.stop_policy(data.get("execution_id"))
                else:
                    result = runtime.stop_motion(data.get("execution_id"))
            except ApiError as exc:
                return self._reply(_http_status(exc.code), exc.response())
            except Exception as exc:
                print(f"[agent_api] request failed: {type(exc).__name__}: {exc}", flush=True)
                return self._reply(500, {"error": {"code": "INTERNAL_ERROR", "message": type(exc).__name__}})
            self._reply(200, result)

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description="TIP Agent-facing local HTTP API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18776)
    args = parser.parse_args()
    if args.host not in ("127.0.0.1", "localhost", "::1"):
        parser.error("Only loopback binding is supported; use an SSH tunnel for a remote Agent")
    runtime = Runtime()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(runtime))
    server.daemon_threads = True

    def stop(*_args: object) -> None:
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    print(f"[agent_api] listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
        runtime.close()


if __name__ == "__main__":
    main()
