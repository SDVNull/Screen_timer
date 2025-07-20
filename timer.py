import time
import os
import threading
import winsound
import pystray
from PIL import Image, ImageDraw


WORK_TIME = 50 * 60  # 50 минут в секундах
BREAK_TIME = 10 * 60  # 10 минут в секундах


def create_icon():
    """Создает изображение для значка в трее"""
    image = Image.new('RGB', (64, 64), 'white')
    dc = ImageDraw.Draw(image)
    dc.ellipse((10, 10, 54, 54), fill='blue')
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
    image = create_icon()
    menu = pystray.Menu(
        pystray.MenuItem("Выход", on_exit)
    )
    icon = pystray.Icon("50 min Timer ", image, "50 минутный Таймер", menu)
    icon.run()


if __name__ == "__main__":
    # Запуск таймера в отдельном потоке
    thread = threading.Thread(target=work_cycle, args=(None,), daemon=True)
    thread.start()

    # Запуск интерфейса в трее
    run_tray_app()
