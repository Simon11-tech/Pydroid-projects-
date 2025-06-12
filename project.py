import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, font

DB_FILE = "habit_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            xp_value INTEGER NOT NULL DEFAULT 10
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS habit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total_xp INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_active_date TEXT
        )
    ''')
    c.execute('INSERT OR IGNORE INTO user_stats (id, total_xp, streak, last_active_date) VALUES (1,0,0,NULL)')
    conn.commit()
    return conn

def today_str():
    return datetime.date.today().isoformat()

class ColorButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        self.default_bg = kwargs.pop('bg', '#3498db')
        self.hover_bg = kwargs.pop('hoverbg', '#2980b9')
        super().__init__(master, bg=self.default_bg, activebackground=self.hover_bg, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e):
        self['background'] = self.hover_bg
    def on_leave(self, e):
        self['background'] = self.default_bg

class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Habit Tracker 🌟")
        self.root.geometry("450x500")
        self.root.configure(bg="#1e1e2f")  # dark background

        self.conn = init_db()
        self.c = self.conn.cursor()

        self.habits = []
        self.check_vars = []

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.habit_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=11, weight="bold")

        # UI Frames
        self.top_frame = tk.Frame(root, bg="#1e1e2f")
        self.top_frame.pack(pady=15)

        self.mid_frame = tk.Frame(root, bg="#1e1e2f")
        self.mid_frame.pack(fill="both", expand=True, pady=10)

        self.bottom_frame = tk.Frame(root, bg="#1e1e2f")
        self.bottom_frame.pack(pady=15)

        # Title Label
        self.title_label = tk.Label(self.top_frame, text="Your Habit Tracker", fg="#f8f8f2", bg="#1e1e2f", font=self.title_font)
        self.title_label.pack()

        # Buttons
        self.add_btn = ColorButton(self.top_frame, text="➕ Add New Habit", fg="white", font=self.button_font,
                                   command=self.add_habit, padx=10, pady=5, bg="#27ae60", hoverbg="#2ecc71", borderwidth=0)
        self.add_btn.pack(side=tk.LEFT, padx=8)

        self.refresh_btn = ColorButton(self.top_frame, text="🔄 Refresh", fg="white", font=self.button_font,
                                      command=self.load_habits, padx=10, pady=5, bg="#2980b9", hoverbg="#3498db", borderwidth=0)
        self.refresh_btn.pack(side=tk.LEFT, padx=8)

        self.save_btn = ColorButton(self.bottom_frame, text="💾 Save Progress", fg="white", font=self.button_font,
                                   command=self.save_progress, padx=10, pady=6, bg="#e67e22", hoverbg="#d35400", borderwidth=0)
        self.save_btn.pack(side=tk.LEFT, padx=8)

        self.stats_btn = ColorButton(self.bottom_frame, text="📊 Show Stats", fg="white", font=self.button_font,
                                    command=self.show_stats, padx=10, pady=6, bg="#9b59b6", hoverbg="#8e44ad", borderwidth=0)
        self.stats_btn.pack(side=tk.LEFT, padx=8)

        self.quit_btn = ColorButton(self.bottom_frame, text="❌ Quit", fg="white", font=self.button_font,
                                   command=self.quit_app, padx=10, pady=6, bg="#c0392b", hoverbg="#e74c3c", borderwidth=0)
        self.quit_btn.pack(side=tk.LEFT, padx=8)

        self.load_habits()

    def add_habit(self):
        name = simpledialog.askstring("Add Habit", "Enter habit name:", parent=self.root)
        if name:
            xp = simpledialog.askinteger("XP Value", "Enter XP for completing habit (default 10):", parent=self.root, minvalue=1)
            xp = xp if xp else 10
            self.c.execute("INSERT INTO habits (name, xp_value) VALUES (?, ?)", (name.strip(), xp))
            self.conn.commit()
            messagebox.showinfo("Success", f'Habit "{name}" added with {xp} XP.')
            self.load_habits()

    def load_habits(self):
        # Clear old widgets
        for widget in self.mid_frame.winfo_children():
            widget.destroy()

        self.habits = []
        self.check_vars = []
        today = today_str()

        self.c.execute("SELECT id, name, xp_value FROM habits ORDER BY id")
        habits = self.c.fetchall()

        # Ensure habit_log for today exists
        for habit in habits:
            self.c.execute("SELECT id FROM habit_log WHERE habit_id=? AND date=?", (habit[0], today))
            if self.c.fetchone() is None:
                self.c.execute("INSERT INTO habit_log (habit_id, date, completed) VALUES (?, ?, 0)", (habit[0], today))
        self.conn.commit()

        # Fetch today's logs
        self.c.execute("""
            SELECT hl.id, h.name, hl.completed, h.xp_value
            FROM habit_log hl JOIN habits h ON hl.habit_id = h.id
            WHERE hl.date = ?
            ORDER BY hl.id
        """, (today,))
        logs = self.c.fetchall()

        if not logs:
            lbl = tk.Label(self.mid_frame, text="No habits yet! Add some from above.", fg="#f8f8f2", bg="#1e1e2f", font=self.habit_font)
            lbl.pack(pady=10)
            return

        for hl_id, name, completed, xp_value in logs:
            var = tk.IntVar(value=completed)
            cb = tk.Checkbutton(self.mid_frame, text=f"{name} (XP: {xp_value})", variable=var,
                                fg="#f1c40f", bg="#1e1e2f", activebackground="#1e1e2f",
                                selectcolor="#27ae60", font=self.habit_font)
            cb.pack(anchor="w", padx=15, pady=3)
            self.habits.append((hl_id, var))

    def save_progress(self):
        for hl_id, var in self.habits:
            self.c.execute("UPDATE habit_log SET completed=? WHERE id=?", (var.get(), hl_id))
        self.conn.commit()
        self.update_user_stats()
        messagebox.showinfo("Saved", "Today's progress saved!")
        self.load_habits()

    def update_user_stats(self):
        today = today_str()
        self.c.execute("""
            SELECT SUM(h.xp_value)
            FROM habit_log hl JOIN habits h ON hl.habit_id = h.id
            WHERE hl.date = ? AND hl.completed = 1
        """, (today,))
        earned_xp = self.c.fetchone()[0] or 0

        self.c.execute("SELECT total_xp, streak, last_active_date FROM user_stats WHERE id=1")
        total_xp, streak, last_active_date = self.c.fetchone()

        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

        if last_active_date == today:
            return  # already updated

        if earned_xp > 0:
            if last_active_date == yesterday:
                streak += 1
            else:
                streak = 1
        else:
            streak = 0

        total_xp += earned_xp

        self.c.execute("""
            UPDATE user_stats SET total_xp=?, streak=?, last_active_date=?
            WHERE id=1
        """, (total_xp, streak, today))
        self.conn.commit()

    def show_stats(self):
        self.c.execute("SELECT total_xp, streak FROM user_stats WHERE id=1")
        total_xp, streak = self.c.fetchone()
        level = total_xp // 100
        self.c.execute("SELECT COUNT(*) FROM habits")
        habit_count = self.c.fetchone()[0]

        stats_msg = (
            f"Total XP: {total_xp}\n"
            f"Level: {level}\n"
            f"Current Streak: {streak} day(s)\n"
            f"Number of habits: {habit_count}"
        )
        messagebox.showinfo("Your Stats", stats_msg)

    def quit_app(self):
        self.conn.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()