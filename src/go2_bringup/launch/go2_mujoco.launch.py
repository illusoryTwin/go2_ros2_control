
import os
import xacro 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, Command
from launch import LaunchDescription
from launch.event_handlers import OnProcessExit
from launch.actions import RegisterEventHandler


def generate_launch_description():

    package_description = "go2_description"
    pkg_path = os.path.join(get_package_share_directory(package_description))

    xacro_file = os.path.join(pkg_path, 'xacro', 'robot.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare(package_description),
            "config",
            "robot_control.yaml",
        ]
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {
                'publish_frequency': 20.0,
                'use_tf_static': True,
                'robot_description': robot_description,
                'ignore_timestamp': True
            }
        ],
    )
    
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers],
        remappings=[
            ("~/robot_description", "/robot_description"),
        ],
        output="both",
    )


    joint_state_publisher = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster",
                   "--controller-manager", "/controller_manager"],
    )

    imu_sensor_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["imu_sensor_broadcaster",
                   "--controller-manager", "/controller_manager"],
    )

    unitree_guide_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["rl_quadruped_controller", "--controller-manager", "/controller_manager"],
        # arguments=["leg_pd_controller", "--controller-manager", "/controller_manager"],
        # arguments=["unitree_guide_controller", "--controller-manager", "/controller_manager"],
    )

    # Event handlers to chain spawners
    imu_sensor_after_joint_state = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_publisher,
            on_exit=[imu_sensor_broadcaster]
        )
    )

    guide_controller_after_imu = RegisterEventHandler(
        OnProcessExit(
            target_action=imu_sensor_broadcaster,
            on_exit=[unitree_guide_controller]
        )
    )


    return LaunchDescription([
        robot_state_publisher,
        controller_manager,
        joint_state_publisher,
        imu_sensor_after_joint_state,
        guide_controller_after_imu
    ])

