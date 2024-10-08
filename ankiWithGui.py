import time
import threading
import tkinter as tk


class TimerApp:
    def __init__(self, master, work_duration, break_duration, repetitions):
        self.master = master
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.repetitions = repetitions
        self.current_rep = 0
        self.is_paused = threading.Event()
        self.is_paused.set()  # Start with the timer running
        self.is_running = False

        # Setup GUI Elements
        self.master.title("Study Timer")
        self.master.geometry("300x200")

        self.label = tk.Label(
            master, text="Press 'Start' to begin!", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.repetitions_spingbox = tk.Button(
            master, text="Number of repitions", font=("Helvetica", 16)
        )

        # Add Spinbox for setting repetitions
        tk.Label(master, text="Set number of Repetitions:",
                 font=("Helvetica", 14)).pack(pady=5)
        self.repetitions_spinbox = tk.Spinbox(master, from_=1, to=10, font=(
            "Helvetica", 12), command=self.update_repetitions)
        self.repetitions_spinbox.pack(pady=5)

        # Add Spinbox for setting work_duration
        tk.Label(master, text="Set work duration in minutes:",
                 font=("Helvetica", 14)).pack(pady=5)
        self.repetitions_spinbox = tk.Spinbox(master, from_=1, to=60, font=(
            "Helvetica", 12), command=self.update_work_duration)
        self.repetitions_spinbox.pack(pady=5)

        # Add Spinbox for setting break_duration
        tk.Label(master, text="Set break duration in seconds:",
                 font=("Helvetica", 14)).pack(pady=5)
        self.repetitions_spinbox = tk.Spinbox(master, from_=1, to=10, font=(
            "Helvetica", 12), command=self.update_break_duration)
        self.repetitions_spinbox.pack(pady=5)

        self.time_label = tk.Label(master, text="", font=("Helvetica", 16))
        self.time_label.pack(pady=10)

        self.start_button = tk.Button(
            master, text="Start", command=self.start_timer, font=("Helvetica", 12))
        self.start_button.pack(side="left", padx=20)

        self.pause_button = tk.Button(
            master, text="Pause", command=self.pause_timer, state="disabled", font=("Helvetica", 12))
        self.pause_button.pack(side="left", padx=20)

        self.resume_button = tk.Button(
            master, text="Resume", command=self.resume_timer, state="disabled", font=("Helvetica", 12))
        self.resume_button.pack(side="left", padx=20)

    def update_repetitions(self):
        """Update repetitions based on Spinbox value"""
        self.repetitions = int(self.repetitions_spinbox.get())

    def update_work_duration(self):
        """Update work based on Spinbox value"""
        self.repetitions = int(self.repetitions_spinbox.get())*60

    def update_break_duration(self):
        """Update break based on Spinbox value"""
        self.repetitions = int(self.repetitions_spinbox.get())

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.current_rep = 0
            threading.Thread(target=self.run_timer).start()

    def pause_timer(self):
        self.is_paused.clear()
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="normal")
        self.label.config(text="Timer Paused")

    def resume_timer(self):
        self.is_paused.set()
        self.resume_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.label.config(text="Resuming...")

    def run_timer(self):
        for rep in range(self.repetitions):
            self.current_rep = rep + 1
            self.label.config(
                text=f"Round {self.current_rep}: Start studying!")

            # Work Duration Countdown
            for remaining in range(self.work_duration, 0, -1):
                self.is_paused.wait()  # Pause if cleared
                minutes, seconds = divmod(remaining, 60)
                self.time_label.config(text=f"Time remaining: {
                                       minutes:02d}:{seconds:02d}")
                time.sleep(1)

            # Short break message
            self.label.config(text="Time for a break!")
            self.time_label.config(text="")
            time.sleep(self.break_duration)

            self.label.config(
                text=f"Round {self.current_rep} complete. Switch deck!")

        # Completion message
        self.label.config(text="All rounds completed!")
        self.time_label.config(text="")
        self.is_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="disabled")


# Parameters for the timer
work_duration = 2  # Example value: 10 min in seconds
break_duration = 3  # Example value: 5 seconds
repetitions = 3  # default value (?)

# Create the main window and run the app
root = tk.Tk()
app = TimerApp(root, work_duration, break_duration, repetitions)
root.mainloop()
