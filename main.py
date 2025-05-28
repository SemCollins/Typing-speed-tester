import customtkinter as ctk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import time
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

sample_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a powerful programming language.",
    "Typing fast and accurately takes practice.",
    "Graphical user interfaces make applications interactive.",
    "Errors should never pass silently.",
    "Practice makes perfect in everything you do.",
    "Consistency is the key to mastering any skill.",
    "Always strive for progress, not perfection.",
    "The journey of learning never truly ends.",
    "Success comes to those who are persistent.",
    "Attention to detail sets professionals apart.",
    "Learning to type fast saves valuable time.",
    "Coding challenges improve logical thinking.",
    "Great ideas often come from collaboration.",
    "Stay calm and type on with confidence."
]

class TypingSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.geometry("1000x750")
        self.root.resizable(False, False)

        self.level = 1
        self.highest_score = 0
        self.highest_level = 1
        self.time_limit = 60
        self.remaining_time = self.time_limit
        self.start_time = None
        self.current_text = random.choice(sample_texts)
        self.timer_running = False

        try:
            bg_image = Image.open("i/background.png").resize((1000, 750))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = ctk.CTkLabel(self.root, image=self.bg_photo, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Background image not found.")

        self.create_widgets()

    def create_widgets(self):
        try:
            logo = Image.open("i/coyote.png").resize((100, 100))
            self.logo_photo = ImageTk.PhotoImage(logo)
            ctk.CTkLabel(self.root, image=self.logo_photo, text="").place(x=30, y=30)
        except FileNotFoundError:
            print("Logo image not found.")

        ctk.CTkLabel(self.root, text="Typing Speed Tester", font=("Segoe UI", 32, "bold")).pack(pady=20)

        self.instruction = ctk.CTkLabel(self.root, text=f"Level {self.level}: Type the sentence within {self.time_limit} seconds.", font=("Segoe UI", 16))
        self.instruction.pack(pady=10)

        self.countdown_label = ctk.CTkLabel(self.root, text=f"Time Remaining: {self.remaining_time}s", font=("Segoe UI", 16))
        self.countdown_label.pack()

        self.text_display = ctk.CTkLabel(self.root, text=self.current_text, wraplength=850, justify="center", font=("Segoe UI", 18, "italic"), text_color="green")
        self.text_display.pack(pady=20)

        self.typing_input = ctk.CTkTextbox(self.root, height=120, width=900, font=("Consolas", 14))
        self.typing_input.pack(pady=10)
        self.typing_input.bind("<KeyPress>", self.start_typing)
        self.typing_input.bind("<Return>", self.handle_enter_key)
        self.typing_input.focus_set()

        self.result_label = ctk.CTkLabel(self.root, text="", font=("Segoe UI", 14))
        self.result_label.pack(pady=10)

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        self.done_button = ctk.CTkButton(button_frame, text="Done", command=self.calculate_speed, text_color="black")
        self.done_button.grid(row=0, column=0, padx=10)

        self.reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_test, text_color="black")
        self.reset_button.grid(row=0, column=1, padx=10)

        self.help_button = ctk.CTkButton(button_frame, text="Help", command=self.show_help, text_color="black")
        self.help_button.grid(row=0, column=2, padx=10)

        self.stats_button = ctk.CTkButton(button_frame, text="Stats", command=self.show_stats, text_color="black")
        self.stats_button.grid(row=0, column=3, padx=10)

    def show_help(self):
        help_popup = ctk.CTkToplevel(self.root)
        help_popup.title("How to Use")
        help_popup.geometry("500x300")
        help_popup.transient(self.root)
        help_popup.grab_set()
        help_popup.resizable(False, False)

        help_text = (
            "1. Read the sentence displayed.\n"
            "2. Start typing in the input box.\n"
            "3. The timer starts with your first keystroke.\n"
            "4. Press 'Enter' or 'Done' when finished.\n"
            "5. Your speed and accuracy will be calculated.\n"
            "6. Aim for high accuracy and speed to advance levels."
        )
        ctk.CTkLabel(help_popup, text=help_text, font=("Segoe UI", 14), justify="left", wraplength=450).pack(padx=20, pady=20)
        ctk.CTkButton(help_popup, text="OK", command=help_popup.destroy, text_color="black").pack(pady=10)

    def show_stats(self):
        stats_popup = ctk.CTkToplevel(self.root)
        stats_popup.title("Your Stats")
        stats_popup.geometry("500x300")
        stats_popup.transient(self.root)
        stats_popup.grab_set()
        stats_popup.resizable(False, False)

        try:
            bg = Image.open("i/cat.py").resize((500, 300))
            bg_photo = ImageTk.PhotoImage(bg)
            bg_label = ctk.CTkLabel(stats_popup, image=bg_photo, text="")
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            print("Stats background image not found or not valid.")

        ctk.CTkLabel(stats_popup, text=f"Highest Score: {self.highest_score}\nHighest Level: {self.highest_level}", font=("Segoe UI", 16)).pack(pady=40)
        ctk.CTkButton(stats_popup, text="Close", command=stats_popup.destroy, text_color="black").pack(pady=10)

    def start_typing(self, event):
        if self.start_time is None:
            self.start_time = time.time()
            self.remaining_time = self.time_limit
            self.timer_running = True
            self.update_countdown()

    def update_countdown(self):
        if self.remaining_time > 0 and self.timer_running:
            if self.remaining_time > 30:
                self.text_display.configure(text_color="green")
            elif self.remaining_time > 10:
                self.text_display.configure(text_color="yellow")
            else:
                self.text_display.configure(text_color="red")

            self.countdown_label.configure(text=f"Time Remaining: {self.remaining_time}s")
            self.remaining_time -= 1
            self.root.after(1000, self.update_countdown)
        elif self.timer_running:
            self.timer_running = False
            self.time_up_popup()

    def handle_enter_key(self, event):
        self.calculate_speed()
        return "break"

    def calculate_speed(self):
        if self.start_time is None:
            messagebox.showwarning("Warning", "Start typing to begin the test!")
            return

        self.timer_running = False
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        user_input = self.typing_input.get("1.0", "end").strip()
        word_count = len(user_input.split())
        accuracy = self.calculate_accuracy(user_input, self.current_text)
        speed = word_count / (elapsed_time / 60)
        score = round((speed + accuracy) / 2)

        self.result_label.configure(text=f"Speed: {speed:.2f} WPM | Accuracy: {accuracy:.2f}% | Time: {elapsed_time:.2f}s | Score: {score}")

        if score > self.highest_score:
            self.highest_score = score

        if self.level > self.highest_level:
            self.highest_level = self.level

        if elapsed_time <= self.time_limit and accuracy >= 85:
            self.show_congratulations(speed, accuracy, score)
            self.level += 1
            self.time_limit = max(self.time_limit - 5, 20)
            self.reset_test()

    def time_up_popup(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Time Up")
        popup.geometry("400x200")
        popup.transient(self.root)
        popup.grab_set()
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="⏰ Time is up!", font=("Segoe UI", 18)).pack(pady=20)
        ctk.CTkButton(popup, text="Try Again", command=lambda: [popup.destroy(), self.reset_test()], text_color="black").pack(pady=10)

    def show_congratulations(self, speed, accuracy, score):
        top = ctk.CTkToplevel(self.root)
        top.title("Congratulations!")
        top.geometry("500x300")
        top.transient(self.root)
        top.grab_set()
        top.resizable(False, False)

        try:
            bg = Image.open("i/beauty.png").resize((500, 300))
            bg_photo = ImageTk.PhotoImage(bg)
            bg_label = ctk.CTkLabel(top, image=bg_photo, text="")
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Popup background image not found.")

        ctk.CTkLabel(top, text=f"🎉 Great Job! You've completed Level {self.level}! 🎉", font=("Segoe UI", 14)).pack(pady=10)
        ctk.CTkLabel(top, text=f"Speed: {speed:.2f} WPM\nAccuracy: {accuracy:.2f}%\nScore: {score}", font=("Segoe UI", 12)).pack(pady=10)

        ctk.CTkButton(top, text="OK", command=top.destroy, text_color="black").pack(pady=10)

    def calculate_accuracy(self, typed_text, original_text):
        correct_chars = sum(1 for a, b in zip(typed_text, original_text) if a == b)
        total_chars = len(original_text)
        return (correct_chars / total_chars) * 100 if total_chars > 0 else 0

    def reset_test(self):
        self.start_time = None
        self.remaining_time = self.time_limit
        self.timer_running = False
        self.current_text = random.choice(sample_texts)
        self.text_display.configure(text=self.current_text, text_color="green")
        self.typing_input.delete("1.0", "end")
        self.result_label.configure(text="")
        self.instruction.configure(text=f"Level {self.level}: Type the sentence within {self.time_limit} seconds.")
        self.countdown_label.configure(text=f"Time Remaining: {self.remaining_time}s")
        self.typing_input.focus_set()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TypingSpeedTester(root)
    root.mainloop()
