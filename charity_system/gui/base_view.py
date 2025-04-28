import tkinter as tk
from tkinter import ttk, messagebox

class BaseView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create common UI elements
        self.create_toolbar()
        self.create_content()
        
    def create_toolbar(self):
        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Search frame
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(search_frame, text="Search", command=self.search).pack(side=tk.LEFT)
        
        # Action buttons
        ttk.Button(toolbar, text="Add New", command=self.add_new).pack(side=tk.RIGHT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side=tk.RIGHT)
        
    def create_content(self):
        # Create Treeview
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def configure_tree_columns(self, columns, headings):
        """Configure treeview columns"""
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        for col, heading in zip(columns, headings):
            self.tree.heading(col, text=heading)
            self.tree.column(col, anchor="center")
    
    def add_new(self):
        """Override in child class"""
        pass
    
    def edit_item(self, item_id):
        """Override in child class"""
        pass
    
    def delete_item(self, item_id):
        """Override in child class"""
        pass
    
    def search(self):
        """Override in child class"""
        pass
    
    def refresh(self):
        """Override in child class"""
        pass
    
    def on_double_click(self, event):
        """Handle double-click on tree item"""
        item = self.tree.selection()[0]
        self.show_context_menu(item)
    
    def show_context_menu(self, item):
        """Show context menu for selected item"""
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Edit", command=lambda: self.edit_item(item))
        menu.add_command(label="Delete", command=lambda: self.confirm_delete(item))
        menu.post(self.winfo_pointerx(), self.winfo_pointery())
    
    def confirm_delete(self, item):
        """Show confirmation dialog before deleting"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            self.delete_item(item)
