import serial

# Настройка последовательного порта (измените параметры в зависимости от вашего оборудования)
ser = serial.Serial(
    port='COM3',      # Замените на порт вашего радиомодуля
    baudrate=9600,    # Скорость передачи данных
    timeout=1         # Таймаут для чтения (в секундах)
)

def read_radio_data():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(f"Полученные данные: {data}")

try:
    read_radio_data()
except KeyboardInterrupt:
    print("Завершение работы")
finally:
    ser.close()
