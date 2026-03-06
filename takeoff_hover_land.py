import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand
import math


class OffboardControl(Node):
    def __init__(self):
        super().__init__('offboard_sine_wave')

        # Publishers
        self.offboard_mode_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', 10)

        self.setpoint_pub = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)

        self.cmd_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', 10)

        # 10 Hz timer
        self.timer = self.create_timer(0.1, self.timer_callback)

        # States
        self.counter = 0
        self.state = "init"

        self.takeoff_height = -3.0  # drone will rise 3 meters
        self.last_x = 0.0
        self.last_y = 0.0

        self.get_logger().info("Offboard control node started.")


    # ---------------- VEHICLE COMMAND HELPERS ----------------

    def send_vehicle_command(self, command, p1=0.0, p2=0.0):
        msg = VehicleCommand()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.command = command
        msg.param1 = float(p1)
        msg.param2 = float(p2)
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        self.cmd_pub.publish(msg)

    def arm(self):
        self.get_logger().info("Sending ARM command...")
        self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)

    def disarm(self):
        self.get_logger().info("Sending DISARM command...")
        self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 0.0)

    def switch_to_offboard(self):
        self.get_logger().info("Switching to OFFBOARD mode...")
        # p1 = 1.0 (ignore) , p2 = 6.0 (PX4_CUSTOM_MAIN_MODE_OFFBOARD)
        self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)


    # ---------------- BASIC PUBLISHERS ----------------

    def publish_offboard_mode(self):
        msg = OffboardControlMode()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = True
        self.offboard_mode_pub.publish(msg)

    def publish_setpoint(self, x, y, z, yaw=0.0):
        msg = TrajectorySetpoint()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = [float(x), float(y), float(z)]
        msg.yaw = float(yaw)
        self.setpoint_pub.publish(msg)


    # ---------------- MAIN FSM LOOP ----------------

    def timer_callback(self):
        self.publish_offboard_mode()  # must always be sent

        # ---------------- INIT STATE ----------------
        if self.state == "init":
            # Send dummy setpoints to prepare Offboard
            self.publish_setpoint(0.0, 0.0, self.takeoff_height)
            self.counter += 1

            if self.counter == 20:
                self.switch_to_offboard()

            if self.counter == 30:
                self.arm()

            if self.counter > 40:
                self.get_logger().info("Takeoff sequence starting...")
                self.state = "takeoff"
                self.counter = 0

        # ---------------- TAKEOFF ----------------
        elif self.state == "takeoff":
            self.publish_setpoint(0.0, 0.0, self.takeoff_height)
            self.counter += 1
            if self.counter > 50:  # after 5 seconds
                self.get_logger().info("Reached takeoff height. Starting sine wave...")
                self.start_time = self.get_clock().now().nanoseconds / 1e9
                self.state = "sine_wave"

        # ---------------- SINE WAVE FLIGHT ----------------
        elif self.state == "sine_wave":
            now = self.get_clock().now().nanoseconds / 1e9
            elapsed = now - self.start_time

            x = elapsed * 1.0       # move forward 1 m/s
            y = 0.0                # stay centered
            z = self.takeoff_height + math.sin(elapsed * 1.5) # sine wave height

            self.publish_setpoint(x, y, z)
            self.last_x = x
            self.last_y = y

            if elapsed > 20:  # after 20 seconds
                self.get_logger().info("Sine wave complete. Starting landing...")
                self.state = "land"
                self.counter = 0

        # ---------------- LANDING ----------------
        elif self.state == "land":
            self.publish_setpoint(self.last_x, self.last_y, 0.0)
            self.counter += 1

            if self.counter > 80:  # 8 seconds down
                self.disarm()
                self.get_logger().info("Landing complete. Shutting down.")
                rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = OffboardControl()
    rclpy.spin(node)


if __name__ == '__main__':
    main()

