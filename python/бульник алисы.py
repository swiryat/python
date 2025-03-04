import time
import datetime

# Функция для установки будильника
def set_alarm(hour, minute):
    # Создаем объект datetime с текущими временем и датой
    now = datetime.datetime.now()
    
    # Устанавливаем время будильника
    alarm_time = now.replace(hour=hour, minute=minute)
    
    # Сохраняем время будильника в переменную
    alarm = alarm_time.strftime('%H:%M')
    
    print('Будильник установлен на', alarm)


# Основной код программы
while True:
    now = datetime.datetime.now().strftime('%H:%M')

    # Выводим текущее время
    print(now)
time.sleep(1)

# Установка будильника
set_alarm(8, 30)
