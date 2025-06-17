import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from database import get_db_path
from custom_date_picker import DatePicker



class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create a container frame for better layout
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(container, text="Book a Flight", font=("Arial", 16, "bold")).pack(pady=(0, 20))

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
            field_container = tk.Frame(container)
            field_container.pack(fill="x", pady=(0, 10))
            
            # Field label
            tk.Label(field_container, text=field, anchor="w").pack(fill="x", padx=5, pady=(0, 2))
            
            # Hint text
            tk.Label(field_container, text=hint, fg="gray", anchor="w").pack(fill="x", padx=5)
            
            # Input field with special handling for date
            if field == "Date":
                date_frame = tk.Frame(field_container)
                date_frame.pack(fill="x", padx=5)
                
                entry = tk.Entry(date_frame)
                entry.pack(side=tk.LEFT, fill="x", expand=True)
                
                tk.Button(
                    date_frame, 
                    text="📅", 
                    command=lambda e=entry: self.open_calendar(e)
                ).pack(side=tk.RIGHT, padx=(5, 0))
                self.entries[field] = entry
            else:
                entry = tk.Entry(field_container)
                entry.pack(fill="x", padx=5)
                self.entries[field] = entry

        # Separator line
        tk.Frame(container, height=1, bg="gray").pack(fill="x", pady=10)

        # Button container
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)
        
        # Buttons in horizontal layout
        tk.Button(button_frame, text="Cancel", width=10,
                 command=lambda: controller.show_frame("HomePage")).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Book Flight", width=10,
                  command=self.book_flight).pack(side=tk.LEFT, padx=10)

    def open_calendar(self, entry):
        def set_date(date_str):
            entry.delete(0, tk.END)
            entry.insert(0, date_str)
        
        DatePicker(self, set_date)

    def validate_date(self, date_str):
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return selected_date >= datetime.today().date()
        except ValueError:
            return False

    def get_form_data(self):
        """Get and validate form data"""
        data = {
            "Full Name": self.entries["Full Name"].get(),
            "Flight Number": self.entries["Flight Number"].get(),
            "Departure": self.entries["Departure"].get(),
            "Destination": self.entries["Destination"].get(),
            "Date": self.entries["Date"].get(),
            "Seat Number": self.entries["Seat Number"].get()
        }

        # Validate fields
        if any(not value for value in data.values()):
            messagebox.showerror("Error", "All fields must be filled!")
            return None

        if not self.validate_date(data["Date"]):
            messagebox.showerror("Error", "Please enter a valid future date in YYYY-MM-DD format!")
            return None

        return data

    def book_flight(self):
        """Handle new reservation creation"""
        data = self.get_form_data()
        if not data:
            return

        # Check for seat availability
        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()

            # UPDATED: Check if seat is already taken on this flight and date
            cursor.execute("""
                SELECT COUNT(*) FROM reservations 
                WHERE flight_number = ? AND date = ? AND seat_number = ?
            """, (data["Flight Number"], data["Date"], data["Seat Number"]))

            if cursor.fetchone()[0] > 0:
                messagebox.showerror(
                    "Error", "This seat is already booked for the selected flight and date!")
                return

            # Save to database
            cursor.execute("""
                INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data["Full Name"],
                data["Flight Number"],
                data["Departure"],
                data["Destination"],
                data["Date"],
                data["Seat Number"]
            ))
            conn.commit()
            messagebox.showinfo("Success", "Reservation booked successfully!")

            # Redirect to reservations page
            self.controller.show_frame("ReservationsPage")
            self.controller.frames["ReservationsPage"].load_reservations()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                conn.close()
