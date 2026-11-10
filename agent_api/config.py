"""Deployment paths for the Agent-facing process supervisor.

This module contains paths and public model metadata only. Never put token
contents in this file or in API responses.
"""

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "model_hardware_bridge" / "runs" / "agent_api"
MODEL_ROOT = Path(
    "/home/hit/model_ckp/vtla_sandisk100_code_20261027/"
    "vtla_sandisk100_migration_20261027_164730"
)
MODEL_TOKEN_FILE = Path("/home/hit/model_ckp/sandisk100_inference/deploy/token")
MODEL_PORT = 18774
MODEL_URL = f"http://127.0.0.1:{MODEL_PORT}"


@dataclass(frozen=True)
class Policy:
    checkpoint: str
    prompt: str
    asset_id: str | None = None


POLICIES = {
    "pour_tea": Policy("/home/hit/model_ckp/23000", "Pour water."),
    "serve_tea": Policy(
        "/home/hit/桌面/demo02/c_10000",
        "Serve tea or move the teacup",
        "tip_dex02",
    ),
}


def model_environment(policy_id: str, inherited: dict[str, str]) -> dict[str, str]:
    policy = POLICIES[policy_id]
    env = dict(inherited)
    env.pop("CONDA_PREFIX", None)
    env.pop("DEXHIT_COLLECTION_PREFIX", None)
    env.pop("TIP_MODEL_ASSET_ID", None)
    env.pop("TIP_MODEL_PROMPT", None)
    env.update(
        TIP_MODEL_PYTHON=str(MODEL_ROOT / ".venv" / "bin" / "python"),
        TIP_OPENPI_SRC=str(MODEL_ROOT / "src"),
        TIP_OPENPI_CLIENT_SRC=str(MODEL_ROOT / "packages" / "openpi-client" / "src"),
        TIP_MODEL_CHECKPOINT=policy.checkpoint,
        TIP_MODEL_TOKEN_FILE=str(MODEL_TOKEN_FILE),
        OPENPI_DATA_HOME=str(MODEL_ROOT / "bundled_cache"),
    )
    if policy.asset_id:
        env["TIP_MODEL_ASSET_ID"] = policy.asset_id
    if policy_id == "serve_tea":
        env["TIP_MODEL_PROMPT"] = policy.prompt
    return env


def bridge_environment(inherited: dict[str, str]) -> dict[str, str]:
    env = dict(inherited)
    env.pop("CONDA_PREFIX", None)
    env.pop("DEXHIT_COLLECTION_PREFIX", None)
    env.update(
        TIP_BRIDGE_PYTHON="/usr/bin/python3",
        TIP_OPENPI_SRC=str(MODEL_ROOT / "src"),
        TIP_MODEL_TOKEN_FILE=str(MODEL_TOKEN_FILE),
        TIP_MODEL_URL=MODEL_URL,
    )
    return env
