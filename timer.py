import time
import os
import threading
import winsound
import math
import pystray
from PIL import Image, ImageDraw


WORK_TIME = 50 * 60  # 50 минут в секундах
BREAK_TIME = 10 * 60  # 10 минут в секундах

stop_event = threading.Event()

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
    for _ in range(ran):
        winsound.Beep(frequency, duration)
        time.sleep(0.5)


def lock_screen():
    """Блокирует экран (только для Windows)"""
    os.system("rundll32.exe user32.dll, LockWorkStation")


def work_cycle():
    """Цикл работы -> отдыха"""
    while not stop_event.is_set():
        play_sound(1000, 1000, 3)
        time.sleep(WORK_TIME)

        lock_screen()
        play_sound(500, 1000, 3)
        time.sleep(BREAK_TIME)

def on_restart():
    """Останавливает текущий таймер и запускает его заново"""
    stop_event.set()  # Сигнализируем остановку текущего цикла
    time.sleep(0.1)   # Небольшая задержка для завершения потока
    stop_event.clear()  # Сбрасываем событие для нового запуска
    restart_thread = threading.Thread(target=work_cycle, daemon=True)
    restart_thread.start()

def on_exit(icon):
    icon.stop()
    exit()


def run_tray_app():
    """Запуск приложения в трее"""
    image = create_clock_icon()
    menu = pystray.Menu(
        pystray.MenuItem("Перезапустить", on_restart),
        pystray.MenuItem("Выход", on_exit)
    )
    icon = pystray.Icon("50 min Timer", image, "50 минутный Таймер", menu)
    icon.run()


if __name__ == "__main__":
    # Запуск таймера в отдельном потоке
    thread = threading.Thread(target=work_cycle, daemon=True)
    thread.start()

    # Запуск интерфейса в трее
    run_tray_app()
