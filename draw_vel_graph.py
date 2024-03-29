import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os


def get_file_name_without_extension(path: str) -> str:
    file_name = os.path.basename(path)
    return os.path.splitext(file_name)[0]

def main(args):
    save_dir = args.save_dir
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    
    # グラフを描画するための空のリストを作成
    all_time = []
    all_velocity_magnitude = []
    all_csv_names = []  # ファイル名を保持するリスト
    
    # CSVファイルのパス
    for idx, csv in enumerate(args.logcsv):
        # CSVファイルを読み込む
        data = pd.read_csv(csv)
        # 時刻と速度の列を抽出
        time = data.time
        linear_x = data.linear_x
        linear_y = data.linear_y
        linear_z = data.linear_z

        # 速度の合成
        velocity_magnitude = np.sqrt(linear_x**2 + linear_y**2 + linear_z**2)
        
        # 時刻をシフトする
        if idx < len(args.time_shift):
            time = time + args.time_shift[idx]
        
        # 全体のリストにデータを追加
        all_time.append(time)
        all_velocity_magnitude.append(velocity_magnitude)
        
        # ファイル名をリストに追加
        all_csv_names.append(get_file_name_without_extension(csv))

    # グラフを描画
    plt.figure(figsize=(10, 6))
    for time, velocity_magnitude, label in zip(all_time, all_velocity_magnitude, all_csv_names):
        plt.plot(time, velocity_magnitude, label=label)
    plt.xlabel("Time[s]")
    plt.ylabel("Velocity Magnitude")
    plt.title("Velocity Magnitude Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_dir, 'combined_plot02.png'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--logcsv", nargs="*", default=["log/velocity_data.csv", "log/velocity_data02.csv"])
    parser.add_argument("--save_dir", default="fig")
    parser.add_argument("--time_shift", nargs="*", type=float, default=[])
    args = parser.parse_args()
    main(args)
