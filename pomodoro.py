import sys
import time
import signal
from pathlib import Path

try:
    import winsound
except ImportError:
    winsound = None

WORK_SECONDS = 25 * 60
BREAK_SECONDS = 5 * 60

running = True


def handle_interrupt(signum, frame):
    global running
    running = False
    print("\nStopping Pomodoro timer...")


def format_time(seconds: int) -> str:
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def beep() -> None:
    if winsound:
        try:
            winsound.Beep(750, 500)
        except RuntimeError:
            print("\a", end="", flush=True)
    else:
        print("\a", end="", flush=True)


def countdown(duration: int, label: str) -> bool:
    end_time = time.time() + duration
    while running and time.time() < end_time:
        remaining = int(end_time - time.time())
        if remaining < 0:
            remaining = 0
        print(f"{label:<6} | {format_time(remaining)}", end="\r", flush=True)
        time.sleep(1)
    print(" " * 40, end="\r", flush=True)
    return running


def main() -> int:
    signal.signal(signal.SIGINT, handle_interrupt)
    print("Pomodoro Timer started. Press Ctrl+C to stop.")
    session = "Work"
    while running:
        duration = WORK_SECONDS if session == "Work" else BREAK_SECONDS
        label = f"{session}" if session == "Work" else "Break"
        active_text = f"{label} Session"
        print(f"{active_text} - {format_time(duration)}")
        if not countdown(duration, active_text):
            break
        beep()
        if not running:
            break
        print(f"{label} session finished!\n")
        session = "Break" if session == "Work" else "Work"

    print("Pomodoro Timer stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
