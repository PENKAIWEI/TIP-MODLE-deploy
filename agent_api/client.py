"""Small standard-library client for an Agent using the local TIP HTTP API."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class AgentBridgeError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


class AgentBridgeClient:
    def __init__(self, base_url: str = "http://127.0.0.1:18776"):
        self.base_url = base_url.rstrip("/")

    def _request(self, route: str, payload: dict | None = None, timeout_s: float = 10) -> dict:
        body = None if payload is None else json.dumps(payload, allow_nan=False).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + route,
            data=body,
            headers={"Content-Type": "application/json"} if body is not None else {},
            method="GET" if body is None else "POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_s) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            try:
                result = json.load(exc)
                error = result.get("error", {})
                raise AgentBridgeError(str(error.get("code", exc.code)), str(error.get("message", exc.reason))) from exc
            except (ValueError, AttributeError):
                raise AgentBridgeError(str(exc.code), str(exc.reason)) from exc

    def health(self) -> dict:
        return self._request("/health")

    def start_hardware(self, ready_timeout_s: float = 90) -> dict:
        return self._request("/start_hardware", {"ready_timeout_s": ready_timeout_s}, ready_timeout_s + 60)

    def check_policy(self, policy_id: str) -> dict:
        return self._request("/check_policy", {"policy_id": policy_id}, 25)

    def reset_to_initial(self, execution_id: str, timeout_s: float = 60) -> dict:
        return self._request(
            "/reset_to_initial", {"execution_id": execution_id, "timeout_s": timeout_s}, timeout_s + 70
        )

    def start_policy(self, execution_id: str, policy_id: str, params: dict, max_duration_s: float) -> dict:
        return self._request(
            "/start_policy",
            {
                "execution_id": execution_id,
                "policy_id": policy_id,
                "params": params,
                "max_duration_s": max_duration_s,
            },
        )

    def stop_policy(self, execution_id: str) -> dict:
        return self._request("/stop_policy", {"execution_id": execution_id})

    def stop_motion(self, execution_id: str) -> dict:
        return self._request("/stop_motion", {"execution_id": execution_id})
