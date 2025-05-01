from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument 
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    return LaunchDescription([

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[{'publish_frequency': 1000.0}]
        ),

        # Joint State Publisher GUI
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            parameters=[{'use_gui': True}]
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz",
            output="screen",
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('a1_description'),
                'launch',
                'check_joint.rviz'
            ])]
        )
    ])
