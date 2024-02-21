import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import csv
import os
import argparse
import re


# def find_next_available_filename(directory: str, base_name: str) -> str:
#     if not os.path.exists(directory):
#         return f"{base_name}01"
#     # ディレクトリ内のファイルをリストアップ
#     existing_files = os.listdir(directory)
#     matching_files = []
#     # base_nameに一致するファイル名を抽出（拡張子を無視）
#     pattern = re.compile(f"^{re.escape(base_name)}(\d+)(?:\..*)?$")
#     for filename in existing_files:
#         match = pattern.match(filename)
#         if match:
#             number = int(match.group(1))
#             matching_files.append(number)
#     if not matching_files:
#         # base_nameに一致するファイルが存在しない場合
#         return f"{base_name}01"
#     # 一致するファイルの中で最大の連番を見つける
#     max_number = max(matching_files)
#     # 新しいファイル名を生成
#     next_number = max_number + 1
#     new_filename = f"{base_name}{next_number:02d}"
#     return new_filename


class OdometrySubscriber(Node):
    def __init__(self, fname):
        super().__init__('odometry_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/localization/kinematic_state',
            self.odometry_callback,
            10
        )

        # CSVファイルのヘッダー
        self.csv_header = ['time', 'frame_id', 'linear_x', 'linear_y', 'linear_z', 'angular_x', 'angular_y', 'angular_z']
        self.csv_file = open(fname, 'w', newline='')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.csv_header)
        self.csv_writer.writeheader()

    def odometry_callback(self, msg):
        print('hello')
        # OdometryメッセージのデータをCSVファイルに書き込む
        data = {
            'time': msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
            'frame_id': msg.header.frame_id,
            'linear_x': msg.twist.twist.linear.x,
            'linear_y': msg.twist.twist.linear.y,
            'linear_z': msg.twist.twist.linear.z,
            'angular_x': msg.twist.twist.angular.x,
            'angular_y': msg.twist.twist.angular.y,
            'angular_z': msg.twist.twist.angular.z
        }
        self.csv_writer.writerow(data)

def main(args=None):
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    fname = args.save_dir + "/" + args.fname
    rclpy.init(args=None)
    odometry_subscriber = OdometrySubscriber(fname)
    rclpy.spin(odometry_subscriber)
    odometry_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fname", default="velocity_data.csv")
    parser.add_argument("--save_dir", default="log")
    args = parser.parse_args()
    main(args)