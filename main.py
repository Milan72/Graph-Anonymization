import os
import importlib.util
import tkinter as tk
from tkinter import filedialog, messagebox
import builtins
try:
    import matplotlib.pyplot as plt
    plt.ion()
except Exception:
    # matplotlib may not be present in some environments; scripts will handle their own imports
    pass

SCRIPTS_DIR = "scripts"

def load_scripts():
    """Load scripts grouped by category from `scripts/` subfolders.

    Expected subfolders (case-insensitive):
      - anonymization -> Anonymization
      - utils or utility -> Utilities
      - helpers or helper -> Helpers

    Returns a dict: { 'Anonymization': {name: path, ...}, 'Utilities': {...}, 'Helpers': {...} }
    """
    categories = {'Anonymization': {}, 'Utilities': {}, 'Helpers': {}}

    # scan top-level subdirectories
    for entry in os.listdir(SCRIPTS_DIR):
        full = os.path.join(SCRIPTS_DIR, entry)
        if not os.path.isdir(full):
            continue

        key = None
        en = entry.lower()
        if 'anonym' in en:
            key = 'Anonymization'
        elif 'util' in en or 'utility' in en:
            key = 'Utilities'
        elif 'help' in en:
            key = 'Helpers'
        else:
            # skip unknown folders
            continue

        for filename in os.listdir(full):
            if filename.endswith('.py'):
                name = os.path.splitext(filename)[0]
                categories[key][name] = os.path.join(full, filename)

    return categories

def import_script(script_path):
    """Import a script file dynamically"""
    spec = importlib.util.spec_from_file_location("dynamic_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_selected_script():
    # Collect selected scripts from the three category listboxes.
    selected = []

    # Anonymization first
    a_inds = anonym_listbox.curselection()
    for i in a_inds:
        selected.append(('Anonymization', anonym_listbox.get(i)))

    # Utilities next
    u_inds = utils_listbox.curselection()
    for i in u_inds:
        selected.append(('Utilities', utils_listbox.get(i)))

    # Helpers last
    h_inds = helpers_listbox.curselection()
    for i in h_inds:
        selected.append(('Helpers', helpers_listbox.get(i)))

    if not selected:
        messagebox.showwarning("Warning", "Please choose one or more scripts first.")
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

    # Run selected scripts sequentially, piping output of one as input to the next
    current_file = file_path
    for category, script_name in selected:
        script_path = scripts.get(category, {}).get(script_name)
        try:
            module = import_script(script_path)

            if hasattr(module, "run"):
                # Capture script output by replacing print() with ui_print()
                old_print = builtins.print
                def custom_print(*args, **kwargs):
                    message = " ".join(str(a) for a in args)
                    ui_print(message)

                builtins.print = custom_print
                try:
                    result = module.run(current_file, k_value)
                finally:
                    builtins.print = old_print  # restore after script finishes

                # If the script returns a path, use it as the input for the next script
                if isinstance(result, str) and os.path.exists(result):
                    current_file = result
                else:
                    # If no path returned, keep using current_file (scripts may overwrite files)
                    pass
            else:
                messagebox.showerror("Error", f"{script_name}.py does not have a compatible run() function.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run {script_name}:\n{e}")
            return

    messagebox.showinfo(
        "Success",
        f"Ran {len(selected)} script(s) with k={k_value} on:\n{os.path.basename(file_path)}\nFinal output: {os.path.basename(current_file)}"
    )

def ui_print(text):
    console.insert(tk.END, text + "\n")
    console.see(tk.END)  # auto-scroll

def clear_console():
    try:
        console.delete('1.0', tk.END)
    except Exception:
        pass

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

# Script selection (grouped by category)
scripts_frame = tk.Frame(content, bg="#f8f9fa")
scripts_frame.pack(pady=5, fill='x')

anonym_names = sorted(scripts.get('Anonymization', {}).keys())
utils_names = sorted(scripts.get('Utilities', {}).keys())
helpers_names = sorted(scripts.get('Helpers', {}).keys())

# Anonymization listbox
anonym_frame = tk.Frame(scripts_frame, bg="#f8f9fa")
anonym_frame.pack(side='left', padx=10)
anonym_label = tk.Label(anonym_frame, text="Anonymization", font=("Arial", 11, "bold"), bg="#f8f9fa")
anonym_label.pack()
anonym_listbox = tk.Listbox(anonym_frame, selectmode=tk.MULTIPLE, height=6, exportselection=False)
for name in anonym_names:
    anonym_listbox.insert(tk.END, name)
anonym_listbox.config(font=("Arial", 11), width=30)
anonym_listbox.pack()

# Utilities listbox
utils_frame = tk.Frame(scripts_frame, bg="#f8f9fa")
utils_frame.pack(side='left', padx=10)
utils_label = tk.Label(utils_frame, text="Utilities", font=("Arial", 11, "bold"), bg="#f8f9fa")
utils_label.pack()
utils_listbox = tk.Listbox(utils_frame, selectmode=tk.MULTIPLE, height=6, exportselection=False)
for name in utils_names:
    utils_listbox.insert(tk.END, name)
utils_listbox.config(font=("Arial", 11), width=30)
utils_listbox.pack()

# Helpers listbox
helpers_frame = tk.Frame(scripts_frame, bg="#f8f9fa")
helpers_frame.pack(side='left', padx=10)
helpers_label = tk.Label(helpers_frame, text="Helpers", font=("Arial", 11, "bold"), bg="#f8f9fa")
helpers_label.pack()
helpers_listbox = tk.Listbox(helpers_frame, selectmode=tk.MULTIPLE, height=6, exportselection=False)
for name in helpers_names:
    helpers_listbox.insert(tk.END, name)
helpers_listbox.config(font=("Arial", 11), width=30)
helpers_listbox.pack()
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
    bg="#007bff", fg="black",
    activebackground="#0056b3",
    relief="flat",
    width=20, height=2
)
run_button.pack(pady=20)

# (single output console is defined below)

footer = tk.Label(
    root,
    text="Scripts auto-loaded from /scripts folder",
    font=("Arial", 9),
    bg="#f8f9fa", fg="#6c757d"
)
footer.pack(side="bottom", pady=10)

# --- Output console ---
console_frame = tk.Frame(root, bg="#f8f9fa")
console_frame.pack(fill='x', padx=10)

console_label = tk.Label(console_frame, text="Output:", font=("Arial", 11), bg="#f8f9fa")
console_label.pack(side='left', pady=(5, 0))

clear_button = tk.Button(console_frame, text="Clear", command=clear_console, font=("Arial", 10), bg="#dc3545", fg="black", relief="flat")
clear_button.pack(side='right', pady=(5,0))

console = tk.Text(root, height=8, font=("Courier", 10), bg="#eeeeee")
console.pack(fill="both", expand=True, padx=10, pady=10)


root.mainloop()
