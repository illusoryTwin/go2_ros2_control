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


# <launch>

#     <arg name="user_debug" default="false"/>
    
#     <param name="robot_description" command="$(find xacro)/xacro --inorder '$(find a1_description)/urdf/a1.urdf'
#             DEBUG:=$(arg user_debug)"/>

#     <!-- for higher robot_state_publisher average rate-->
#     <!-- <param name="rate" value="1000"/> -->

#     <!-- send fake joint values -->
#     <node pkg="joint_state_publisher_gui" type="joint_state_publisher_gui" name="joint_state_publisher_gui">
#         <param name="use_gui" value="TRUE"/>
#     </node>

#     <node pkg="robot_state_publisher" type="robot_state_publisher" name="robot_state_publisher">
#         <param name="publish_frequency" type="double" value="1000.0"/>
#     </node>

#     <node pkg="rviz" type="rviz" name="rviz" respawn="false" output="screen"
#         args="-d $(find a1_description)/launch/check_joint.rviz"/>

# </launch>
