import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro

def generate_launch_description():

    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    a1_description_path = os.path.join(
        get_package_share_directory('a1_description'))
    xacro_file = os.path.join(a1_description_path, 'xacro', 'robot.xacro')
    params = {'robot_description': Command(['xacro ', xacro_file]), 'use_sim_time': True}
    # params = {'robot_description': Command(['xacro ', xacro_file, ' use_gazebo:=true DEBUG:=false']), 'use_sim_time': True}

    # Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[params],
        remappings=[
            ('/joint_states', '/a1_gazebo/joint_states')
        ]
    )

    # Joint State Publisher
    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros') + '/launch/gazebo.launch.py']),
        launch_arguments={'world': get_package_share_directory('a1_description') + '/world/normal.world'}.items()
    )

    Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'FR_hip_joint', 'FR_thigh_joint', 'FR_calf_joint',
            'FL_hip_joint', 'FL_thigh_joint', 'FL_calf_joint',
            'RR_hip_joint', 'RR_thigh_joint', 'RR_calf_joint',
            'RL_hip_joint', 'RL_thigh_joint', 'RL_calf_joint',
            '--controller-manager-timeout', '60'
        ],
        namespace='a1_gazebo',
        output='screen'
    ),

    # Spawn Entity
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'a1',
                   '-x', '0.0',
                   '-y', '0.0',
                   '-z', '0.1'],
        output='screen'
    )

    # Launch Description
    ld = LaunchDescription()

    # # Add Launch Arguments
    ld.add_action(DeclareLaunchArgument('use_sim_time', default_value='true'))

    # Add nodes
    ld.add_action(node_robot_state_publisher)
    ld.add_action(node_joint_state_publisher)
    ld.add_action(gazebo)
    ld.add_action(spawn_entity)

    return ld


