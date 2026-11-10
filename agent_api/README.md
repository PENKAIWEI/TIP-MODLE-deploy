# Agent 真机接口服务

本目录提供 Agent 调用入口，管理项目现有的相机、双手、双臂、模型服务和 Bridge 命令。接口服务运行在 Ubuntu 部署机上；它自己不发布 ROS 运动目标。硬件、模型及 Bridge 子进程仍使用项目根目录 README 中的启动脚本和运行环境。首次使用前请先核对现场设备与 `model_hardware_bridge/config/reset.json` 的目标姿态。

## 启动

使用系统 Python，**不要激活 Conda**，也不要使用模型虚拟环境启动接口服务：

```bash
cd /home/hit/TIP_deploy
/usr/bin/python3 -m agent_api.server --host 127.0.0.1 --port 18776
```

服务只监听本机回环地址。Agent 若运行在另一台机器，通过 SSH 端口转发访问 `127.0.0.1:18776`。模型服务继续使用 `18774`。模型 token 仅由模型服务和本地检查代码从 README 指定的文件读取；接口请求与响应中不传 token。

该服务管理的硬件进程按相机、双手、双臂的顺序启动。关闭接口服务时，先请求当前 Bridge 停止，再关闭本服务启动的模型和硬件进程。不要把接口服务与手工启动的同一套真机控制进程同时当作控制入口。

## HTTP/JSON 接口

所有写入请求使用 `POST`，请求头为 `Content-Type: application/json`。除 `/health` 外不提供其他 GET 路由。`execution_id` 由 Agent 生成，整个服务内不能重复；策略、复位分别使用新的 ID。第一版 `params` 必须是 `{}`，模型 prompt 和权重由 `policy_id` 固定选择。

| Agent 函数 | 路由 | 请求示例 | 行为与结果 |
| --- | --- | --- | --- |
| `start_hardware()` | `/start_hardware` | `{}` | 启动或识别已有的相机、双手、双臂；使用只读 `bridge.sh observe` 检查反馈。返回 `ready`、`devices`、`reason`。可用 `ready_timeout_s` 覆盖默认 90 秒。 |
| `check_policy(policy_id)` | `/check_policy` | `{"policy_id":"pour_tea"}` | 自动启动对应模型服务并查询 `/status`；预热中返回 `model_state: LOADING`。返回模型就绪、`can_start` 和该策略当前或最近一次 `execution`。 |
| `reset_to_initial(execution_id, timeout_s)` | `/reset_to_initial` | `{"execution_id":"reset-001","timeout_s":60}` | 调用 `bridge.sh reset --execute --confirm-motion`；等待 `reset_complete` 或失败。Agent 可在 `stop_policy` 被接受后立即调用，服务会先等旧 Bridge 进程退出。 |
| `start_policy(execution_id, policy_id, params, max_duration_s)` | `/start_policy` | `{"execution_id":"pour-001","policy_id":"pour_tea","params":{},"max_duration_s":100}` | 后台调用 `bridge.sh infer --execute --confirm-motion --duration ...`。立即返回 `accepted`；之后使用 `check_policy` 查询。达到时长记为 `TIMED_OUT`，不代表业务成功。 |
| `stop_policy(execution_id)` | `/stop_policy` | `{"execution_id":"pour-001"}` | 向指定的运行中 `infer` Bridge 进程发送停止信号，立即返回是否接受。后续状态从 `check_policy` 读取。不自动归位。 |
| `stop_motion(execution_id)` | `/stop_motion` | `{"execution_id":"reset-001"}` | 中断指定的当前 Bridge 执行，包括正在运行的复位；不关闭硬件驱动。原 `reset_to_initial` 请求返回最终结果。 |
| 服务健康 | `GET /health` | 无 | 返回硬件、模型进程与当前 Bridge 执行概况。 |

`stop_status: REQUESTED` 只表示收到停止请求。子进程退出后才记为 `CONFIRMED`，其依据是**该 Bridge 进程已无法继续发布目标**；这不宣称机械臂已物理静止。复位会从实时反馈开始，最终须得到 `reset_complete`。若上一执行未释放控制权，复位返回失败，不会与其同时运行。执行日志及状态记录保存在 `model_hardware_bridge/runs/agent_api/`；接口服务重启后，未完成执行标记为 `UNKNOWN`，不会猜测其成功。

如果复位超时后停止过程仍未结束，调用可能返回 `state: STOPPING`。此时不能启动下一策略；应保留日志并确认该 Bridge 执行已经退出。

## 调用顺序

```text
start_hardware
→ check_policy(pour_tea)，重复查询直至 model_state=READY
→ reset_to_initial(reset-1)，确认 state=COMPLETED
→ start_policy(pour-1, pour_tea, {}, max_duration_s)
→ Agent 观察已有相机话题，判断倒茶完成
→ stop_policy(pour-1)
→ reset_to_initial(reset-2)，确认 state=COMPLETED
→ check_policy(serve_tea)，重复查询直至 model_state=READY
→ start_policy(serve-1, serve_tea, {}, max_duration_s)
→ Agent 判断奉茶完成，stop_policy(serve-1)
→ reset_to_initial(reset-3)
```

模型 1 与模型 2 均使用本机端口 `18774`。切换 `policy_id` 时，接口服务先结束上一模型服务，再启动下一模型并等待预热；Bridge 执行不能与另一策略重叠。模型服务的 `/status` 不表示真机已归位，`reset_to_initial` 的成功结果才表示保存的完整双臂、双手姿态已通过反馈确认。`pour_tea` 在接口层映射到 README 中模型 1 的权重与 `Pour water.` 提示词；其覆盖的完整任务动作仍按真机观测验收。

## 命令示例

```bash
curl -sS -H 'Content-Type: application/json' \
  -d '{}' http://127.0.0.1:18776/start_hardware

curl -sS -H 'Content-Type: application/json' \
  -d '{"policy_id":"pour_tea"}' http://127.0.0.1:18776/check_policy

curl -sS -H 'Content-Type: application/json' \
  -d '{"execution_id":"reset-001","timeout_s":60}' \
  http://127.0.0.1:18776/reset_to_initial

curl -sS -H 'Content-Type: application/json' \
  -d '{"execution_id":"pour-001","policy_id":"pour_tea","params":{},"max_duration_s":100}' \
  http://127.0.0.1:18776/start_policy

curl -sS -H 'Content-Type: application/json' \
  -d '{"execution_id":"pour-001"}' http://127.0.0.1:18776/stop_policy
```

Agent 也可直接使用本目录的标准库 Python 客户端；它不会自动重发请求：

```python
import time
from agent_api.client import AgentBridgeClient

bridge = AgentBridgeClient("http://127.0.0.1:18776")
hardware = bridge.start_hardware()
if not hardware["ready"]:
    raise RuntimeError(hardware["issues"])
for _ in range(150):
    policy = bridge.check_policy("pour_tea")
    if policy["model_state"] == "READY":
        break
    if policy["model_state"] in ("ERROR", "NOT_READY"):
        raise RuntimeError(policy["reason"])
    time.sleep(2)
else:
    raise TimeoutError("Model did not become ready")
reset = bridge.reset_to_initial("reset-001", timeout_s=60)
if reset["state"] != "COMPLETED":
    raise RuntimeError(reset["reason"])
started = bridge.start_policy("pour-001", "pour_tea", {}, max_duration_s=100)
# Agent 根据已有相机话题判断完成后：
stopping = bridge.stop_policy("pour-001")
```

`start_hardware` 的 HTTP 超时应大于 `ready_timeout_s + 60` 秒；`reset_to_initial` 会等待运动完成，调用方超时应大于 `timeout_s + 70` 秒。`check_policy` 只负责启动和检查模型，不会调用 `infer`。相机观测仍通过项目已有 ROS 话题订阅，接口服务不传图像。

## 实现边界

- 第一版复用现有一次性 `bridge.sh reset/infer` 命令；**常驻的是本目录的 Agent 接口服务**，每次 Bridge 控制器子进程结束后再启动下一次。
- `stop_policy` 停止当前 Bridge 推理和动作输出；模型服务可以继续加载。`check_policy` 切换策略时会停止旧模型服务。仅终止模型服务而不停止 Bridge，可能留下缓冲动作，因此不这样实现。
- `stop_motion` 是针对指定 `execution_id` 的 Bridge 执行停止；不调用无 ID 的全局 `bridge.sh stop`，也不关闭相机、手或机械臂。
- 当前模型服务和 Bridge 没有业务完成判定；Agent 根据画面提出停止，Bridge 只报告执行、复位、超时和停止结果。
