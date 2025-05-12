# Go2_ros2_control 

A module containing ROS2 packages for launching Go2 in simulation.

## Key packages 

- `go2_bringup`

- `go2_description`

    Contains the model of the robot in xacro format and in urdf. 

- `controllers`

    Contains `rl_quadruped_controller` and `unitree_guide_controller`.

    If you want to launch them from a separate launch file rather than the whole bringup launcher, use either of these commands:

    ```bash 
    ros2 launch unitree_guide_controller mujoco.launch.py
    ```

    or:

    ```bash 
    ros2 launch rl_quadruped_controller mujoco.launch.py
    ```