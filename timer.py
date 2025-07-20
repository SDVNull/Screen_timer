import time
import os
import threading
import winsound
import pystray
from PIL import Image, ImageDraw


WORK_TIME = 50 * 60  # 50 минут в секундах
BREAK_TIME = 10 * 60  # 10 минут в секундах


def create_clock_icon():
    """Создает изображение часов для значка в трее"""
    # Создаем белый фон
    image = Image.new('RGB', (64, 64), 'white')
    draw = ImageDraw.Draw(image)
    
    # Центральные координаты
    center = (32, 32)
    radius = 25
    
    # Рисуем циферблат
    draw.ellipse(
        [center[0]-radius, center[1]-radius, 
         center[0]+radius, center[1]+radius],
        outline='black',
        width=2
    )
    
    # Рисуем часовые метки
    for hour in range(12):
        angle = 2 * 3.1416 * hour / 12
        
        # Координаты внешней точки
        x1 = center[0] + (radius - 5) * math.cos(angle)
        y1 = center[1] - (radius - 5) * math.sin(angle)
        
        # Координаты внутренней точки
        x2 = center[0] + (radius - 15) * math.cos(angle)
        y2 = center[1] - (radius - 15) * math.sin(angle)
        
        # Рисуем линию
        draw.line([x1, y1, x2, y2], fill='black', width=2)
    
    return image


def play_sound(frequency, duration, ran):
    for i in range(ran):
        winsound.Beep(frequency, duration)
        time.sleep(0.5)


def lock_screen():
    """Блокирует экран (только для Windows)"""
    os.system("rundll32.exe user32.dll, LockWorkStation")


def work_cycle(icon):
    """Цикл работы -> отдыха"""
    while True:
        print(f"Работаем {WORK_TIME//60} минут...")
        play_sound(1000, 1000, 3)
        time.sleep(WORK_TIME)

        print(f"Начало перерыва {BREAK_TIME//60} минут...")
        lock_screen()
        play_sound(500, 1000, 3)
        time.sleep(BREAK_TIME)


def on_exit(icon, item):
    icon.stop()
    exit()


def run_tray_app():
    """Запуск приложения в трее"""
    image = create_clock_icon()
    menu = pystray.Menu(
        pystray.MenuItem("Выход", on_exit)
    )
    icon = pystray.Icon("50 min Timer", image, "50 минутный Таймер", menu)
    icon.run()


if __name__ == "__main__":
    import math  # Добавлен импорт для математических операций
    # Запуск таймера в отдельном потоке
    thread = threading.Thread(target=work_cycle, args=(None,), daemon=True)
    thread.start()

    # Запуск интерфейса в трее
    run_tray_app()
