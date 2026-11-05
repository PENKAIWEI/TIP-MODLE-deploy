# RM65 双臂模型控制接口

本目录包含 RM65 控制、安全校验、Ruckig 平滑和 RealMan SDK 反馈，
组成纯模型控制包 `arm_model_control`。
Bridge 发布目标，控制节点校验后调用 `rm_movej_canfd`；SDK UDP 上报状态。
不连接 Tracker，也不自动回 home。同一时刻只允许一个控制进程连接双臂。

| 方向 | 话题 | 类型和内容 |
| --- | --- | --- |
| Bridge → 控制节点 | `/observation/left_arm/joint_cmd`、`/observation/right_arm/joint_cmd` | `sensor_msgs/msg/JointState`，7 槽绝对目标，rad |
| 机械臂 → Bridge | `/observation/left_arm/joint_states`、`/observation/right_arm/joint_states` | `sensor_msgs/msg/JointState`，前 6 轴为 SDK UDP 反馈，第 7 轴固定 `0` |
| 机械臂 → Bridge | `/observation/left_arm/pose`、`/observation/right_arm/pose` | `geometry_msgs/msg/PoseStamped`，SDK UDP 末端位姿 |

**没有额外的 `/model_control/{side}_arm/enable` 或 `/ready` 话题。**
节点运行后，某侧收到第一条新鲜、有效的 `joint_cmd` 时，先从 SDK 读取该侧当前
六轴位置并初始化平滑器，然后校验和执行目标；因此模型开始发布动作就可能使机械臂
运动。左右臂分别处理，双臂同步与观测新鲜度由 Bridge 保证。

命令的 `name` 须恰好包含 `joint1` 至 `joint7`；`position` 为 7 个有限弧度值。
第 7 槽必须接近零（默认容差 `0.0001 rad`），只有前 6 轴进入 RM65。
`header.stamp` 使用与接收节点一致的 ROS 时钟，须严格递增且未过期
（默认 0.3 秒）；未来时间最多容忍 20 ms。目标还要通过关节限位、相对当前
位置的最大变化量、工作空间和奇异性检查，才进入 Ruckig 限速线程。

命令流超时或无效目标会让该侧减速停止；停止完成后，下一条新鲜有效目标可以重新
开始控制。CANFD 连续失败会锁存该侧故障并调用 slow stop，此时不会因新命令自动
恢复，需排查故障后正常重启节点。命令已发布不等于到位，应比较新鲜的
`/observation/{side}_arm/joint_states` 与目标。

## 构建与运行

```bash
cd /home/hit/TIP_demo_deploy/hardware/arm_ws
bash build.sh
bash start_model_control.sh --check-only
bash start_model_control.sh --dry-run
```

`--check-only` 不连接 ROS 或 SDK；`--dry-run` 不连接真臂。目标机需系统 ROS 2 Jazzy
和 Python 3.12。机械臂运行所需的 RealMan SDK、NumPy、Ruckig
统一从 `../../third_party/` 加载；启动脚本检查实际模块路径，拒绝使用用户目录或
系统目录中的同名副本。真机运行前核对 `arm_model_control/arm_model_control/model_node.py`
中的左右臂 IP 默认值（沿用参考工程的 `192.168.1.19`、`192.168.1.18`），
并确保没有旧双臂控制进程占用 SDK 连接。

```bash
bash start_model_control.sh --confirm-motion
```

此命令启动接收端，**一旦 Bridge 发送有效动作就可能运动**。先在无动作来源的条件下
确认左右臂 `joint_states` 和 `pose` 持续到达，再启动 Bridge 并从小幅目标验收。
停止 Bridge 的动作发布后，等待目标流超时并减速停止；从原启动终端按 `Ctrl-C`
正常关闭双臂连接。
