#Modified by: lnotspotl, Ekaterina Mozhegova (illusoryTwin), Yaroslav Kivaev (catdog905)

import rclpy 
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy, Imu
from a1_controller.inverse_kinematics import robot_IK
from a1_controller.robot_controller import RobotController

USE_IMU = True
RATE = 60

class RobotControllerNode(Node):
    def __init__(self):
        super().__init__('robot_controller_node') 
        
        # Robot geometry
        body = [0.366, 0.094]
        legs = [0.,0.08505, 0.2, 0.2] 
        
        self.a1_robot = RobotController.Robot(body, legs, USE_IMU)
        self.inverse_kinematics = robot_IK.InverseKinematics(body, legs)

        command_topics = ["/a1_gazebo/FR_hip_joint/command",
                  "/a1_gazebo/FR_thigh_joint/command",
                  "/a1_gazebo/FR_calf_joint/command",
                  "/a1_gazebo/FL_hip_joint/command",
                  "/a1_gazebo/FL_thigh_joint/command",
                  "/a1_gazebo/FL_calf_joint/command",
                  "/a1_gazebo/RR_hip_joint/command",
                  "/a1_gazebo/RR_thigh_joint/command",
                  "/a1_gazebo/RR_calf_joint/command",
                  "/a1_gazebo/RL_hip_joint/command",
                  "/a1_gazebo/RL_thigh_joint/command",
                  "/a1_gazebo/RL_calf_joint/command"]

        self.controller_publishers = []
        for topic in command_topics:
            pub = self.create_publisher(Float64, topic, 10)
            self.controller_publishers.append(pub)
        
        self.RL_calf_controller_publisher = self.create_publisher(Float64, '/a1_gazebo/RL_calf_joint/command', 10)

        if USE_IMU:
            self.create_subscription(Imu, "a1_imu/base_link_orientation", self.a1_robot.imu_orientation, 10)
        self.create_subscription(Joy, "a1_joy/joy_ramped", self.a1_robot.joystick_command, 10)
        
        self.timer = self.create_timer(1.0 / RATE, self.control_loop)

        self.get_logger().info("Robot controller node initialized")

    def control_loop(self):
        leg_positions = self.a1_robot.run()
        self.a1_robot.change_controller()

        dx = self.a1_robot.state.body_local_position[0]
        dy = self.a1_robot.state.body_local_position[1]
        dz = self.a1_robot.state.body_local_position[2]

        roll = self.a1_robot.state.body_local_orientation[0]
        pitch = self.a1_robot.state.body_local_orientation[1]
        yaw = self.a1_robot.state.body_local_orientation[2]

        try:
            # joint_angles = self.inverse_kinematics.inverse_kinematics(leg_positions,
            #                     dx, dy, dz, roll, pitch, yaw)
            joint_angles = [15.0] * 12  # Example: all joints set to 0.5 radians

            for i in range(len(joint_angles)):
                msg = Float64()
                msg.data = joint_angles[i]
                self.get_logger().info(f"msg.data: {msg.data}")
                self.controller_publishers[i].publish(msg)
                self.RL_calf_controller_publisher.publish(msg)
                
        except Exception as e:
            self.get_logger().warn(f"Inverse kinematics failed: {e}")

    
def main(args=None):
    rclpy.init(args=args)
    node = RobotControllerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass 
    finally:
        node.destroy_node()
        rclpy.shutdown() 

if __name__ == "__main__":
    main()

