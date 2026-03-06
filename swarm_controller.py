import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class TurtleTrain(Node):

    def __init__(self, follower, leader, spacing=1.5):
        super().__init__(f'{follower}_train')

        self.follower = follower
        self.leader = leader
        self.spacing = spacing

        self.pose = None
        self.leader_pose = None

        self.create_subscription(
            Pose,
            f'/{leader}/pose',
            self.leader_callback,
            10)

        self.create_subscription(
            Pose,
            f'/{follower}/pose',
            self.pose_callback,
            10)

        self.publisher = self.create_publisher(
            Twist,
            f'/{follower}/cmd_vel',
            10)

        self.timer = self.create_timer(0.1, self.control)

    def pose_callback(self, msg):
        self.pose = msg

    def leader_callback(self, msg):
        self.leader_pose = msg

    def control(self):

        if self.pose is None or self.leader_pose is None:
            return

        dx = self.leader_pose.x - self.pose.x
        dy = self.leader_pose.y - self.pose.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        angle = math.atan2(dy, dx)

        msg = Twist()

        # spacing control (this creates delay effect)
        if distance > self.spacing:
            msg.linear.x = 1.5 * (distance - self.spacing)
        else:
            msg.linear.x = 0.0

        msg.angular.z = 4 * (angle - self.pose.theta)

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    followers = [
        TurtleTrain("turtle2", "turtle1"),
        TurtleTrain("turtle3", "turtle2"),
        TurtleTrain("turtle4", "turtle3"),
        TurtleTrain("turtle5", "turtle4")
    ]

    executor = rclpy.executors.MultiThreadedExecutor()  #Allows multiple nodes to run simultaneously.

    for node in followers:
        executor.add_node(node)

    executor.spin()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
