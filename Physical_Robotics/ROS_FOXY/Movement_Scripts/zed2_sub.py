import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from zed_interfaces.msg import ObjectsStamped
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection_node')
        self.bridge = CvBridge()
        self.object_detection_subscription = self.create_subscription(ObjectsStamped, '/zed_tb2/map', self.object_detection_callback, 10)
        self.image_publisher = self.create_publisher(Image, 'object_detection_result/image', 10)
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

    def object_detection_callback(self, msg):
        print(msg.origin)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
