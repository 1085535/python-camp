#habit tracker

import tkinter as tk
def addfunc():
    new_habit_name = entry_widget.get()
    habits.append(new_habit_name)
    print(habits)
    entry_widget.delete(0,tk.END)
window = tk.Tk()
window.title("Habit Tracker")
title_label =tk.Label(window, text="Habit Tracker")
first_habit=tk.Label(window, text="Drink water-streak three days")
def mark_done():
    print("clicked!")
mark_as_done=tk.Button(window, text="Mark as done",command=mark_done)
habit_button=tk.Button(window, text="Add habit", command=addfunc)
habit_button.pack()
title_label.pack()
first_habit.pack()
mark_as_done.pack()


entry_widget=tk.Entry(window)
entry_widget.pack()

habits=[]

window.mainloop()