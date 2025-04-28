import tkinter as tk
from tkinter import ttk, messagebox
from models.donor import Donor
from .base_view import BaseView

class DonorView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure treeview columns
        columns = ("id", "name", "type", "phone", "postcode")
        headings = ("ID", "Name", "Type", "Phone", "Postcode")
        self.configure_tree_columns(columns, headings)
        
        # Initial data load
        self.refresh()
        
    def refresh(self):
        """Load all donors into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load donors
        donors = Donor.get_all()
        for donor in donors:
            name = donor['business_name'] if donor['business_name'] else f"{donor['first_name']} {donor['surname']}"
            self.tree.insert("", "end", donor['donor_id'], values=(
                donor['donor_id'],
                name,
                donor['donor_type'],
                donor['phone_number'],
                donor['postcode']
            ))
            
    def add_new(self):
        """Open dialog to add new donor"""
        self.open_donor_dialog()
        
    def edit_item(self, item_id):
        """Open dialog to edit donor"""
        donor = Donor.get_by_id(item_id)
        if donor:
            self.open_donor_dialog(donor)
            
    def delete_item(self, item_id):
        """Delete donor"""
        if Donor.delete(item_id):
            self.refresh()
            messagebox.showinfo("Success", "Donor deleted successfully")
        else:
            messagebox.showerror("Error", "Cannot delete donor with existing donations")
            
    def search(self):
        """Search donors"""
        term = self.search_var.get()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load matching donors
        donors = Donor.search(term)
        for donor in donors:
            name = donor['business_name'] if donor['business_name'] else f"{donor['first_name']} {donor['surname']}"
            self.tree.insert("", "end", donor['donor_id'], values=(
                donor['donor_id'],
                name,
                donor['donor_type'],
                donor['phone_number'],
                donor['postcode']
            ))
            
    def open_donor_dialog(self, donor=None):
        """Open dialog to add/edit donor"""
        dialog = tk.Toplevel(self)
        dialog.title("Add Donor" if donor is None else "Edit Donor")
        dialog.geometry("400x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Donor Type:").pack(pady=5)
        donor_type = tk.StringVar(value=donor['donor_type'] if donor else 'individual')
        type_frame = ttk.Frame(dialog)
        type_frame.pack(pady=5)
        ttk.Radiobutton(type_frame, text="Individual", variable=donor_type, 
                       value="individual").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Business", variable=donor_type,
                       value="business").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(dialog, text="First Name:").pack(pady=5)
        first_name = ttk.Entry(dialog)
        first_name.pack(pady=5)
        if donor:
            first_name.insert(0, donor['first_name'] or '')
            
        ttk.Label(dialog, text="Surname:").pack(pady=5)
        surname = ttk.Entry(dialog)
        surname.pack(pady=5)
        if donor:
            surname.insert(0, donor['surname'] or '')
            
        ttk.Label(dialog, text="Business Name:").pack(pady=5)
        business_name = ttk.Entry(dialog)
        business_name.pack(pady=5)
        if donor:
            business_name.insert(0, donor['business_name'] or '')
            
        ttk.Label(dialog, text="Postcode:*").pack(pady=5)
        postcode = ttk.Entry(dialog)
        postcode.pack(pady=5)
        if donor:
            postcode.insert(0, donor['postcode'])
            
        ttk.Label(dialog, text="House Number:").pack(pady=5)
        house_number = ttk.Entry(dialog)
        house_number.pack(pady=5)
        if donor:
            house_number.insert(0, donor['house_number'] or '')
            
        ttk.Label(dialog, text="Phone Number:*").pack(pady=5)
        phone_number = ttk.Entry(dialog)
        phone_number.pack(pady=5)
        if donor:
            phone_number.insert(0, donor['phone_number'])
            
        def save():
            # Validate required fields
            if not postcode.get() or not phone_number.get():
                messagebox.showerror("Error", "Postcode and Phone Number are required")
                return
                
            try:
                if donor:
                    success = Donor.update(
                        donor['donor_id'], first_name.get(), surname.get(),
                        business_name.get(), postcode.get(), house_number.get(),
                        phone_number.get(), donor_type.get()
                    )
                else:
                    success = Donor.create(
                        first_name.get(), surname.get(), business_name.get(),
                        postcode.get(), house_number.get(), phone_number.get(),
                        donor_type.get()
                    )
                
                if success:
                    dialog.destroy()
                    self.refresh()
                    messagebox.showinfo("Success", 
                                      "Donor updated successfully" if donor 
                                      else "Donor added successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
