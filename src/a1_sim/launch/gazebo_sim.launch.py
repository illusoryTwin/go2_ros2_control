from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    a1_description_pkg = get_package_share_directory('a1_sim')
    # a1_gazebo_pkg = get_package_share_directory('a1_gazebo')
    # gazebo_ros_pkg = get_package_share_directory('gazebo_ros')

    robot_urdf_path = os.path.join(a1_description_pkg, 'urdf', 'a1.urdf')
    world_path = os.path.join(a1_gazebo_pkg, 'launch', 'world', 'normal.world')
    # controllers_yaml = os.path.join(a1_gazebo_pkg, 'config', 'controllers.yaml')

    return LaunchDescription([
        # Use simulation time
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # # Include Gazebo empty world
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         os.path.join(gazebo_ros_pkg, 'launch', 'gazebo.launch.py')
        #     ),
        #     launch_arguments={'world': world_path}.items(),
        # ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command(['xacro ', robot_urdf_path]),
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'publish_frequency': 40.0,
            }],
            remappings=[('/joint_states', '/a1_gazebo/joint_states')],
        ),

        # # Spawn robot in Gazebo
        # Node(
        #     package='gazebo_ros',
        #     executable='spawn_entity.py',
        #     arguments=[
        #         '-topic', 'robot_description',
        #         '-entity', 'a1_gazebo',
        #         '-z', '0.3'
        #     ],
        #     output='screen'
        # ),

        # # Load controllers
        # ExecuteProcess(
        #     cmd=['ros2', 'param', 'load', '/controller_manager', controllers_yaml],
        #     output='screen'
        # ),

        # # Spawn controllers
        # ExecuteProcess(
        #     cmd=[
        #         'ros2', 'run', 'controller_manager', 'spawner',
        #         'FR_hip_joint', 'FR_thigh_joint', 'FR_calf_joint',
        #         'FL_hip_joint', 'FL_thigh_joint', 'FL_calf_joint',
        #         'RR_hip_joint', 'RR_thigh_joint', 'RR_calf_joint',
        #         'RL_hip_joint', 'RL_thigh_joint', 'RL_calf_joint',
        #         '--controller-manager', '/a1_gazebo/controller_manager'
        #     ],
        #     output='screen'
        # )
    ])
