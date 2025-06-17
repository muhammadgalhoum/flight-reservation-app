import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import get_db_path
from edit_reservation import EditReservationForm


class ReservationsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create a container frame for better layout
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(container, text="All Reservations", font=(
            "Arial", 16, "bold")).pack(pady=(0, 15))

        # Create treeview with scrollbars
        tree_frame = tk.Frame(container)
        tree_frame.pack(fill="both", expand=True)

        # Create horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")

        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame)
        v_scrollbar.pack(side="right", fill="y")

        # Create treeview with action columns
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "flight", "name", "departure",
                     "destination", "date", "seat", "edit", "delete"),
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )

        # Configure scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)

        # Define columns
        self.tree.heading("id", text="ID", anchor="w")
        self.tree.heading("flight", text="Flight Number", anchor="w")
        self.tree.heading("name", text="Name", anchor="w")
        self.tree.heading("departure", text="Departure", anchor="w")
        self.tree.heading("destination", text="Destination", anchor="w")
        self.tree.heading("date", text="Date", anchor="w")
        self.tree.heading("seat", text="Seat", anchor="w")
        self.tree.heading("edit", text="Edit", anchor="center")
        self.tree.heading("delete", text="Delete", anchor="center")

        # Set column widths and hide ID column
        self.tree.column("id", width=0, stretch=False)  # Hide ID column
        self.tree.column("flight", width=120, minwidth=120)
        self.tree.column("name", width=150, minwidth=150)
        self.tree.column("departure", width=120, minwidth=120)
        self.tree.column("destination", width=120, minwidth=120)
        self.tree.column("date", width=120, minwidth=120)
        self.tree.column("seat", width=80, minwidth=80)
        self.tree.column("edit", width=50, minwidth=50, anchor="center")
        self.tree.column("delete", width=50, minwidth=50, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        # Bind click events for the action columns
        self.tree.bind("<Button-1>", self.handle_click)

        # Back button
        tk.Button(container, text="Back",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=10)

        # Load initial reservations
        self.load_reservations()

    def load_reservations(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, flight_number, name, departure, destination, date, seat_number 
                FROM reservations
            """)
            reservations = cursor.fetchall()
            conn.close()

            for res in reservations:
                # Add pencil and trash icons in the action columns
                self.tree.insert("", "end", values=(
                    res[0],  # id
                    res[1],  # flight_number
                    res[2],  # name
                    res[3],  # departure
                    res[4],  # destination
                    res[5],  # date
                    res[6],  # seat
                    "✏️",    # edit icon
                    "🗑️"     # delete icon
                ))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def handle_click(self, event):
        """Handle clicks on the edit or delete icons"""
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)

        if not row_id:
            return

        # Get the reservation ID (first value in the row)
        values = self.tree.item(row_id)['values']
        reservation_id = values[0]

        if column == "#8":  # Edit column
            EditReservationForm(self, reservation_id, self.load_reservations)
        elif column == "#9":  # Delete column
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reservation?"):
                try:
                    conn = sqlite3.connect(get_db_path())
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM reservations WHERE id = ?", (reservation_id,))
                    conn.commit()
                    conn.close()

                    # Reload reservations
                    self.load_reservations()
                    messagebox.showinfo(
                        "Success", "Reservation deleted successfully!")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", str(e))
