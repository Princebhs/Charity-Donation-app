import tkinter as tk
from tkinter import ttk, messagebox
from models.donation import Donation
from models.donor import Donor
from models.event import Event
from models.volunteer import Volunteer
from datetime import datetime
from tkcalendar import DateEntry
from .base_view import BaseView

class DonationView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure treeview columns
        columns = ("id", "amount", "date", "donor", "event", "collector", "gift_aid")
        headings = ("ID", "Amount", "Date", "Donor", "Event", "Collector", "Gift Aid")
        self.configure_tree_columns(columns, headings)
        
        # Add filter options to toolbar
        self.add_filters()
        
        # Initial data load
        self.refresh()
        
    def add_filters(self):
        """Add filter options to the toolbar"""
        filter_frame = ttk.Frame(self)
        filter_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # Donor filter
        ttk.Label(filter_frame, text="Filter by Donor:").pack(side=tk.LEFT, padx=5)
        self.donor_var = tk.StringVar()
        donors = Donor.get_all()
        donor_cb = ttk.Combobox(filter_frame, textvariable=self.donor_var, width=20)
        donor_cb['values'] = ["All"] + [
            f"{d['donor_id']}: {d['business_name'] or f'{d['first_name']} {d['surname']}'}"
            for d in donors
        ]
        donor_cb.current(0)
        donor_cb.pack(side=tk.LEFT, padx=5)
        
        # Event filter
        ttk.Label(filter_frame, text="Filter by Event:").pack(side=tk.LEFT, padx=5)
        self.event_var = tk.StringVar()
        events = Event.get_all()
        event_cb = ttk.Combobox(filter_frame, textvariable=self.event_var, width=20)
        event_cb['values'] = ["All"] + [
            f"{e['event_id']}: {e['event_name']}"
            for e in events
        ]
        event_cb.current(0)
        event_cb.pack(side=tk.LEFT, padx=5)
        
        # Volunteer filter
        ttk.Label(filter_frame, text="Filter by Volunteer:").pack(side=tk.LEFT, padx=5)
        self.volunteer_var = tk.StringVar()
        volunteers = Volunteer.get_all()
        volunteer_cb = ttk.Combobox(filter_frame, textvariable=self.volunteer_var, width=20)
        volunteer_cb['values'] = ["All"] + [
            f"{v['volunteer_id']}: {v['first_name']} {v['surname']}"
            for v in volunteers
        ]
        volunteer_cb.current(0)
        volunteer_cb.pack(side=tk.LEFT, padx=5)
        
        # Apply filters button
        ttk.Button(filter_frame, text="Apply Filters", 
                  command=self.apply_filters).pack(side=tk.LEFT, padx=5)
        
    def refresh(self):
        """Load all donations into the treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        donations = Donation.get_all()
        self.populate_tree(donations)
            
    def populate_tree(self, donations):
        """Populate treeview with donation data"""
        for donation in donations:
            self.tree.insert("", "end", donation['donation_id'], values=(
                donation['donation_id'],
                f"£{donation['amount']:.2f}",
                donation['donation_date'],
                donation['donor_name'],
                donation['event_name'] or "No Event",
                donation['collector_name'],
                "Yes" if donation['gift_aid'] else "No"
            ))
            
    def add_new(self):
        """Open dialog to add new donation"""
        self.open_donation_dialog()
        
    def edit_item(self, item_id):
        """Open dialog to edit donation"""
        donation = Donation.get_by_id(item_id)
        if donation:
            self.open_donation_dialog(donation)
            
    def delete_item(self, item_id):
        """Delete donation"""
        if Donation.delete(item_id):
            self.refresh()
            messagebox.showinfo("Success", "Donation deleted successfully")
        else:
            messagebox.showerror("Error", "Failed to delete donation")
            
    def search(self):
        """Search donations"""
        term = self.search_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        donations = Donation.search(term=term)
        self.populate_tree(donations)
            
    def apply_filters(self):
        """Apply selected filters"""
        donor_id = None
        if self.donor_var.get() != "All":
            donor_id = int(self.donor_var.get().split(':')[0])
            
        event_id = None
        if self.event_var.get() != "All":
            event_id = int(self.event_var.get().split(':')[0])
            
        volunteer_id = None
        if self.volunteer_var.get() != "All":
            volunteer_id = int(self.volunteer_var.get().split(':')[0])
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        donations = Donation.search(
            donor_id=donor_id,
            event_id=event_id,
            volunteer_id=volunteer_id
        )
        self.populate_tree(donations)
            
    def open_donation_dialog(self, donation=None):
        """Open dialog to add/edit donation"""
        dialog = tk.Toplevel(self)
        dialog.title("Add Donation" if donation is None else "Edit Donation")
        dialog.geometry("400x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Amount (£):*").pack(pady=5)
        amount = ttk.Entry(dialog)
        amount.pack(pady=5)
        if donation:
            amount.insert(0, f"{donation['amount']:.2f}")
            
        ttk.Label(dialog, text="Date:*").pack(pady=5)
        date_entry = DateEntry(dialog, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
        date_entry.pack(pady=5)
        if donation:
            date_entry.set_date(datetime.strptime(donation['donation_date'], '%Y-%m-%d'))
            
        ttk.Label(dialog, text="Donor:*").pack(pady=5)
        donors = Donor.get_all()
        donor_id = tk.StringVar()
        donor = ttk.Combobox(dialog, textvariable=donor_id)
        donor['values'] = [
            f"{d['donor_id']}: {d['business_name'] or f'{d['first_name']} {d['surname']}'}"
            for d in donors
        ]
        donor.pack(pady=5)
        if donation:
            for i, d in enumerate(donors):
                if d['donor_id'] == donation['donor_id']:
                    donor.current(i)
                    break
                    
        ttk.Label(dialog, text="Event:").pack(pady=5)
        events = Event.get_all()
        event_id = tk.StringVar()
        event = ttk.Combobox(dialog, textvariable=event_id)
        event['values'] = [""] + [
            f"{e['event_id']}: {e['event_name']}"
            for e in events
        ]
        event.pack(pady=5)
        if donation and donation['event_id']:
            for i, e in enumerate(events):
                if e['event_id'] == donation['event_id']:
                    event.current(i + 1)
                    break
                    
        ttk.Label(dialog, text="Collected By:*").pack(pady=5)
        volunteers = Volunteer.get_all()
        collector_id = tk.StringVar()
        collector = ttk.Combobox(dialog, textvariable=collector_id)
        collector['values'] = [
            f"{v['volunteer_id']}: {v['first_name']} {v['surname']}"
            for v in volunteers
        ]
        collector.pack(pady=5)
        if donation:
            for i, v in enumerate(volunteers):
                if v['volunteer_id'] == donation['collected_by']:
                    collector.current(i)
                    break
                    
        gift_aid = tk.BooleanVar(value=donation['gift_aid'] if donation else False)
        ttk.Checkbutton(dialog, text="Gift Aid", variable=gift_aid).pack(pady=5)
        
        ttk.Label(dialog, text="Notes:").pack(pady=5)
        notes = tk.Text(dialog, height=4, width=40)
        notes.pack(pady=5)
        if donation and donation['notes']:
            notes.insert('1.0', donation['notes'])
            
        def save():
            # Validate required fields
            if not all([amount.get(), donor.get(), collector.get()]):
                messagebox.showerror("Error", "Required fields missing")
                return
                
            try:
                # Get IDs from combobox selections
                donor_id = int(donor.get().split(':')[0])
                collector_id = int(collector.get().split(':')[0])
                evt_id = None
                if event.get():
                    evt_id = int(event.get().split(':')[0])
                
                if donation:
                    success = Donation.update(
                        donation['donation_id'], float(amount.get()),
                        date_entry.get_date().strftime('%Y-%m-%d'),
                        gift_aid.get(), notes.get('1.0', 'end-1c'),
                        donor_id, evt_id, collector_id
                    )
                else:
                    success = Donation.create(
                        float(amount.get()),
                        date_entry.get_date().strftime('%Y-%m-%d'),
                        gift_aid.get(), notes.get('1.0', 'end-1c'),
                        donor_id, evt_id, collector_id
                    )
                
                if success:
                    dialog.destroy()
                    self.refresh()
                    messagebox.showinfo("Success", 
                        "Donation updated successfully" if donation 
                        else "Donation added successfully")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount value")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
