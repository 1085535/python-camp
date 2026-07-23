import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import date, timedelta, datetime
import subprocess
import random
import math
import platform
import uuid

TITLE_FONT = ("Garamond", 24, "bold")
HEADER_FONT = ("Georgia", 12, "bold")
BODY_FONT = ("Segoe UI", 10)

PERIOD_WORDS = {"Daily": "days", "Monthly": "months", "Yearly": "years"}

BG_COLOR = "#FAF6F0"
TEXT_COLOR = "#3A3A3A"
SUBTEXT_COLOR = "#8A8A8A"

PRESET_COLORS = [
    "#D97A7A", "#D9A15D", "#D8C76A", "#8FBF8F", "#6FA8DC",
    "#8C7CC9", "#D68BB5", "#A9826D", "#7A9AA8"
]

MILESTONES = [7, 30, 100]
MILESTONE_LABELS = {
    7: "One Week Strong! 🔥",
    30: "One Month Milestone! 🌟",
    100: "100 Day Legend! 🏆"
}

HEAT_COLORS = ["#FFF6D6", "#FFE066", "#FFB13D", "#FF7A3D", "#D62839"]

rendered_canvases = {}

def play_sound(sound_type="progress"):
    if platform.system() == "Darwin":
        sound_file = "/System/Library/Sounds/Pop.aiff" if sound_type == "progress" else "/System/Library/Sounds/Glass.aiff"
        try:
            subprocess.Popen(["afplay", sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def send_notification(title, message):
    if platform.system() == "Darwin":
        script = f'display notification "{message}" with title "{title}"'
        try:
            subprocess.Popen(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def show_toast(title, message):
    toast = tk.Toplevel(window)
    toast.overrideredirect(True)
    toast.configure(bg="black")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    toast_width = 300
    toast_height = 80
    x = screen_width - toast_width - 20
    y = screen_height - toast_height - 60
    toast.geometry(f"{toast_width}x{toast_height}+{x}+{y}")

    tk.Label(toast, text=title, font=HEADER_FONT, bg="black", fg="white").pack(pady=(10, 2))
    tk.Label(toast, text=message, font=BODY_FONT, bg="black", fg="#CCCCCC").pack()

    toast.after(4000, toast.destroy)

def trigger_confetti(canvas):
    particles = []
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3", "#33FFF5", "#FF9900"]

    for _ in range(25):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed - 2
        p_id = canvas.create_oval(58, 58, 62, 62, fill=random.choice(colors), outline="")
        particles.append({"id": p_id, "dx": dx, "dy": dy, "life": 18})

    def update_particles():
        keep = []
        try:
            for p in particles:
                canvas.move(p["id"], p["dx"], p["dy"])
                p["dy"] += 0.35
                p["life"] -= 1
                if p["life"] > 0:
                    keep.append(p)
                else:
                    canvas.delete(p["id"])
        except tk.TclError:
            return
        particles[:] = keep
        if particles:
            canvas.after(30, update_particles)

    update_particles()

def show_badge_popup(habit, milestone):
    badge_win = tk.Toplevel(window)
    badge_win.overrideredirect(True)
    badge_win.configure(bg="black")

    popup_width = 320
    popup_height = 140
    screen_width = window.winfo_screenwidth()
    x = (screen_width - popup_width) // 2
    y = 80
    badge_win.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    label_text = MILESTONE_LABELS.get(milestone, str(milestone) + " Day Streak!")
    tk.Label(badge_win, text="🏆", font=("Segoe UI", 28), bg="black", fg="white").pack(pady=(15, 0))
    tk.Label(badge_win, text=habit["name"], font=HEADER_FONT, bg="black", fg="white").pack()
    tk.Label(badge_win, text=label_text, font=BODY_FONT, bg="black", fg="#FFD700").pack(pady=(0, 10))

    badge_win.after(3500, badge_win.destroy)

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
    return "black" if brightness > 150 else "white"

def get_heat_color(count):
    if count == 0:
        return HEAT_COLORS[0]
    elif count == 1:
        return HEAT_COLORS[1]
    elif count <= 3:
        return HEAT_COLORS[2]
    elif count <= 6:
        return HEAT_COLORS[3]
    else:
        return HEAT_COLORS[4]

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

def draw_edit_icon(canvas):
    canvas.create_line(6, 17, 15, 8, fill="black", width=2)
    canvas.create_line(15, 8, 18, 11, fill="black", width=2)
    canvas.create_line(18, 11, 9, 20, fill="black", width=2)
    canvas.create_line(9, 20, 5, 20, fill="black", width=2)
    canvas.create_line(5, 20, 6, 17, fill="black", width=2)

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
                habit["color"] = PRESET_COLORS[0]
            if "period" not in habit:
                habit["period"] = "Daily"
            if "id" not in habit:
                habit["id"] = str(uuid.uuid4())
            if "reminder_time" not in habit:
                habit["reminder_time"] = None
            if "last_reminder_date" not in habit:
                habit["last_reminder_date"] = None
            if "milestones_earned" not in habit:
                habit["milestones_earned"] = []

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

def load_activity_log():
    try:
        file = open("activity_log.json", "r")
        data = json.load(file)
        file.close()
        return data
    except FileNotFoundError:
        return {}

activity_log = load_activity_log()

def save_activity_log():
    file = open("activity_log.json", "w")
    json.dump(activity_log, file)
    file.close()

selected_color = PRESET_COLORS[0]
entry_widget = None
goal_entry = None
reminder_entry = None
add_window = None
edit_window = None

def save_habits():
    file = open("habits.json", "w")
    json.dump(habits, file)
    file.close()

def on_window_close():
    save_habits()
    save_activity_log()
    window.destroy()

def get_current_period():
    current_tab_index = notebook.index(notebook.select())
    periods = ["Daily", "Monthly", "Yearly"]
    return periods[current_tab_index]

def parse_reminder_time(raw):
    raw = raw.strip()
    if raw == "" or raw == "Reminder (e.g. 18:00)":
        return None
    try:
        datetime.strptime(raw, "%H:%M")
        return raw
    except ValueError:
        return None

def check_reminders():
    now = datetime.now()
    current_time_str = now.strftime("%H:%M")
    today_str = str(date.today())

    for habit in habits:
        reminder_time = habit.get("reminder_time")
        if not reminder_time:
            continue
        if habit.get("last_reminder_date") == today_str:
            continue

        if habit["current"] >= habit["goal"]:
            continue

        if current_time_str >= reminder_time:
            if platform.system() == "Darwin":
                send_notification("Habit Reminder ⏰", f"Don't forget: {habit['name']}")
            else:
                show_toast("Habit Reminder ⏰", f"Don't forget: {habit['name']}")
            play_sound("progress")
            habit["last_reminder_date"] = today_str
            save_habits()

    window.after(60000, check_reminders)

def open_weekly_report_window():
    report_win = tk.Toplevel(window)
    report_win.title("Weekly Report")
    report_win.configure(bg=BG_COLOR)

    popup_width = 460
    popup_height = 540
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    report_win.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    report_win.resizable(False, False)

    tk.Label(report_win, text="📊 Weekly Progress Report", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(15, 5))

    daily_habits = [h for h in habits if h["period"] == "Daily"]

    total_current = sum(h["current"] for h in habits)
    total_goal = sum(h["goal"] for h in habits)
    overall_pct = int((total_current / total_goal * 100)) if total_goal > 0 else 0

    top_streak_habit = max(habits, key=lambda h: h.get("streak", 0)) if habits else None
    top_streak_num = top_streak_habit.get("streak", 0) if top_streak_habit else 0
    top_streak_name = top_streak_habit["name"] if top_streak_habit and top_streak_num > 0 else "None yet"

    if overall_pct >= 80:
        status_msg = "🔥 Outstanding week! You're crushing your goals."
    elif overall_pct >= 50:
        status_msg = "👍 Solid effort! You're over halfway there."
    else:
        status_msg = "🌱 A fresh start! Keep taking small steps forward."

    tk.Label(report_win, text=status_msg, font=BODY_FONT, bg=BG_COLOR, fg=SUBTEXT_COLOR).pack(pady=(0, 15))

    stats_card = tk.Frame(report_win, bg="#EFE9E0", highlightthickness=1, highlightbackground="#DCD3C7", padx=15, pady=12)
    stats_card.pack(fill="x", padx=25, pady=5)

    tk.Label(stats_card, text=f"Overall Goal Progress: {overall_pct}%", font=HEADER_FONT, bg="#EFE9E0", fg=TEXT_COLOR).pack(anchor="w", pady=2)
    tk.Label(stats_card, text=f"Total Steps Logged: {total_current} / {total_goal}", font=BODY_FONT, bg="#EFE9E0", fg=TEXT_COLOR).pack(anchor="w", pady=2)
    tk.Label(stats_card, text=f"Top Active Streak: 🔥 {top_streak_num} days ({top_streak_name})", font=BODY_FONT, bg="#EFE9E0", fg=TEXT_COLOR).pack(anchor="w", pady=2)

    tk.Label(report_win, text="Daily Habits Summary", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=25, pady=(15, 5))

    list_frame = tk.Frame(report_win, bg=BG_COLOR)
    list_frame.pack(fill="both", expand=True, padx=25, pady=5)

    if not daily_habits:
        tk.Label(list_frame, text="No daily habits set yet.", font=BODY_FONT, bg=BG_COLOR, fg=SUBTEXT_COLOR).pack(pady=10)
    else:
        for h in daily_habits:
            item_row = tk.Frame(list_frame, bg=BG_COLOR)
            item_row.pack(fill="x", pady=4)

            name_lbl = tk.Label(item_row, text=h["name"], font=BODY_FONT, bg=BG_COLOR, fg=TEXT_COLOR, width=18, anchor="w")
            name_lbl.pack(side="left")

            pct = min(1.0, h["current"] / h["goal"]) if h["goal"] > 0 else 0

            p_bar = tk.Canvas(item_row, width=120, height=12, bg="#E0DCD5", highlightthickness=0)
            p_bar.pack(side="left", padx=5)
            if pct > 0:
                p_bar.create_rectangle(0, 0, int(120 * pct), 12, fill=h["color"], outline="")

            ratio_lbl = tk.Label(item_row, text=f"{h['current']}/{h['goal']}", font=BODY_FONT, bg=BG_COLOR, fg=SUBTEXT_COLOR)
            ratio_lbl.pack(side="left", padx=5)

    close_btn = tk.Label(report_win, text="Close Report", bg="black", fg="white", font=HEADER_FONT, padx=15, pady=6, cursor="hand2")
    close_btn.pack(pady=15)
    close_btn.bind("<Button-1>", lambda e: report_win.destroy())

def open_calendar_heatmap_window():
    heat_win = tk.Toplevel(window)
    heat_win.title("Activity Heatmap")
    heat_win.configure(bg=BG_COLOR)

    popup_width = 620
    popup_height = 260
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    heat_win.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    heat_win.resizable(False, False)

    tk.Label(heat_win, text="🔥 Activity Heatmap", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(15, 5))
    tk.Label(heat_win, text="Last 12 weeks of activity", font=BODY_FONT, bg=BG_COLOR, fg=SUBTEXT_COLOR).pack(pady=(0, 10))

    cell_size = 16
    cell_gap = 4
    weeks = 12
    total_columns = weeks + 1

    canvas_width = total_columns * (cell_size + cell_gap) - cell_gap
    canvas_height = 7 * (cell_size + cell_gap) - cell_gap

    heat_canvas = tk.Canvas(heat_win, width=canvas_width, height=canvas_height, bg=BG_COLOR, highlightthickness=0)
    heat_canvas.pack(pady=5)

    today = date.today()
    start_day = today - timedelta(days=(weeks * 7 - 1))
    grid_start = start_day - timedelta(days=start_day.weekday())

    for week in range(total_columns):
        for day_of_week in range(7):
            current_day = grid_start + timedelta(days=(week * 7 + day_of_week))
            day_str = str(current_day)
            count = activity_log.get(day_str, 0)
            color = get_heat_color(count)

            x0 = week * (cell_size + cell_gap)
            y0 = day_of_week * (cell_size + cell_gap)
            heat_canvas.create_rectangle(x0, y0, x0 + cell_size, y0 + cell_size, fill=color, outline=BG_COLOR)

    legend_frame = tk.Frame(heat_win, bg=BG_COLOR)
    legend_frame.pack(pady=10)
    tk.Label(legend_frame, text="Less", font=BODY_FONT, bg=BG_COLOR, fg=SUBTEXT_COLOR).pack(side="left", padx=3)
    for c in HEAT_COLORS:
        swatch = tk.Canvas(legend_frame, width=14, height=14, bg=BG_COLOR, highlightthickness=0)
        swatch.create_rectangle(1, 1, 13, 13, fill=c, outline="")
        swatch.pack(side="left", padx=2)
    tk.Label(legend_frame, text="More", font=BODY_FONT, bg=BG_COLOR, fg=SUBTEXT_COLOR).pack(side="left", padx=3)

    close_btn = tk.Label(heat_win, text="Close", bg="black", fg="white", font=HEADER_FONT, padx=15, pady=6, cursor="hand2")
    close_btn.pack(pady=10)
    close_btn.bind("<Button-1>", lambda e: heat_win.destroy())

def open_add_habit_window(default_period):
    global entry_widget, goal_entry, reminder_entry, add_window, selected_color

    selected_color = PRESET_COLORS[0]

    add_window = tk.Toplevel(window)
    add_window.title("New Habit")
    add_window.configure(bg=BG_COLOR)

    popup_width = 380
    popup_height = 560
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    add_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    add_window.resizable(False, False)

    tk.Label(add_window, text="New Habit", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    entry_widget = tk.Entry(add_window, font=BODY_FONT, fg="lightgray", insertbackground="white")
    entry_widget.insert(0, "New habit...")
    entry_widget.bind("<FocusIn>", on_name_click)
    entry_widget.bind("<FocusOut>", on_name_leave)
    entry_widget.pack(pady=5)

    goal_entry = tk.Entry(add_window, font=BODY_FONT, fg="lightgray", insertbackground="white")
    goal_entry.insert(0, "Goal (e.g. 8)")
    goal_entry.bind("<FocusIn>", on_goal_click)
    goal_entry.bind("<FocusOut>", on_goal_leave)
    goal_entry.pack(pady=5)

    reminder_entry = tk.Entry(add_window, font=BODY_FONT, fg="lightgray", insertbackground="white")
    reminder_entry.insert(0, "Reminder (e.g. 18:00)")
    reminder_entry.bind("<FocusIn>", on_reminder_click)
    reminder_entry.bind("<FocusOut>", on_reminder_leave)
    reminder_entry.pack(pady=5)

    period_var.set(default_period)
    period_menu = tk.OptionMenu(add_window, period_var, "Daily", "Monthly", "Yearly")
    period_menu.config(
        highlightthickness=0, bd=0, borderwidth=0, bg="#333333", fg="white",
        activebackground="#444444", activeforeground="white", relief=tk.FLAT
    )
    period_menu.pack(pady=5)

    tk.Label(add_window, text="Pick a color", font=BODY_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 5))

    color_container = tk.Frame(add_window, bg=BG_COLOR)
    color_container.pack(pady=5)

    preview_canvas = tk.Canvas(color_container, width=32, height=32, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
    preview_canvas.pack(anchor="center")

    def draw_preview():
        preview_canvas.delete("all")
        preview_canvas.create_rectangle(2, 2, 30, 30, fill=selected_color, outline="#333333", width=2)

    draw_preview()

    palette_frame = tk.Frame(color_container, bg=BG_COLOR)

    def draw_palette():
        for widget in palette_frame.winfo_children():
            widget.destroy()

        for i, color in enumerate(PRESET_COLORS):
            if i % 5 == 0:
                row_frame = tk.Frame(palette_frame, bg=BG_COLOR)
                row_frame.pack(pady=2)

            c_canvas = tk.Canvas(row_frame, width=28, height=28, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
            c_canvas.pack(side="left", padx=3)

            outline_col = "#000000" if color == selected_color else "#CCCCCC"
            stroke_width = 2 if color == selected_color else 1
            c_canvas.create_rectangle(2, 2, 26, 26, fill=color, outline=outline_col, width=stroke_width)

            def pick_this_color(chosen=color):
                global selected_color
                selected_color = chosen
                draw_preview()
                palette_frame.pack_forget()

            c_canvas.bind("<Button-1>", lambda event, chosen=color: pick_this_color(chosen))

    def toggle_palette(event):
        if palette_frame.winfo_ismapped():
            palette_frame.pack_forget()
        else:
            draw_palette()
            palette_frame.pack(pady=8)

    preview_canvas.bind("<Button-1>", toggle_palette)

    add_button = tk.Label(
        add_window, text="Add Habit", bg="black", fg="white",
        font=HEADER_FONT, padx=15, pady=6, cursor="hand2"
    )
    add_button.pack(pady=20)
    add_button.bind("<Button-1>", lambda event: addfunc())
    add_button.bind("<Enter>", lambda event: add_button.config(bg="#333333"))
    add_button.bind("<Leave>", lambda event: add_button.config(bg="black"))

def open_edit_habit_window(target_habit):
    global entry_widget, goal_entry, reminder_entry, edit_window, selected_color

    selected_color = target_habit.get("color", PRESET_COLORS[0])

    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Habit")
    edit_window.configure(bg=BG_COLOR)

    popup_width = 380
    popup_height = 560
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    edit_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    edit_window.resizable(False, False)

    tk.Label(edit_window, text="Edit Habit", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    entry_widget = tk.Entry(edit_window, font=BODY_FONT, fg="white", insertbackground="white")
    entry_widget.insert(0, target_habit["name"])
    entry_widget.pack(pady=5)

    goal_entry = tk.Entry(edit_window, font=BODY_FONT, fg="white", insertbackground="white")
    goal_entry.insert(0, str(target_habit["goal"]))
    goal_entry.pack(pady=5)

    reminder_entry = tk.Entry(edit_window, font=BODY_FONT, insertbackground="white")
    existing_reminder = target_habit.get("reminder_time")
    if existing_reminder:
        reminder_entry.insert(0, existing_reminder)
        reminder_entry.config(fg="white")
    else:
        reminder_entry.insert(0, "Reminder (e.g. 18:00)")
        reminder_entry.config(fg="lightgray")
    reminder_entry.bind("<FocusIn>", on_reminder_click)
    reminder_entry.bind("<FocusOut>", on_reminder_leave)
    reminder_entry.pack(pady=5)

    edit_period_var = tk.StringVar(edit_window)
    edit_period_var.set(target_habit.get("period", "Daily"))
    period_menu = tk.OptionMenu(edit_window, edit_period_var, "Daily", "Monthly", "Yearly")
    period_menu.config(
        highlightthickness=0, bd=0, borderwidth=0, bg="#333333", fg="white",
        activebackground="#444444", activeforeground="white", relief=tk.FLAT
    )
    period_menu.pack(pady=5)

    tk.Label(edit_window, text="Pick a color", font=BODY_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 5))

    color_container = tk.Frame(edit_window, bg=BG_COLOR)
    color_container.pack(pady=5)

    preview_canvas = tk.Canvas(color_container, width=32, height=32, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
    preview_canvas.pack(anchor="center")

    def draw_preview():
        preview_canvas.delete("all")
        preview_canvas.create_rectangle(2, 2, 30, 30, fill=selected_color, outline="#333333", width=2)

    draw_preview()

    palette_frame = tk.Frame(color_container, bg=BG_COLOR)

    def draw_palette():
        for widget in palette_frame.winfo_children():
            widget.destroy()

        for i, color in enumerate(PRESET_COLORS):
            if i % 5 == 0:
                row_frame = tk.Frame(palette_frame, bg=BG_COLOR)
                row_frame.pack(pady=2)

            c_canvas = tk.Canvas(row_frame, width=28, height=28, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
            c_canvas.pack(side="left", padx=3)

            outline_col = "#000000" if color == selected_color else "#CCCCCC"
            stroke_width = 2 if color == selected_color else 1
            c_canvas.create_rectangle(2, 2, 26, 26, fill=color, outline=outline_col, width=stroke_width)

            def pick_this_color(chosen=color):
                global selected_color
                selected_color = chosen
                draw_preview()
                palette_frame.pack_forget()

            c_canvas.bind("<Button-1>", lambda event, chosen=color: pick_this_color(chosen))

    def toggle_palette(event):
        if palette_frame.winfo_ismapped():
            palette_frame.pack_forget()
        else:
            draw_palette()
            palette_frame.pack(pady=8)

    preview_canvas.bind("<Button-1>", toggle_palette)

    def save_edit_func():
        new_name = entry_widget.get().strip()
        raw_goal = goal_entry.get().strip()
        new_period = edit_period_var.get()
        raw_reminder = reminder_entry.get()

        if not new_name:
            return

        try:
            goal_num = int(raw_goal)
            if goal_num < 1:
                goal_num = 1
        except ValueError:
            goal_num = 1

        target_habit["name"] = new_name
        target_habit["goal"] = goal_num
        target_habit["period"] = new_period
        target_habit["color"] = selected_color
        target_habit["reminder_time"] = parse_reminder_time(raw_reminder)

        if target_habit["current"] > goal_num:
            target_habit["current"] = goal_num

        save_habits()
        edit_window.destroy()
        render_all_habits()

    save_button = tk.Label(
        edit_window, text="Save Changes", bg="black", fg="white",
        font=HEADER_FONT, padx=15, pady=6, cursor="hand2"
    )
    save_button.pack(pady=20)
    save_button.bind("<Button-1>", lambda event: save_edit_func())
    save_button.bind("<Enter>", lambda event: save_button.config(bg="#333333"))
    save_button.bind("<Leave>", lambda event: save_button.config(bg="black"))

def addfunc():
    global selected_color, add_window
    new_habit_name = entry_widget.get().strip()
    raw_goal = goal_entry.get()
    chosen_period = period_var.get()
    raw_reminder = reminder_entry.get()

    if new_habit_name == "" or new_habit_name == "New habit...":
        return

    try:
        goal_num = int(raw_goal)
        if goal_num < 1:
            goal_num = 1
    except ValueError:
        goal_num = 1

    habits.append({
        "id": str(uuid.uuid4()),
        "name": new_habit_name,
        "streak": 0,
        "last_completed": None,
        "goal": goal_num,
        "current": 0,
        "last_active": None,
        "color": selected_color,
        "period": chosen_period,
        "reminder_time": parse_reminder_time(raw_reminder),
        "last_reminder_date": None,
        "milestones_earned": []
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

    if habit["current"] >= habit["goal"]:
        return

    habit["current"] += 1
    now_completed = (habit["current"] >= habit["goal"])

    today_str = str(date.today())
    activity_log[today_str] = activity_log.get(today_str, 0) + 1
    save_activity_log()

    if now_completed:
        previous_key = get_previous_period_key(habit["period"], today)

        if habit["last_completed"] != current_key:
            if habit["last_completed"] == previous_key:
                habit["streak"] += 1
            else:
                habit["streak"] = 1
            habit["last_completed"] = current_key

            if habit["period"] == "Daily":
                for m in MILESTONES:
                    if habit["streak"] == m and m not in habit["milestones_earned"]:
                        habit["milestones_earned"].append(m)
                        window.after(400, lambda h=habit, ms=m: show_badge_popup(h, ms))

        play_sound("complete")
        send_notification("Habit Completed! 🎉", f"Great job hitting your goal for '{habit['name']}'!")
        save_habits()
        render_all_habits()

        if habit["id"] in rendered_canvases:
            trigger_confetti(rendered_canvases[habit["id"]])
    else:
        play_sound("progress")
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

        habit_box = tk.Frame(container, bg=BG_COLOR, width=190, height=220)
        habit_box.grid(row=current_row, column=current_column, padx=15, pady=10)
        habit_box.pack_propagate(False)

        trash_canvas = tk.Canvas(habit_box, width=24, height=24, bg=BG_COLOR, highlightthickness=0)
        draw_trash_icon(trash_canvas)
        trash_canvas.bind("<Button-1>", lambda event, h=habit: delete_habit(h))
        trash_canvas.config(cursor="hand2")
        trash_canvas.place(x=5, y=5)

        edit_canvas = tk.Canvas(habit_box, width=24, height=24, bg=BG_COLOR, highlightthickness=0)
        draw_edit_icon(edit_canvas)
        edit_canvas.bind("<Button-1>", lambda event, h=habit: open_edit_habit_window(h))
        edit_canvas.config(cursor="hand2")
        edit_canvas.place(x=32, y=5)

        ring_canvas = tk.Canvas(habit_box, width=120, height=120, bg=BG_COLOR, highlightthickness=0)
        ring_canvas.pack(pady=(25, 5))
        rendered_canvases[habit["id"]] = ring_canvas

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

        is_done_now = habit["current"] >= habit["goal"]

        if not is_done_now:
            ring_canvas.bind("<Button-1>", lambda event, h=habit: mark_done(h))
            ring_canvas.config(cursor="hand2")

        name_label = tk.Label(
            habit_box, text=habit["name"], bg=BG_COLOR, fg=TEXT_COLOR,
            font=HEADER_FONT, wraplength=170, justify="center"
        )
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
    rendered_canvases.clear()
    render_period("Daily", daily_habit_frame)
    render_period("Monthly", monthly_habit_frame)
    render_period("Yearly", yearly_habit_frame)

def on_name_click(event):
    if entry_widget.get() == "New habit...":
        entry_widget.delete(0, tk.END)
        entry_widget.config(fg="white")

def on_name_leave(event):
    if entry_widget.get() == "":
        entry_widget.insert(0, "New habit...")
        entry_widget.config(fg="lightgray")

def on_goal_click(event):
    if goal_entry.get() == "Goal (e.g. 8)":
        goal_entry.delete(0, tk.END)
        goal_entry.config(fg="white")

def on_goal_leave(event):
    if goal_entry.get() == "":
        goal_entry.insert(0, "Goal (e.g. 8)")
        goal_entry.config(fg="lightgray")

def on_reminder_click(event):
    if reminder_entry.get() == "Reminder (e.g. 18:00)":
        reminder_entry.delete(0, tk.END)
        reminder_entry.config(fg="white")

def on_reminder_leave(event):
    if reminder_entry.get() == "":
        reminder_entry.insert(0, "Reminder (e.g. 18:00)")
        reminder_entry.config(fg="lightgray")

window = tk.Tk()
window.title("Habit Tracker")
window.geometry("950x700")
window.configure(bg=BG_COLOR)

header_frame = tk.Frame(window, bg=BG_COLOR)
header_frame.pack(fill="x", padx=20, pady=15)

title_label = tk.Label(header_frame, text="Habit Tracker", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(side="left", expand=True, padx=(120, 0))

new_habit_button = tk.Label(
    header_frame, text="+ New Habit", bg="black", fg="white",
    font=HEADER_FONT, padx=12, pady=6, cursor="hand2"
)
new_habit_button.pack(side="right", padx=(5, 0))
new_habit_button.bind("<Button-1>", lambda event: open_add_habit_window(get_current_period()))
new_habit_button.bind("<Enter>", lambda event: new_habit_button.config(bg="#333333"))
new_habit_button.bind("<Leave>", lambda event: new_habit_button.config(bg="black"))

report_button = tk.Label(
    header_frame, text="📊 Weekly Report", bg="#3A3A3A", fg="white",
    font=HEADER_FONT, padx=12, pady=6, cursor="hand2"
)
report_button.pack(side="right", padx=5)
report_button.bind("<Button-1>", lambda event: open_weekly_report_window())
report_button.bind("<Enter>", lambda event: report_button.config(bg="#555555"))
report_button.bind("<Leave>", lambda event: report_button.config(bg="#3A3A3A"))

heatmap_button = tk.Label(
    header_frame, text="🔥 Activity", bg="#3A3A3A", fg="white",
    font=HEADER_FONT, padx=12, pady=6, cursor="hand2"
)
heatmap_button.pack(side="right", padx=5)
heatmap_button.bind("<Button-1>", lambda event: open_calendar_heatmap_window())
heatmap_button.bind("<Enter>", lambda event: heatmap_button.config(bg="#555555"))
heatmap_button.bind("<Leave>", lambda event: heatmap_button.config(bg="#3A3A3A"))

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

render_all_habits()

window.protocol("WM_DELETE_WINDOW", on_window_close)

check_reminders()

window.mainloop()