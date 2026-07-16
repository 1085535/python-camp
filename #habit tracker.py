#habit tracker

import tkinter as tk
def addfunc():
    new_habit_name = entry_widget.get()
    habits.append(new_habit_name)
    print(habits)
    entry_widget.delete(0,tk.END)
def mark_done():
    print("clicked!")
def on_entry_click(event):
    if entry_widget.get()=="New habit...":
        entry_widget.delete(0,tk.END)
        entry_widget.config(fg="black")
def on_entry_leave(event):
    if entry_widget.get()=="":
        entry_widget.insert(0, "New habit...")
        entry_widget.config(fg="black")
window = tk.Tk()
window.title("Habit Tracker")
title_label =tk.Label(window, text="Habit Tracker")
first_habit=tk.Label(window, text="Drink water-streak three days")
mark_as_done=tk.Button(window, text="Mark as done",command=mark_done)
habit_button=tk.Button(window, text="Add habit", command=addfunc)


habit_button.pack()
title_label.pack()
first_habit.pack()
mark_as_done.pack()


entry_widget=tk.Entry(window)
entry_widget.insert(0,"New habit...")
entry_widget.config(fg="gray")
entry_widget.bind("<FocusIn>",on_entry_click)
entry_widget.bind("<FocusOut>", on_entry_leave)
entry_widget.pack()

habits=[]

window.mainloop()