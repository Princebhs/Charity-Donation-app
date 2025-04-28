import tkinter as tk
from tkinter import ttk, messagebox
from gui.donor_view import DonorView
from gui.volunteer_view import VolunteerView
from gui.event_view import EventView
from gui.donation_view import DonationView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Charity Donation Tracker")
        self.root.geometry("1200x800")
        
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create main containers
        self.create_sidebar()
        self.create_main_content()
        
        # Dictionary to hold all views
        self.views = {}
        
        # Initialize views
        self.initialize_views()
        
        # Show default view
        self.show_view('donations')

    def create_sidebar(self):
        sidebar = ttk.Frame(self.root, padding="10")
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Style configuration for buttons
        style = ttk.Style()
        style.configure('Sidebar.TButton', padding=10, width=20)
        
        # Navigation buttons
        ttk.Button(sidebar, text="Donations", style='Sidebar.TButton',
                  command=lambda: self.show_view('donations')).pack(pady=5)
        ttk.Button(sidebar, text="Donors", style='Sidebar.TButton',
                  command=lambda: self.show_view('donors')).pack(pady=5)
        ttk.Button(sidebar, text="Events", style='Sidebar.TButton',
                  command=lambda: self.show_view('events')).pack(pady=5)
        ttk.Button(sidebar, text="Volunteers", style='Sidebar.TButton',
                  command=lambda: self.show_view('volunteers')).pack(pady=5)

    def create_main_content(self):
        self.main_content = ttk.Frame(self.root, padding="10")
        self.main_content.grid(row=0, column=1, sticky="nsew")
        
        # Configure grid
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

    def initialize_views(self):
        # Create all views
        self.views['donations'] = DonationView(self.main_content)
        self.views['donors'] = DonorView(self.main_content)
        self.views['events'] = EventView(self.main_content)
        self.views['volunteers'] = VolunteerView(self.main_content)

    def show_view(self, view_name):
        # Hide all views
        for view in self.views.values():
            view.grid_remove()
        
        # Show selected view
        self.views[view_name].grid(row=0, column=0, sticky="nsew")
        # Refresh the view's content
        self.views[view_name].refresh()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
