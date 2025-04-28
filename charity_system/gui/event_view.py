import tkinter as tk
from tkinter import ttk, messagebox
from models.event import Event
from models.volunteer import Volunteer
from datetime import datetime
from tkcalendar import DateEntry
from .base_view import BaseView

class EventView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure treeview columns
        columns = ("id", "name", "room", "date", "time", "cost", "organizer")
        headings = ("ID", "Event Name", "Room", "Date", "Time", "Cost", "Organizer")
        self.configure_tree_columns(columns, headings)
        
        # Add Manage Volunteers button to toolbar
        ttk.Button(self.tree_frame, text="Manage Volunteers", 
                  command=self.manage_volunteers).pack(side=tk.BOTTOM, pady=5)
        
        # Initial data load
        self.refresh()
        
    def refresh(self):
        """Load all events into the treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        events = Event.get_all()
        for event in events:
            self.tree.insert("", "end", event['event_id'], values=(
                event['event_id'],
                event['event_name'],
                event['room_name'],
                event['booking_date'],
                event['booking_time'],
                f"£{event['cost']:.2f}",
                event['organizer_name'] or "No Organizer"
            ))
            
    def add_new(self):
        """Open dialog to add new event"""
        self.open_event_dialog()
        
    def edit_item(self, item_id):
        """Open dialog to edit event"""
        event = Event.get_by_id(item_id)
        if event:
            self.open_event_dialog(event)
            
    def delete_item(self, item_id):
        """Delete event"""
        if Event.delete(item_id):
            self.refresh()
            messagebox.showinfo("Success", "Event deleted successfully")
        else:
            messagebox.showerror("Error", "Cannot delete event with existing donations")
            
    def search(self):
        """Search events"""
        term = self.search_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        events = Event.search(term)
        for event in events:
            self.tree.insert("", "end", event['event_id'], values=(
                event['event_id'],
                event['event_name'],
                event['room_name'],
                event['booking_date'],
                event['booking_time'],
                f"£{event['cost']:.2f}",
                event['organizer_name'] or "No Organizer"
            ))
            
    def open_event_dialog(self, event=None):
        """Open dialog to add/edit event"""
        dialog = tk.Toplevel(self)
        dialog.title("Add Event" if event is None else "Edit Event")
        dialog.geometry("400x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Event Name:*").pack(pady=5)
        event_name = ttk.Entry(dialog)
        event_name.pack(pady=5)
        if event:
            event_name.insert(0, event['event_name'])
            
        ttk.Label(dialog, text="Room Name:*").pack(pady=5)
        room_name = ttk.Entry(dialog)
        room_name.pack(pady=5)
        if event:
            room_name.insert(0, event['room_name'])
            
        ttk.Label(dialog, text="Booking Date:*").pack(pady=5)
        booking_date = DateEntry(dialog, width=12, background='darkblue',
                               foreground='white', borderwidth=2)
        booking_date.pack(pady=5)
        if event:
            booking_date.set_date(datetime.strptime(event['booking_date'], '%Y-%m-%d'))
            
        ttk.Label(dialog, text="Booking Time:*").pack(pady=5)
        time_frame = ttk.Frame(dialog)
        time_frame.pack(pady=5)
        hour = ttk.Spinbox(time_frame, from_=0, to=23, width=3)
        hour.pack(side=tk.LEFT)
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT)
        minute = ttk.Spinbox(time_frame, from_=0, to=59, width=3)
        minute.pack(side=tk.LEFT)
        if event:
            time = datetime.strptime(event['booking_time'], '%H:%M').time()
            hour.set(time.hour)
            minute.set(time.minute)
            
        ttk.Label(dialog, text="Cost (£):*").pack(pady=5)
        cost = ttk.Entry(dialog)
        cost.pack(pady=5)
        if event:
            cost.insert(0, f"{event['cost']:.2f}")
            
        ttk.Label(dialog, text="Organizer:").pack(pady=5)
        volunteers = Volunteer.get_all()
        organizer_id = tk.StringVar()
        organizer = ttk.Combobox(dialog, textvariable=organizer_id)
        organizer['values'] = [""] + [
            f"{v['volunteer_id']}: {v['first_name']} {v['surname']}" 
            for v in volunteers
        ]
        organizer.pack(pady=5)
        if event and event['organizer_id']:
            for i, v in enumerate(volunteers):
                if v['volunteer_id'] == event['organizer_id']:
                    organizer.current(i + 1)
                    break
            
        def save():
            # Validate required fields
            if not all([event_name.get(), room_name.get(), 
                       booking_date.get(), cost.get()]):
                messagebox.showerror("Error", "Required fields missing")
                return
                
            try:
                # Format time
                time_str = f"{int(hour.get()):02d}:{int(minute.get()):02d}"
                # Get organizer ID
                org_id = None
                if organizer.get():
                    org_id = int(organizer.get().split(':')[0])
                
                if event:
                    success = Event.update(
                        event['event_id'], event_name.get(), room_name.get(),
                        booking_date.get(), time_str, float(cost.get()), org_id
                    )
                else:
                    success = Event.create(
                        event_name.get(), room_name.get(), booking_date.get(),
                        time_str, float(cost.get()), org_id
                    )
                
                if success:
                    dialog.destroy()
                    self.refresh()
                    messagebox.showinfo("Success", 
                        "Event updated successfully" if event 
                        else "Event added successfully")
            except ValueError as e:
                messagebox.showerror("Error", "Invalid cost value")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
        
    def manage_volunteers(self):
        """Open dialog to manage event volunteers"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an event first")
            return
            
        event_id = selection[0]
        event = Event.get_by_id(event_id)
        if not event:
            return
            
        dialog = tk.Toplevel(self)
        dialog.title(f"Manage Volunteers - {event['event_name']}")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Create frames
        left_frame = ttk.Frame(dialog)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(dialog)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Available volunteers
        ttk.Label(left_frame, text="Available Volunteers").pack()
        available_tree = ttk.Treeview(left_frame, columns=("id", "name"), show="headings")
        available_tree.heading("id", text="ID")
        available_tree.heading("name", text="Name")
        available_tree.pack(fill=tk.BOTH, expand=True)
        
        # Assigned volunteers
        ttk.Label(right_frame, text="Assigned Volunteers").pack()
        assigned_tree = ttk.Treeview(right_frame, columns=("id", "name", "role"), 
                                   show="headings")
        assigned_tree.heading("id", text="ID")
        assigned_tree.heading("name", text="Name")
        assigned_tree.heading("role", text="Role")
        assigned_tree.pack(fill=tk.BOTH, expand=True)
        
        def refresh_volunteers():
            # Clear trees
            for item in available_tree.get_children():
                available_tree.delete(item)
            for item in assigned_tree.get_children():
                assigned_tree.delete(item)
                
            # Get all volunteers
            all_volunteers = {v['volunteer_id']: v for v in Volunteer.get_all()}
            
            # Get assigned volunteers
            assigned = Event.get_event_volunteers(event_id)
            assigned_ids = {v['volunteer_id'] for v in assigned}
            
            # Fill assigned tree
            for v in assigned:
                assigned_tree.insert("", "end", v['volunteer_id'], values=(
                    v['volunteer_id'],
                    f"{v['first_name']} {v['surname']}",
                    v['role']
                ))
                
            # Fill available tree
            for v_id, v in all_volunteers.items():
                if v_id not in assigned_ids:
                    available_tree.insert("", "end", v_id, values=(
                        v_id,
                        f"{v['first_name']} {v['surname']}"
                    ))
        
        def assign_volunteer():
            selection = available_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a volunteer to assign")
                return
                
            volunteer_id = selection[0]
            
            # Ask for role
            role_dialog = tk.Toplevel(dialog)
            role_dialog.title("Assign Role")
            role_dialog.transient(dialog)
            role_dialog.grab_set()
            
            ttk.Label(role_dialog, text="Role:").pack(pady=5)
            role = ttk.Entry(role_dialog)
            role.pack(pady=5)
            
            def save_role():
                if not role.get():
                    messagebox.showerror("Error", "Role is required")
                    return
                    
                if Event.assign_volunteer(event_id, volunteer_id, role.get()):
                    role_dialog.destroy()
                    refresh_volunteers()
                else:
                    messagebox.showerror("Error", "Failed to assign volunteer")
                    
            ttk.Button(role_dialog, text="Save", command=save_role).pack(pady=5)
            ttk.Button(role_dialog, text="Cancel", 
                      command=role_dialog.destroy).pack(pady=5)
            
        def remove_volunteer():
            selection = assigned_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", 
                    "Please select a volunteer to remove")
                return
                
            volunteer_id = selection[0]
            if Event.remove_volunteer(event_id, volunteer_id):
                refresh_volunteers()
            else:
                messagebox.showerror("Error", "Failed to remove volunteer")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Assign →", 
                  command=assign_volunteer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="← Remove", 
                  command=remove_volunteer).pack(side=tk.RIGHT, padx=5)
        
        # Initial load
        refresh_volunteers()
