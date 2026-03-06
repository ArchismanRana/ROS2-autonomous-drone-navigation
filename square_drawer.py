import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class DrawSquare(Node):

    def __init__(self):
        super().__init__('draw_square')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.draw_square()

    def move_forward(self):

        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 0.0

        t_end = time.time() + 2

        while time.time() < t_end:
            self.publisher.publish(msg)

        self.stop()

    def rotate(self):

        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 1.57

        t_end = time.time() + 1

        while time.time() < t_end:
            self.publisher.publish(msg)

        self.stop()

    def stop(self):

        msg = Twist()
        self.publisher.publish(msg)

    def draw_square(self):

        for i in range(4):
            self.get_logger().info("Drawing side {}".format(i+1))
            self.move_forward()
            self.rotate()


def main(args=None):

    rclpy.init(args=args)

    node = DrawSquare()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()