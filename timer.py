import time
import os
import winsound

WORK_TIME = 3000  # 50 минут работы (3000 секунд)
BREAK_TIME = 600  # 10 минут перерыва (600 секунд)


def lock_screen():
    """Блокирует экран (только для Windows)"""
    os.system("rundll32.exe user32.dll, LockWorkStation")

def play_sound():
    for _ in range(5):
        winsound.Beep(1000, 500)
        time.sleep(0.5)

def work_cycle():
    while True:
        # Рабочий цикл
        for i in range(WORK_TIME, 0, -1):
            mins, secs = divmod(i, 60)
            timer_text = f"\r[Работа] Осталось: {mins:02d}:{secs:02d}"
            print(timer_text, end="")
            time.sleep(1)

        # Блокировка экрана после работы
        lock_screen()
        print("\nЭкран заблокирован. Перерыв начался.")

        # Перерыв
        for i in range(BREAK_TIME, 0, -1):
            mins, secs = divmod(i, 60)
            timer_text = f"\r[Перерыв] Осталось: {mins:02d}:{secs:02d}"
            print(timer_text, end="")
            time.sleep(1)

        play_sound()
        print("\nПерерыв окончен. Начался новый рабочий цикл.")


if __name__ == "__main__":
    print("Старт таймера. Ctrl+C для выхода.")
    work_cycle()

#  Команды для сборки
# pyinstaller --onefile --upx-dir C:\upx timer.py
# pyinstaller --onefile --noconsole --upx-dir C:\upx timer.py
