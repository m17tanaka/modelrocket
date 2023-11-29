import time
import serial

# シリアルポートの設定
serial_port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

try:
    while True:
        # シリアルポートにデータを書き込む
        serial_port.write(b"hello\n")
        
        # 1秒待機
        time.sleep(1)

except KeyboardInterrupt:
    # Ctrl+Cが押されたときに終了する
    print("\nプログラムが終了しました。")

finally:
    # シリアルポートを閉じる
    serial_port.close()
