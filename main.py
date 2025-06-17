import os
import tkinter as tk
from home import HomePage
from booking import BookingPage
from database import create_database
from home import resource_path
from reservations import ReservationsPage


class FlightApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Flight Reservation System")
        self.geometry("800x600")
        
        # Set application icon
        try:
            icon_path = resource_path(os.path.join("assets", "logo.png"))
            icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, icon)
        except Exception as e:
            print(f"Error loading icon: {e}")
        
        create_database()
        
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (HomePage, BookingPage, ReservationsPage):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("HomePage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        if page_name == "ReservationsPage":
            frame.load_reservations()

if __name__ == "__main__":
    app = FlightApp()
    app.mainloop()