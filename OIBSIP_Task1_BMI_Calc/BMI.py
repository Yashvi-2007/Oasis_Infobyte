import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator - OIBSIP Python Task 1")
        self.root.geometry("650x600")
        self.root.configure(bg='#f0f0f0')
        
        # Data file for storing BMI records
        self.data_file = "bmi_records.csv"
        self.ensure_data_file()
        
        self.create_widgets()
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def ensure_data_file(self):
        """Create CSV file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Weight(kg)', 'Height(m)', 'BMI', 'Category'])
    
    def create_widgets(self):
        # main canvas and scrollbar for scrollable interface
        self.canvas = tk.Canvas(self.root, bg='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Title
        title_frame = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        title_frame.pack(pady=15)
        
        title_label = tk.Label(title_frame, text="🧮 BMI Calculator", 
                              font=('Arial', 20, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Body Mass Index Calculator & Tracker", 
                                 font=('Arial', 10), 
                                 bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack()
        
        # Action buttons at the top for easy access
        button_frame = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        self.history_button = tk.Button(button_frame, text="📊 View History", 
                                       command=self.show_history,
                                       bg='#27ae60', fg='white', 
                                       font=('Arial', 9, 'bold'),
                                       padx=15, pady=5)
        self.history_button.pack(side='left', padx=5)
        
        self.chart_button = tk.Button(button_frame, text="📈 Show Chart", 
                                     command=self.show_chart,
                                     bg='#e74c3c', fg='white', 
                                     font=('Arial', 9, 'bold'),
                                     padx=15, pady=5)
        self.chart_button.pack(side='left', padx=5)
        
        self.clear_button = tk.Button(button_frame, text="🗑️ Clear History", 
                                     command=self.clear_history,
                                     bg='#95a5a6', fg='white', 
                                     font=('Arial', 9, 'bold'),
                                     padx=15, pady=5)
        self.clear_button.pack(side='left', padx=5)
        
        # Main input frame
        main_frame = tk.Frame(self.scrollable_frame, bg='#ffffff', relief='raised', bd=2)
        main_frame.pack(pady=15, padx=20, fill='x')
        
        # Weight input
        weight_frame = tk.Frame(main_frame, bg='#ffffff')
        weight_frame.pack(pady=12, padx=15, fill='x')
        
        tk.Label(weight_frame, text="Weight:", font=('Arial', 11, 'bold'), 
                bg='#ffffff').pack(anchor='w')
        
        weight_input_frame = tk.Frame(weight_frame, bg='#ffffff')
        weight_input_frame.pack(fill='x', pady=5)
        
        self.weight_var = tk.StringVar()
        self.weight_entry = tk.Entry(weight_input_frame, textvariable=self.weight_var, 
                                    font=('Arial', 10), width=12)
        self.weight_entry.pack(side='left')
        
        tk.Label(weight_input_frame, text="kg", font=('Arial', 10), 
                bg='#ffffff', fg='#7f8c8d').pack(side='left', padx=(5,0))
        
        # Height input
        height_frame = tk.Frame(main_frame, bg='#ffffff')
        height_frame.pack(pady=12, padx=15, fill='x')
        
        tk.Label(height_frame, text="Height:", font=('Arial', 11, 'bold'), 
                bg='#ffffff').pack(anchor='w')
        
        # Height format selection
        format_frame = tk.Frame(height_frame, bg='#ffffff')
        format_frame.pack(fill='x', pady=5)
        
        self.height_format = tk.StringVar(value="cm")
        
        formats = [("cm", "cm"), ("m", "m"), ("ft/in", "ft")]
        for text, value in formats:
            tk.Radiobutton(format_frame, text=text, variable=self.height_format, 
                          value=value, bg='#ffffff', font=('Arial', 9),
                          command=self.update_height_inputs).pack(side='left', padx=8)
        
        # Height input fields
        self.height_input_frame = tk.Frame(height_frame, bg='#ffffff')
        self.height_input_frame.pack(fill='x', pady=5)
        
        self.create_height_inputs()
        
        # Calc button
        calc_frame = tk.Frame(main_frame, bg='#ffffff')
        calc_frame.pack(pady=15)
        
        self.calc_button = tk.Button(calc_frame, text="🧮 Calculate BMI", 
                                    command=self.calculate_bmi,
                                    bg='#3498db', fg='white', 
                                    font=('Arial', 11, 'bold'),
                                    padx=25, pady=8,
                                    cursor='hand2')
        self.calc_button.pack()
        
        # New calc button 
        self.new_calc_button = tk.Button(calc_frame, text="➕ New Calculation", 
                                        command=self.new_calculation,
                                        bg='#16a085', fg='white', 
                                        font=('Arial', 10, 'bold'),
                                        padx=20, pady=6)
        
        # Results frame
        self.results_frame = tk.Frame(self.scrollable_frame, bg='#ffffff', relief='raised', bd=2)
        
        # BMI reference card
        self.create_reference_card()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_height_inputs(self):
        """Create height input fields based on selected format"""
        # Clear existing inputs
        for widget in self.height_input_frame.winfo_children():
            widget.destroy()
        
        if self.height_format.get() == "ft":
            # Feet and inches input
            self.feet_var = tk.StringVar()
            self.inches_var = tk.StringVar()
            
            tk.Entry(self.height_input_frame, textvariable=self.feet_var, 
                    font=('Arial', 10), width=6).pack(side='left')
            tk.Label(self.height_input_frame, text="ft", font=('Arial', 10), 
                    bg='#ffffff', fg='#7f8c8d').pack(side='left', padx=(3,8))
            
            tk.Entry(self.height_input_frame, textvariable=self.inches_var, 
                    font=('Arial', 10), width=6).pack(side='left')
            tk.Label(self.height_input_frame, text="in", font=('Arial', 10), 
                    bg='#ffffff', fg='#7f8c8d').pack(side='left', padx=(3,0))
        else:
            # Single input for cm or m
            self.height_var = tk.StringVar()
            tk.Entry(self.height_input_frame, textvariable=self.height_var, 
                    font=('Arial', 10), width=12).pack(side='left')
            unit = self.height_format.get()
            tk.Label(self.height_input_frame, text=unit, font=('Arial', 10), 
                    bg='#ffffff', fg='#7f8c8d').pack(side='left', padx=(5,0))
    
    def update_height_inputs(self):
        """Update height input fields when format changes"""
        self.create_height_inputs()
    
    def get_height_in_meters(self):
        """Convert height input to meters"""
        try:
            if self.height_format.get() == "m":
                return float(self.height_var.get())
            elif self.height_format.get() == "cm":
                return float(self.height_var.get()) / 100
            elif self.height_format.get() == "ft":
                feet = float(self.feet_var.get()) if self.feet_var.get() else 0
                inches = float(self.inches_var.get()) if self.inches_var.get() else 0
                return (feet * 12 + inches) * 0.0254
        except ValueError:
            raise ValueError("Invalid height input")
    
    def calculate_bmi(self):
        """Calculate BMI and display results"""
        try:
            # Val inputs
            weight = float(self.weight_var.get())
            height = self.get_height_in_meters()
            
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive values")
            
            if weight > 1000 or height > 3:
                raise ValueError("Please enter realistic values")
            
            if height < 0.5:
                raise ValueError("Height seems too small")
            
            # BMI
            bmi = weight / (height ** 2)
            category = self.get_bmi_category(bmi)
            
            # results
            self.display_results(bmi, category, weight, height)
            
            # Save to file
            self.save_record(weight, height, bmi, category)
            
            # Show new calculation button and hide calculate button
            self.calc_button.pack_forget()
            self.new_calc_button.pack()
            
            # Scroll to results
            self.root.after(100, self.scroll_to_results)
            
        except ValueError as e:
            if "could not convert" in str(e):
                messagebox.showerror("Input Error", "Please enter valid numeric values")
            else:
                messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def scroll_to_results(self):
        """Scroll to show results"""
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
    
    def new_calculation(self):
        """Reset for new calculation"""
        # Clear input fields
        self.weight_var.set("")
        if hasattr(self, 'height_var'):
            self.height_var.set("")
        if hasattr(self, 'feet_var'):
            self.feet_var.set("")
        if hasattr(self, 'inches_var'):
            self.inches_var.set("")
        
        # Hide results and new calc button, show calculate button
        self.results_frame.pack_forget()
        self.new_calc_button.pack_forget()
        self.calc_button.pack()
        
        # Scroll to top
        self.canvas.yview_moveto(0.0)
    
    def get_bmi_category(self, bmi):
        """Classify BMI according to WHO standards"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def get_category_color(self, category):
        """Get color for BMI category"""
        colors = {
            "Underweight": "#3498db",
            "Normal weight": "#27ae60",
            "Overweight": "#f39c12",
            "Obese": "#e74c3c"
        }
        return colors.get(category, "#34495e")
    
    def display_results(self, bmi, category, weight, height):
        """Display BMI calculation results"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        #results frame
        self.results_frame.pack(pady=15, padx=20, fill='x')
        
        # Results title
        tk.Label(self.results_frame, text="📊 Your BMI Results", 
                font=('Arial', 14, 'bold'), 
                bg='#ffffff', fg='#2c3e50').pack(pady=12)
        
        # BMI value in a highlighted box
        bmi_frame = tk.Frame(self.results_frame, bg='#ecf0f1', relief='solid', bd=1)
        bmi_frame.pack(pady=8, padx=15, fill='x')
        
        bmi_text = f"BMI: {bmi:.1f}"
        tk.Label(bmi_frame, text=bmi_text, 
                font=('Arial', 18, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=8)
        
        # Categ with color
        color = self.get_category_color(category)
        category_frame = tk.Frame(self.results_frame, bg=color, relief='solid', bd=1)
        category_frame.pack(pady=5, padx=15, fill='x')
        
        tk.Label(category_frame, text=category, 
                font=('Arial', 12, 'bold'), 
                bg=color, fg='white').pack(pady=6)
        
        # Add. info
        info_frame = tk.Frame(self.results_frame, bg='#ffffff')
        info_frame.pack(pady=8)
        
        info_text = f"Weight: {weight} kg | Height: {height:.2f} m"
        tk.Label(info_frame, text=info_text, 
                font=('Arial', 9), 
                bg='#ffffff', fg='#7f8c8d').pack()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        tk.Label(info_frame, text=f"Calculated: {timestamp}", 
                font=('Arial', 8), 
                bg='#ffffff', fg='#95a5a6').pack()
    
    def create_reference_card(self):
        """Create BMI reference card"""
        ref_main_frame = tk.Frame(self.scrollable_frame, bg='#ffffff', relief='raised', bd=2)
        ref_main_frame.pack(pady=15, padx=20, fill='x')
        
        tk.Label(ref_main_frame, text="📋 BMI Categories (WHO)", 
                font=('Arial', 12, 'bold'), 
                bg='#ffffff', fg='#2c3e50').pack(pady=10)
        
        ranges = [
            ("Underweight", "< 18.5"),
            ("Normal weight", "18.5 - 24.9"),
            ("Overweight", "25 - 29.9"),
            ("Obese", "≥ 30")
        ]
        
        for cat, range_text in ranges:
            cat_frame = tk.Frame(ref_main_frame, bg='#ffffff')
            cat_frame.pack(fill='x', padx=15, pady=2)
            
            color = self.get_category_color(cat)
            
            # Color indicator
            color_label = tk.Label(cat_frame, text="●", font=('Arial', 12), 
                                  bg='#ffffff', fg=color)
            color_label.pack(side='left')
            
            # Categ. and range
            text = f"{cat}: {range_text}"
            tk.Label(cat_frame, text=text, font=('Arial', 9), 
                    bg='#ffffff', fg='#34495e').pack(side='left', padx=(5,0))
        
        tk.Label(ref_main_frame, text=" ", bg='#ffffff').pack(pady=5)  # Spacing
    
    def save_record(self, weight, height, bmi, category):
        """Save BMI record to CSV file"""
        try:
            with open(self.data_file, 'a', newline='') as file:
                writer = csv.writer(file)
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                writer.writerow([date_str, weight, height, f"{bmi:.1f}", category])
        except Exception as e:
            print(f"Error saving record: {e}")
    
    def show_history(self):
        """Display BMI history in a new window"""
        try:
            history_window = tk.Toplevel(self.root)
            history_window.title("📊 BMI History")
            history_window.geometry("750x450")
            history_window.configure(bg='#f0f0f0')
            
            # Title
            title_frame = tk.Frame(history_window, bg='#f0f0f0')
            title_frame.pack(pady=10)
            tk.Label(title_frame, text="📊 Your BMI History", 
                    font=('Arial', 16, 'bold'), 
                    bg='#f0f0f0', fg='#2c3e50').pack()
            
            # treeview for data display
            tree_frame = tk.Frame(history_window, bg='#ffffff', relief='raised', bd=2)
            tree_frame.pack(fill='both', expand=True, padx=15, pady=10)
            
            columns = ('Date', 'Weight(kg)', 'Height(m)', 'BMI', 'Category')
            tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
            
            # columns
            tree.column('Date', width=130)
            tree.column('Weight(kg)', width=100)
            tree.column('Height(m)', width=100)
            tree.column('BMI', width=80)
            tree.column('Category', width=120)
            
            for col in columns:
                tree.heading(col, text=col, anchor='center')
                tree.column(col, anchor='center')
            
            #scrollbars
            v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
            h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            tree.pack(side='left', fill='both', expand=True)
            v_scrollbar.pack(side='right', fill='y')
            h_scrollbar.pack(side='bottom', fill='x')
            
            # Load data from CSV
            record_count = 0
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    rows = list(reader)
                    for row in reversed(rows):  # Show newest first
                        if len(row) >= 5:
                            tree.insert('', 'end', values=row)
                            record_count += 1
            
            if record_count == 0:
                no_data_label = tk.Label(history_window, text="📝 No BMI records found.\nCalculate your first BMI to start tracking!", 
                        font=('Arial', 12), bg='#f0f0f0', fg='#7f8c8d')
                no_data_label.pack(pady=30)
            else:
                # Show record count
                count_label = tk.Label(history_window, text=f"Total Records: {record_count}", 
                        font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
                count_label.pack(pady=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load history: {str(e)}")
    
    def show_chart(self):
        """Display BMI trend chart"""
        try:
            if not os.path.exists(self.data_file):
                messagebox.showinfo("No Data", "No BMI records found to chart.")
                return
            
            # Read data
            dates, bmis = [], []
            with open(self.data_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 4:
                        try:
                            dates.append(datetime.strptime(row[0], "%Y-%m-%d %H:%M"))
                            bmis.append(float(row[3]))
                        except (ValueError, IndexError):
                            continue
            
            if not bmis:
                messagebox.showinfo("No Data", "No valid BMI records found to chart.")
                return
            
            #chart window
            chart_window = tk.Toplevel(self.root)
            chart_window.title("📈 BMI Trend Chart")
            chart_window.geometry("900x650")
            chart_window.configure(bg='#f0f0f0')
            
            # Title
            title_frame = tk.Frame(chart_window, bg='#f0f0f0')
            title_frame.pack(pady=10)
            tk.Label(title_frame, text="📈 Your BMI Trend Over Time", 
                    font=('Arial', 16, 'bold'), 
                    bg='#f0f0f0', fg='#2c3e50').pack()
            
            #matplotlib figure
            fig, ax = plt.subplots(figsize=(11, 7))
            fig.patch.set_facecolor('#f0f0f0')
            
            ax.plot(dates, bmis, marker='o', linewidth=2, markersize=8, color='#3498db')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('BMI', fontsize=12)
            ax.set_title('BMI Progression', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            #BMI category zones
            ax.axhspan(0, 18.5, alpha=0.1, color='#3498db', label='Underweight')
            ax.axhspan(18.5, 25, alpha=0.1, color='#27ae60', label='Normal')
            ax.axhspan(25, 30, alpha=0.1, color='#f39c12', label='Overweight')
            ax.axhspan(30, max(max(bmis) + 2, 35), alpha=0.1, color='#e74c3c', label='Obese')
            
            ax.legend(loc='upper right')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Embed chart in tkinter window
            chart_frame = tk.Frame(chart_window, bg='#ffffff', relief='raised', bd=2)
            chart_frame.pack(fill='both', expand=True, padx=15, pady=10)
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            # Stats
            stats_frame = tk.Frame(chart_window, bg='#f0f0f0')
            stats_frame.pack(pady=5)
            
            if len(bmis) > 1:
                latest_bmi = bmis[-1]
                previous_bmi = bmis[-2]
                change = latest_bmi - previous_bmi
                change_text = f"Latest Change: {change:+.1f}"
                color = '#27ae60' if change <= 0 else '#e74c3c'
            else:
                change_text = f"Current BMI: {bmis[0]:.1f}"
                color = '#34495e'
            
            tk.Label(stats_frame, text=f"Records: {len(bmis)} | {change_text}", 
                    font=('Arial', 10), bg='#f0f0f0', fg=color).pack()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not create chart: {str(e)}")
    
    def clear_history(self):
        """Clear all BMI history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all BMI history?"):
            try:
                with open(self.data_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Date', 'Weight(kg)', 'Height(m)', 'BMI', 'Category'])
                messagebox.showinfo("Success", "BMI history cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clear history: {str(e)}")

def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
