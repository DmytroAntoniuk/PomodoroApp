from tkinter import *
import math
from tkinter import messagebox, simpledialog
import winsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global timer
    if timer:
        window.after_cancel(timer)
        timer = None
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, timer
    if timer:
        return

    reps += 1
    update_timer_label_color()

    work_sec = simpledialog.askinteger("Input", "Enter work time in minutes:", minvalue=1, maxvalue=60) * 60
    short_break_sec = simpledialog.askinteger("Input", "Enter short break time in minutes:", minvalue=1,
                                              maxvalue=15) * 60
    long_break_sec = simpledialog.askinteger("Input", "Enter long break time in minutes:", minvalue=15,
                                             maxvalue=30) * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
    elif reps % 2 == 0:
        count_down(short_break_sec)
    else:
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(seconds):
    count_min = math.floor(seconds / 60)
    count_sec = seconds % 60
    canvas.itemconfig(timer_text, text=f"{count_min:02d}:{count_sec:02d}")
    if seconds > 0:
        global timer
        timer = window.after(1000, count_down, seconds - 1)
    else:
        play_sound()
        start_timer()
        update_checkmark()


def play_sound():
    winsound.Beep(440, 1000)


# ---------------------------- UI SETUP ------------------------------- #
def update_checkmark():
    marks = ""
    work_sessions = math.floor(reps / 2)
    for _ in range(work_sessions):
        marks += "✔"
    check_marks.config(text=marks)


def update_timer_label_color():
    if reps % 8 == 0:
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        timer_label.config(text="Break", fg=PINK)
    else:
        timer_label.config(text="Work", fg=GREEN)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        reset_timer()
        window.destroy()


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(window, fg=GREEN, bg=YELLOW, text="Timer", font=(FONT_NAME, 50))
timer_label.grid(column=1, row=0)

canvas = Canvas(window, width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(window, text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(window, text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(window, fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
