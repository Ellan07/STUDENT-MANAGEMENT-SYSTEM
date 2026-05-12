# =========================================================
# MODERN STUDENT PORTAL SYSTEM
# Fully Updated Version
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox
import os

# =========================================================
# WINDOW
# =========================================================

root = tk.Tk()
root.title("Student Portal")
root.geometry("1400x780")
root.config(bg="#0d0d17")
root.resizable(False, False)

# =========================================================
# COLORS
# =========================================================

BG = "#0d0d17"
SIDEBAR = "#131320"

CARD = "#8B5CF6"
CARD_LIGHT = "#9F73FF"

WHITE = "#FFFFFF"
TEXT = "#D6D6E7"

ENTRY_BG = "#1D1D2E"
ENTRY_BORDER = "#343454"

BTN = "#9B6DFF"
BTN_HOVER = "#B388FF"

TABLE_BG = "#181827"

FILE_NAME = "students.txt"

# =========================================================
# FILE HANDLING
# =========================================================

def read_records():

    records = []

    if not os.path.exists(FILE_NAME):
        return records

    try:
        with open(FILE_NAME, "r") as file:

            for line in file:

                data = line.strip().split("|")

                if len(data) == 4:
                    records.append(data)

    except Exception as e:
        messagebox.showerror("Error", f"{e}")

    return records


def write_records(records):

    try:
        with open(FILE_NAME, "w") as file:

            for record in records:
                file.write("|".join(record) + "\n")

    except Exception as e:
        messagebox.showerror("Error", f"{e}")


# =========================================================
# HOVER EFFECTS
# =========================================================

def hover_on(e):
    e.widget["background"] = BTN_HOVER


def hover_off(e):
    e.widget["background"] = BTN


# =========================================================
# CLEAR INPUTS
# =========================================================

def clear_fields():

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)


# =========================================================
# DISPLAY RECORDS
# =========================================================

def display_records():

    tree.delete(*tree.get_children())

    records = read_records()

    for record in records:
        tree.insert("", tk.END, values=record)


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    grade = grade_entry.get().strip()

    if not student_id or not name or not age or not grade:
        status_label.config(text="Fill all fields.")
        return

    try:
        int(age)
        float(grade)

    except:
        messagebox.showerror(
            "Invalid Input",
            "Age must be integer.\nGrade must be numeric."
        )
        return

    records = read_records()

    for record in records:

        if record[0] == student_id:
            messagebox.showerror(
                "Duplicate ID",
                "Student ID already exists."
            )
            return

    records.append([student_id, name, age, grade])

    write_records(records)

    display_records()
    clear_fields()

    status_label.config(text="Student added successfully.")


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    keyword = search_entry.get().strip().lower()

    tree.delete(*tree.get_children())

    records = read_records()

    found = False

    for record in records:

        if keyword in record[0].lower() or keyword in record[1].lower():

            tree.insert("", tk.END, values=record)
            found = True

    if found:
        status_label.config(text="Search completed.")
    else:
        status_label.config(text="No matching student found.")


# =========================================================
# SELECT RECORD
# =========================================================

def select_record(event):

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    clear_fields()

    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    grade_entry.insert(0, values[3])


# =========================================================
# UPDATE STUDENT
# =========================================================

def update_student():

    student_id = id_entry.get().strip()

    records = read_records()

    updated = False

    for record in records:

        if record[0] == student_id:

            record[1] = name_entry.get().strip()
            record[2] = age_entry.get().strip()
            record[3] = grade_entry.get().strip()

            updated = True

    if updated:

        write_records(records)

        display_records()
        clear_fields()

        status_label.config(text="Student updated successfully.")

    else:
        messagebox.showerror("Error", "Student not found.")


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student():

    student_id = id_entry.get().strip()

    records = read_records()

    new_records = []

    deleted = False

    for record in records:

        if record[0] != student_id:
            new_records.append(record)

        else:
            deleted = True

    if deleted:

        write_records(new_records)

        display_records()
        clear_fields()

        status_label.config(text="Student deleted successfully.")

    else:
        messagebox.showerror("Error", "Student not found.")


# =========================================================
# COMPUTE AVERAGE
# =========================================================

def compute_average():

    records = read_records()

    if not records:
        messagebox.showinfo("Average", "No records found.")
        return

    total = 0

    for record in records:
        total += float(record[3])

    average = total / len(records)

    messagebox.showinfo(
        "Grade Average",
        f"Average Grade: {average:.2f}"
    )


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=340
)

sidebar.pack(side="left", fill="y")

# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    sidebar,
    text="Student\nPortal",
    bg=SIDEBAR,
    fg=WHITE,
    font=("Segoe UI", 34, "bold"),
    justify="left"
)

title.pack(anchor="w", padx=40, pady=(55, 10))

subtitle = tk.Label(
    sidebar,
    text="Modern Student Record System",
    bg=SIDEBAR,
    fg=TEXT,
    font=("Segoe UI", 12)
)

subtitle.pack(anchor="w", padx=42)

# =========================================================
# FORM FRAME
# =========================================================

form_frame = tk.Frame(
    sidebar,
    bg=SIDEBAR
)

form_frame.pack(padx=40, pady=40, fill="x")

# =========================================================
# LABEL STYLE
# =========================================================

label_style = {
    "bg": SIDEBAR,
    "fg": WHITE,
    "font": ("Segoe UI", 10)
}

# =========================================================
# ENTRY FUNCTION
# =========================================================

def create_entry(parent):

    entry = tk.Entry(
        parent,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Segoe UI", 11),
        bd=1,
        highlightthickness=1,
        highlightbackground=ENTRY_BORDER,
        highlightcolor=CARD
    )

    return entry


# =========================================================
# INPUT FIELDS
# =========================================================

tk.Label(form_frame, text="Student ID", **label_style).pack(anchor="w")

id_entry = create_entry(form_frame)
id_entry.pack(fill="x", ipady=12, pady=(6, 18))

tk.Label(form_frame, text="Student Name", **label_style).pack(anchor="w")

name_entry = create_entry(form_frame)
name_entry.pack(fill="x", ipady=12, pady=(6, 18))

tk.Label(form_frame, text="Student Age", **label_style).pack(anchor="w")

age_entry = create_entry(form_frame)
age_entry.pack(fill="x", ipady=12, pady=(6, 18))

tk.Label(form_frame, text="Student Grade", **label_style).pack(anchor="w")

grade_entry = create_entry(form_frame)
grade_entry.pack(fill="x", ipady=12, pady=(6, 25))

# =========================================================
# BUTTON FUNCTION
# =========================================================

def create_button(parent, text, command):

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=BTN,
        fg=WHITE,
        activebackground=BTN_HOVER,
        activeforeground=WHITE,
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        height=1,
        pady=13
    )

    btn.bind("<Enter>", hover_on)
    btn.bind("<Leave>", hover_off)

    return btn


# =========================================================
# BUTTON CONTAINER
# =========================================================

button_container = tk.Frame(
    form_frame,
    bg=SIDEBAR
)

button_container.pack(fill="x")

# =========================================================
# BUTTONS
# =========================================================

add_btn = create_button(
    button_container,
    "Add Student",
    add_student
)

add_btn.pack(fill="x", pady=6)

update_btn = create_button(
    button_container,
    "Update Student",
    update_student
)

update_btn.pack(fill="x", pady=6)

delete_btn = create_button(
    button_container,
    "Delete Student",
    delete_student
)

delete_btn.pack(fill="x", pady=6)

average_btn = create_button(
    button_container,
    "Compute Average",
    compute_average
)

average_btn.pack(fill="x", pady=6)

# =========================================================
# STATUS LABEL
# =========================================================

status_label = tk.Label(
    sidebar,
    text="System Ready",
    bg=SIDEBAR,
    fg="#7dffae",
    font=("Segoe UI", 10)
)

status_label.pack(side="bottom", pady=25)

# =========================================================
# MAIN AREA
# =========================================================

main_area = tk.Frame(
    root,
    bg=BG
)

main_area.pack(side="right", fill="both", expand=True)

# =========================================================
# TOP CARD
# =========================================================

top_card = tk.Frame(
    main_area,
    bg=CARD,
    height=210
)

top_card.pack(fill="x", padx=35, pady=30)

# =========================================================
# WELCOME TEXT
# =========================================================

welcome = tk.Label(
    top_card,
    text="Welcome to\nStudent Portal",
    bg=CARD,
    fg=WHITE,
    font=("Segoe UI", 31, "bold"),
    justify="left"
)

welcome.place(x=45, y=35)

desc = tk.Label(
    top_card,
    text="Manage student records with a modern interface",
    bg=CARD,
    fg="#f5efff",
    font=("Segoe UI", 12)
)

desc.place(x=50, y=145)

# =========================================================
# SEARCH SECTION
# =========================================================

search_frame = tk.Frame(
    main_area,
    bg=BG
)

search_frame.pack(fill="x", padx=35)

search_entry = tk.Entry(
    search_frame,
    bg=ENTRY_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    font=("Segoe UI", 11),
    bd=0
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=14
)

search_btn = tk.Button(
    search_frame,
    text="Search",
    command=search_student,
    bg=BTN,
    fg=WHITE,
    relief="flat",
    borderwidth=0,
    font=("Segoe UI", 10, "bold"),
    padx=28,
    pady=13,
    cursor="hand2"
)

search_btn.pack(side="left", padx=12)

search_btn.bind("<Enter>", hover_on)
search_btn.bind("<Leave>", hover_off)

# =========================================================
# TABLE FRAME
# =========================================================

table_frame = tk.Frame(
    main_area,
    bg=BG
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=25
)

# =========================================================
# TREEVIEW STYLE
# =========================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=TABLE_BG,
    foreground=WHITE,
    fieldbackground=TABLE_BG,
    rowheight=42,
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#25253a",
    foreground=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", CARD)]
)

# =========================================================
# TREEVIEW
# =========================================================

tree = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Age", "Grade"),
    show="headings"
)

tree.heading("ID", text="Student ID")
tree.heading("Name", text="Student Name")
tree.heading("Age", text="Age")
tree.heading("Grade", text="Grade")

tree.column("ID", width=160)
tree.column("Name", width=350)
tree.column("Age", width=120)
tree.column("Grade", width=120)

tree.pack(fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", select_record)

# =========================================================
# INITIAL DISPLAY
# =========================================================

display_records()

# =========================================================
# START APP
# =========================================================

root.mainloop()
