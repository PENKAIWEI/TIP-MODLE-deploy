# O10 灵巧手：模型控制 + 状态/触觉反馈

本目录启动 `omnihand_o10_control` 和 `omnihand_o10_hardware_adapter`，保留控制节点的动作校验、限速、控制状态和故障处理。模型侧 Bridge 发布 10 维关节目标；控制节点校验和限速后交给硬件节点，硬件节点返回关节与触觉数据。接口格式见部署根目录的 [手部接口文档](../../手部接口文档.md)。

触觉数据仅发布左右手各 7 路 `sensor_msgs/msg/Image`（`mono8`），保留原始尺寸和 0～255 读数。每只手的区域顺序为手背、手掌、拇指、食指、中指、无名指、小指；后续 ROS Bridge 负责模型张量组装、历史缓存和时间对齐。

## 文件

- `src/collection/`：4 个原生产 ROS2 包：控制、硬件适配、关节契约、ROS 消息/服务。
- `../../third_party/omnihand_sdk/`：原生产 OmniHand SDK 及 Linux 动态库。
- `config/hand.json`：以 JSON 格式配置左手/右手、HCAN 序列号、触觉请求频率。
- `build.sh`：编译这 4 个包；`launch.sh`：启动硬件与控制节点。

`build/`、`install/`、`log/` 是目标机器生成的目录，不从原工作区复制。原来的手套接收、拇指映射、IK、相机和机械臂代码不在此包内。

## Ubuntu 24.04 / ROS 2 Jazzy 使用

目标机器需为 Linux x86_64、Python 3.12，并已安装 ROS 2 Jazzy、`colcon`、ROS 消息生成器、`rclpy`、`sensor_msgs`、`std_msgs`、`geometry_msgs`、`builtin_interfaces`、`numpy`、`setuptools`。SDK 动态库随包提供。若使用独立 Python 3.12 环境，将其路径设为 `DEXHIT_COLLECTION_PREFIX`；其中必须有 `numpy`。构建和运行 ROS 环境默认是 `/opt/ros/jazzy/setup.bash`，可通过 `ROS_SETUP` 覆盖。

以下命令在目标 Ubuntu 机器的 **Bash 终端**中执行。将整个 `TIP_demo_deploy` 目录复制到目标机器，保留 `hardware/` 和 `third_party/` 的相对位置；将示例中的 `/path/to/TIP_demo_deploy` 替换为实际部署路径。随包 SDK 是 Linux 动态库，不能直接在 Windows PowerShell 中运行这套启动流程。

### 1. 配置要连接的手

给灵巧手上电并连接对应的 HCAN 适配器，然后编辑 [config/hand.json](config/hand.json)：

```json
{
  "hand_sides": "both",
  "left_hcan_serial_number": "1011226306",
  "right_hcan_serial_number": "1011229039",
  "tactile_rate_hz": 50
}
```

| 字段 | 格式与含义 |
| --- | --- |
| `hand_sides` | 字符串：`"left"` 只启动左手，`"right"` 只启动右手，`"both"` 启动双手 |
| `left_hcan_serial_number` | 左手 HCAN 序列号，必须是双引号包围的数字字符串；启用左手时必填 |
| `right_hcan_serial_number` | 右手 HCAN 序列号，必须是双引号包围的数字字符串；启用右手时必填 |
| `tactile_rate_hz` | 非负数字，支持小数；`0` 表示不启用定时触觉读取 |

示例中的序列号来自包内原有配置，使用前按实际 HCAN 适配器标签核对或修改。只接了一只手时，将 `hand_sides` 改成对应的 `"left"` 或 `"right"`；未启用一侧的序列号可以省略。双手模式下两个 HCAN 序列号必须不同。50 Hz 是请求值，实际发布频率受 SDK 读取耗时影响。

配置使用标准 JSON：字段名和字符串使用双引号，不写注释或末尾多余的逗号。启动器用 Python 3 标准库解析，不需要 `jq`；会检查字段名、重复字段和取值类型，并在配置错误时退出。

### 2. 首次部署：检查文件并编译

```bash
cd /path/to/TIP_demo_deploy
bash hardware/hand_ws/launch.sh --check-only
bash hardware/hand_ws/build.sh
```

`--check-only` 需要 `python3`，只校验 JSON 配置和部署文件，不连接硬件，也不验证 ROS 环境、设备连接或硬件是否可用。编译成功后会生成 `hardware/hand_ws/install/setup.bash`。首次部署或修改源码后需要编译；只修改 `hand.json` 时，重启即可。

### 3. 启动硬件与控制节点

在启动终端执行：

```bash
cd /path/to/TIP_demo_deploy
bash hardware/hand_ws/launch.sh --confirm-motion
```

启动脚本自动加载 ROS 和本工作空间的环境，依次启动：

1. 硬件节点 `/omnihand_o10_hardware_provider`：连接所选的手，收发硬件数据。
2. 控制节点 `/o10_control_node`：处理目标校验、限速和故障状态。
3. 按 `tactile_rate_hz` 为所选的手开启触觉读取；配置为 `0` 时跳过。

看到 `[hand] running: sides=...; logs=...` 表示启动脚本已完成上述步骤。保持这个终端运行；两个节点由同一个启动器管理，无需分别手动启动。后续使用已编译的工作空间时，执行本步骤即可。

`--confirm-motion` 表示允许实际下发动作；收到 Bridge 的有效目标后，灵巧手可能立即运动。模型/Bridge 需要在上层工程中另外启动，这个脚本负责启动手部节点。

### 4. 在另一个终端检查状态和反馈

新开的终端需要单独加载环境，启动脚本中的环境设置不会传回其他终端：

```bash
cd /path/to/TIP_demo_deploy
source "${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
source hardware/hand_ws/install/setup.bash

ros2 node list
ros2 topic type /o10_control/left/command
ros2 topic echo /o10_control/left/state --once
ros2 topic echo /o10/left/joint_states --once
ros2 topic type /observation/left_hand/tactile/back
ros2 topic echo /observation/left_hand/tactile/back --once
ros2 topic hz /observation/left_hand/tactile/back
```

节点列表应包含 `/omnihand_o10_hardware_provider` 和 `/o10_control_node`，指令话题类型应为 `sensor_msgs/msg/JointState`。检查控制状态中的 `feedback_ready`、`motion_enabled`、`fault_latched`，并确认能收到关节反馈；节点出现在列表中不代表已经完成控制初始化。

手背触觉话题类型应为 `sensor_msgs/msg/Image`，消息中的 `encoding=mono8`、`height=11`、`width=12`、`step=12`，`data` 长度为 132。其余区域话题后缀为 `palm`、`thumb/distal`、`index/distal`、`middle/distal`、`ring/distal`、`pinky/distal`；完整话题表和各区域尺寸见 [手部接口文档](../../手部接口文档.md)。双手模式共 14 路触觉数据话题。

右手将上述 `left` 改为 `right`；双手模式分别检查两侧。`ros2 topic hz` 持续运行，按 `Ctrl-C` 结束这条查看命令。如果 `tactile_rate_hz` 为 `0`，触觉话题没有定时数据是预期行为。

如果设置了自定义 `ROS_SETUP` 或 `ROS_DOMAIN_ID`，在启动终端、检查终端和 Bridge 环境中使用一致的设置；跨机器运行时还需保证 ROS 2 节点能够互相发现。

### 5. 接入模型动作

Bridge 向 `/o10_control/{side}/command` 发布 `sensor_msgs/msg/JointState`，每只手提供 10 个主动关节的目标角度，单位为 rad。控制节点处理后会转发到硬件节点。保留这条控制路径，Bridge 不直接向内部话题 `/o10/{side}/joint_cmd` 下发动作。

关节顺序、消息示例、触觉解析和故障处理接口见 [手部接口文档](../../手部接口文档.md)。模型可通过后续 Bridge 订阅 `/o10/{side}/joint_states`、`/observation/{side}_hand/tactile/...` 的 7 路区域图像和 `/o10_control/{side}/state` 获取反馈。图像发布时保留各部位原始 H × W，硬件节点不生成 `[B,14,16,14,15]` 张量或模型有效性掩码。

从旧版更新后，先在原启动终端停止节点，再重新执行 `build.sh` 和 `launch.sh --confirm-motion`。旧整手 `mono16` 和编号兼容触觉数据接口已移除，订阅程序需要使用上述 14 路 `mono8` 区域话题。

### 6. 停止与查看日志

在运行 `launch.sh` 的终端按 `Ctrl-C`，启动器会停止硬件与控制两个节点，不自动发送回位动作。如果任一节点异常退出，启动器也会退出并清理另一节点。

默认日志目录为 `${TMPDIR:-/tmp}/tip-hand-时间/`，启动终端会输出实际路径：

- `provider.log`：硬件连接、SDK 调用及数据读取日志。
- `control.log`：控制节点运行日志。

如需指定日志目录，可用以下命令替代第 3 步的启动命令；同一目录下再次启动会覆盖这两个日志文件：

```bash
cd /path/to/TIP_demo_deploy
OMNIHAND_LOG_DIR="$PWD/hand-logs" bash hardware/hand_ws/launch.sh --confirm-motion
```

常见启动错误：

| 提示或现象 | 处理方式 |
| --- | --- |
| `python3 is required to read hand.json` | 安装或启用 Python 3，确保当前 Bash 终端能运行 `python3` |
| `could not load hand.json` | 按前一行错误提示检查 JSON 语法、字段名、序列号字符串和采样频率 |
| `missing ROS setup` | 确认 ROS 2 Jazzy 已安装；若安装路径不同，通过 `ROS_SETUP` 指定 `setup.bash` |
| `workspace is not built` | 先运行 `bash hardware/hand_ws/build.sh` |
| `invalid Python 3.12 environment` | 检查 `DEXHIT_COLLECTION_PREFIX` 或当前 Conda 环境是否为 Python 3.12 |
| `Python cannot import ...` | 根据前面的 Python 异常检查依赖、工作空间编译结果和 `third_party/omnihand_sdk` 是否完整 |
| `is already running` | 回到已有的启动终端管理节点，避免重复启动 |
| Provider 提前退出或没有出现 | 查看输出路径下的 `provider.log`，核对供电、HCAN 连接、序列号和所选手侧 |

`SHA256SUMS` 用于检查拷贝完整性；修改配置、文档或源码后，对应文件的哈希会变化。

## 消息格式验证

在已构建并加载 ROS 环境的 Ubuntu 终端执行以下测试；测试不连接实物：

```bash
cd /path/to/TIP_demo_deploy
source "${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
source hardware/hand_ws/install/setup.bash
python3 -m unittest discover \
  -s hardware/hand_ws/src/collection/omnihand_o10_hardware_provider_node/test \
  -p 'test_tactile_images.py' -v
```

测试覆盖 14 个话题、各区域尺寸、`mono8` 消息字段、原始数值、时间戳、左右手布局，以及采样失败和停止读取时不发布伪造数据。
