import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
import time

class DataLoggerNode(Node):
    def __init__(self):
        super().__init__('data_logger_node')
        
        # Create subscribers for the topics
        self.joint_state_subscriber = self.create_subscription(
            JointState, 
            '/dynamic_joint_states', 
            self.joint_state_callback, 
            10)
        
        self.imu_subscriber = self.create_subscription(
            Imu, 
            '/imu_sensor_broadcaster/imu', 
            self.imu_callback, 
            10)
        
        # Create a log file to save the data
        self.log_file = open('/home/ekaterina/Workspace/log_file.txt', 'w')  # Update this path
        
        # Set logging
        self.logger = self.get_logger()

    
    def joint_state_callback(self, msg):
        # Print the data to console
        self.logger.info(f"Received Joint State: {msg}")
        
        # Save the data to the log file
        log_msg = f"Time: {self.get_clock().now().to_msg().sec}, Joint Names: {msg.name}, Positions: {msg.position}\n"
        self.log_file.write(log_msg)
        self.log_file.flush()

    def imu_callback(self, msg):
        # Print the data to console
        self.logger.info(f"Received IMU Data: {msg}")
        
        # Save the data to the log file
        log_msg = f"Time: {self.get_clock().now().to_msg().sec}, Orientation: {msg.orientation}, Angular Velocity: {msg.angular_velocity}, Linear Acceleration: {msg.linear_acceleration}\n"
        self.log_file.write(log_msg)
        self.log_file.flush()

    def __del__(self):
        # Close the log file on shutdown
        if self.log_file:
            self.log_file.close()


def main(args=None):
    rclpy.init(args=args)

    # Create and spin the node
    data_logger = DataLoggerNode()

    rclpy.spin(data_logger)

    # Shutdown the node
    data_logger.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()