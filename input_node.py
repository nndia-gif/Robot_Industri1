import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class InputNode(Node):

    def __init__(self):
        super().__init__('input_node')

        self.publisher = self.create_publisher(
            Twist,
            '/input_ik',
            10
        )

    def send_input(self, v, omega):
        msg = Twist()

        msg.linear.x = v
        msg.angular.z = omega

        self.publisher.publish(msg)

        print()
        print("Input:")
        print(f"  v     = {v:.3f} m/s")
        print(f"  omega = {omega:.3f} rad/s")
        print("Input dikirim ke /input_ik")


def main(args=None):
    rclpy.init(args=args)

    node = InputNode()

    print()
    print("======================================")
    print("       INVERSE KINEMATICS INPUT       ")
    print("======================================")
    print("Masukkan nilai v dan omega.")
    print("Ketik q untuk keluar.")
    print()

    try:
        while rclpy.ok():

            v_input = input("Kecepatan linear v (m/s) : ")

            if v_input.lower() == 'q':
                break

            omega_input = input("Kecepatan angular ω (rad/s): ")

            if omega_input.lower() == 'q':
                break

            try:
                v = float(v_input)
                omega = float(omega_input)

                node.send_input(v, omega)

            except ValueError:
                print("Input harus berupa angka.")
                print()

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
