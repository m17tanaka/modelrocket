import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

# シリアルポートの設定
ser = serial.Serial('/dev/ttyUSB0', 57600)  # '/dev/ttyUSB0'はRaspberry Pi Zero上のシリアルポートに依存します

elevation_data = []  # 標高のデータを保存するリスト
smoothed_data = []   # 平滑化されたデータを保存するリスト
timestamps = []      # 時間のデータを保存するリスト

# CSVファイルにデータを保存するためのファイルハンドラを作成
csv_file = open('elevation_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'Temperature', 'Pressure', 'Elevation'])

current_time = 0  # 時間変数を初期化

# 指数移動平均の係数
alpha = 0.2

# アニメーションのコールバック関数
def animate(frame):
    global current_time

    received_line = ser.readline().decode().strip()  # データの受信

    # データの分割
    parts = received_line.split(',')
    if len(parts) == 2:
        tmp, pressure = map(float, parts)

        # 標高の計算
        elevation = (((101325 / pressure) ** (1 / 5.257) - 1) * (tmp + 273.15)) / 0.0065
        elevation_data.append(elevation)

        # 平滑化されたデータの計算（指数移動平均）
        if not smoothed_data:
            smoothed_data.append(elevation)
        else:
            smoothed_data.append(alpha * elevation + (1 - alpha) * smoothed_data[-1])

        # 時間の計算
        timestamps.append(current_time)

        # CSVファイルにデータを追加
        csv_writer.writerow([current_time, tmp, pressure, elevation])

        # 時間変数を更新
        current_time += 1

    # プロットの設定
    plt.cla()
    plt.plot(timestamps, elevation_data, label='Raw Data')
    plt.plot(timestamps, smoothed_data, label='Smoothed Data')
    plt.xlabel('Time')
    plt.ylabel('Elevation')
    plt.title('Real-time Elevation Plot with Low-pass Filter')

    # 縦軸の範囲を指定
    plt.ylim(80, 150)

    plt.legend()

# アニメーションの作成
ani = FuncAnimation(plt.gcf(), animate, frames=None, interval=100, cache_frame_data=False)  # 100ミリ秒ごとにデータを受信

# プロットの表示
plt.show()
