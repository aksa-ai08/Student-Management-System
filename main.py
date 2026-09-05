import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Matplotlib for embedded graph
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Database:
    def __init__(self, db_name="students_hub.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.seed_initial_data()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                dept TEXT NOT NULL,
                sem INTEGER,
                cgpa REAL,
                skills TEXT
            )
        ''')
        self.conn.commit()

    def seed_initial_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM students")
        if self.cursor.fetchone()[0] == 0:
            sample = [
                ("S001", "Hamza", "AI", 4, 3.92, "Machine Learning, Deep Learning, Python"),
                ("S002", "Babar", "SE", 4, 3.85, "Software Architecture, UI/UX, Agile"),
                ("S003", "Shadab", "IT", 3, 3.70, "Network Security, Ethical Hacking, IT Infrastructure"),
                ("S004", "Pat Cummins", "DS", 4, 3.65, "Data Analytics, Big Data, Statistics"),
                ("S005", "Shaheen", "AI", 2, 3.55, "Computer Vision, OpenCV, Python"),
                ("S006", "Rizwan", "IT", 3, 3.75, "Cloud Computing, DevOps, Linux"),
                ("S007", "Amir", "DS", 2, 3.40, "Database Management, SQL, Data Warehousing")
            ]
            self.cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)", sample)
            self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def add_student(self, s):
        try:
            self.cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)", 
                                (s['id'], s['name'], s['dept'], s['sem'], s['cgpa'], s['skills']))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_student(self, s, original_id):
        self.cursor.execute('''
            UPDATE students SET id=?, name=?, dept=?, sem=?, cgpa=?, skills=? WHERE id=?
        ''', (s['id'], s['name'], s['dept'], s['sem'], s['cgpa'], s['skills'], original_id))
        self.conn.commit()

    def delete_student(self, s_id):
        self.cursor.execute("SELECT * FROM students WHERE id=?", (s_id,))
        if self.cursor.fetchone():
            self.cursor.execute("DELETE FROM students WHERE id=?", (s_id,))
            self.conn.commit()
            return True
        return False

class BlueWhiteStudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management Hub — Professional Edition")
        self.root.geometry("1150x660")
        
        self.db = Database()
        self.current_update_id = None

        # Clean Professional Blue & White Color Palette
        self.palette = {
            "bg": "#f0f4f8",             # Soft light blue-gray background
            "panel": "#ffffff",          # Pure white cards
            "fg": "#1e293b",             # Deep slate text
            "secondary_fg": "#64748b",   # Muted gray-blue text
            "border": "#cbd5e1",         # Clean light border
            "primary": "#2563eb",        # Royal Blue accent
            "primary_hover": "#1d4ed8",  # Darker blue
            "header_bg": "#1e40af",      # Deep corporate blue header
            "header_fg": "#ffffff",      # White header text
            "tree_select": "#bfdbfe"     # Soft blue row selection
        }

        self.apply_theme()

    def apply_theme(self):
        p = self.palette
        self.root.config(bg=p["bg"])

        # --- Top Header Bar ---
        self.header_frame = tk.Frame(self.root, bg=p["header_bg"], height=55)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        self.header_frame.pack_propagate(False)

        self.title_lbl = tk.Label(self.header_frame, text="  Student Information & Analytics Hub", 
                                  font=("Segoe UI", 13, "bold"), bg=p["header_bg"], fg=p["header_fg"])
        self.title_lbl.pack(side=tk.LEFT, padx=10)

        # --- Main Layout Container ---
        self.main_container = tk.Frame(self.root, bg=p["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # --- Left Panel: Input & Control Form ---
        self.left_panel = tk.Frame(self.main_container, bg=p["panel"], bd=1, relief="solid")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.form_title = tk.Label(self.left_panel, text="Student Record Form", 
                                   font=("Segoe UI", 11, "bold"), bg=p["panel"], fg=p["fg"])
        self.form_title.pack(pady=12)

        self.fields_frame = tk.Frame(self.left_panel, bg=p["panel"])
        self.fields_frame.pack(padx=12, fill=tk.X)

        labels = ["ID", "Name", "Department", "Semester", "CGPA", "Skills (comma sep)"]
        self.entries = {}

        for text in labels:
            row_f = tk.Frame(self.fields_frame, bg=p["panel"])
            row_f.pack(fill=tk.X, pady=4)
            
            lbl = tk.Label(row_f, text=text, width=14, anchor="w", font=("Segoe UI", 9, "bold"), bg=p["panel"], fg=p["secondary_fg"])
            lbl.pack(side=tk.LEFT)
            ent = tk.Entry(row_f, font=("Segoe UI", 10), width=22, relief="solid", bd=1, bg="#ffffff", fg=p["fg"])
            ent.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            self.entries[text] = (lbl, ent, row_f)

        # Action Buttons Area
        self.btn_area = tk.Frame(self.left_panel, bg=p["panel"])
        self.btn_area.pack(padx=12, pady=12, fill=tk.X)

        b_common = {"font": ("Segoe UI", 9, "bold"), "relief": "flat", "pady": 5, "fg": "white"}

        self.b_add = tk.Button(self.btn_area, text="Add Record", command=self.add_student, bg="#2563eb", width=12, **b_common)
        self.b_add.grid(row=0, column=0, padx=3, pady=3)
        
        self.b_update = tk.Button(self.btn_area, text="Update Form", command=self.update_student_action, bg="#0284c7", width=12, **b_common)
        self.b_update.grid(row=0, column=1, padx=3, pady=3)
        
        self.b_delete = tk.Button(self.btn_area, text="Delete", command=self.delete_student_action, bg="#dc2626", width=12, **b_common)
        self.b_delete.grid(row=1, column=0, padx=3, pady=3)
        
        self.b_avg = tk.Button(self.btn_area, text="Avg CGPA", command=self.calc_avg_cgpa, bg="#0d9488", width=12, **b_common)
        self.b_avg.grid(row=1, column=1, padx=3, pady=3)

        self.b_topper = tk.Button(self.btn_area, text="View Top Performer", command=self.show_top_performer, bg="#1e40af", width=26, **b_common)
        self.b_topper.grid(row=2, column=0, columnspan=2, pady=6)

        # --- Right Panel: Notebook for Table & Live Graph Analytics ---
        self.right_panel = tk.Frame(self.main_container, bg=p["bg"])
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Directory Table & Live Search Bar
        self.tab_table = tk.Frame(self.notebook, bg=p["panel"])
        self.notebook.add(self.tab_table, text="  Directory & Search  ")

        search_bar_frame = tk.Frame(self.tab_table, bg=p["panel"])
        search_bar_frame.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(search_bar_frame, text="Live Search (Name/ID):", font=("Segoe UI", 9, "bold"), bg=p["panel"], fg=p["fg"]).pack(side=tk.LEFT, padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_table_live)
        self.search_ent = tk.Entry(search_bar_frame, textvariable=self.search_var, font=("Segoe UI", 10), width=30, relief="solid", bd=1)
        self.search_ent.pack(side=tk.LEFT)

        table_sub = tk.Frame(self.tab_table, bg=p["panel"])
        table_sub.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        columns = ("ID", "Name", "Dept", "Sem", "CGPA", "Skills")
        self.tree = ttk.Treeview(table_sub, columns=columns, show="headings", height=16)

        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=90, anchor=tk.W)
        self.tree.column("Skills", width=160)

        scrollbar = ttk.Scrollbar(table_sub, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Treeview Styling for Blue & White
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ffffff", foreground=p["fg"], rowheight=26, fieldbackground="#ffffff", font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=p["header_bg"], foreground="white", font=("Segoe UI", 9, "bold"))
        style.map('Treeview', background=[('selected', p["tree_select"])], foreground=[('selected', '#1e293b')])

        # Tab 2: Live Analytics Graph (Matplotlib)
        self.tab_graph = tk.Frame(self.notebook, bg=p["panel"])
        self.notebook.add(self.tab_graph, text="  Live Analytics Graph  ")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graph)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Footer ---
        self.footer_frame = tk.Frame(self.root, bg=p["header_bg"], height=26)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.footer_frame.pack_propagate(False)
        
        self.footer_lbl = tk.Label(self.footer_frame, text="Developed By aksa-ai08  |  SQLite Powered Blue-White Edition", font=("Segoe UI", 8, "italic"), bg=p["header_bg"], fg=p["header_fg"])
        self.footer_lbl.pack(pady=4)

        self.refresh_table()

    def refresh_table(self):
        records = self.db.get_all()
        self.populate_tree(records)
        self.refresh_graph()

    def populate_tree(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in records:
            self.tree.insert("", tk.END, values=r)

    def filter_table_live(self, *args):
        query = self.search_var.get().strip().lower()
        records = self.db.get_all()
        if not query:
            self.populate_tree(records)
            return
        
        filtered = [r for r in records if query in r[0].lower() or query in r[1].lower()]
        self.populate_tree(filtered)

    def refresh_graph(self):
        self.ax.clear()
        records = self.db.get_all()
        
        if not records:
            self.canvas.draw()
            return

        dept_counts = {}
        for r in records:
            d = r[2].upper()
            dept_counts[d] = dept_counts.get(d, 0) + 1

        depts = list(dept_counts.keys())
        counts = list(dept_counts.values())

        p = self.palette
        self.fig.patch.set_facecolor(p["panel"])
        self.ax.set_facecolor(p["panel"])

        self.ax.bar(depts, counts, color="#2563eb", width=0.5)
        self.ax.set_title("Department-wise Student Distribution", fontsize=10, fontweight="bold", color=p["fg"])
        self.ax.set_ylabel("Number of Students", fontsize=9, color=p["fg"])
        self.ax.tick_params(colors=p["fg"], labelsize=9)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(p["secondary_fg"])
        self.ax.spines['bottom'].set_color(p["secondary_fg"])

        self.fig.tight_layout()
        self.canvas.draw()

    def clear_form(self):
        for lbl, ent, row_f in self.entries.values():
            ent.delete(0, tk.END)
        self.current_update_id = None

    def add_student(self):
        try:
            s = {
                "id": self.entries["ID"][1].get().strip(),
                "name": self.entries["Name"][1].get().strip(),
                "dept": self.entries["Department"][1].get().strip(),
                "sem": int(self.entries["Semester"][1].get().strip()),
                "cgpa": float(self.entries["CGPA"][1].get().strip()),
                "skills": self.entries["Skills (comma sep)"][1].get().strip()
            }
            if not s["id"] or not s["name"]:
                messagebox.showerror("Error", "ID and Name cannot be empty.")
                return

            success = self.db.add_student(s)
            if success:
                messagebox.showinfo("Success", "Student record successfully saved to database.")
                self.clear_form()
                self.refresh_table()
            else:
                messagebox.showerror("Error", "A student with this ID already exists.")
        except ValueError:
            messagebox.showerror("Error", "Please provide valid numeric entries for Semester and CGPA.")

    def update_student_action(self):
        if not self.current_update_id:
            s_id = simpledialog.askstring("Update Record", "Enter Student ID to modify:")
            if not s_id: return
            
            records = self.db.get_all()
            target = next((r for r in records if r[0] == s_id), None)
            
            if target:
                self.current_update_id = s_id
                self.clear_form()
                self.current_update_id = s_id
                
                fields_keys = ["ID", "Name", "Department", "Semester", "CGPA", "Skills (comma sep)"]
                for i, key in enumerate(fields_keys):
                    self.entries[key][1].insert(0, str(target[i]))
                messagebox.showinfo("Loaded", "Record loaded into form. Make changes and click 'Update Form' again.")
            else:
                messagebox.showerror("Not Found", "Student ID not found.")
        else:
            try:
                s = {
                    "id": self.entries["ID"][1].get().strip(),
                    "name": self.entries["Name"][1].get().strip(),
                    "dept": self.entries["Department"][1].get().strip(),
                    "sem": int(self.entries["Semester"][1].get().strip()),
                    "cgpa": float(self.entries["CGPA"][1].get().strip()),
                    "skills": self.entries["Skills (comma sep)"][1].get().strip()
                }
                self.db.update_student(s, self.current_update_id)
                messagebox.showinfo("Success", "Student record updated successfully.")
                self.clear_form()
                self.refresh_table()
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric format in Semester or CGPA.")

    def delete_student_action(self):
        s_id = simpledialog.askstring("Delete Record", "Enter Student ID to delete:")
        if not s_id: return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete student ID {s_id}?"):
            if self.db.delete_student(s_id):
                messagebox.showinfo("Success", "Record deleted from database.")
                self.clear_form()
                self.refresh_table()
            else:
                messagebox.showerror("Not Found", "Student ID not found.")

    def calc_avg_cgpa(self):
        records = self.db.get_all()
        if not records:
            messagebox.showwarning("Warning", "No records found.")
            return
        avg = sum(r[4] for r in records) / len(records)
        messagebox.showinfo("Average CGPA", f"Overall Institute Average CGPA: {avg:.2f}")

    def show_top_performer(self):
        records = self.db.get_all()
        if not records:
            messagebox.showwarning("Warning", "No records found.")
            return
        topper = max(records, key=lambda r: r[4])
        messagebox.showinfo("Top Performer", f"🌟 Top Performer:\n\nID: {topper[0]}\nName: {topper[1]}\nDepartment: {topper[2]}\nCGPA: {topper[4]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueWhiteStudentApp(root)
    root.mainloop()