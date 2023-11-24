import serial
import csv

# シリアルポートの設定
ser = serial.Serial('/dev/ttyUSB0', 57600)  # '/dev/ttyUSB0'はRaspberry Pi Zero上のシリアルポートに依存します

elevation_data = []  # 標高のデータを保存するリスト
timestamps = []      # 時間のデータを保存するリスト

# CSVファイルにデータを保存するためのファイルハンドラを作成
csv_file = open('elevation_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'Temperature', 'Pressure', 'Elevation'])

current_time = 0  # 時間変数を初期化

# 指数移動平均の係数
alpha = 0.2

try:
    while True:
        received_line = ser.readline().decode().strip()  # データの受信

        # データの分割
        parts = received_line.split(',')
        if len(parts) == 2:
            tmp, pressure = map(float, parts)

            # 標高の計算
            elevation = (((101325 / pressure) ** (1 / 5.257) - 1) * (tmp + 273.15)) / 0.0065
            elevation_data.append(elevation)

            # 時間の計算
            timestamps.append(current_time)

            # CSVファイルにデータを追加
            csv_writer.writerow([current_time, tmp, pressure, elevation])

            # 時間変数を更新
            current_time += 1

except KeyboardInterrupt:
    ser.close()
    csv_file.close()
