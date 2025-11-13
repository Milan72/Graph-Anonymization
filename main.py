import os
import importlib.util
import tkinter as tk
from tkinter import filedialog, messagebox

SCRIPTS_DIR = "scripts"

def load_scripts():
    """Dynamically load all .py files in /scripts"""
    scripts = {}
    for filename in os.listdir(SCRIPTS_DIR):
        if filename.endswith(".py"):
            script_name = os.path.splitext(filename)[0]
            scripts[script_name] = os.path.join(SCRIPTS_DIR, filename)
    return scripts

def import_script(script_path):
    """Import a script file dynamically"""
    spec = importlib.util.spec_from_file_location("dynamic_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_selected_script():
    selected_script = script_var.get()
    if selected_script == "Select script...":
        messagebox.showwarning("Warning", "Please choose a script first.")
        return

    # Read k value from entry
    try:
        k_value = int(k_entry.get())
    except ValueError:
        messagebox.showerror("Error", "k must be an integer.")
        return

    # Ask user for file
    file_path = filedialog.askopenfilename(title="Select a file")
    if not file_path:
        return

    # Run script
    script_path = scripts[selected_script]
    try:
        module = import_script(script_path)

        if hasattr(module, "run"):
            module.run(file_path, k_value)
            messagebox.showinfo(
                "Success",
                f"Ran '{selected_script}' with k={k_value} on:\n{os.path.basename(file_path)}"
            )
        else:
            messagebox.showerror("Error", f"{selected_script}.py does not have a compatible run() function.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {selected_script}:\n{e}")


# --- GUI setup ---
root = tk.Tk()
root.title("NetGUC")
root.resizable(True, True)
root.configure(bg="#f8f9fa")

# Load all scripts at startup
scripts = load_scripts()

# --- Title bar ---
title_label = tk.Label(
    root, text="NetGUC",
    font=("Helvetica", 18, "bold"),
    bg="#343a40", fg="white", pady=15
)
title_label.pack(fill="x")

# --- Content ---
content = tk.Frame(root, bg="#f8f9fa")
content.pack(expand=True, fill="both", pady=10)

desc_label = tk.Label(
    content,
    text="Choose a script then select a file:",
    font=("Arial", 12),
    bg="#f8f9fa"
)
desc_label.pack(pady=(20, 10))

# Dropdown for scripts
script_var = tk.StringVar(value="Select script...")
dropdown = tk.OptionMenu(content, script_var, *scripts.keys())
dropdown.config(font=("Arial", 11), width=18)
dropdown.pack(pady=5)
# Entry for k value
k_label = tk.Label(
    content,
    text="Enter k value:",
    font=("Arial", 11),
    bg="#f8f9fa"
)
k_label.pack(pady=(10,0))

k_entry = tk.Entry(content, font=("Arial", 12), width=10)
k_entry.insert(0, "10")  # default value
k_entry.pack(pady=(0,10))


run_button = tk.Button(
    content,
    text="Choose File and Run",
    command=run_selected_script,
    font=("Arial", 12, "bold"),
    bg="#007bff", fg="white",
    activebackground="#0056b3",
    relief="flat",
    width=20, height=2
)
run_button.pack(pady=20)

footer = tk.Label(
    root,
    text="Scripts auto-loaded from /scripts folder",
    font=("Arial", 9),
    bg="#f8f9fa", fg="#6c757d"
)
footer.pack(side="bottom", pady=10)

root.mainloop()
