#habit tracker

import tkinter as tk

window = tk.Tk()
window.title("Habit Tracker")
title_label =tk.Label(window, text="Habit Tracker")
first_habit=tk.Label(window, text="Drink water-streak three days")
def mark_done():
    print("clicked!")
habit_button=tk.Button(window, text="Mark as done",command=mark_done)
title_label.pack()
first_habit.pack()
habit_button.pack()
window.mainloop()

entry_widget=tk.Entry(parent_window)