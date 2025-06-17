import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from database import get_db_path
from custom_date_picker import DatePicker



class EditReservationForm:
    def __init__(self, parent, reservation_id, on_update_callback):
        self.reservation_id = reservation_id
        self.on_update_callback = on_update_callback

        # Create a new top-level window
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Reservation")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.grab_set()  # Make it modal

        # Center the window
        parent.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (parent.winfo_width() // 2) - (width // 2) + parent.winfo_x()
        y = (parent.winfo_height() // 2) - (height // 2) + parent.winfo_y()
        self.window.geometry(f'+{x}+{y}')

        # Create the form
        self.create_form()

        # Load reservation data
        self.load_reservation_data()

    def create_form(self):
        # Title with larger font
        tk.Label(self.window, text="Edit Reservation", font=(
            "Arial", 16, "bold")).pack(pady=(20, 10))

        self.entries = {}
        fields = [
            ("Full Name", "Enter your full name"),
            ("Flight Number", "e.g. FS123"),
            ("Departure", "e.g. New York"),
            ("Destination", "e.g. London"),
            ("Date", "Pick a date"),
            ("Seat Number", "e.g. 12A")
        ]

        for field, hint in fields:
            # Field container
            field_frame = tk.Frame(self.window)
            field_frame.pack(fill="x", padx=20, pady=5)

            # Field label
            tk.Label(field_frame, text=field, anchor="w").pack(fill="x")

            # Hint text
            tk.Label(field_frame, text=hint, fg="gray",
                     anchor="w").pack(fill="x")

            # Input field with special handling for date
            if field == "Date":
                date_frame = tk.Frame(field_frame)
                date_frame.pack(fill="x")

                entry = tk.Entry(date_frame)
                entry.pack(side="left", fill="x", expand=True)

                tk.Button(
                    date_frame,
                    text="📅",
                    command=lambda e=entry: self.open_calendar(e)
                ).pack(side="right", padx=(5, 0))
                self.entries[field] = entry
            else:
                entry = tk.Entry(field_frame)
                entry.pack(fill="x")
                self.entries[field] = entry

        # Separator line
        tk.Frame(self.window, height=1, bg="gray").pack(
            fill="x", pady=10, padx=20)

        # Button container
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Cancel", width=10,
                  command=self.window.destroy).pack(side="left", padx=10)
        tk.Button(button_frame, text="Update Reservation", width=15,
                  command=self.update_reservation).pack(side="left", padx=10)

    def load_reservation_data(self):
        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, flight_number, departure, destination, date, seat_number 
                FROM reservations WHERE id = ?
            """, (self.reservation_id,))
            reservation = cursor.fetchone()
            conn.close()

            if reservation:
                data = {
                    "Full Name": reservation[0],
                    "Flight Number": reservation[1],
                    "Departure": reservation[2],
                    "Destination": reservation[3],
                    "Date": reservation[4],
                    "Seat Number": reservation[5]
                }

                for field, value in data.items():
                    self.entries[field].delete(0, tk.END)
                    self.entries[field].insert(0, value)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def open_calendar(self, entry):
        def set_date(date_str):
            entry.delete(0, tk.END)
            entry.insert(0, date_str)

        DatePicker(self.window, set_date)

    def validate_date(self, date_str):
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return selected_date >= datetime.today().date()
        except ValueError:
            return False

    def update_reservation(self):
        data = {
            "Full Name": self.entries["Full Name"].get(),
            "Flight Number": self.entries["Flight Number"].get(),
            "Departure": self.entries["Departure"].get(),
            "Destination": self.entries["Destination"].get(),
            "Date": self.entries["Date"].get(),
            "Seat Number": self.entries["Seat Number"].get()
        }

        if any(not value for value in data.values()):
            messagebox.showerror("Error", "All fields must be filled!")
            return

        if not self.validate_date(data["Date"]):
            messagebox.showerror(
                "Error", "Please enter a valid future date in YYYY-MM-DD format!")
            return

        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()

            # Check if seat is available (excluding current reservation)
            cursor.execute("""
                SELECT COUNT(*) FROM reservations 
                WHERE flight_number = ? AND date = ? AND seat_number = ? AND id != ?
            """, (data["Flight Number"], data["Date"], data["Seat Number"], self.reservation_id))

            if cursor.fetchone()[0] > 0:
                messagebox.showerror(
                    "Error", "This seat is already booked for the selected date!")
                return

            # Update reservation
            cursor.execute("""
                UPDATE reservations 
                SET name = ?, flight_number = ?, departure = ?, destination = ?, date = ?, seat_number = ?
                WHERE id = ?
            """, (
                data["Full Name"],
                data["Flight Number"],
                data["Departure"],
                data["Destination"],
                data["Date"],
                data["Seat Number"],
                self.reservation_id
            ))
            conn.commit()
            messagebox.showinfo("Success", "Reservation updated successfully!")
            conn.close()

            # Refresh reservations list
            self.on_update_callback()

            # Close the edit window
            self.window.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
