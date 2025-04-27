import rclpy 
from rclpy.node import Node

from sensor_msgs.msg import Joy, Imu
# from robot_controller import RobotController
from a1_controller.inverse_kinematics import robot_IK
from a1_controller.robot_controller import RobotController


# # from .robot_controller import RobotController
# from .inverse_kinematics import robot_IK

from std_msgs.msg import Float64

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

        self.publishers = []
        for topic in command_topics:
            pub = self.create_publisher(Float64, topic, 10)
            self.publishers.append(pub)
        
        if USE_IMU:
            self.create_subscription(Imu, "a1_imu/base_link_orientation", self.a1_robot.imu_orientation)
        self.create_subscription(Joy, "a1_joy/joy_ramped", self.a1_robot.joystick_command)

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
            joint_angles = self.inverse_kinematics.inverse_kinematics(leg_positions,
                                dx, dy, dz, roll, pitch, yaw)

            for i in range(len(joint_angles)):
                msg = Float64
                msg.data = joint_angles[i]
                self.publishers[i].publish(msg)
        except:
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

