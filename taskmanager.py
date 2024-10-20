import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime


class Task:
    def __init__(self, name, priority, due_date, status="Pending"):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.status = status


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.tasks = []

        self.task_name_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Task Name Label and Entry
        tk.Label(self.root, text="Task Name:").grid(row=0, column=0, sticky="w")
        task_name_entry = tk.Entry(self.root, textvariable=self.task_name_var)
        task_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Priority Label and Dropdown
        tk.Label(self.root, text="Priority:").grid(row=1, column=0, sticky="w")
        priority_values = ["Low", "Medium", "High"]
        priority_dropdown = ttk.Combobox(self.root, textvariable=self.priority_var, values=priority_values)
        priority_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Due Date Label and Calendar
        tk.Label(self.root, text="Due Date:").grid(row=2, column=0, sticky="w")
        due_date_entry = DateEntry(self.root, textvariable=self.due_date_var, date_pattern="yyyy-mm-dd")
        due_date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Add Task Button
        add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_task_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Task Report Button
        task_report_button = tk.Button(self.root, text="Report Task", command=self.open_task_report)
        task_report_button.grid(row=6, column=0, columnspan=4, padx=10, pady=5)

        # Update Status Button
        update_status_button = tk.Button(self.root, text="Update Status", command=self.update_status)
        update_status_button.grid(row=7, column=0, columnspan=4, padx=10, pady=5)

        # Task List Treeview
        self.task_list_treeview = ttk.Treeview(self.root, columns=("Priority", "Due Date", "Status"))
        self.task_list_treeview.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.task_list_treeview.heading("#0", text="Task Name")
        self.task_list_treeview.heading("Priority", text="Priority")
        self.task_list_treeview.heading("Due Date", text="Due Date")
        self.task_list_treeview.heading("Status", text="Status")

        # Delete Task Button
        delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_task_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        # Clear Task Button
        clear_task_button = tk.Button(self.root, text="Clear Task", command=self.clear_task)
        clear_task_button.grid(row=5, column=1, padx=10, pady=5, sticky="e")

    def open_task_report(self):
        task_report_window = tk.Toplevel(self.root)
        task_report_window.title("Task Report")

        # Task List Treeview in the new window
        task_list_treeview = ttk.Treeview(task_report_window, columns=("Priority", "Due Date", "Status"))
        task_list_treeview.grid(row=0, column=0, columnspan=3, padx=10, pady=5)
        task_list_treeview.heading("#0", text="Task Name")
        task_list_treeview.heading("Priority", text="Priority")
        task_list_treeview.heading("Due Date", text="Due Date")
        task_list_treeview.heading("Status", text="Status")

        # Populate the Treeview with tasks
        for task in self.tasks:
            task_list_treeview.insert("", tk.END, text=task.name, values=(task.priority, task.due_date, task.status))

    def update_status(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            task_name = self.task_list_treeview.item(selected_item)["text"]
            for task in self.tasks:
                if task.name == task_name:
                    new_status = messagebox.askquestion("Update Status", f"Update status for '{task.name}' to Completed?")
                    if new_status == "yes":
                        task.status = "Completed"
                        self.update_task_list_treeview()
                    break

    def update_task_list_treeview(self):
        # Clear existing items in Treeview
        for item in self.task_list_treeview.get_children():
            self.task_list_treeview.delete(item)

        # Populate the Treeview with updated tasks
        for task in self.tasks:
            self.task_list_treeview.insert("", tk.END, text=task.name, values=(task.priority, task.due_date, task.status))

    def add_task(self):
        name = self.task_name_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()

        if name and priority and due_date:
            task = Task(name, priority, due_date)
            self.tasks.append(task)

            self.task_list_treeview.insert("", tk.END, text=task.name, values=(task.priority, task.due_date, task.status))

            self.task_name_var.set("")
            self.priority_var.set("")
            self.due_date_var.set("")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_task(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            task_name = self.task_list_treeview.item(selected_item)["text"]
            for task in self.tasks:
                if task.name == task_name:
                    self.tasks.remove(task)
                    self.task_list_treeview.delete(selected_item)
                    break

    def clear_task(self):
        self.task_name_var.set("")
        self.priority_var.set("")
        self.due_date_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
