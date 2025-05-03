# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument 
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare
# from launch.substitutions import PathJoinSubstitution
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
# from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
# from launch_ros.actions import Node
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from ament_index_python.packages import get_package_share_directory
# import os 





# def generate_launch_description():
#     # Package paths
#     pkg_share = FindPackageShare(package='a1_description')
#     pkg_gazebo_ros = FindPackageShare(package='gazebo_ros')

#     # Launch arguments
#     use_sim_time = LaunchConfiguration('use_sim_time', default='true')

#     # URDF/Xacro
#     robot_urdf_path = PathJoinSubstitution([pkg_share, 'urdf', 'a1.urdf'])

#     return LaunchDescription([

#         Node(
#             package="robot_state_publisher",
#             executable="robot_state_publisher",
#             name="robot_state_publisher",
#             # parameters=[{'publish_frequency': 1000.0}]
#             output='screen',
#             parameters=[{
#                 'robot_description': Command(['xacro ', robot_urdf_path]),
#                 # 'use_sim_time': LaunchConfiguration('use_sim_time'),
#                 'publish_frequency': 40.0,
#             }],
#             remappings=[('/joint_states', '/a1_gazebo/joint_states')],
#         ),

#         # Spawn robot in Gazebo
#         Node(
#             package='gazebo_ros',
#             executable='spawn_entity.py',
#             arguments=[
#                 '-topic', 'robot_description',
#                 '-entity', 'a1_gazebo',
#                 '-z', '0.3'
#             ],
#             output='screen'
#         ),

#         # Joint State Publisher GUI
#         Node(
#             package='joint_state_publisher_gui',
#             executable='joint_state_publisher_gui',
#             name='joint_state_publisher_gui',
#             parameters=[{'use_gui': True}]
#         ),

#         Node(
#             package="rviz2",
#             executable="rviz2",
#             name="rviz",
#             output="screen",
#             arguments=['-d', PathJoinSubstitution([
#                 FindPackageShare('a1_description'),
#                 'launch',
#                 'check_joint.rviz'
#             ])]
#         )
#     ])


# # =================

# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare


# def generate_launch_description():
#     # Package paths
#     pkg_share = FindPackageShare(package='a1_description')
#     pkg_gazebo_ros = FindPackageShare(package='gazebo_ros')

#     # Launch arguments
#     use_sim_time = LaunchConfiguration('use_sim_time', default='true')

#     # Path to robot description (Xacro, not URDF directly!)
#     robot_description_path = PathJoinSubstitution([pkg_share, 'urdf', 'a1.urdf'])

#     return LaunchDescription([

#         # # Robot State Publisher
#         # Node(
#         #     package="robot_state_publisher",
#         #     executable="robot_state_publisher",
#         #     name="robot_state_publisher",
#         #     output='screen',
#         #     parameters=[{
#         #         'robot_description': Command(['xacro ', robot_description_path]),
#         #         'publish_frequency': 40.0,
#         #         'use_sim_time': use_sim_time
#         #     }],
#         #     remappings=[('/joint_states', '/a1_gazebo/joint_states')],
#         # ),
#         # Static transform: map -> base_link
#         Node(
#             package='tf2_ros',
#             executable='static_transform_publisher',
#             name='static_map_to_base_link',
#             arguments=['--frame-id', 'map', '--child-frame-id', 'base_link', '0', '0', '0', '0', '0', '0'],
#             # arguments=['0', '0', '0', '0', '0', '0', 'map', 'base_link'],
#         ),

#         # Robot State Publisher
#         Node(
#             package="robot_state_publisher",
#             executable="robot_state_publisher",
#             name="robot_state_publisher",
#             output='screen',
#             parameters=[{
#                 'robot_description': Command(['xacro ', robot_description_path]),
#                 'publish_frequency': 40.0,
#                 'use_sim_time': use_sim_time
#             }],
#             remappings=[('/joint_states', '/a1_gazebo/joint_states')],
#         ),
        
#         # Gazebo Server
#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource(
#                 PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gzserver.launch.py'])
#             )
#         ),

#         # Gazebo Client
#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource(
#                 PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gzclient.launch.py'])
#             )
#         ),

#         # Spawn robot in Gazebo
#         Node(
#             package='gazebo_ros',
#             executable='spawn_entity.py',
#             arguments=[
#                 '-topic', 'robot_description',
#                 '-entity', 'a1_gazebo',
#                 '-z', '0.3'
#             ],
#             output='screen'
#         ),

#         # # Joint State Publisher GUI
#         # Node(
#         #     package='joint_state_publisher_gui',
#         #     executable='joint_state_publisher_gui',
#         #     name='joint_state_publisher_gui',
#         #     parameters=[{'use_gui': True}]
#         # ),

#         # RViz2 with preconfigured display
#         Node(
#             package="rviz2",
#             executable="rviz2",
#             name="rviz",
#             output="screen",
#             arguments=['-d', PathJoinSubstitution([
#                 pkg_share,
#                 'launch',
#                 'check_joint.rviz'
#             ])]
#         )
#     ])





import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Find the package share for 'a1_description' and 'gazebo_ros'
    pkg_share = FindPackageShare(package='a1_description').find('a1_description')
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')

    # Path to the URDF file
    robot_description_path = PathJoinSubstitution([pkg_share, 'urdf', 'a1.urdf'])

    return LaunchDescription([

        # # Start Gazebo with ROS 2 integration
        # Node(
        #     package='gazebo_ros', 
        #     executable='gzserver', 
        #     name='gazebo',
        #     output='screen',
        #     parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time', default='true')}],
        #     arguments=['--verbose']
        # ),

        # Spawn the robot in Gazebo using URDF file
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'a1_gazebo',
                '-file', robot_description_path,
                '-z', '0.3'
            ],
            output='screen'
        ),
        
    ])
