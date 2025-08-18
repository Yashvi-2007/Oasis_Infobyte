import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re
from datetime import datetime

class SimplePasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("700x500")
        self.root.configure(bg='#f0f0f0')
        
        # Password history
        self.password_history = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Password Generator", 
                              font=('Arial', 20, 'bold'), fg='#2c3e50', bg='#f0f0f0')
        title_label.pack(pady=(0, 20))
        
        # Main content
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Controls
        left_panel = tk.Frame(content_frame, bg='#ffffff', relief='solid', bd=1)
        left_panel.pack(side='left', fill='y', padx=(0, 15), pady=5, ipadx=20, ipady=20)
        
        # Right panel - Results
        right_panel = tk.Frame(content_frame, bg='#ffffff', relief='solid', bd=1)
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5, ipadx=20, ipady=20)
        
        self.create_controls(left_panel)
        self.create_results_panel(right_panel)
        
    def create_controls(self, parent):
        """Create the control panel"""
        
        # Password Length
        tk.Label(parent, text="Password Length:", font=('Arial', 12, 'bold'),
                fg='#2c3e50', bg='#ffffff').pack(anchor='w', pady=(0, 10))
        
        length_frame = tk.Frame(parent, bg='#ffffff')
        length_frame.pack(fill='x', pady=(0, 20))
        
        self.length_var = tk.IntVar(value=8)
        length_scale = tk.Scale(length_frame, from_=4, to=12, orient='horizontal',
                               variable=self.length_var, bg='#ffffff', fg='#3498db',
                               highlightbackground='#ffffff', troughcolor='#ecf0f1',
                               activebackground='#3498db', font=('Arial', 10))
        length_scale.pack(fill='x')
        
        # Character Options
        tk.Label(parent, text="Include Characters:", font=('Arial', 12, 'bold'),
                fg='#2c3e50', bg='#ffffff').pack(anchor='w', pady=(0, 10))
        
        self.include_vars = {}
        options = [
            ('Uppercase Letters (A-Z)', 'uppercase', True),
            ('Lowercase Letters (a-z)', 'lowercase', True),
            ('Numbers (0-9)', 'numbers', True),
            ('Symbols (!@#$%^&*)', 'symbols', True)
        ]
        
        for text, key, default in options:
            var = tk.BooleanVar(value=default)
            self.include_vars[key] = var
            tk.Checkbutton(parent, text=text, variable=var,
                          bg='#ffffff', fg='#2c3e50', selectcolor='#ffffff',
                          activebackground='#ffffff', activeforeground='#2c3e50',
                          font=('Arial', 10)).pack(anchor='w', pady=3)
        
        # Generate Button
        generate_btn = tk.Button(parent, text="Generate Password", 
                               command=self.generate_password, bg='#3498db', fg='white',
                               font=('Arial', 12, 'bold'), relief='flat', pady=10,
                               cursor='hand2', width=20)
        generate_btn.pack(pady=(30, 20))
        
    def create_results_panel(self, parent):
        """Create the results display panel"""
        
        # Generated Password Display
        tk.Label(parent, text="Generated Password:", font=('Arial', 12, 'bold'), 
                fg='#2c3e50', bg='#ffffff').pack(anchor='w', pady=(0, 10))
        
        password_frame = tk.Frame(parent, bg='#ecf0f1', relief='solid', bd=1)
        password_frame.pack(fill='x', pady=(0, 15))
        
        self.password_display = tk.Text(password_frame, height=3, bg='#ecf0f1', fg='#e74c3c',
                                       font=('Courier New', 14, 'bold'), wrap='word', relief='flat',
                                       insertbackground='#e74c3c')
        self.password_display.pack(fill='x', padx=15, pady=15)
        
        # Copy Button
        copy_btn = tk.Button(parent, text="Copy to Clipboard", command=self.copy_password,
                           bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), 
                           relief='flat', cursor='hand2', width=20)
        copy_btn.pack(pady=(0, 20))
        
        # Password Strength
        tk.Label(parent, text="Password Strength:", font=('Arial', 12, 'bold'), 
                fg='#2c3e50', bg='#ffffff').pack(anchor='w', pady=(0, 10))
        
        self.strength_frame = tk.Frame(parent, bg='#ffffff')
        self.strength_frame.pack(fill='x', pady=(0, 10))
        
        self.strength_bars = []
        for i in range(5):
            bar = tk.Frame(self.strength_frame, bg='#ecf0f1', height=15, width=40)
            bar.pack(side='left', padx=3, pady=2)
            self.strength_bars.append(bar)
        
        self.strength_label = tk.Label(parent, text="Generate a password to see strength", 
                                     font=('Arial', 10), fg='#7f8c8d', bg='#ffffff')
        self.strength_label.pack(anchor='w')
        
        # Check Password Strength Section
        tk.Label(parent, text="Check Password Strength:", font=('Arial', 12, 'bold'), 
                fg='#2c3e50', bg='#ffffff').pack(anchor='w', pady=(20, 10))
        
        check_frame = tk.Frame(parent, bg='#ecf0f1', relief='solid', bd=1)
        check_frame.pack(fill='x', pady=(0, 10))
        
        self.check_entry = tk.Entry(check_frame, bg='#ecf0f1', fg='#2c3e50',
                                   font=('Arial', 12), show='*')
        self.check_entry.pack(fill='x', padx=10, pady=10)
        self.check_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Check result
        self.check_strength_frame = tk.Frame(parent, bg='#ffffff')
        self.check_strength_frame.pack(fill='x', pady=(0, 10))
        
        self.check_strength_bars = []
        for i in range(5):
            bar = tk.Frame(self.check_strength_frame, bg='#ecf0f1', height=15, width=40)
            bar.pack(side='left', padx=3, pady=2)
            self.check_strength_bars.append(bar)
        
        self.check_strength_label = tk.Label(parent, text="Type a password to check its strength", 
                                           font=('Arial', 10), fg='#7f8c8d', bg='#ffffff')
        self.check_strength_label.pack(anchor='w')
        
        # Password History
        tk.Label(parent, text="Password History:", font=('Arial', 12, 'bold'), 
                fg='#2c3e50', bg='#ffffff').pack(anchor='w', pady=(20, 10))
        
        self.history_listbox = tk.Listbox(parent, bg='#ecf0f1', fg='#2c3e50',
                                        font=('Courier', 10), selectbackground='#3498db',
                                        selectforeground='white')
        self.history_listbox.pack(fill='both', expand=True)
        self.history_listbox.bind('<Double-1>', self.select_from_history)
        
    def get_character_set(self):
        """Build character set based on selections"""
        chars = ""
        
        if self.include_vars['uppercase'].get():
            chars += string.ascii_uppercase
        if self.include_vars['lowercase'].get():
            chars += string.ascii_lowercase
        if self.include_vars['numbers'].get():
            chars += string.digits
        if self.include_vars['symbols'].get():
            chars += "!@#$%^&*"
        
        return chars
        
    def generate_password(self):
        """Generate a single password"""
        try:
            length = self.length_var.get()
            chars = self.get_character_set()
            
            if not chars:
                messagebox.showerror("Error", "Please select at least one character type!")
                return
            
            # Generate password ensuring at least one character from each selected type
            password_chars = []
            
            # Add required characters
            if self.include_vars['uppercase'].get():
                available = [c for c in string.ascii_uppercase if c in chars]
                if available:
                    password_chars.append(random.choice(available))
                    
            if self.include_vars['lowercase'].get():
                available = [c for c in string.ascii_lowercase if c in chars]
                if available:
                    password_chars.append(random.choice(available))
                    
            if self.include_vars['numbers'].get():
                available = [c for c in string.digits if c in chars]
                if available:
                    password_chars.append(random.choice(available))
                    
            if self.include_vars['symbols'].get():
                available = [c for c in "!@#$%^&*" if c in chars]
                if available:
                    password_chars.append(random.choice(available))
            
            # Fill remaining length
            remaining = length - len(password_chars)
            for _ in range(remaining):
                password_chars.append(random.choice(chars))
            
            # Shuffle the password
            random.shuffle(password_chars)
            password = ''.join(password_chars)
            
            # Display the password
            self.password_display.delete('1.0', tk.END)
            self.password_display.insert('1.0', password)
            
            # Update strength display
            self.update_strength_display(password)
            
            # Add to history
            self.add_to_history(password)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def calculate_password_strength(self, password):
        """Calculate password strength score (0-100)"""
        score = 0
        length = len(password)
        
        # Length scoring
        score += min(length * 8, 40)  # Up to 40 points for length
        
        # Character variety (40 points total)
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 10
        
        # Unique characters bonus (20 points)
        unique_chars = len(set(password))
        score += min(unique_chars * 3, 20)
        
        return min(100, score)
    
    def update_strength_display(self, password):
        """Update the strength visualization"""
        score = self.calculate_password_strength(password)
        
        # Determine strength level and color
        if score < 40:
            level = "Weak"
            color = "#e74c3c"
            filled_bars = 1
        elif score < 60:
            level = "Fair"
            color = "#f39c12"
            filled_bars = 2
        elif score < 75:
            level = "Good"
            color = "#f1c40f"
            filled_bars = 3
        elif score < 90:
            level = "Strong"
            color = "#27ae60"
            filled_bars = 4
        else:
            level = "Very Strong"
            color = "#2ecc71"
            filled_bars = 5
        
        # Update strength bars
        for i, bar in enumerate(self.strength_bars):
            if i < filled_bars:
                bar.configure(bg=color)
            else:
                bar.configure(bg='#ecf0f1')
        
        self.strength_label.configure(text=f"{level} ({score}/100)", fg=color)
    
    def check_password_strength(self, event=None):
        """Check strength of typed password"""
        password = self.check_entry.get()
        
        if not password:
            # Reset bars and label
            for bar in self.check_strength_bars:
                bar.configure(bg='#ecf0f1')
            self.check_strength_label.configure(text="Type a password to check its strength", fg='#7f8c8d')
            return
        
        score = self.calculate_password_strength(password)
        
        # Determine strength level and color
        if score < 40:
            level = "Weak"
            color = "#e74c3c"
            filled_bars = 1
        elif score < 60:
            level = "Fair"
            color = "#f39c12"
            filled_bars = 2
        elif score < 75:
            level = "Good"
            color = "#f1c40f"
            filled_bars = 3
        elif score < 90:
            level = "Strong"
            color = "#27ae60"
            filled_bars = 4
        else:
            level = "Very Strong"
            color = "#2ecc71"
            filled_bars = 5
        
        # Update check strength bars
        for i, bar in enumerate(self.check_strength_bars):
            if i < filled_bars:
                bar.configure(bg=color)
            else:
                bar.configure(bg='#ecf0f1')
        
        self.check_strength_label.configure(text=f"{level} ({score}/100)", fg=color)
    
    def add_to_history(self, password):
        """Add password to history"""
        # Add timestamp to password
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {password}"
        
        if password not in [item.split('] ')[1] for item in self.password_history]:
            self.password_history.insert(0, entry)
            if len(self.password_history) > 15:  # Keep last 15
                self.password_history.pop()
        
        # Update history display
        self.history_listbox.delete(0, tk.END)
        for entry in self.password_history:
            self.history_listbox.insert(tk.END, entry)
    
    def select_from_history(self, event):
        """Select password from history"""
        selection = self.history_listbox.curselection()
        if selection:
            entry = self.history_listbox.get(selection[0])
            # Extract password (after timestamp)
            password = entry.split('] ', 1)[1]
            self.password_display.delete('1.0', tk.END)
            self.password_display.insert('1.0', password)
            
            self.update_strength_display(password)
    
    def copy_password(self):
        """Copy password to clipboard"""
        password = self.password_display.get('1.0', tk.END).strip()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Generate a password first!")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePasswordGenerator(root)
    root.mainloop()
