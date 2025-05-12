from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler, ExecuteProcess
from launch.event_handlers import OnProcessExit
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os
import xacro
from ament_index_python.packages import get_package_share_directory


def launch_setup(context, *args, **kwargs):
    controller_type = LaunchConfiguration('controller_type').perform(context)

    package_description = "go2_description"
    pkg_path = os.path.join(get_package_share_directory(package_description))
    xacro_file = os.path.join(pkg_path, 'xacro', 'robot.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    robot_controllers = PathJoinSubstitution(
        [FindPackageShare(package_description), "config", "robot_control.yaml"]
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'publish_frequency': 20.0,
            'use_tf_static': True,
            'robot_description': robot_description,
            'ignore_timestamp': True
        }],
    )

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers],
        remappings=[("~/robot_description", "/robot_description")],
        output="both",
    )

    joint_state_publisher = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    imu_sensor_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["imu_sensor_broadcaster", "--controller-manager", "/controller_manager"],
    )

    imu_sensor_after_joint_state = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_publisher,
            on_exit=[imu_sensor_broadcaster]
        )
    )

    # Conditional controller spawning
    if controller_type == "unitree_guide":
        specific_controller = Node(
            package="controller_manager",
            executable="spawner",
            arguments=["unitree_guide_controller", "--controller-manager", "/controller_manager"],
        )
    elif controller_type == "rl":
        specific_controller = Node(
            package="controller_manager",
            executable="spawner",
            arguments=["rl_quadruped_controller", "--controller-manager", "/controller_manager"],
        )
    else:
        raise ValueError(f"Unsupported controller type: {controller_type}")

    specific_controller_after_imu = RegisterEventHandler(
        OnProcessExit(
            target_action=imu_sensor_broadcaster,
            on_exit=[specific_controller]
        )
    )

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="camera_static_tf",
        arguments=["0", "0", "0", "0", "0", "0", "trunk", "front_camera"]
    )

    keyboard_controller = ExecuteProcess(
        cmd=['gnome-terminal', '--', 'ros2', 'run', 'keyboard_input', 'keyboard_input'],
        output='screen'
    )

    rosbag_record = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', '/data/bagfile2',
             '/dynamic_joint_states', '/imu_sensor_broadcaster/imu'],
        output='screen'
    )

    return [
        robot_state_publisher,
        controller_manager,
        joint_state_publisher,
        imu_sensor_after_joint_state,
        specific_controller_after_imu,
        static_tf,
        keyboard_controller,
        rosbag_record
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'controller_type',
            default_value='unitree_guide',
            description='Choose the controller: "unitree_guide" or "rl"'
        ),
        OpaqueFunction(function=launch_setup)
    ])
