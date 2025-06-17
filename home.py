import sys
import os
import tkinter as tk
from PIL import Image, ImageTk




def resource_path(rel_path):
    """
    Get absolute path to resource, works for dev (IDE) & for PyInstaller bundles.
    """
    if getattr(sys, 'frozen', False):
        # Running as bundle
        base = sys._MEIPASS
    else:
        # Running in IDE
        base = os.path.dirname(__file__)
    return os.path.join(base, rel_path)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create a container frame for better layout
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Logo section
        logo_frame = tk.Frame(container)
        logo_frame.pack(pady=(20, 30))

        try:
            logo_file = resource_path(os.path.join("assets", "logo.png"))
            original_image = Image.open(logo_file)
            resized_image = original_image.resize((120, 120), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(resized_image)

            logo_label = tk.Label(logo_frame, image=self.logo)
            logo_label.pack()
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback text if logo fails to load
            tk.Label(logo_frame, text="✈️", font=("Arial", 48)).pack()

        # Heading
        tk.Label(container, text="Simple Flight Reservation System",
                 font=("Arial", 18, "bold")).pack(pady=(0, 30))

        # Button container
        button_frame = tk.Frame(container)
        button_frame.pack(pady=20)

        # Book Flight button
        book_btn = tk.Button(
            button_frame,
            text="Book a Flight",
            width=20,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",  # Green color
            fg="white",
            command=lambda: controller.show_frame("BookingPage")
        )
        book_btn.pack(side=tk.LEFT, padx=15, pady=10)
        book_btn.bind("<Enter>", lambda e: book_btn.config(bg="#45a049"))
        book_btn.bind("<Leave>", lambda e: book_btn.config(bg="#4CAF50"))

        # View Reservations button
        view_btn = tk.Button(
            button_frame,
            text="View Reservations",
            width=20,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#2196F3",  # Blue color
            fg="white",
            command=lambda: controller.show_frame("ReservationsPage")
        )
        view_btn.pack(side=tk.LEFT, padx=15, pady=10)
        view_btn.bind("<Enter>", lambda e: view_btn.config(bg="#0b7dda"))
        view_btn.bind("<Leave>", lambda e: view_btn.config(bg="#2196F3"))