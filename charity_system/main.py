import tkinter as tk
from tkinter import ttk
from gui.main_window import MainWindow

def main():
    root = tk.Tk()
    root.title("Charity Donation Tracker")
    
    # Set theme
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' theme for a modern look
    
    # Configure colors
    style.configure(".", font=('Helvetica', 10))
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
    
    # Create main application window
    app = MainWindow(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
