import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import MySQLdb
import csv
import json
from datetime import datetime

class DesktopSQLTool:
    def __init__(self, root):
        self.root = root
        self.root.title("MySQL Query Tool - Desktop Edition")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1e1e1e')
        
        # Dark mode colors
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_medium': '#2d2d2d',
            'bg_light': '#3c3c3c',
            'fg_primary': '#d4d4d4',
            'fg_secondary': '#9cdcfe',
            'accent': '#007acc',
            'accent_hover': '#1a8ad4',
            'red': '#f44747',
            'green': '#4ec9b0',
            'yellow': '#dcdcaa',
            'orange': '#ce9178',
            'border': '#404040'
        }
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.connection = None
        self.setup_ui()
        
    def configure_styles(self):
        # Configure ttk styles for dark mode
        self.style.configure('TFrame', background=self.colors['bg_dark'])
        self.style.configure('TLabel', background=self.colors['bg_dark'], foreground=self.colors['fg_primary'])
        self.style.configure('TLabelframe', background=self.colors['bg_dark'], foreground=self.colors['fg_primary'])
        self.style.configure('TLabelframe.Label', background=self.colors['bg_dark'], foreground=self.colors['fg_primary'])
        self.style.configure('TButton', 
            background=self.colors['bg_medium'], 
            foreground=self.colors['fg_primary'],
            borderwidth=1,
            focusthickness=0,
            padding=5
        )
        self.style.map('TButton',
            background=[('active', self.colors['accent'])],
            foreground=[('active', '#ffffff')]
        )
        
        self.style.configure('TEntry', 
            fieldbackground=self.colors['bg_medium'],
            foreground=self.colors['fg_primary'],
            insertcolor=self.colors['fg_primary']
        )
        
        self.style.configure('Treeview',
            background=self.colors['bg_medium'],
            foreground=self.colors['fg_primary'],
            fieldbackground=self.colors['bg_medium'],
            borderwidth=0
        )
        self.style.configure('Treeview.Heading',
            background=self.colors['bg_light'],
            foreground=self.colors['fg_primary'],
            relief='flat'
        )
        self.style.map('Treeview',
            background=[('selected', self.colors['accent'])],
            foreground=[('selected', '#ffffff')]
        )
        
        self.style.configure('TScrollbar',
            background=self.colors['bg_medium'],
            troughcolor=self.colors['bg_dark'],
            borderwidth=0,
            arrowcolor=self.colors['fg_primary']
        )
        
        self.style.configure('TPanedwindow', background=self.colors['bg_dark'])
        self.style.configure('TSeparator', background=self.colors['border'])
        
    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill="both", expand=True)
        
        # Connection Panel (Top)
        self.create_connection_panel(main_container)
        
        # Main content area (Split into left and right)
        content_paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        content_paned.pack(fill="both", expand=True, pady=10)
        
        # Left panel - Query input
        left_frame = ttk.Frame(content_paned)
        content_paned.add(left_frame, weight=1)
        self.create_query_panel(left_frame)
        
        # Right panel - Results
        right_frame = ttk.Frame(content_paned)
        content_paned.add(right_frame, weight=2)
        self.create_results_panel(right_frame)
        
        # Status bar (Bottom)
        self.create_status_bar(main_container)
    
    def create_connection_panel(self, parent):
        conn_frame = ttk.LabelFrame(parent, text="Database Connection", padding="10")
        conn_frame.pack(fill="x")
        
        # Connection fields
        fields_frame = ttk.Frame(conn_frame)
        fields_frame.pack(fill="x")
        
        # Row 1
        ttk.Label(fields_frame, text="Host:").grid(row=0, column=0, sticky="w", padx=5)
        self.host_entry = ttk.Entry(fields_frame, width=20)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(fields_frame, text="Port:").grid(row=0, column=2, sticky="w", padx=5)
        self.port_entry = ttk.Entry(fields_frame, width=10)
        self.port_entry.insert(0, "3306")
        self.port_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(fields_frame, text="User:").grid(row=0, column=4, sticky="w", padx=5)
        self.user_entry = ttk.Entry(fields_frame, width=20)
        self.user_entry.insert(0, "root")
        self.user_entry.grid(row=0, column=5, padx=5)
        
        ttk.Label(fields_frame, text="Password:").grid(row=0, column=6, sticky="w", padx=5)
        self.password_entry = ttk.Entry(fields_frame, width=20, show="*")
        self.password_entry.grid(row=0, column=7, padx=5)
        
        # Row 2
        ttk.Label(fields_frame, text="Database:").grid(row=1, column=0, sticky="w", padx=5, pady=10)
        self.database_entry = ttk.Entry(fields_frame, width=20)
        self.database_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(fields_frame)
        btn_frame.grid(row=1, column=2, columnspan=6, pady=10)
        
        self.connect_btn = ttk.Button(btn_frame, text="🔌 Connect", command=self.connect_database)
        self.connect_btn.pack(side="left", padx=5)
        
        self.disconnect_btn = ttk.Button(btn_frame, text="🔌 Disconnect", command=self.disconnect_database, state="disabled")
        self.disconnect_btn.pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="📋 Show Databases", command=self.show_databases).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📊 Show Tables", command=self.show_tables).pack(side="left", padx=5)
    
    def create_query_panel(self, parent):
        query_frame = ttk.LabelFrame(parent, text="SQL Query", padding="10")
        query_frame.pack(fill="both", expand=True)
        
        # Query toolbar
        toolbar = ttk.Frame(query_frame)
        toolbar.pack(fill="x", pady=(0, 5))
        
        ttk.Button(toolbar, text="▶ Execute (F5)", command=self.execute_query).pack(side="left", padx=2)
        ttk.Button(toolbar, text="📝 Format SQL", command=self.format_sql).pack(side="left", padx=2)
        ttk.Button(toolbar, text="📂 Load SQL", command=self.load_sql_file).pack(side="left", padx=2)
        ttk.Button(toolbar, text="💾 Save SQL", command=self.save_sql_file).pack(side="left", padx=2)
        ttk.Button(toolbar, text="🗑 Clear", command=self.clear_query).pack(side="left", padx=2)
        
        # Query text area with line numbers
        query_text_frame = ttk.Frame(query_frame)
        query_text_frame.pack(fill="both", expand=True)
        
        self.line_numbers = tk.Text(query_text_frame, 
            width=4, 
            bg=self.colors['bg_medium'], 
            fg=self.colors['fg_secondary'],
            state='disabled', 
            wrap='none',
            font=('Consolas', 11),
            padx=5,
            pady=5,
            borderwidth=0,
            highlightthickness=0,
            spacing1=0,
            spacing2=0,
            spacing3=0
        )
        self.line_numbers.pack(side="left", fill="y")
        
        # Create a frame for the query text with border effect
        text_container = tk.Frame(query_text_frame, bg=self.colors['border'])
        text_container.pack(side="left", fill="both", expand=True)
        
        self.query_text = scrolledtext.ScrolledText(
            text_container, 
            wrap='none',
            font=('Consolas', 11),
            bg=self.colors['bg_medium'],
            fg=self.colors['fg_primary'],
            insertbackground=self.colors['fg_primary'],
            selectbackground=self.colors['accent'],
            selectforeground='#ffffff',
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=5,
            spacing1=0,
            spacing2=0,
            spacing3=0
        )
        self.query_text.pack(fill="both", expand=True)
        self.query_text.insert("1.0", "-- Enter your SQL query here\nSELECT * FROM your_table LIMIT 10;")
        self.query_text.config(yscrollcommand=self.on_text_scroll)
        self.query_text.vbar.config(command=self.on_scrollbar_scroll)
        
        # Bind events
        self.query_text.bind('<KeyRelease>', self.update_line_numbers)
        self.query_text.bind('<F5>', lambda e: self.execute_query())
        
        # Bind mouse wheel for scrolling sync
        self.query_text.bind("<MouseWheel>", self.on_mousewheel)  # Windows/Mac
        self.query_text.bind("<Button-4>", self.on_mousewheel)    # Linux scroll up
        self.query_text.bind("<Button-5>", self.on_mousewheel)    # Linux scroll down
        
        # Configure tags for syntax highlighting
        self.query_text.tag_configure('keyword', foreground='#569cd6', font=('Consolas', 11, 'bold'))
        self.query_text.tag_configure('string', foreground='#ce9178')
        self.query_text.tag_configure('comment', foreground='#6a9955', font=('Consolas', 11, 'italic'))
        self.query_text.tag_configure('number', foreground='#b5cea8')
        
        # Initialize line numbers
        self.update_line_numbers()
    
    def create_results_panel(self, parent):
        result_frame = ttk.LabelFrame(parent, text="Query Results", padding="10")
        result_frame.pack(fill="both", expand=True)
        
        # Results toolbar
        result_toolbar = ttk.Frame(result_frame)
        result_toolbar.pack(fill="x", pady=(0, 5))
        
        ttk.Button(result_toolbar, text="📄 Export CSV", command=self.export_csv).pack(side="left", padx=2)
        ttk.Button(result_toolbar, text="📋 Copy Selected", command=self.copy_selected).pack(side="left", padx=2)
        ttk.Button(result_toolbar, text="🗑 Clear Results", command=self.clear_results).pack(side="left", padx=2)
        
        self.row_count_label = ttk.Label(result_toolbar, text="Rows: 0")
        self.row_count_label.pack(side="right", padx=5)
        
        # Results treeview with scrollbars
        tree_frame = ttk.Frame(result_frame)
        tree_frame.pack(fill="both", expand=True)
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Treeview
        self.results_tree = ttk.Treeview(
            tree_frame,
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        self.results_tree.pack(fill="both", expand=True)
        
        # Configure treeview colors
        self.results_tree.tag_configure('oddrow', background=self.colors['bg_medium'])
        self.results_tree.tag_configure('evenrow', background=self.colors['bg_light'])
        
        v_scrollbar.config(command=self.results_tree.yview)
        h_scrollbar.config(command=self.results_tree.xview)
        
        # Bind double-click to show full cell value
        self.results_tree.bind('<Double-1>', self.show_cell_value)
    
    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.connection_status = tk.Label(status_frame, 
            text="⚫ Not Connected", 
            fg=self.colors['red'],
            bg=self.colors['bg_dark'],
            font=('Segoe UI', 9)
        )
        self.connection_status.pack(side="left")
        
        self.query_status = tk.Label(status_frame, 
            text="Ready",
            fg=self.colors['fg_secondary'],
            bg=self.colors['bg_dark'],
            font=('Segoe UI', 9)
        )
        self.query_status.pack(side="right")
        
        separator = ttk.Separator(status_frame, orient='horizontal')
        separator.pack(fill="x", pady=5)
    
    def update_line_numbers(self, event=None):
        lines = self.query_text.get("1.0", "end-1c").count('\n') + 1
        line_numbers_text = '\n'.join(str(i) for i in range(1, lines + 1))
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state='disabled')
        
        # Sync scroll position
        self.line_numbers.yview_moveto(self.query_text.yview()[0])
    
    def on_text_scroll(self, *args):
        """When text widget scrolls, sync line numbers and update scrollbar"""
        # Update scrollbar position
        self.query_text.vbar.set(*args)
        # Sync line numbers scroll
        self.line_numbers.yview_moveto(args[0])
    
    def on_scrollbar_scroll(self, *args):
        """When scrollbar is dragged, scroll both text widgets"""
        self.query_text.yview(*args)
        self.line_numbers.yview(*args)
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling for cross-platform compatibility"""
        if event.num == 4 or event.delta > 0:
            # Scroll up
            self.query_text.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            # Scroll down
            self.query_text.yview_scroll(1, "units")
        
        # Sync line numbers after mouse wheel scroll
        self.line_numbers.yview_moveto(self.query_text.yview()[0])
        return "break"
    
    def connect_database(self):
        try:
            self.connection = MySQLdb.connect(
                host=self.host_entry.get(),
                port=int(self.port_entry.get()),
                user=self.user_entry.get(),
                passwd=self.password_entry.get(),
                db=self.database_entry.get()
            )
            
            self.connection_status.config(text="🟢 Connected", fg=self.colors['green'])
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            self.query_status.config(text="Connected to database successfully")
            
            messagebox.showinfo("Success", "Connected to database successfully!")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect:\n{str(e)}")
            self.query_status.config(text="Connection failed")
    
    def disconnect_database(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            
        self.connection_status.config(text="⚫ Not Connected", fg=self.colors['red'])
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")
        self.query_status.config(text="Disconnected")
    
    def execute_query(self):
        if not self.connection:
            messagebox.showwarning("No Connection", "Please connect to a database first!")
            return
        
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Empty Query", "Please enter a SQL query!")
            return
        
        try:
            cursor = self.connection.cursor()
            
            # Handle multiple queries
            queries = [q.strip() for q in query.split(';') if q.strip()]
            
            # Clear previous results
            self.clear_results()
            
            for single_query in queries:
                cursor.execute(single_query)
                
                if cursor.description:  # SELECT query
                    # Configure columns
                    columns = [desc[0] for desc in cursor.description]
                    self.results_tree["columns"] = columns
                    
                    for col in columns:
                        self.results_tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
                        self.results_tree.column(col, width=120, minwidth=50)
                    
                    # Insert data with alternating row colors
                    rows = cursor.fetchall()
                    for i, row in enumerate(rows):
                        formatted_row = [str(val) if val is not None else 'NULL' for val in row]
                        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                        self.results_tree.insert("", "end", values=formatted_row, tags=(tag,))
                    
                    self.row_count_label.config(text=f"Rows: {len(rows)}")
                    self.query_status.config(text=f"Query executed: {len(rows)} rows returned")
                else:
                    # Non-SELECT query
                    self.connection.commit()
                    affected_rows = cursor.rowcount
                    self.query_status.config(text=f"Query executed: {affected_rows} rows affected")
                    messagebox.showinfo("Success", f"Query executed successfully!\n{affected_rows} rows affected.")
            
            cursor.close()
            
        except Exception as e:
            messagebox.showerror("Query Error", f"Query execution failed:\n{str(e)}")
            self.query_status.config(text="Query failed")
    
    def show_databases(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()]
                cursor.close()
                
                # Show in a popup
                db_list = "\n".join(databases)
                messagebox.showinfo("Databases", f"Available Databases:\n\n{db_list}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def show_tables(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                cursor.close()
                
                table_list = "\n".join(tables)
                messagebox.showinfo("Tables", f"Tables in Database:\n\n{table_list}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def export_csv(self):
        if not self.results_tree.get_children():
            messagebox.showwarning("No Data", "No results to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    
                    # Write headers
                    headers = [self.results_tree.heading(col)["text"] for col in self.results_tree["columns"]]
                    writer.writerow(headers)
                    
                    # Write data
                    for item in self.results_tree.get_children():
                        values = self.results_tree.item(item)["values"]
                        writer.writerow(values)
                
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
    
    def copy_selected(self):
        selected = self.results_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select rows to copy!")
            return
        
        # Copy to clipboard
        text_lines = []
        for item in selected:
            values = self.results_tree.item(item)["values"]
            text_lines.append("\t".join(str(v) for v in values))
        
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(text_lines))
        messagebox.showinfo("Copied", f"Copied {len(selected)} rows to clipboard")
    
    def show_cell_value(self, event):
        selection = self.results_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        column = self.results_tree.identify_column(event.x)
        col_index = int(column.replace('#', '')) - 1
        value = self.results_tree.item(item)["values"][col_index]
        
        # Show full value in a dark popup
        popup = tk.Toplevel(self.root)
        popup.title("Cell Value")
        popup.geometry("400x300")
        popup.configure(bg=self.colors['bg_dark'])
        
        text = scrolledtext.ScrolledText(popup, 
            wrap='word',
            bg=self.colors['bg_medium'],
            fg=self.colors['fg_primary'],
            insertbackground=self.colors['fg_primary'],
            font=('Consolas', 10)
        )
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", value)
        text.config(state='disabled')
    
    def sort_column(self, col):
        # Simple column sorting
        items = [(self.results_tree.set(item, col), item) for item in self.results_tree.get_children('')]
        items.sort()
        
        for index, (val, item) in enumerate(items):
            self.results_tree.move(item, '', index)
    
    def format_sql(self):
        # Basic SQL formatting
        query = self.query_text.get("1.0", tk.END)
        keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'ORDER BY', 'GROUP BY', 
                   'HAVING', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'LIMIT']
        
        for keyword in keywords:
            query = query.replace(f' {keyword} ', f'\n{keyword} ')
            query = query.replace(f'\n{keyword} ', f'\n{keyword}\n    ')
        
        self.query_text.delete("1.0", tk.END)
        self.query_text.insert("1.0", query)
        self.update_line_numbers()
    
    def load_sql_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'r') as file:
                self.query_text.delete("1.0", tk.END)
                self.query_text.insert("1.0", file.read())
            self.update_line_numbers()
    
    def save_sql_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".sql",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.query_text.get("1.0", tk.END))
            messagebox.showinfo("Saved", f"Query saved to {file_path}")
    
    def clear_query(self):
        self.query_text.delete("1.0", tk.END)
        self.update_line_numbers()
    
    def clear_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.row_count_label.config(text="Rows: 0")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopSQLTool(root)
    root.mainloop()