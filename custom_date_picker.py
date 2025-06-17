import tkinter as tk
from datetime import datetime, timedelta


class DatePicker:
    """Custom date picker widget without external dependencies"""

    def __init__(self, parent, on_date_selected):
        self.top = tk.Toplevel(parent)
        self.top.title("Select Date")
        self.top.geometry("250x250")
        self.top.resizable(False, False)
        self.on_date_selected = on_date_selected
        self.selected_date = None

        # Header with navigation
        self.header_frame = tk.Frame(self.top)
        self.header_frame.pack(fill=tk.X)

        self.prev_btn = tk.Button(
            self.header_frame, text="<", command=self.prev_month)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.month_year = tk.Label(
            self.header_frame, font=("Arial", 10, "bold"))
        self.month_year.pack(side=tk.LEFT, expand=True)

        self.next_btn = tk.Button(
            self.header_frame, text=">", command=self.next_month)
        self.next_btn.pack(side=tk.RIGHT, padx=5)

        # Weekday headers
        weekdays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        self.week_frame = tk.Frame(self.top)
        self.week_frame.pack(fill=tk.X)
        for day in weekdays:
            tk.Label(self.week_frame, text=day, width=4,
                     font=("Arial", 8)).pack(side=tk.LEFT)

        # Calendar grid
        self.cal_frame = tk.Frame(self.top)
        self.cal_frame.pack(fill=tk.BOTH, expand=True)

        self.current_date = datetime.today()
        self.render_calendar()

    def render_calendar(self):
        # Clear existing buttons
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        # Set header
        self.month_year.config(text=self.current_date.strftime("%B %Y"))

        # Get first day of month and days in month
        first_day = self.current_date.replace(day=1)
        days_in_month = (first_day.replace(month=first_day.month %
                         12 + 1, day=1) - timedelta(days=1)).day

        # Calculate starting weekday (0=Monday, 6=Sunday)
        starting_weekday = (first_day.weekday() + 1) % 7

        # Create empty days for start of month
        for i in range(starting_weekday):
            tk.Label(self.cal_frame, text="", width=4).grid(row=0, column=i)

        # Create day buttons
        row, col = 0, starting_weekday
        for day in range(1, days_in_month + 1):
            if col == 7:
                row += 1
                col = 0

            date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
            btn = tk.Button(
                self.cal_frame,
                text=str(day),
                width=4,
                command=lambda d=date_str: self.select_date(d)
            )

            # Highlight today
            today = datetime.today()
            if today.year == self.current_date.year and today.month == self.current_date.month and today.day == day:
                btn.config(bg="#e0e0ff")

            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1

    def prev_month(self):
        self.current_date = self.current_date.replace(
            day=1) - timedelta(days=1)
        self.current_date = self.current_date.replace(day=1)
        self.render_calendar()

    def next_month(self):
        self.current_date = self.current_date.replace(
            day=28) + timedelta(days=4)
        self.current_date = self.current_date.replace(day=1)
        self.render_calendar()

    def select_date(self, date_str):
        self.selected_date = date_str
        self.on_date_selected(date_str)
        self.top.destroy()
