import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class InverseKinematics(Node):

    def __init__(self):
        super().__init__('inverse_kinematics')

        # Parameter robot
        self.wheel_radius = 0.03
        self.wheel_separation = 0.17

        # Subscriber input
        self.create_subscription(
            Twist,
            '/input_ik',
            self.velocity_callback,
            10
        )

        # Publisher roda kiri
        self.left_publisher = self.create_publisher(
            Float64,
            '/left_wheel/command',
            10
        )

        # Publisher roda kanan
        self.right_publisher = self.create_publisher(
            Float64,
            '/right_wheel/command',
            10
        )

        self.get_logger().info(
            'Inverse Kinematics aktif.'
        )

    def velocity_callback(self, msg):

        # Ambil input kecepatan robot
        VB = msg.linear.x
        omega = msg.angular.z

        # Parameter robot
        r = self.wheel_radius
        s = self.wheel_separation

        # Perhitungan inverse kinematics
        phi_L = (VB - (s * omega / 2)) / r
        phi_R = (VB + (s * omega / 2)) / r

        # Buat pesan output
        left_msg = Float64()
        right_msg = Float64()

        left_msg.data = phi_L
        right_msg.data = phi_R

        # Publish hasil
        self.left_publisher.publish(left_msg)
        self.right_publisher.publish(right_msg)

        # Tampilkan hasil
        self.get_logger().info(
            f'VB = {VB:.3f} m/s, '
            f'omega = {omega:.3f} rad/s | '
            f'Left = {phi_L:.3f} rad/s, '
            f'Right = {phi_R:.3f} rad/s'
        )


def main(args=None):
    rclpy.init(args=args)

    node = InverseKinematics()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
