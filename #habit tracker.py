import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import date, timedelta

TITLE_FONT = ("Garamond", 24, "bold")
HEADER_FONT = ("Georgia", 12, "bold")
BODY_FONT = ("Segoe UI", 10)

PERIOD_WORDS = {"Daily": "days", "Monthly": "months", "Yearly": "years"}

BG_COLOR = "#FAF6F0"
TEXT_COLOR = "#3A3A3A"
SUBTEXT_COLOR = "#8A8A8A"

PRESET_COLORS = ["#E53935", "#FB8C00", "#FDD835", "#7CB342", "#1E88E5", "#5E35B1", "#D81B60", "#6D4C41", "#546E7A"]

def get_period_key(period, d):
    if period == "Daily":
        return str(d)
    elif period == "Monthly":
        return str(d.year) + "-" + str(d.month).zfill(2)
    else:
        return str(d.year)

def get_previous_period_key(period, d):
    if period == "Daily":
        return str(d - timedelta(days=1))
    elif period == "Monthly":
        year = d.year
        month = d.month - 1
        if month == 0:
            month = 12
            year -= 1
        return str(year) + "-" + str(month).zfill(2)
    else:
        return str(d.year - 1)

def darken_color(hex_color, factor=0.55):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def get_contrast_text_color(hex_color):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    brightness = (0.299 * r) + (0.587 * g) + (0.114 * b)
    if brightness > 150:
        return "black"
    else:
        return "white"

def draw_trash_icon(canvas):
    canvas.create_line(5, 7, 19, 7, fill="black", width=2)
    canvas.create_line(9, 7, 9, 4, fill="black", width=2)
    canvas.create_line(15, 7, 15, 4, fill="black", width=2)
    canvas.create_line(9, 4, 15, 4, fill="black", width=2)
    canvas.create_line(6, 7, 7, 20, fill="black", width=2)
    canvas.create_line(18, 7, 17, 20, fill="black", width=2)
    canvas.create_line(7, 20, 17, 20, fill="black", width=2)
    canvas.create_line(10, 10, 10, 17, fill="black", width=1)
    canvas.create_line(12, 10, 12, 17, fill="black", width=1)
    canvas.create_line(14, 10, 14, 17, fill="black", width=1)

def load_habits():
    try:
        file = open("habits.json", "r")
        loaded_data = json.load(file)
        file.close()

        for habit in loaded_data:
            if "current" not in habit:
                habit["current"] = 0
            if "goal" not in habit or habit["goal"] == 0:
                habit["goal"] = 1
            if "last_active" not in habit:
                habit["last_active"] = None
            if "color" not in habit:
                habit["color"] = "#4CAF50"
            if "period" not in habit:
                habit["period"] = "Daily"

        return loaded_data
    except FileNotFoundError:
        return []

habits = load_habits()

def reset_progress():
    today = date.today()
    for habit in habits:
        current_key = get_period_key(habit["period"], today)
        if habit.get("last_active") != current_key:
            habit["current"] = 0

reset_progress()

selected_color = PRESET_COLORS[0]
entry_widget = None
goal_entry = None
add_window = None

def save_habits():
    file = open("habits.json", "w")
    json.dump(habits, file)
    file.close()

def on_window_close():
    save_habits()
    window.destroy()

def get_current_period():
    current_tab_index = notebook.index(notebook.select())
    periods = ["Daily", "Monthly", "Yearly"]
    return periods[current_tab_index]

def select_preset_color(color, clicked_button, all_buttons):
    global selected_color
    selected_color = color
    for b in all_buttons:
        b.config(highlightthickness=0)
    clicked_button.config(highlightthickness=3, highlightbackground="black")

def open_add_habit_window(default_period):
    global entry_widget, goal_entry, add_window, selected_color

    selected_color = PRESET_COLORS[0]

    add_window = tk.Toplevel(window)
    add_window.title("New Habit")
    add_window.configure(bg=BG_COLOR)

    popup_width = 360
    popup_height = 480
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    add_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    add_window.resizable(False, False)

    tk.Label(add_window, text="New Habit", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    entry_widget = tk.Entry(add_window, font=BODY_FONT)
    entry_widget.insert(0, "New habit...")
    entry_widget.config(fg="gray")
    entry_widget.bind("<FocusIn>", on_name_click)
    entry_widget.bind("<FocusOut>", on_name_leave)
    entry_widget.pack(pady=5)

    goal_entry = tk.Entry(add_window, font=BODY_FONT)
    goal_entry.insert(0, "Goal (e.g. 8)")
    goal_entry.config(fg="gray")
    goal_entry.bind("<FocusIn>", on_goal_click)
    goal_entry.bind("<FocusOut>", on_goal_leave)
    goal_entry.pack(pady=5)

    period_var.set(default_period)
    period_menu = tk.OptionMenu(add_window, period_var, "Daily", "Monthly", "Yearly")
    period_menu.config(highlightthickness=0, bd=0, relief=tk.FLAT)
    period_menu.pack(pady=5)

    tk.Label(add_window, text="Pick a color", font=BODY_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 5))

    swatch_frame = tk.Frame(add_window, bg=BG_COLOR)
    swatch_frame.pack(pady=5)

    swatch_buttons = []
    for color in PRESET_COLORS:
        b = tk.Button(swatch_frame, bg=color, width=2, height=1, relief=tk.FLAT, highlightthickness=0)
        b.pack(side="left", padx=3)
        swatch_buttons.append(b)

    for color, b in zip(PRESET_COLORS, swatch_buttons):
        b.config(command=lambda c=color, btn=b: select_preset_color(c, btn, swatch_buttons))

    swatch_buttons[0].config(highlightthickness=3, highlightbackground="black")

    add_button = tk.Button(add_window, text="Add Habit", bg="black", fg="white",
                            activebackground="#333333", activeforeground="white",
                            relief=tk.FLAT, highlightthickness=0, bd=0, command=addfunc)
    add_button.pack(pady=20)

def addfunc():
    global selected_color, add_window
    new_habit_name = entry_widget.get()
    raw_goal = goal_entry.get()
    chosen_period = period_var.get()

    if new_habit_name == "" or new_habit_name == "New habit...":
        return

    try:
        goal_num = int(raw_goal)
        if goal_num < 1:
            goal_num = 1
    except ValueError:
        goal_num = 1

    habits.append({
        "name": new_habit_name,
        "streak": 0,
        "last_completed": None,
        "goal": goal_num,
        "current": 0,
        "last_active": None,
        "color": selected_color,
        "period": chosen_period
    })

    save_habits()
    add_window.destroy()
    render_all_habits()

def mark_done(habit):
    today = date.today()
    current_key = get_period_key(habit["period"], today)

    if habit.get("last_active") != current_key:
        habit["current"] = 0
        habit["last_active"] = current_key

    habit["current"] += 1

    if habit["current"] >= habit["goal"]:
        previous_key = get_previous_period_key(habit["period"], today)

        if habit["last_completed"] != current_key:
            if habit["last_completed"] == previous_key:
                habit["streak"] += 1
            else:
                habit["streak"] = 1
            habit["last_completed"] = current_key

    save_habits()
    render_all_habits()

def delete_habit(habit):
    confirm = messagebox.askyesno("Delete Habit", "Delete '" + habit["name"] + "'?")
    if confirm:
        habits.remove(habit)
        save_habits()
        render_all_habits()

def render_period(period, container):
    for widget in container.winfo_children():
        widget.destroy()

    current_row = 0
    current_column = 0

    for habit in habits:
        if habit["period"] != period:
            continue

        habit_box = tk.Frame(container, bg=BG_COLOR, width=160, height=220)
        habit_box.grid(row=current_row, column=current_column, padx=15, pady=10)
        habit_box.pack_propagate(False)

        trash_canvas = tk.Canvas(habit_box, width=24, height=24, bg=BG_COLOR, highlightthickness=0)
        draw_trash_icon(trash_canvas)
        trash_canvas.bind("<Button-1>", lambda event, h=habit: delete_habit(h))
        trash_canvas.config(cursor="hand2")
        trash_canvas.place(x=5, y=5)

        ring_canvas = tk.Canvas(habit_box, width=120, height=120, bg=BG_COLOR, highlightthickness=0)
        ring_canvas.pack(pady=(25, 5))

        ring_canvas.create_oval(8, 8, 112, 112, fill=habit["color"], outline="")

        rim_color = darken_color(habit["color"], factor=0.8)
        ring_canvas.create_oval(8, 8, 112, 112, outline=rim_color, width=6)

        progress = habit["current"] / habit["goal"]
        if progress > 1:
            progress = 1

        progress_color = darken_color(habit["color"], factor=0.5)

        if progress >= 1:
            ring_canvas.create_oval(8, 8, 112, 112, outline=progress_color, width=6)
        elif progress > 0:
            extent = -360 * progress
            ring_canvas.create_arc(8, 8, 112, 112, start=90, extent=extent, outline=progress_color, width=6, style=tk.ARC)

        text_color = get_contrast_text_color(habit["color"])
        center_text = str(habit["current"]) + "/" + str(habit["goal"])
        ring_canvas.create_text(60, 60, text=center_text, fill=text_color, font=("Segoe UI", 14, "bold"))

        current_key = get_period_key(habit["period"], date.today())
        is_done_now = (habit["last_completed"] == current_key and habit["current"] >= habit["goal"])

        if not is_done_now:
            ring_canvas.bind("<Button-1>", lambda event, h=habit: mark_done(h))
            ring_canvas.config(cursor="hand2")

        name_label = tk.Label(habit_box, text=habit["name"], bg=BG_COLOR, fg=TEXT_COLOR, font=HEADER_FONT)
        name_label.pack()

        if habit["period"] == "Daily":
            streak_word = PERIOD_WORDS[habit["period"]]
            streak_label = tk.Label(habit_box, text="streak: " + str(habit["streak"]) + " " + streak_word, bg=BG_COLOR, fg=SUBTEXT_COLOR, font=BODY_FONT)
            streak_label.pack()

        current_column += 1
        if current_column > 2:
            current_column = 0
            current_row += 1

def render_all_habits():
    render_period("Daily", daily_habit_frame)
    render_period("Monthly", monthly_habit_frame)
    render_period("Yearly", yearly_habit_frame)

def on_name_click(event):
    if entry_widget.get() == "New habit...":
        entry_widget.delete(0, tk.END)
        entry_widget.config(fg="black")

def on_name_leave(event):
    if entry_widget.get() == "":
        entry_widget.insert(0, "New habit...")
        entry_widget.config(fg="gray")

def on_goal_click(event):
    if goal_entry.get() == "Goal (e.g. 8)":
        goal_entry.delete(0, tk.END)
        goal_entry.config(fg="black")

def on_goal_leave(event):
    if goal_entry.get() == "":
        goal_entry.insert(0, "Goal (e.g. 8)")
        goal_entry.config(fg="gray")
def open_add_habit_window(default_period, habit=None):
    global entry_widget, goal_entry, add_window, selected_color

    selected_color = PRESET_COLORS[0]

    add_window = tk.Toplevel(window)
    add_window.title("New Habit")
    add_window.configure(bg=BG_COLOR)

    popup_width = 360
    popup_height = 480
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    add_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    add_window.resizable(False, False)

    tk.Label(add_window, text="New Habit", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    entry_widget = tk.Entry(add_window, font=BODY_FONT)
    entry_widget.insert(0, "New habit...")
    entry_widget.config(fg="gray")
    entry_widget.bind("<FocusIn>", on_name_click)
    entry_widget.bind("<FocusOut>", on_name_leave)
    entry_widget.pack(pady=5)

    goal_entry = tk.Entry(add_window, font=BODY_FONT)
    goal_entry.insert(0, "Goal (e.g. 8)")
    goal_entry.config(fg="gray")
    goal_entry.bind("<FocusIn>", on_goal_click)
    goal_entry.bind("<FocusOut>", on_goal_leave)
    goal_entry.pack(pady=5)

    period_var.set(default_period)
    period_menu = tk.OptionMenu(add_window, period_var, "Daily", "Monthly", "Yearly")
    period_menu.config(highlightthickness=0, bd=0, relief=tk.FLAT)
    period_menu.pack(pady=5)

    tk.Label(add_window, text="Pick a color", font=BODY_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 5))

    swatch_frame = tk.Frame(add_window, bg=BG_COLOR)
    swatch_frame.pack(pady=5)

    swatch_buttons = []
    for color in PRESET_COLORS:
        b = tk.Button(swatch_frame, bg=color, width=2, height=1,
                      relief=tk.FLAT, highlightthickness=0)
        b.pack(side="left", padx=3)
        swatch_buttons.append(b)

    for color, b in zip(PRESET_COLORS, swatch_buttons):
        b.config(command=lambda c=color, btn=b: select_preset_color(c, btn, swatch_buttons))

    swatch_buttons[0].config(highlightthickness=3, highlightbackground="black")

    add_button = tk.Button(
        add_window,
        text="Add Habit",
        bg="black",
        fg="white",
        activebackground="#333333",
        activeforeground="white",
        relief=tk.FLAT,
        highlightthickness=0,
        bd=0,
        command=addfunc
    )
    add_button.pack(pady=20)
window = tk.Tk()
window.title("Habit Tracker")
window.geometry("950x700")
window.configure(bg=BG_COLOR)

title_label = tk.Label(window, text="Habit Tracker", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(pady=15)

period_var = tk.StringVar(window)
period_var.set("Daily")

notebook = ttk.Notebook(window)
notebook.pack(pady=10, fill="both", expand=True)

daily_tab = tk.Frame(notebook, bg=BG_COLOR)
monthly_tab = tk.Frame(notebook, bg=BG_COLOR)
yearly_tab = tk.Frame(notebook, bg=BG_COLOR)

notebook.add(daily_tab, text="Daily")
notebook.add(monthly_tab, text="Monthly")
notebook.add(yearly_tab, text="Yearly")

daily_habit_frame = tk.Frame(daily_tab, bg=BG_COLOR)
daily_habit_frame.pack(pady=10)

monthly_habit_frame = tk.Frame(monthly_tab, bg=BG_COLOR)
monthly_habit_frame.pack(pady=10)

yearly_habit_frame = tk.Frame(yearly_tab, bg=BG_COLOR)
yearly_habit_frame.pack(pady=10)

new_habit_button = tk.Button(window, text="+ New Habit", bg="black", fg="white",
                              activebackground="#333333", activeforeground="white",
                              font=HEADER_FONT, relief=tk.FLAT, highlightthickness=0, bd=0,
                              command=lambda: open_add_habit_window(get_current_period()))
new_habit_button.place(x=780, y=20)

render_all_habits()

window.protocol("WM_DELETE_WINDOW", on_window_close)

window.mainloop()