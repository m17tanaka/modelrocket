import time
import datetime
import csv
import serial
import pandas as pd

ser1 = serial.Serial('/dev/tty.usbmodem716357A936391', 560000)
ser2 = serial.Serial('/dev/tty.usbmodem11201', 9600)  
file_name = 'test.csv'

with open(file_name, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["time", "power[N]", "distortion[mm]"])

    try:
        for i in range(1000):
            # ASCIIコードの入力
            ser1.write(b"4")
            sokuteiti = ser1.readline(16)  # /rを消す
            gomi = ser1.readline(1)

            # byte型を文字列に変換
            sokuteiti_disp = sokuteiti.strip().decode('UTF-8')
            s = '0x' + sokuteiti_disp
            sokutei = int(s, 0)
            # 位置計算
            Position = sokutei >> 17 & 0xffffffff

            # 距離計算
            Resolution = 0.000005
            kekka = Position * Resolution
            print(kekka, "mm")

            # Arduino
            val_arduino = ser2.readline()

            # byte型を文字列に変換
            val_arduino_disp = val_arduino.strip().decode('UTF-8')
            s2 = val_arduino_disp
            val = float(s2)

            # 力計算
            Sensitivity = 0.0002199
            tikara = val / Sensitivity
            print(tikara, "N")

            # CSVへの出力
            rows = [[datetime.datetime.now().strftime("%H:%M:%S"), tikara, kekka]]
            for row in rows:
                writer.writerow(row)
            time.sleep(0.02)

    finally:
        print("終了")
        ser1.close()
        ser2.close()
