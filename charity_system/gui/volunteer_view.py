import tkinter as tk
from tkinter import ttk, messagebox
from models.volunteer import Volunteer
from datetime import datetime
from .base_view import BaseView

class VolunteerView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure treeview columns
        columns = ("id", "name", "phone", "email", "join_date")
        headings = ("ID", "Name", "Phone", "Email", "Join Date")
        self.configure_tree_columns(columns, headings)
        
        # Initial data load
        self.refresh()
        
    def refresh(self):
        """Load all volunteers into the treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        volunteers = Volunteer.get_all()
        for volunteer in volunteers:
            name = f"{volunteer['first_name']} {volunteer['surname']}"
            self.tree.insert("", "end", volunteer['volunteer_id'], values=(
                volunteer['volunteer_id'],
                name,
                volunteer['phone_number'],
                volunteer['email'],
                volunteer['join_date']
            ))
            
    def add_new(self):
        """Open dialog to add new volunteer"""
        self.open_volunteer_dialog()
        
    def edit_item(self, item_id):
        """Open dialog to edit volunteer"""
        volunteer = Volunteer.get_by_id(item_id)
        if volunteer:
            self.open_volunteer_dialog(volunteer)
            
    def delete_item(self, item_id):
        """Delete volunteer"""
        if Volunteer.delete(item_id):
            self.refresh()
            messagebox.showinfo("Success", "Volunteer deleted successfully")
        else:
            messagebox.showerror("Error", 
                "Cannot delete volunteer with associated donations or events")
            
    def search(self):
        """Search volunteers"""
        term = self.search_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        volunteers = Volunteer.search(term)
        for volunteer in volunteers:
            name = f"{volunteer['first_name']} {volunteer['surname']}"
            self.tree.insert("", "end", volunteer['volunteer_id'], values=(
                volunteer['volunteer_id'],
                name,
                volunteer['phone_number'],
                volunteer['email'],
                volunteer['join_date']
            ))
            
    def open_volunteer_dialog(self, volunteer=None):
        """Open dialog to add/edit volunteer"""
        dialog = tk.Toplevel(self)
        dialog.title("Add Volunteer" if volunteer is None else "Edit Volunteer")
        dialog.geometry("400x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="First Name:*").pack(pady=5)
        first_name = ttk.Entry(dialog)
        first_name.pack(pady=5)
        if volunteer:
            first_name.insert(0, volunteer['first_name'])
            
        ttk.Label(dialog, text="Surname:*").pack(pady=5)
        surname = ttk.Entry(dialog)
        surname.pack(pady=5)
        if volunteer:
            surname.insert(0, volunteer['surname'])
            
        ttk.Label(dialog, text="Phone Number:*").pack(pady=5)
        phone_number = ttk.Entry(dialog)
        phone_number.pack(pady=5)
        if volunteer:
            phone_number.insert(0, volunteer['phone_number'])
            
        ttk.Label(dialog, text="Email:*").pack(pady=5)
        email = ttk.Entry(dialog)
        email.pack(pady=5)
        if volunteer:
            email.insert(0, volunteer['email'])
            
        def save():
            # Validate required fields
            if not all([first_name.get(), surname.get(), 
                       phone_number.get(), email.get()]):
                messagebox.showerror("Error", "All fields are required")
                return
                
            try:
                if volunteer:
                    success = Volunteer.update(
                        volunteer['volunteer_id'], first_name.get(), 
                        surname.get(), phone_number.get(), email.get()
                    )
                else:
                    success = Volunteer.create(
                        first_name.get(), surname.get(), 
                        phone_number.get(), email.get()
                    )
                
                if success:
                    dialog.destroy()
                    self.refresh()
                    messagebox.showinfo("Success", 
                        "Volunteer updated successfully" if volunteer 
                        else "Volunteer added successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
