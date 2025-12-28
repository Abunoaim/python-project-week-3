import tkinter as tk
import json
from datetime import date
habits = [
    "Morning Exercise",
    "Read Book",
    "Drink Water",
    "Practice Coding"
]
TODAY_FILE = "today.json"
HISTORY_FILE = "history.json"
def load_today():
    try:
        with open(TODAY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

today_data = load_today()
history = load_history()
root = tk.Tk()
root.title("Habit Tracker")
root.geometry("420x380")
vars = {}
def save_today():
    global history
    today = str(date.today())
    final_data = {}
    for h in habits:
        final_data[h] = "Yes" if vars[h].get() else "No"
    with open(TODAY_FILE, "w") as f:
        json.dump(final_data, f)
    found = False
    for day in history:
        if day["date"] == today:
            day["habits"] = final_data 
            found = True
            break

    if not found:
        history.append({
            "date": today,
            "habits": final_data
        })
    if len(history) > 21:
        history.pop(0)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)
    show_overview()
def show_overview():
    win = tk.Toplevel(root)
    win.title("Overview")
    win.geometry("350x300")

    tk.Label(
        win,
        text=f"DAY - {len(history)}",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    for h in habits:
        count = 0
        for day in history:
            if day["habits"].get(h) == "Yes":
                count += 1

        tk.Label(
            win,
            text=f"{h} ({count})",
            font=("Arial", 11)
        ).pack(anchor="w", padx=20)
tk.Label(
    root,
    text="Habit Tracker",
    font=("Arial", 16, "bold")
).pack(pady=10)

tk.Label(
    root,
    text=f"Today: {date.today()}"
).pack()

frame = tk.Frame(root)
frame.pack(pady=15)
for h in habits:
    value = today_data.get(h) == "Yes"
    vars[h] = tk.BooleanVar(value=value)

    tk.Checkbutton(
        frame,
        text=h,
        variable=vars[h]
    ).pack(anchor="w")

tk.Button(
    root,
    text="Save Today",
    width=15,
    command=save_today
).pack(pady=10)

tk.Button(
    root,
    text="See Overview",
    width=15,
    command=show_overview
).pack()

root.mainloop()
