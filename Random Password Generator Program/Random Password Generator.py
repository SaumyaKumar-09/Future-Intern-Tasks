import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate the password
def generate_password():
    try:
        length = int(entry_length.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for length!")
        return
    
    include_uppercase = var_uppercase.get()
    include_lowercase = var_lowercase.get()
    include_numbers = var_numbers.get()
    include_specials = var_specials.get()

    # Create the character pool based on conditions
    character_pool = ""
    if include_uppercase:
        character_pool += string.ascii_uppercase
    if include_lowercase:
        character_pool += string.ascii_lowercase
    if include_numbers:
        character_pool += string.digits
    if include_specials:
        character_pool += string.punctuation

    # Ensure at least one type of character is selected
    if not character_pool:
        messagebox.showerror("Error", "Please select at least one character type!")
        return

    # Generate the password
    password = "".join(random.choices(character_pool, k=length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

# Function to copy password to clipboard
def copy_password():
    password = entry_password.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Function to dynamically resize elements based on window size
def resize(event):
    global resize_after_id
    if resize_after_id:
        root.after_cancel(resize_after_id)
    resize_after_id = root.after(300, adjust_layout)  # Call adjust_layout after 300ms

def adjust_layout():
    w, h = root.winfo_width(), root.winfo_height()
    scale_factor_w = w / 600  # Default window width
    scale_factor_h = h / 400  # Default window height

    # Adjust the font size and element size dynamically
    label_length.config(font=("Arial", int(14 * scale_factor_w)))
    entry_length.config(font=("Arial", int(12 * scale_factor_w)))
    label_password.config(font=("Arial", int(14 * scale_factor_w)))
    entry_password.config(font=("Arial", int(12 * scale_factor_w)))
    button_generate.config(font=("Arial", int(14 * scale_factor_w)))
    button_copy.config(font=("Arial", int(16 * scale_factor_w)))
    for chk in checkboxes:
        chk.config(font=("Arial", int(12 * scale_factor_w)))

# Create the GUI window
root = tk.Tk()
root.title("Random Password Generator")

# Set default screen size
default_width = 600
default_height = 400
root.geometry(f"{default_width}x{default_height}")
root.configure(bg="#F2F3F4")  # Light Gray background

# Password length input
label_length = tk.Label(root, text="Password Length:", bg="#F2F3F4", fg="#1B4F72", font=("Arial", 14))
label_length.pack(pady=5)
entry_length = tk.Entry(root, width=15, font=("Arial", 12), bg="#D6EAF8")
entry_length.pack(pady=5)

# Checkboxes for conditions
checkboxes = []
var_uppercase = tk.BooleanVar()
chk_upper = tk.Checkbutton(root, text="Include Uppercase Letters", variable=var_uppercase, bg="#F2F3F4", fg="#2874A6")
chk_upper.pack(pady=5)
checkboxes.append(chk_upper)

var_lowercase = tk.BooleanVar()
chk_lower = tk.Checkbutton(root, text="Include Lowercase Letters", variable=var_lowercase, bg="#F2F3F4", fg="#2874A6")
chk_lower.pack(pady=5)
checkboxes.append(chk_lower)

var_numbers = tk.BooleanVar()
chk_numbers = tk.Checkbutton(root, text="Include Numbers", variable=var_numbers, bg="#F2F3F4", fg="#2874A6")
chk_numbers.pack(pady=5)
checkboxes.append(chk_numbers)

var_specials = tk.BooleanVar()
chk_specials = tk.Checkbutton(root, text="Include Special Characters", variable=var_specials, bg="#F2F3F4", fg="#2874A6")
chk_specials.pack(pady=5)
checkboxes.append(chk_specials)

# Entry to display the generated password with a copy button next to it
frame_password = tk.Frame(root, bg="#F2F3F4")
frame_password.pack(pady=15)
label_password = tk.Label(frame_password, text="Generated Password:", bg="#F2F3F4", fg="#1B4F72", font=("Arial", 14))
label_password.grid(row=0, column=0, padx=5)
entry_password = tk.Entry(frame_password, width=30, font=("Arial", 12), bg="#D6EAF8")
entry_password.grid(row=0, column=1, padx=5)

# Button to copy the generated password (using symbol)
button_copy = tk.Button(frame_password, text="📋", command=copy_password, bg="#C0392B", fg="white", font=("Arial", 16))
button_copy.grid(row=0, column=2, padx=5)

# Button to generate the password (now relocated)
button_generate = tk.Button(root, text="Generate Password", command=generate_password, bg="#117864", fg="white", font=("Arial", 14))
button_generate.pack(side=tk.BOTTOM, pady=15)

# Global resize_after_id to handle debouncing
resize_after_id = None

# Bind the resize event to dynamically adjust element sizes
root.bind("<Configure>", resize)

# Run the GUI loop
root.mainloop()