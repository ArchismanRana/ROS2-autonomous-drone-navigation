import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBool, SetMode
import math

class OffboardSineWave(Node):
    def __init__(self):
        super().__init__('offboard_sine_wave_mavros')

        # Publishers
        self.local_pos_pub = self.create_publisher(
            PoseStamped,
            '/mavros/setpoint_position/local',
            10
        )

        # Service clients (for arming and mode)
        self.arming_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')

        # Timer for publishing setpoints (10 Hz)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # Internal state
        self.counter = 0
        self.start_time = self.get_clock().now().nanoseconds / 1e9
        self.state = "init"
        self.takeoff_height = 3.0  # meters up
        self.last_x = 0.0
        self.last_y = 0.0

        # Wait for services
        self.get_logger().info("Waiting for MAVROS services...")
        self.arming_client.wait_for_service()
        self.set_mode_client.wait_for_service()
        self.get_logger().info("Connected to MAVROS services")

        # Set to OFFBOARD mode and arm
        self.set_mode("OFFBOARD")
        self.arm()

    # -----------------------------
    # MAVROS service helper methods
    # -----------------------------
    def arm(self):
        req = CommandBool.Request()
        req.value = True
        future = self.arming_client.call_async(req)
        self.get_logger().info("Arming drone...")
        rclpy.spin_until_future_complete(self, future)
        if future.result() and future.result().success:
            self.get_logger().info("✅ Armed successfully")
        else:
            self.get_logger().warn("❌ Arming failed")

    def disarm(self):
        req = CommandBool.Request()
        req.value = False
        future = self.arming_client.call_async(req)
        self.get_logger().info("Disarming drone...")
        rclpy.spin_until_future_complete(self, future)
        if future.result() and future.result().success:
            self.get_logger().info("✅ Disarmed successfully")
        else:
            self.get_logger().warn("❌ Disarming failed")

    def set_mode(self, mode_name):
        req = SetMode.Request()
        req.custom_mode = mode_name
        future = self.set_mode_client.call_async(req)
        self.get_logger().info(f"Setting mode to {mode_name}...")
        rclpy.spin_until_future_complete(self, future)
        if future.result() and future.result().mode_sent:
            self.get_logger().info(f"✅ Mode set to {mode_name}")
        else:
            self.get_logger().warn("❌ Failed to set mode")

    # -----------------------------
    # Main control loop
    # -----------------------------
    def publish_setpoint(self, x, y, z):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        self.local_pos_pub.publish(msg)

    def timer_callback(self):
        if self.state == "init":
            # Publish a few setpoints before switching to OFFBOARD mode
            self.publish_setpoint(0.0, 0.0, 0.0)
            self.counter += 1
            if self.counter > 20:
                self.state = "takeoff"
                self.counter = 0
                self.get_logger().info("Taking off...")

        elif self.state == "takeoff":
            self.publish_setpoint(0.0, 0.0, self.takeoff_height)
            self.counter += 1
            if self.counter > 100:
                self.state = "sine_wave"
                self.start_time = self.get_clock().now().nanoseconds / 1e9
                self.get_logger().info("Starting sine wave pattern...")

        elif self.state == "sine_wave":
            elapsed = (self.get_clock().now().nanoseconds / 1e9) - self.start_time
            x = elapsed * 1.0  # forward motion
            y = 0.0
            z = self.takeoff_height + math.sin(elapsed * 1.5) * 1.0
            self.publish_setpoint(x, y, z)

            self.last_x, self.last_y = x, y

            if elapsed > 20:
                self.state = "land"
                self.counter = 0
                self.get_logger().info("Landing...")

        elif self.state == "land":
            self.publish_setpoint(self.last_x, self.last_y, 0.0)
            self.counter += 1
            if self.counter > 100:
                self.disarm()
                self.get_logger().info("✅ Landing complete. Shutting down.")
                rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = OffboardSineWave()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
