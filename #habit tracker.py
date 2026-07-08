#habit tracker

import tkinter as tk

window = tk.Tk()
window.title("Habit Tracker")
title_label =tk.Label(window, text="Habit Tracker")
first_habit=tk.Label(window, text="Drink water-streak three days")
habit_button=tk.Button(window, text="Mark as done")
title_label.pack()
first_habit.pack()
habit_button.pack()
window.mainloop()