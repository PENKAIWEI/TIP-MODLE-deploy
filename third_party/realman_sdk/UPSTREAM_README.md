# 机械臂版本操作示例

## 1. 项目介绍

本项目是一个使用睿尔曼Python开发包完成的示例：双机械臂连接（左臂 192.168.1.19、右臂 192.168.1.18）、三线程模式开启 UDP 实时状态接收（按 ROS 消息格式封装为 `/observation/left_arm/joint_states`、`/observation/right_arm/joint_states`（sensor_msgs/JointState）与 `/observation/left_arm/pose`、`/observation/right_arm/pose`（geometry_msgs/PoseStamped））、以及 CANFD 透传模式控制关节/末端运动的测试案例。

## 2. 代码结构

```
RMDemo_DoubleRoboticArm/
│
├── README.md        <- 项目的核心文档
├── requirements.txt    <- 项目的依赖列表
├── setup.py        <- 项目的安装脚本
│
├── src/          <- 项目的源代码
│  ├── main.py       <- 程序的主入口
│  └── core/        <- 核心功能或业务逻辑代码
│    └── demo_double_robotic_arm.py      <- 完成机械臂连接、机械臂版本获取、API版本获取、movej运动、moveL运动、moveC运动、关闭连接的示例。
└── Robotic_Arm/      <- 睿尔曼机械臂二次开发包
```

## 3.项目下载

通过链接下载 `RM_API2` 到本地：[开发包下载](https://github.com/RealManRobot/RM_API2.git)，进入`RM_API2\Demo\RMDemo_Python`目录，可找到RMDemo_DoubleRoboticArm。

## 4. 环境配置

在Windows和Linux环境下运行时需要的环境和依赖项：

| 项目         | Linux     | Windows   |
| :--          | :--       | :--       |
| 系统架构     | x86架构   | -         |
| python       | 3.9以上   | 3.9以上   |
| 特定依赖     | -         | -         |

### Linux环境配置

   1. 参考[python官网-linux](https://www.python.org/downloads/source/)下载安装python3.9。

   2. 进入项目目录后打开终端运行以下指令安装依赖：

```bash
pip install -r requirements.txt
```

### Windows环境配置

   1. 参考[python官网-Windows](https://www.python.org/downloads/windows/)下载安装python3.9。

   2. 进入项目目录后打开终端运行以下指令安装依赖：

```bash
pip install -r requirements.txt
```

## 5. 注意事项

1. 多机械臂连接，只需要第一个机械臂初始化线程模式，后续初始化无需填写线程参数，如：

    ```python
    arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
    arm1 = RoboticArm()
    handle = arm.rm_create_robot_arm("192.168.1.18", 8080, level=3)
    handle1 = arm1.rm_create_robot_arm("192.168.1.19", 8080, level=3)
    print(handle.id)
    print(handle1.id)
    print(arm.rm_get_current_arm_state())
    print(arm1.rm_get_current_arm_state())
    ```

## 6. 使用指南

### 6.1 快速运行

按照以下步骤快速运行代码：

1. **配置机械臂IP地址**：打开 `demo_double_robotic_arm.py` 文件，默认左臂 IP 为 `"192.168.1.19"`，右臂 IP 为 `"192.168.1.18"`。

    ```python
    LEFT_IP = "192.168.1.19"   # 左臂（首个连接，初始化三线程模式）
    RIGHT_IP = "192.168.1.18"  # 右臂
    ```

    程序主流程：连接双臂 -> 开启 UDP 实时接收并封装 ROS 消息 -> CANFD 透传关节/末端运动测试 -> 打印接收统计 -> 断开连接。

    其中 CANFD 透传测试位于 `demo_canfd.py`，UDP 接收与消息封装位于 `arm_observer.py`。若运行环境安装了 ROS 2（rclpy），数据会同时发布到上述真实话题；否则以相同消息字段结构缓存，通过 `observer.print_summary()` 查看。

2. **命令行运行**：在终端进入 `RMDemo_DoubleRoboticArm` 目录，输入以下命令运行Python脚本：

    ```bash
    python ./src/main.py
    ```

3. **运行结果**：在终端中查看运行结果。

运行脚本后，输出结果如下所示：

```
Successfully connected to the robot arm: 1
Successfully connected to the robot arm: 2

movej motion succeeded
movej motion succeeded

movej_p motion succeeded
movel motion succeeded
movec motion succeeded

Successfully disconnected from the robot arm
Successfully disconnected from the robot arm
Both robot motions completed
```

### **2. 代码说明**

下面是 `demo_double_robotic_arm.py` 文件的主要功能：

- **连接机械臂**

    ```python
    robot1 = connect_robot("192.168.1.18", 8080, 3, 2)
    robot2 = connect_robot("192.168.1.19", 8080, 3)
    ```
    分别连接到指定IP和端口的两个机械臂。

- **执行运动指令**

    ```python
    demo_movej(robot1)
    demo_movej(robot1, [0, 20, 70, 0, 90, 0])
    demo_movej_p(robot1, [0.3, 0, 0.3, 3.141, 0, 0])
    demo_movel(robot1, [0.2, 0, 0.3, 3.141, 0, 0])
    demo_movec(robot1, [0.25, 0.05, 0.3, 3.141, 0, 0], [0.25, -0.05, 0.3, 3.141, 0, 0], loop=2)
    ```

    ```python
    demo_movej(robot2)
    demo_movej(robot2, [0, 20, 70, 0, 90, 0])
    demo_movej_p(robot2, [0.3, 0, 0.3, 3.141, 0, 0])
    demo_movel(robot2, [0.2, 0, 0.3, 3.141, 0, 0])
    demo_movec(robot2, [0.25, 0.05, 0.3, 3.141, 0, 0], [0.25, -0.05, 0.3, 3.141, 0, 0], loop=2)
    ```

    分别对两个机械臂执行不同的运动指令，包括 `movej`、`movej_p`、`movel` 和 `movec`。

- **断开机械臂连接**

    ```python
    disconnect_robot(robot1)
    disconnect_robot(robot2)
    ```

    分别断开与两个机械臂的连接。



## 7. 许可证信息

- 本项目遵循MIT许可证。
