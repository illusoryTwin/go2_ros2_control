import rclpy
from rclpy.node import Node
from go2_msgs.msg import WebRtcReq  # Import your custom message

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')

        # QoS profile (can be customized)
        qos_profile = rclpy.qos.qos_profile_sensor_data

        # Create the subscription to the camera topic
        self.subscription = self.create_subscription(
            WebRtcReq,                   # Message type
            'webrtc_req',               # Topic name
            lambda msg: self.webrtc_req_cb(msg, "0"),  # Callback with extra arg
            qos_profile
        )
        self.get_logger().info("Subscribed to topic: /webrtc_req")

    def webrtc_req_cb(self, msg, camera_id):
        # Example: print fields in WebRtcReq message
        self.get_logger().info(f"Received WebRtcReq from camera {camera_id}: {msg}")
        # Access fields from msg like: msg.image, msg.timestamp, etc.
        # (assuming those exist in your custom message)

def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
