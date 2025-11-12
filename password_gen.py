import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 

AMBIGUOUS_CHARS = 'l1Io0O'

def generate_secure_password(length, use_lower, use_upper, use_numbers, use_symbols, exclude_ambiguous):
    all_chars = ""
    required_chars = []
    
    if use_lower:
        chars = string.ascii_lowercase
        all_chars += chars
        required_chars.append(random.choice(chars))
    if use_upper:
        chars = string.ascii_uppercase
        all_chars += chars
        required_chars.append(random.choice(chars))
    if use_numbers:
        chars = string.digits
        all_chars += chars
        required_chars.append(random.choice(chars))
    if use_symbols:
        chars = string.punctuation
        all_chars += chars
        required_chars.append(random.choice(chars))

    if exclude_ambiguous:
        for char in AMBIGUOUS_CHARS:
            all_chars = all_chars.replace(char, '')
        
        temp_required = []
        for char in required_chars:
            if char not in AMBIGUOUS_CHARS:
                temp_required.append(char)
        required_chars = temp_required
        
    if not all_chars or not required_chars:
        return "Error: Select at least one character type that is not excluded.", "Error"

    if length < len(required_chars):
        return "Error: Length too short for selected complexity.", "Error"

    remaining_length = length - len(required_chars)
    password_list = required_chars + [random.choice(all_chars) for _ in range(remaining_length)]
    random.shuffle(password_list)
    
    return "".join(password_list), "Success"

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Password Generator 🔐")
        
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))

        main_frame = ttk.Frame(master, padding="15 15 15 15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        settings_frame = ttk.LabelFrame(main_frame, text="Generation Settings", padding="10 10 10 10")
        settings_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
        ttk.Label(settings_frame, text="Password Length:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.length_var = tk.IntVar(value=16) 
        self.length_spinbox = ttk.Spinbox(settings_frame, from_=8, to=32, textvariable=self.length_var, width=5)
        self.length_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        complexity_frame = ttk.LabelFrame(settings_frame, text="Character Types (Complexity Rules)", padding="10")
        complexity_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')
        
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(complexity_frame, text="Lowercase (a-z)", variable=self.lower_var).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Checkbutton(complexity_frame, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        ttk.Checkbutton(complexity_frame, text="Numbers (0-9)", variable=self.number_var).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Checkbutton(complexity_frame, text="Symbols (!@#$)", variable=self.symbol_var).grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        self.ambiguous_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text=f"Exclude Ambiguous Chars ({AMBIGUOUS_CHARS})", variable=self.ambiguous_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        output_frame = ttk.LabelFrame(main_frame, text="Result", padding="10 10 10 10")
        output_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.password_display = ttk.Entry(output_frame, width=35, font=('Consolas', 12, 'bold'), justify='center', state='readonly')
        self.password_display.grid(row=0, column=0, padx=5, pady=5)
        
        self.complexity_label = ttk.Label(output_frame, text="Strength: Unknown", foreground='gray')
        self.complexity_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')

        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        ttk.Button(button_frame, text="Generate Password", command=self.generate_and_display).pack(side=tk.LEFT, padx=10)
        self.copy_button = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, state='disabled')
        self.copy_button.pack(side=tk.LEFT, padx=10)


    def get_password_strength(self, password):
        score = 0
        if len(password) >= 12: score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in string.punctuation for c in password): score += 1
        
        if score <= 2:
            return "Weak", 'red'
        elif score <= 4:
            return "Moderate", 'orange'
        else:
            return "Strong!", 'green'

    def update_complexity_meter(self, password):
        strength, color = self.get_password_strength(password)
        self.complexity_label.config(text=f"Strength: {strength}", foreground=color)


    def generate_and_display(self):
        try:
            length = self.length_var.get()
            use_lower = self.lower_var.get()
            use_upper = self.upper_var.get()
            use_numbers = self.number_var.get()
            use_symbols = self.symbol_var.get()
            exclude_ambiguous = self.ambiguous_var.get()

            if not any([use_lower, use_upper, use_numbers, use_symbols]):
                messagebox.showerror("Validation Error", "Please select at least one character type.")
                self.complexity_label.config(text="Strength: Unknown", foreground='gray')
                return
            
            password, status = generate_secure_password(
                length, use_lower, use_upper, use_numbers, use_symbols, exclude_ambiguous
            )
            
            self.password_display.config(state='normal')
            self.password_display.delete(0, tk.END)
            self.password_display.insert(0, password)
            self.password_display.config(state='readonly')
            
            if status == "Success":
                self.copy_button.config(state='normal')
                self.update_complexity_meter(password)
            else:
                messagebox.showerror("Generation Error", password)
                self.copy_button.config(state='disabled')
                self.complexity_label.config(text="Strength: Error", foreground='red')
                
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def copy_to_clipboard(self):
        password = self.password_display.get()
        if password and self.copy_button['state'] != 'disabled':
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Copied!", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Generate a password first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
