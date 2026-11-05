# 三路 RealSense 相机启动

本部署包基于 `collection10.15/four_terminal/cameras/`，相机配置统一写在 [config.yaml](config.yaml)。
相机启动文件直接读取并校验 YAML，配置不需要单独的读取脚本。
完整的消息字段、话题、订阅示例和排查方法见 [相机接口文档](../../相机接口文档.md)。

## 运行环境

- Ubuntu 24.04 / amd64（x86_64），ROS 2 Jazzy。
- RealSense ROS 驱动、librealsense2、udev 规则和 `rs-enumerate-devices`。
- 使用压缩图像接口时，需要 `compressed_image_transport` 插件。
- 读取 YAML 需要系统 Python 的 `python3-yaml`。
- 头部 D435 一台，左右腕 D405 各一台，USB 连接至采集机。

`C:\TIP_demo_deploy` 是 Windows 上的交付目录。将部署目录复制到 Ubuntu 采集机后运行；
这些 Bash/Linux 启动文件不能直接在 Windows PowerShell 中启动相机。

## 首次安装

以下命令在 Ubuntu 上执行，路径按实际部署位置替换：

```bash
cd /home/hit/TIP_demo_deploy
sudo apt update
sudo apt install ./third_party/realsense/debs/*.deb
sudo apt install ros-jazzy-compressed-image-transport python3-yaml
source /opt/ros/jazzy/setup.bash
ros2 pkg prefix realsense2_camera
ros2 pkg prefix realsense2_camera_msgs
ros2 pkg prefix compressed_image_transport
command -v rs-enumerate-devices
rs-enumerate-devices -s
```

ROS/Ubuntu 软件源需已配置且可访问。随包只有两个 ROS 驱动 deb，不包含全部系统依赖；
`rs-enumerate-devices` 和 udev 规则也需在采集机准备好。检查命令必须能发现下面的三台相机。

## 启动与停止

```bash
cd /home/hit/TIP_demo_deploy
bash hardware/cameras_ws/launch.sh
```

按 `Ctrl-C` 停止本次相机进程组。启动器先校验 `config.yaml`，再加载相机；配置不合法时会报错退出。
它会按配置编号清理旧的同名 RealSense 节点；不要同时运行两套使用相同编号的启动器。

驱动工作区覆盖规则：显式设置的 `REALSENSE_WS_SETUP` 优先；未设置时，如果
`/home/hit/node_ws/install/setup.bash` 存在，脚本会自动加载它；否则使用系统 ROS 环境。
若要明确只使用系统 deb 驱动，可这样启动：

```bash
REALSENSE_WS_SETUP=/opt/ros/jazzy/setup.bash bash hardware/cameras_ws/launch.sh
```

## 当前配置

| 相机 | 型号 | 序列号 |
| --- | --- | --- |
| 头部 | D435 | `233522072433` |
| 左腕 | D405 | `352122271900` |
| 右腕 | D405 | `260422270009` |

三路均请求 640×480、30 FPS、RGB8 彩色流，深度和 TF 发布关闭。
更换相机后修改 `config.yaml` 的 `cameras`；`rs_4cam.launch.py` 保留历史命名，默认配置三台。
配置中缺席的设备会跳过，额外设备会忽略。启动命令返回成功不等于三路都已出图。

默认完整话题如下，均在 YAML 中逐条配置：

| 相机 | 功能 | 完整话题名 |
| --- | --- | --- |
| 头部 | 原始图像 | `/observation/head/images` |
| 头部 | 压缩图像 | `/observation/head/images/compressed` |
| 头部 | 内参 | `/observation/head/camera_info` |
| 左腕 | 原始图像 | `/observation/left_wrist/images` |
| 左腕 | 压缩图像 | `/observation/left_wrist/images/compressed` |
| 左腕 | 内参 | `/observation/left_wrist/camera_info` |
| 右腕 | 原始图像 | `/observation/right_wrist/images` |
| 右腕 | 压缩图像 | `/observation/right_wrist/images/compressed` |
| 右腕 | 内参 | `/observation/right_wrist/camera_info` |

启动只发布 ROS 话题；保存图像或录制由订阅端完成。

## 修改相机配置

先停止采集，再修改 [config.yaml](config.yaml) 中对应条目，检查通过后重启；配置不热更新。

| 字段 | 含义 / 示例 |
| --- | --- |
| `id` | 正整数编号；`7` 对应 ROS 节点 `/cam7/cam7`，不改变业务话题名称 |
| `name` | 相机标签，仅用于日志；修改它不会自动改变话题 |
| `serial` | 带引号的物理序列号；用 `rs-enumerate-devices -s` 查询 |
| `enabled` | `true` 启用，`false` 跳过该相机；不加引号 |
| `color_module` | D435 用 `"rgb_camera"`，D405 用 `"depth_module"` |
| `color_profile` | `"宽x高x帧率"`，例如 `"640x480x30"`；必须受设备支持 |
| `image_topic` | 完整原始图像话题，例如 `"/observation/front/images"` |
| `compressed_topic` | 完整压缩图像话题，例如 `"/observation/front/images/compressed"` |
| `camera_info_topic` | 完整相机内参话题，例如 `"/observation/front/camera_info"` |

例如，把第一路编号改为 7、标签改为 front，并指定三个完整输出话题：

```yaml
cameras:
  - id: 7
    name: front
    serial: "233522072433"
    enabled: true
    color_module: rgb_camera
    color_profile: "640x480x30"
    image_topic: "/observation/front/images"
    compressed_topic: "/observation/front/images/compressed"
    camera_info_topic: "/observation/front/camera_info"
```

上例展示一个条目；保留其他两路时，在同一个 `cameras` 列表下保留它们。
只换物理相机时改 `serial` 即可。改输出路径时修改三个完整话题字段，并同步更新 Bridge/VLA 订阅。
所有条目的 `id`、`name`、`serial` 各自不能重复（包括停用项），至少启用一路。
所有输出话题也不能重复。完整话题必须以 `/` 开头，各段只用英文字母、数字、下划线且不以数字开头。
标签同样只使用英文字母、数字、下划线且不以数字开头；序列号必须加引号。
停用某一路后，需要三路观测的业务端也必须相应调整。

```bash
# 只校验配置并逐条打印全部完整话题；不需要 ROS，不操作硬件
python3 hardware/cameras_ws/rs_4cam.launch.py --check-config

# 校验通过后启动，命令不变
bash hardware/cameras_ws/launch.sh
```

配置检查通过不代表设备已连接或支持所填分辨率。修改编号之前必须先停止旧实例，避免旧编号节点仍占用设备。
