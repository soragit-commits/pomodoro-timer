import tkinter as tk
from tkinter import ttk
import time
import threading

try:
    import winsound
except ImportError:
    winsound = None

WORK_SECONDS = 25 * 60
BREAK_SECONDS = 5 * 60


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use("clam")
        
        self.is_work = True
        self.remaining = WORK_SECONDS
        self.total = WORK_SECONDS
        self.is_running = False
        self.paused_time = 0
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Session label
        self.session_label = tk.Label(
            main_frame,
            text="WORK SESSION",
            font=("Helvetica", 24, "bold"),
            fg="blue"
        )
        self.session_label.pack(pady=(0, 20))
        
        # Time display
        self.time_label = tk.Label(
            main_frame,
            text="25:00",
            font=("Helvetica", 80, "bold"),
            fg="blue"
        )
        self.time_label.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            length=400,
            mode="determinate",
            value=100
        )
        self.progress.pack(pady=20)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        
        self.start_button = ttk.Button(
            button_frame,
            text="START",
            command=self.start_timer,
            width=15
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ttk.Button(
            button_frame,
            text="PAUSE",
            command=self.pause_timer,
            width=15,
            state=tk.DISABLED
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = ttk.Button(
            button_frame,
            text="RESET",
            command=self.reset_timer,
            width=15
        )
        self.reset_button.grid(row=0, column=2, padx=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Session Info", padding="10")
        stats_frame.pack(pady=20, fill=tk.X)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Sessions completed: 0",
            font=("Helvetica", 12)
        )
        self.stats_label.pack()
        
        self.sessions_completed = 0
        self.timer_thread = None
    
    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def update_display(self):
        self.time_label.config(text=self.format_time(self.remaining))
        progress = (self.total - self.remaining) / self.total * 100
        self.progress["value"] = progress
    
    def beep(self):
        if winsound:
            try:
                winsound.Beep(800, 500)
            except RuntimeError:
                pass
    
    def run_timer(self):
        while self.is_running and self.remaining > 0:
            time.sleep(1)
            if self.is_running:
                self.remaining -= 1
                self.root.after(0, self.update_display)
        
        if self.is_running and self.remaining == 0:
            self.beep()
            self.is_running = False
            self.root.after(0, self.switch_session)
    
    def switch_session(self):
        self.is_work = not self.is_work
        self.remaining = WORK_SECONDS if self.is_work else BREAK_SECONDS
        self.total = self.remaining
        
        if not self.is_work:
            self.sessions_completed += 1
            self.stats_label.config(
                text=f"Sessions completed: {self.sessions_completed}"
            )
        
        self.session_label.config(
            text="WORK SESSION" if self.is_work else "BREAK TIME",
            fg="blue" if self.is_work else "#388E3C"
        )
        self.time_label.config(fg="blue" if self.is_work else "#388E3C")
        self.update_display()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
    
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.DISABLED)
            
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def pause_timer(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
    
    def reset_timer(self):
        self.is_running = False
        self.is_work = True
        self.remaining = WORK_SECONDS
        self.total = WORK_SECONDS
        self.sessions_completed = 0
        
        self.session_label.config(text="WORK SESSION", fg="blue")
        self.time_label.config(fg="blue")
        self.stats_label.config(text="Sessions completed: 0")
        self.update_display()
        
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
