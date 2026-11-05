# TIP 模型与硬件适配层

本目录接收 `TIP_demo_deploy/hardware` 的 ROS 观测，组装 Sandisk100 模型输入，
通过 HTTP 调用远程模型，再将 34 维动作拆成双臂、双手四路 ROS 指令。
运行目标为 Ubuntu 24.04 / ROS 2 Jazzy / Python 3.12。

开发与联调接口详见 [接口文档](接口文档.md)，包含 ROS 话题、HTTP 请求/响应、数据维度、Python 接口、配置与调用示例。

## 与目标驱动对齐的接口

| 方向 | 话题 | 类型 / 约定 |
| --- | --- | --- |
| 输出：左臂 | `/observation/left_arm/joint_cmd` | `JointState`，`joint1`～`joint7`，7 槽绝对目标，rad，最后一槽为 0 |
| 输出：右臂 | `/observation/right_arm/joint_cmd` | 同上；与左臂使用同一 ROS 时间戳 |
| 输出：双手 | `/o10_control/{left,right}/command` | `JointState`，各 10 个主动关节，rad |
| 输入：双臂关节 | `/observation/{left,right}_arm/joint_states` | 7 槽实测关节，rad，第 7 槽为 0 |
| 输入：双臂末端 | `/observation/{left,right}_arm/pose` | `PoseStamped`，位置 m，四元数转 RPY rad |
| 输入：双手关节 | `/o10/{left,right}/joint_states` | 10 维实测关节，rad；Provider 的空 `name` 按契约固定顺序解释 |
| 输入：双手状态 | `/o10_control/{left,right}/state` | `O10ControlState`，检查就绪、故障、目标拒绝和手部指令时间 |
| 输入：触觉 | `/observation/{left,right}_hand/tactile/{patch}` | 每手 7 块原始 `mono8` 图像 |
| 输入：三路相机 | 读取 `../hardware/cameras_ws/config.yaml` 的 `compressed_topic` | `CompressedImage`；按 `camera_roles` 将头部映射为模型 `top` |

手部名称、顺序和限位直接导入部署包的 `omnihand_o10_contracts`，不另维护副本。
机械臂边界读取部署包 `hardware/arm_ws/rm_65.urdf` 并与 RM65 参考限位取交集；
驱动自身的 SDK、工作空间、奇异性和平滑检查仍是最终执行约束。

当前机械臂接收端**没有** prepare / enable / stop 服务，也没有动作接受确认或聚合故障话题。
Bridge 使能只创建四路发布器并检查订阅者；第一条有效 `joint_cmd` 就可能开始运动。
左右发布使用同一时间戳，但两个 ROS Topic 不提供原子同步执行保证。

停止时停止发布双臂指令，原驱动依 `target_timeout_sec`（默认 0.3 秒）减速；
双手尝试发送一次新鲜实测姿态作为保持目标。不能把该行为描述为同步急停。
`reset_complete` 代表双臂位置反馈到位稳定、双手有本次指令时间反馈，**不是机械臂 ACK**。

## 数据转换与调用链

```text
ROS 相机 / 关节 / 末端位姿 → sensors.Store.snapshot()
  → 三路 JPEG224 + state46 → controller.Workers → HTTP /slow、/fast
ROS 原始触觉 → 按序上传 HTTP /feed → stream.DualStream → 模型触觉输入
远程 actions[30,34] → 原模型 ActionBuffer → 限位 / 步长限制
  → IO.publish() → 左臂7、右臂7、左手10、右手10 → 既有硬件驱动
```

模型约定保持参考部署：`sandisk100_dual_o10_v1`，`FPS=29.994`，任务 `Pour water.`，
内部动作 48 维、部署动作 34 维、状态 46 维。34 维布局如下（Python 下标）：

| 切片 | 内容 |
| --- | --- |
| `0:6` / `6` | 左臂 6 关节 / 零填充 |
| `7:17` | 左手 10 关节 |
| `17:23` / `23` | 右臂 6 关节 / 零填充 |
| `24:34` | 右手 10 关节 |
| 状态额外 `34:40` / `40:46` | 左 / 右末端 `[x,y,z,roll,pitch,yaw]` |

Bridge 向驱动保持 rad；角度与 SDK 的转换由现有 `arm_model_control` 完成。
每次指令机械臂变化不超过 0.02 rad，手指不超过 0.025 rad；机械臂目标额外限制在
新鲜实测位置 ±0.06 rad 内，避免目标缓冲不断领先于硬件反馈。

图像按 YAML 中的原始分辨率校验，保持比例缩放补边到 224×224，RGB，JPEG 质量 90。
原始采集时间、角色、`frame_id` 保存在 `Store.snapshot_metadata`，不进入旧模型的状态向量。
本模型不使用相机内参，不执行几何计算。

相机默认最大包龄 100 ms，三路采集时间的最大差值 100 ms；关节反馈最大包龄 150 ms，
线性插值两端各允许距目标时间 100 ms。先计算 ROS 源时间与当前 ROS 时间的差，
再映射到本机单调时钟；不直接比较两种时钟。坏图丢弃且不更新有效帧时间，重复源时间
不视作新帧；源时钟倒退清理相机配对并结束本次 Bridge 会话，重启会话后重新校准。
推理结果超过 8 帧（约 266.7 ms）丢弃；30 帧动作范围耗尽则停止输出。

## 触觉策略

**默认按此次迁移要求保留参考代码的 `hold` 策略。** 每块触觉使用目标时刻之前的最近
一包数据；单手超过 150 ms 未更新后复用旧包，不设断流时长上限。保持真实时间戳和
无效掩码，不借用另一只手的数据，不用未来包，也不将无效新包替换为更早的有效包。
开始推理仍需最初 16 个相机时间点的校准以及双手真实历史。

这项明确选择覆盖目标目录《手部接口文档》中“50 ms 包龄检查 / 触觉超时停用”的描述；
硬件发布的消息格式保持一致。配置中保留可选 `tactile_mode: strict`，此时默认 50 ms
采样有效期、150 ms 整手超时。切换时客户端和模型服务端必须采用一致配置；客户端启动
会核对 `/status` 的触觉策略，拒绝不匹配的服务。当前默认 `hold` 可连接参考目录当前版本的服务。

## 文件与移植来源

| 文件 | 实现来源 / 修改 |
| --- | --- |
| `tip_bridge/common.py` | 移植 RPC、NPZ 封装、状态/动作校验、限幅和稳定性判断；改为相对路径和严格目标限位 |
| `tip_bridge/controller.py` | 移植复位、影子/执行推理、触觉上传、slow/fast 调度；适配新反馈语义及触觉策略核对 |
| `tip_bridge/stream.py` | 移植触觉历史查询、first16 校准、因果保持；增加可选严格策略 |
| `tip_bridge/runtime.py` | 直接移植原模型运行时注解检查优化 |
| `tip_bridge/server.py` | 移植原 HTTP 模型适配服务，修改包名和配置路径；可选部署到模型机 |
| `tip_bridge/sensors.py` | 复用缓存、时间对齐、图像与触觉逻辑；按本部署驱动重写 ROS 输出与检查 |
| `tip_bridge/contracts.py` | 将无 ROS 依赖的解码、维度映射、话题、关节顺序集中，供测试复用 |
| `tip_bridge/config.py` | 加载本桥接层配置及目标相机配置 |
| `config/reset.json` | 复制参考部署的采集复位姿态，`source` 只是来源记录，不读取该旧路径 |
| `data/replay.npz` | 复制参考部署预热样本，仅供模型服务预热 |

旧 `pour_deploy/arm.py` 和 `manage.py` 未迁入：目标目录已有机械臂驱动和三个硬件启动器，
Bridge 不新建 SDK 连接、不管理其他硬件进程、不自动清除硬件锁存故障。

## 环境与启动

以下命令在 Linux 目标机 `TIP_demo_deploy` 根目录执行。硬件驱动按原有文档构建。
CPU Bridge 需要 NumPy、Pillow、OpenCV、PyYAML、ROS 2 及已构建的手部消息/契约包。
`requirements.txt` 仅列 CPU Python 依赖；ROS 组件来自系统和 `hardware/hand_ws`。

原始模型的 `ActionBuffer` 保留外部依赖，避免重写动作融合算法。
运行 `infer` 时，匹配该 checkpoint 的 OpenPI 源码必须可导入；可设置：

```bash
export TIP_OPENPI_SRC=/path/to/matching/openpi/src
# 此目录下必须存在 openpi/fastslow/buffer.py
export TIP_MODEL_URL=http://192.168.101.6:18774
export TIP_MODEL_TOKEN_FILE=/secure/path/to/the-existing-model-token
```

凭据未从参考目录复制。将原模型服务使用的同一个 token 文件通过 `TIP_MODEL_TOKEN_FILE`
指定，或自行放入 `model_hardware_bridge/config/token`（已加入忽略规则）。
`observe`、`reset` 和配置检查不需要模型 token；`infer`、`model-status` 需要。

先检查配置（不启动 ROS、设备或网络请求）：

```bash
bash model_hardware_bridge/scripts/bridge.sh check
```

硬件启动仍使用目标目录现有入口，分别在终端运行：

```bash
bash hardware/arm_ws/start_model_control.sh --confirm-motion
bash hardware/hand_ws/launch.sh --confirm-motion
bash hardware/cameras_ws/launch.sh
```

观察与影子推理：

```bash
bash model_hardware_bridge/scripts/bridge.sh observe --duration 5
bash model_hardware_bridge/scripts/bridge.sh model-status
bash model_hardware_bridge/scripts/bridge.sh infer --duration 10
```

复位文件沿用参考场景，需要适合现场布置。下面第一条仅打印实测值、复位目标和误差；
后两条明确启用动作：

```bash
bash model_hardware_bridge/scripts/bridge.sh reset
bash model_hardware_bridge/scripts/bridge.sh reset --execute --confirm-motion
bash model_hardware_bridge/scripts/bridge.sh infer --execute --confirm-motion --duration 30
```

停止当前 Bridge：

```bash
bash model_hardware_bridge/scripts/bridge.sh stop
```

`Ctrl-C` 也会走同一清理流程。Bridge 退出不自动复位，硬件进程仍由各自启动终端管理。

可选：模型机部署本目录的服务适配层，继续使用原模型的 Python/JAX/OpenPI 环境：

```bash
export TIP_MODEL_PYTHON=/path/to/model-environment/bin/python
export TIP_OPENPI_SRC=/path/to/matching/openpi/src
export TIP_OPENPI_CLIENT_SRC=/path/to/openpi/packages/openpi-client/src
export TIP_MODEL_CHECKPOINT=/path/to/checkpoint/23000
export TIP_MODEL_TOKEN_FILE=/secure/path/to/the-existing-model-token
CUDA_VISIBLE_DEVICES=6 bash model_hardware_bridge/scripts/model_server.sh --port 18774
```

客户端只需要模型 CPU 缓冲模块；服务端才需要模型权重、JAX/CUDA、训练配置和触觉特征实现。
本目录不附带神经网络源码或权重，也不重新安装模型环境。

其他配置：`TIP_DEPLOY_ROOT` 可覆盖硬件根目录，`TIP_BRIDGE_CONFIG` 可覆盖桥接配置文件，
`TIP_BRIDGE_PYTHON` 可选择 CPU Python（须与 ROS Jazzy 的 Python 3.12 兼容）。

## 离线验证与边界

```bash
cd model_hardware_bridge
python3 -m unittest discover -s tests -v
```

测试直接调用目标驱动的纯 Python `ModelCommandGate` 及真实 O10 契约，使用 Mock ROS
验证四路发布、共同时间戳、只读初始化、故障拦截、停止行为和状态对齐；触觉测试覆盖
长时间双手暂停、未来包、无效包和队列淘汰。
Windows Python 3.10 测试环境仅在测试代码中补充 `StrEnum` 兼容基类以导入手部契约；
不改变部署源码，也不意味着生产环境支持 Python 3.10。

本次验证不包含实机 ROS/DDS QoS、设备在线率、现场动作、模型权重加载、真实 OpenPI
动作融合/校准或 GPU 时延。实际硬件启动和模型联调应在上述目标环境中完成。
