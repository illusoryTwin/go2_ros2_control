# # import os
# # from ament_index_python.packages import get_package_share_directory
# # from launch import LaunchDescription
# # from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
# # from launch.launch_description_sources import PythonLaunchDescriptionSource
# # from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
# # from launch_ros.actions import Node
# # from launch_ros.substitutions import FindPackageShare
# # import xacro

# # def generate_launch_description():

# #     # Launch arguments
# #     use_sim_time = LaunchConfiguration('use_sim_time', default='true')

# #     a1_description_path = os.path.join(
# #         get_package_share_directory('a1_description'))
# #     xacro_file = os.path.join(a1_description_path, 'xacro', 'robot.xacro')
# #     controller_yaml = os.path.join(a1_description_path, 'config', 'controller.yaml')
    

# #     params = {'robot_description': Command(['xacro ', xacro_file]), 'use_sim_time': True}
# #     # params = {'robot_description': Command(['xacro ', xacro_file, ' use_gazebo:=true DEBUG:=false']), 'use_sim_time': True}

# #     # Robot State Publisher
# #     node_robot_state_publisher = Node(
# #         package='robot_state_publisher',
# #         executable='robot_state_publisher',
# #         output='both',
# #         parameters=[params],
# #         remappings=[
# #             ('/joint_states', '/a1_gazebo/joint_states')
# #         ]
# #     )

# #     # Joint State Publisher
# #     node_joint_state_publisher = Node(
# #         package='joint_state_publisher',
# #         executable='joint_state_publisher',
# #         output='screen',
# #         parameters=[{
# #             'use_sim_time': use_sim_time
# #         }]
# #     )

# #     # # Load controllers with ros2_control_node
# #     # ros2_control_node = Node(
# #     #     package='controller_manager',
# #     #     executable='ros2_control_node',
# #     #     parameters=[params, controller_yaml],
# #     #     output='screen',
# #     #     namespace='a1_gazebo'
# #     # )

# #     gazebo = IncludeLaunchDescription(
# #         PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros') + '/launch/gazebo.launch.py']),
# #         launch_arguments={'world': get_package_share_directory('a1_description') + '/world/normal.world'}.items()
# #     )

# #     controller_spawner = Node(
# #         package='controller_manager',
# #         executable='spawner',
# #         arguments=[
# #             'FR_hip_joint', 'FR_thigh_joint', 'FR_calf_joint',
# #             'FL_hip_joint', 'FL_thigh_joint', 'FL_calf_joint',
# #             'RR_hip_joint', 'RR_thigh_joint', 'RR_calf_joint',
# #             'RL_hip_joint', 'RL_thigh_joint', 'RL_calf_joint',
# #             '--controller-manager-timeout', '60'
# #         ],
# #         namespace='a1_gazebo',
# #         output='screen',
# #         parameters=[controller_yaml]  # Loading controller YAML here
# #     )

# #     # Spawn Entity
# #     spawn_entity = Node(
# #         package='gazebo_ros',
# #         executable='spawn_entity.py',
# #         arguments=['-topic', 'robot_description',
# #                    '-entity', 'a1',
# #                    '-x', '0.0',
# #                    '-y', '0.0',
# #                    '-z', '0.1'],
# #         output='screen'
# #     )

# #     # Launch Description
# #     ld = LaunchDescription()

# #     # # Add Launch Arguments
# #     ld.add_action(DeclareLaunchArgument('use_sim_time', default_value='true'))

# #     # Add nodes
# #     ld.add_action(node_robot_state_publisher)
# #     ld.add_action(node_joint_state_publisher)
# #     ld.add_action(gazebo)
# #     # ld.add_action(ros2_control_node)
# #     ld.add_action(spawn_entity)
# #     ld.add_action(controller_spawner)

# #     return ld







# # #=======================

# import os
# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import LaunchConfiguration, Command
# from launch_ros.actions import Node
# import xacro


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

    package_description = "b2_description"
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
        arguments=["unitree_guide_controller", "--controller-manager", "/controller_manager"],
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

