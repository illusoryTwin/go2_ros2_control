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
    # Package paths
    pkg_share = FindPackageShare(package='a1_description')
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros')

    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # # URDF/Xacro
    # xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'robot.urdf.xacro'])
    # robot_description_raw = Command(['xacro ', xacro_file])

    a1_description_path = os.path.join(
        get_package_share_directory('a1_description'))
    xacro_file = os.path.join(a1_description_path, 'xacro', 'robot.xacro')
    params = {'robot_description': Command(['xacro ', xacro_file, ' use_gazebo:=true DEBUG:=false']), 'use_sim_time': True}

    # Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[params],
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
        # launch_arguments={'world': get_package_share_directory('a1_gazebo') + '/worlds/a1_empty.world'}.items()
    )

    # # Gazebo
    # gazebo_server = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gzserver.launch.py'])
    #     ),
    #     launch_arguments={'world': world_path}.items()
    # )

    # gazebo_client = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gzclient.launch.py'])
    #     )
    # )

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
    # ld.add_action(gazebo_server)
    # ld.add_action(gazebo_client)
    ld.add_action(node_robot_state_publisher)
    ld.add_action(node_joint_state_publisher)
    ld.add_action(gazebo)
    ld.add_action(spawn_entity)

    return ld


