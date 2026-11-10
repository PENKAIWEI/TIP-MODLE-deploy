"""Supervise the existing TIP launchers without sending ROS motion commands here."""

from __future__ import annotations

import copy
import fcntl
import json
import math
import os
import re
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .config import (
    MODEL_PORT,
    MODEL_TOKEN_FILE,
    MODEL_URL,
    POLICIES,
    ROOT,
    RUNS,
    bridge_environment,
    model_environment,
)


EXECUTION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
TERMINAL = {"COMPLETED", "STOPPED", "TIMED_OUT", "FAILED", "UNKNOWN"}
HARDWARE_COMMANDS = {
    "camera": ["bash", "hardware/cameras_ws/launch.sh"],
    "hand": ["bash", "hardware/hand_ws/launch.sh", "--confirm-motion"],
    "arm": ["bash", "hardware/arm_ws/start_model_control.sh", "--confirm-motion"],
}


class ApiError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

    def response(self) -> dict:
        return {"accepted": False, "error": {"code": self.code, "message": self.message}}


@dataclass
class Slot:
    process: subprocess.Popen[str]
    role: str
    log_path: Path
    execution_id: str | None = None
    policy_id: str | None = None
    events: set[str] = field(default_factory=set)
    reason: str | None = None
    stop_requested: bool = False
    reader: threading.Thread | None = None


class Runtime:
    """One Agent API process owns one active Bridge operation at a time."""

    def __init__(self, root: Path = ROOT, runs: Path = RUNS):
        if os.name != "posix":
            raise RuntimeError("The Agent API must run on the Ubuntu deployment host")
        self.root = root
        self.runs = runs
        self.runs.mkdir(parents=True, exist_ok=True)
        self._lease = (self.runs / "server.lock").open("w")
        try:
            fcntl.flock(self._lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another Agent API server already owns this deployment") from exc
        self._lock = threading.RLock()
        self._changed = threading.Condition(self._lock)
        self._hardware_start_lock = threading.Lock()
        self._model_switch_lock = threading.Lock()
        self._hardware: dict[str, Slot] = {}
        self._hardware_external: dict[str, bool] = {}
        self._hardware_ready = False
        self._hardware_reason: str | None = "start_hardware has not completed"
        self._model: Slot | None = None
        self._model_policy: str | None = None
        self._active: Slot | None = None
        self._pending_reset: str | None = None
        self._records: dict[str, dict] = {}
        self._latest_policy: dict[str, str] = {}
        self._journal = self.runs / "executions.jsonl"
        self._load_records()

    def _load_records(self) -> None:
        if not self._journal.exists():
            return
        for line in self._journal.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
                if not all(key in record for key in ("execution_id", "kind", "state", "updated_at")):
                    continue
                self._records[record["execution_id"]] = record
            except (ValueError, KeyError, TypeError):
                continue
        for record in self._records.values():
            if record["state"] not in TERMINAL:
                record["state"] = "UNKNOWN"
                record["stop_status"] = "UNCONFIRMED"
                record["reason"] = "Agent API restarted before this execution reached a known result"
                self._save(record)
            if record["kind"] == "policy":
                policy_id = record["policy_id"]
                previous = self._latest_policy.get(policy_id)
                if previous is None or record["updated_at"] > self._records[previous]["updated_at"]:
                    self._latest_policy[policy_id] = record["execution_id"]

    def _save(self, record: dict) -> None:
        record["updated_at"] = datetime.now(timezone.utc).isoformat()
        with self._journal.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _validate_id(value: object) -> str:
        if not isinstance(value, str) or not EXECUTION_ID.fullmatch(value):
            raise ApiError("INVALID_ARGUMENT", "execution_id must be 1-128 safe ASCII characters")
        return value

    @staticmethod
    def _positive_seconds(value: object, name: str) -> float:
        try:
            seconds = float(value) if type(value) in (int, float) else math.nan
        except (OverflowError, ValueError):
            seconds = math.nan
        if not math.isfinite(seconds) or seconds <= 0:
            raise ApiError("INVALID_ARGUMENT", f"{name} must be a positive finite number of seconds")
        return seconds

    @staticmethod
    def _validate_policy(value: object) -> str:
        if not isinstance(value, str) or value not in POLICIES:
            raise ApiError("INVALID_ARGUMENT", "policy_id must be pour_tea or serve_tea")
        return value

    def _new_record(self, execution_id: str, kind: str, policy_id: str | None = None) -> dict:
        if execution_id in self._records:
            raise ApiError("DUPLICATE_EXECUTION_ID", "execution_id has already been used")
        record = {
            "execution_id": execution_id,
            "kind": kind,
            "policy_id": policy_id,
            "state": "QUEUED",
            "stop_status": "NOT_REQUESTED",
            "reason": None,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "finished_at": None,
            "log_path": None,
        }
        self._records[execution_id] = record
        if policy_id is not None:
            self._latest_policy[policy_id] = execution_id
        self._save(record)
        return record

    def _spawn(
        self,
        role: str,
        command: list[str],
        env: dict[str, str],
        execution_id: str | None = None,
        policy_id: str | None = None,
        start_watchers: bool = True,
    ) -> Slot:
        process = subprocess.Popen(
            command,
            cwd=self.root,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            start_new_session=True,
        )
        log_path = self.runs / f"{role}_{process.pid}.log"
        slot = Slot(process, role, log_path, execution_id, policy_id)
        if start_watchers:
            self._start_watchers(slot)
        return slot

    def _start_watchers(self, slot: Slot) -> None:
        slot.reader = threading.Thread(target=self._read_output, args=(slot,), daemon=True)
        slot.reader.start()
        threading.Thread(target=self._watch_process, args=(slot,), daemon=True).start()

    def _read_output(self, slot: Slot) -> None:
        assert slot.process.stdout is not None
        with slot.log_path.open("a", encoding="utf-8", newline="\n") as log:
            for line in slot.process.stdout:
                log.write(line)
                log.flush()
                print(f"[{slot.role}:{slot.process.pid}] {line.rstrip()}", flush=True)
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(event, dict) or not isinstance(event.get("event"), str):
                    continue
                with self._changed:
                    slot.events.add(event["event"])
                    if event["event"] in ("controller_blocked", "hand_hold_unavailable"):
                        slot.reason = str(event.get("reason", event["event"]))
                    if slot.execution_id and self._active is slot:
                        record = self._records[slot.execution_id]
                        if event["event"] == "controller_start":
                            record["state"] = "RUNNING"
                            self._save(record)
                        elif event["event"] == "outputs_stopped":
                            record["stop_status"] = "OUTPUTS_STOPPED"
                            self._save(record)
                    self._changed.notify_all()
        slot.process.stdout.close()

    def _watch_process(self, slot: Slot) -> None:
        returncode = slot.process.wait()
        if slot.reader is not None:
            slot.reader.join(timeout=5)
        with self._changed:
            if self._active is slot and slot.execution_id:
                record = self._records[slot.execution_id]
                if slot.stop_requested:
                    record["state"] = "STOPPED" if returncode in (0, 130, -15) else "FAILED"
                    record["reason"] = slot.reason or "Stop requested"
                elif slot.role == "reset" and returncode == 0 and "reset_complete" in slot.events:
                    record["state"] = "COMPLETED"
                elif slot.role == "infer" and returncode == 0 and "inference_complete" in slot.events:
                    record["state"] = "TIMED_OUT"
                    record["reason"] = "max_duration_s elapsed; task success is not inferred"
                else:
                    record["state"] = "FAILED"
                    record["reason"] = slot.reason or f"Bridge process exited with code {returncode}"
                record["finished_at"] = datetime.now(timezone.utc).isoformat()
                # This confirms that this Bridge process can no longer publish.
                # It does not claim that the physical joints are stationary.
                record["stop_status"] = "CONFIRMED"
                record["stop_basis"] = "bridge_process_exited"
                self._save(record)
                self._active = None
            self._changed.notify_all()

    def _controller_lock_available(self) -> bool:
        path = self.root / "model_hardware_bridge" / "runs" / "controller.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as lease:
            try:
                fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            fcntl.flock(lease, fcntl.LOCK_UN)
        return True

    def _ros_nodes(self) -> set[str]:
        result = subprocess.run(
            ["bash", "-lc", 'source "${ROS_SETUP:-/opt/ros/jazzy/setup.bash}" && ros2 node list --no-daemon --spin-time 2'],
            cwd=self.root,
            env=bridge_environment(os.environ),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=12,
            check=False,
        )
        if result.returncode:
            raise ApiError("ROS_UNAVAILABLE", result.stderr.strip() or "Cannot inspect ROS nodes")
        return set(result.stdout.splitlines())

    def _probe_hardware(self) -> tuple[bool, str | None]:
        try:
            result = subprocess.run(
                ["bash", "model_hardware_bridge/scripts/bridge.sh", "observe", "--duration", "1"],
                cwd=self.root,
                env=bridge_environment(os.environ),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=25,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, "Read-only Bridge observation timed out"
        reason = None
        ready = False
        for line in result.stdout.splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict):
                if event.get("event") == "observation_ready":
                    ready = True
                if event.get("event") == "controller_blocked":
                    reason = str(event.get("reason", "Observation unavailable"))
        return ready and result.returncode == 0, reason or (None if ready else "Observation unavailable")

    def _hardware_status(self) -> dict:
        devices = {}
        issues = []
        for role in HARDWARE_COMMANDS:
            slot = self._hardware.get(role)
            running = bool(slot and slot.process.poll() is None)
            reason = f"launcher exited with code {slot.process.returncode}" if slot and not running else None
            devices[role] = {
                "running": running or self._hardware_external.get(role, False),
                "managed": running,
                "log_path": str(slot.log_path) if slot else None,
                "reason": reason,
            }
            if reason:
                issues.append({"device": role, "reason": reason})
        if self._hardware_reason:
            lower = self._hardware_reason.lower()
            if "hand" in lower or "o10" in lower or re.search(r"\b[lr]h\b", lower):
                device = "hand"
            elif "arm" in lower or re.search(r"\b[lr]a\b", lower):
                device = "arm"
            elif "camera" in lower or "image" in lower or "wrist" in lower:
                device = "camera"
            else:
                device = "observation"
            issues.append({"device": device, "reason": self._hardware_reason})
            if device in devices and devices[device]["reason"] is None:
                devices[device]["reason"] = self._hardware_reason
        return {"ready": self._hardware_ready, "devices": devices, "issues": issues, "reason": self._hardware_reason}

    def start_hardware(self, ready_timeout_s: object = 90) -> dict:
        timeout = self._positive_seconds(ready_timeout_s, "ready_timeout_s")
        with self._hardware_start_lock:
            with self._lock:
                if self._active is not None or self._pending_reset is not None:
                    raise ApiError("RESOURCE_BUSY", "A Bridge execution is active")
            nodes = self._ros_nodes()
            self._hardware_external = {
                "camera": any("/cam" in name for name in nodes),
                "hand": "/omnihand_o10_hardware_provider" in nodes or "/o10_control_node" in nodes,
                "arm": "/arm_model_control_node" in nodes,
            }
            with self._lock:
                for role, command in HARDWARE_COMMANDS.items():
                    slot = self._hardware.get(role)
                    if (slot and slot.process.poll() is None) or self._hardware_external[role]:
                        continue
                    env = dict(os.environ)
                    env.pop("CONDA_PREFIX", None)
                    env.pop("DEXHIT_COLLECTION_PREFIX", None)
                    try:
                        self._hardware[role] = self._spawn(role, command, env)
                    except OSError as exc:
                        self._hardware_ready = False
                        self._hardware_reason = f"Cannot launch {role}: {exc}"
                        print(f"[agent_api] {self._hardware_reason}", flush=True)
                        return self._hardware_status()
            deadline = time.monotonic() + timeout
            reason = "Hardware feedback did not become ready"
            while time.monotonic() < deadline:
                with self._lock:
                    exited = [name for name, slot in self._hardware.items() if slot.process.poll() is not None]
                if exited:
                    reason = "Hardware launcher exited: " + ", ".join(exited)
                    break
                if not self._controller_lock_available():
                    reason = "Another Bridge controller owns the hardware"
                    break
                ready, probe_reason = self._probe_hardware()
                if ready:
                    with self._lock:
                        self._hardware_ready = True
                        self._hardware_reason = None
                        return self._hardware_status()
                reason = probe_reason or reason
                time.sleep(min(2, max(0, deadline - time.monotonic())))
            with self._lock:
                self._hardware_ready = False
                self._hardware_reason = reason
                print(f"[agent_api] hardware not ready: {reason}", flush=True)
                return self._hardware_status()

    def _model_status(self) -> dict:
        with MODEL_TOKEN_FILE.open("r", encoding="utf-8") as stream:
            token = stream.read().strip()
        if not token:
            raise ValueError("Model token file is empty")
        request = urllib.request.Request(
            MODEL_URL + "/status", headers={"Authorization": "Bearer " + token}
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            return json.load(response)

    @staticmethod
    def _port_open() -> bool:
        try:
            with socket.create_connection(("127.0.0.1", MODEL_PORT), timeout=0.3):
                return True
        except OSError:
            return False

    def check_policy(self, policy_id: object) -> dict:
        policy_id = self._validate_policy(policy_id)
        with self._model_switch_lock:
            with self._lock:
                active = self._active
                if active and active.role == "infer" and active.policy_id != policy_id:
                    return self._policy_response(policy_id, "BUSY", False, "Another policy is running")
                old = self._model
                old_policy = self._model_policy
            if old and old_policy != policy_id and old.process.poll() is None:
                old.process.terminate()
                try:
                    old.process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    return self._policy_response(policy_id, "BUSY", False, "Previous model service did not exit")
            with self._lock:
                current = self._model
                if current is not None and self._model_policy == policy_id and current.process.poll() is not None:
                    return self._policy_response(policy_id, "ERROR", False, f"Model service exited; see {current.log_path}")
                if current is None or self._model_policy != policy_id:
                    if self._port_open():
                        return self._policy_response(policy_id, "ERROR", False, "Model port 18774 is occupied by an unmanaged service")
                    env = model_environment(policy_id, os.environ)
                    self._model = self._spawn(
                        "model_" + policy_id,
                        ["bash", "model_hardware_bridge/scripts/model_server.sh", "--host", "127.0.0.1", "--port", str(MODEL_PORT)],
                        env,
                        policy_id=policy_id,
                    )
                    self._model_policy = policy_id
                model = self._model
            if model.process.poll() is not None:
                return self._policy_response(policy_id, "ERROR", False, f"Model service exited; see {model.log_path}")
            try:
                status = self._model_status()
            except (FileNotFoundError, PermissionError, ValueError, urllib.error.HTTPError) as exc:
                return self._policy_response(policy_id, "ERROR", False, f"Model status check failed: {type(exc).__name__}")
            except Exception as exc:
                return self._policy_response(policy_id, "LOADING", False, f"Model is loading: {type(exc).__name__}")
            expected = POLICIES[policy_id]
            contract = (status.get("schema"), status.get("state_dim"), status.get("physical_action_dim"), status.get("model_action_dim"))
            if contract != ("sandisk100_dual_o10_v1", 46, 34, 48) or status.get("checkpoint") != expected.checkpoint or status.get("prompt") != expected.prompt:
                return self._policy_response(policy_id, "ERROR", False, "Model status does not match policy contract")
            if not status.get("ready") or not status.get("live_budget_ok"):
                return self._policy_response(policy_id, "NOT_READY", False, "Model warmup or live latency budget failed")
            with self._lock:
                hardware_alive = all(slot.process.poll() is None for slot in self._hardware.values())
                can_start = self._hardware_ready and hardware_alive and self._active is None and self._pending_reset is None
                reason = None if can_start else "Hardware is not ready or another execution is active"
                return self._policy_response(policy_id, "READY", can_start, reason)

    def _policy_response(self, policy_id: str, model_state: str, can_start: bool, reason: str | None) -> dict:
        with self._lock:
            execution_id = self._latest_policy.get(policy_id)
            return {
                "policy_id": policy_id,
                "model_state": model_state,
                "model_ready": model_state == "READY",
                "can_start": can_start,
                "reason": reason,
                "active_execution_id": self._active.execution_id if self._active else None,
                "execution": copy.deepcopy(self._records.get(execution_id)) if execution_id else None,
            }

    def _start_bridge(self, record: dict, role: str, options: list[str], policy_id: str | None) -> None:
        if not self._controller_lock_available():
            raise ApiError("RESOURCE_BUSY", "Another Bridge controller owns this deployment")
        command = ["bash", "model_hardware_bridge/scripts/bridge.sh", role, "--execute", "--confirm-motion", *options]
        slot = self._spawn(
            role, command, bridge_environment(os.environ), record["execution_id"], policy_id,
            start_watchers=False,
        )
        self._active = slot
        record["state"] = "STARTING"
        record["log_path"] = str(slot.log_path)
        self._save(record)
        self._start_watchers(slot)

    def start_policy(self, execution_id: object, policy_id: object, params: object, max_duration_s: object) -> dict:
        with self._model_switch_lock:
            return self._start_policy_under_model_lock(execution_id, policy_id, params, max_duration_s)

    def _start_policy_under_model_lock(self, execution_id: object, policy_id: object, params: object, max_duration_s: object) -> dict:
        execution_id = self._validate_id(execution_id)
        policy_id = self._validate_policy(policy_id)
        duration = self._positive_seconds(max_duration_s, "max_duration_s")
        if params != {}:
            raise ApiError("INVALID_ARGUMENT", "params must be an empty object for the current fixed-prompt models")
        with self._lock:
            if execution_id in self._records:
                raise ApiError("DUPLICATE_EXECUTION_ID", "execution_id has already been used")
            if not self._hardware_ready:
                raise ApiError("HARDWARE_NOT_READY", self._hardware_reason or "Call start_hardware first")
            dead_hardware = [name for name, slot in self._hardware.items() if slot.process.poll() is not None]
            if dead_hardware:
                raise ApiError("HARDWARE_NOT_READY", "Hardware launcher exited: " + ", ".join(dead_hardware))
            if self._active is not None or self._pending_reset is not None:
                raise ApiError("RESOURCE_BUSY", "Another Bridge execution is active")
            if self._model_policy != policy_id or self._model is None or self._model.process.poll() is not None:
                raise ApiError("MODEL_NOT_READY", "Call check_policy until the requested model is ready")
        try:
            status = self._model_status()
        except Exception as exc:
            raise ApiError("MODEL_NOT_READY", f"Cannot reach model status: {type(exc).__name__}") from exc
        if not status.get("ready") or not status.get("live_budget_ok") or status.get("checkpoint") != POLICIES[policy_id].checkpoint:
            raise ApiError("MODEL_NOT_READY", "Model is not ready for this policy")
        with self._lock:
            if self._active is not None or self._pending_reset is not None:
                raise ApiError("RESOURCE_BUSY", "Another Bridge execution is active")
            record = self._new_record(execution_id, "policy", policy_id)
            try:
                self._start_bridge(record, "infer", ["--duration", str(duration)], policy_id)
            except Exception as exc:
                record["state"] = "FAILED"
                record["reason"] = str(exc)
                record["finished_at"] = datetime.now(timezone.utc).isoformat()
                self._save(record)
                raise
            return {"accepted": True, "execution_id": execution_id, "state": record["state"], "reason": None}

    def reset_to_initial(self, execution_id: object, timeout_s: object = 60) -> dict:
        execution_id = self._validate_id(execution_id)
        timeout = self._positive_seconds(timeout_s, "timeout_s")
        with self._changed:
            if execution_id in self._records:
                record = self._records[execution_id]
                if record["kind"] != "reset":
                    raise ApiError("DUPLICATE_EXECUTION_ID", "execution_id belongs to another operation")
                retry_deadline = time.monotonic() + timeout + 50
                while record["state"] not in TERMINAL and time.monotonic() < retry_deadline:
                    self._changed.wait(timeout=min(1, retry_deadline - time.monotonic()))
                return copy.deepcopy(record)
            if not self._hardware_ready:
                raise ApiError("HARDWARE_NOT_READY", self._hardware_reason or "Call start_hardware first")
            if self._pending_reset is not None:
                raise ApiError("RESOURCE_BUSY", "Another reset request is queued")
            if self._active is not None and not self._active.stop_requested:
                raise ApiError("RESOURCE_BUSY", "Stop the active execution before resetting")
            record = self._new_record(execution_id, "reset")
            self._pending_reset = execution_id
            deadline = time.monotonic() + 20
            while self._active is not None and record["state"] != "STOPPED" and time.monotonic() < deadline:
                self._changed.wait(timeout=min(1, deadline - time.monotonic()))
            if record["state"] == "STOPPED":
                return copy.deepcopy(record)
            if self._active is not None:
                record["state"] = "FAILED"
                record["reason"] = "Previous Bridge execution did not release control"
                record["finished_at"] = datetime.now(timezone.utc).isoformat()
                self._pending_reset = None
                self._save(record)
                self._changed.notify_all()
                return copy.deepcopy(record)
            try:
                self._start_bridge(record, "reset", ["--reset-timeout", str(timeout)], None)
            except Exception as exc:
                record["state"] = "FAILED"
                record["reason"] = str(exc)
                record["finished_at"] = datetime.now(timezone.utc).isoformat()
                self._save(record)
                self._pending_reset = None
                self._changed.notify_all()
                raise
            self._pending_reset = None
            self._changed.notify_all()
            deadline = time.monotonic() + timeout + 30
            while record["state"] not in TERMINAL and time.monotonic() < deadline:
                self._changed.wait(timeout=min(1, deadline - time.monotonic()))
            if record["state"] not in TERMINAL:
                self._request_stop(self._active)
                stop_deadline = time.monotonic() + 10
                while record["state"] not in TERMINAL and time.monotonic() < stop_deadline:
                    self._changed.wait(timeout=min(1, stop_deadline - time.monotonic()))
                if record["state"] not in TERMINAL:
                    return {**copy.deepcopy(record), "reason": "Reset deadline elapsed; stop requested, final state pending"}
            return copy.deepcopy(record)

    def _request_stop(self, slot: Slot | None) -> None:
        if slot is None or slot.execution_id is None:
            raise ApiError("NOT_ACTIVE", "No matching Bridge execution is active")
        if slot.stop_requested:
            return
        slot.stop_requested = True
        record = self._records[slot.execution_id]
        record["state"] = "STOPPING"
        record["stop_status"] = "REQUESTED"
        self._save(record)
        if slot.process.poll() is None:
            try:
                slot.process.terminate()
            except ProcessLookupError:
                pass
        self._changed.notify_all()

    def stop_policy(self, execution_id: object) -> dict:
        execution_id = self._validate_id(execution_id)
        with self._changed:
            slot = self._active
            if slot is None or slot.execution_id != execution_id or slot.role != "infer":
                raise ApiError("NOT_ACTIVE", "This execution_id is not the active policy")
            self._request_stop(slot)
            return {"accepted": True, "execution_id": execution_id, "stop_status": "REQUESTED"}

    def stop_motion(self, execution_id: object) -> dict:
        execution_id = self._validate_id(execution_id)
        with self._changed:
            if self._pending_reset == execution_id and (
                self._active is None or self._active.execution_id != execution_id
            ):
                record = self._records[execution_id]
                record["state"] = "STOPPED"
                record["stop_status"] = "CONFIRMED"
                record["stop_basis"] = "canceled_before_start"
                record["reason"] = "Reset canceled before motion began"
                record["finished_at"] = datetime.now(timezone.utc).isoformat()
                self._pending_reset = None
                self._save(record)
                self._changed.notify_all()
                return {"accepted": True, "execution_id": execution_id, "stop_status": "CONFIRMED"}
            slot = self._active
            if slot is None or slot.execution_id != execution_id:
                raise ApiError("NOT_ACTIVE", "This execution_id is not the active Bridge execution")
            self._request_stop(slot)
            return {"accepted": True, "execution_id": execution_id, "stop_status": "REQUESTED"}

    def health(self) -> dict:
        with self._lock:
            return {
                "hardware": self._hardware_status(),
                "model_policy": self._model_policy,
                "model_process_running": bool(self._model and self._model.process.poll() is None),
                "active_execution_id": self._active.execution_id if self._active else None,
            }

    def close(self) -> None:
        """Stop owned children in Bridge, model, hardware order on API shutdown."""
        with self._changed:
            active = self._active
            if active is not None:
                self._request_stop(active)
        if active is not None:
            try:
                active.process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                try:
                    active.process.kill()
                    active.process.wait(timeout=5)
                except ProcessLookupError:
                    pass
                print("[agent_api] Bridge required forced exit; hardware launchers remain running for inspection", flush=True)
                self._lease.close()
                return
        with self._lock:
            children = [self._model] + [self._hardware.get(role) for role in ("arm", "hand", "camera")]
        for slot in children:
            if slot is not None and slot.process.poll() is None:
                slot.process.terminate()
                try:
                    slot.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print(f"[agent_api] {slot.role} did not exit: pid={slot.process.pid}", flush=True)
        self._lease.close()
