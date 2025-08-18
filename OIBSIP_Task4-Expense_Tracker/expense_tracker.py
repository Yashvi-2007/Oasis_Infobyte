import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")
        self.root.configure(bg='#808080')  # Simple grey
        
        # CSV file path
        self.csv_file = "expenses.csv"
        
        # Categories
        self.categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Others"]
        
        # Initialize CSV file
        self.init_csv()
        
        # Create GUI
        self.create_widgets()
        
        # Load existing data
        self.refresh_display()
    
    def init_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Description', 'Amount'])
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="💰 Expense Tracker", 
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#808080')
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#808080')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Add Expense
        left_frame = tk.Frame(main_frame, bg='#A0A0A0', relief=tk.RAISED, bd=2)  # Light grey
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.config(width=300)
        left_frame.pack_propagate(False)
        
        # Add Expense Section
        tk.Label(left_frame, text="Add Expense", 
                font=('Arial', 14, 'bold'), 
                fg='black', bg='#A0A0A0').pack(pady=15)
        
        # Category
        tk.Label(left_frame, text="Category:", font=('Arial', 10, 'bold'),
                fg='black', bg='#A0A0A0').pack(anchor='w', padx=20)
        
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(left_frame, textvariable=self.category_var,
                                     values=self.categories, state='readonly', width=25)
        category_combo.pack(padx=20, pady=5)
        category_combo.set(self.categories[0])
        
        # Description
        tk.Label(left_frame, text="Description:", font=('Arial', 10, 'bold'),
                fg='black', bg='#A0A0A0').pack(anchor='w', padx=20, pady=(10,0))
        
        self.desc_var = tk.StringVar()
        desc_entry = tk.Entry(left_frame, textvariable=self.desc_var,
                             font=('Arial', 10), width=30)
        desc_entry.pack(padx=20, pady=5)
        
        # Amount
        tk.Label(left_frame, text="Amount (₹):", font=('Arial', 10, 'bold'),
                fg='black', bg='#A0A0A0').pack(anchor='w', padx=20, pady=(10,0))
        
        self.amount_var = tk.StringVar()
        amount_entry = tk.Entry(left_frame, textvariable=self.amount_var,
                               font=('Arial', 10), width=30)
        amount_entry.pack(padx=20, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(left_frame, bg='#A0A0A0')
        btn_frame.pack(pady=15)
        
        # Add Button - smaller size
        add_btn = tk.Button(btn_frame, text="Add Expense", 
                           font=('Arial', 10, 'bold'),
                           bg='#606060', fg='white',
                           command=self.add_expense,
                           padx=10, pady=4, width=12)
        add_btn.pack(pady=2)
        
        # Clear Button - smaller size
        clear_btn = tk.Button(btn_frame, text="Clear All", 
                             font=('Arial', 10, 'bold'),
                             bg='#808080', fg='white',
                             command=self.clear_expenses,
                             padx=10, pady=4, width=12)
        clear_btn.pack(pady=2)
        
        # Summary
        tk.Label(left_frame, text="Summary", 
                font=('Arial', 12, 'bold'), 
                fg='black', bg='#A0A0A0').pack(pady=(20,10))
        
        self.today_label = tk.Label(left_frame, text="Today: ₹0", 
                                   font=('Arial', 10), 
                                   fg='black', bg='#A0A0A0')
        self.today_label.pack(pady=2)
        
        self.week_label = tk.Label(left_frame, text="This Week: ₹0", 
                                  font=('Arial', 10), 
                                  fg='black', bg='#A0A0A0')
        self.week_label.pack(pady=2)
        
        self.month_label = tk.Label(left_frame, text="This Month: ₹0", 
                                   font=('Arial', 10), 
                                   fg='black', bg='#A0A0A0')
        self.month_label.pack(pady=2)
        
        # Right side - Chart
        right_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chart buttons - smaller size
        chart_btn_frame = tk.Frame(right_frame, bg='white')
        chart_btn_frame.pack(pady=10)
        
        daily_btn = tk.Button(chart_btn_frame, text="Last 7 Days", 
                             font=('Arial', 9),
                             bg='#606060', fg='white',
                             command=lambda: self.show_chart('daily'),
                             padx=8, pady=3)
        daily_btn.pack(side=tk.LEFT, padx=5)
        
        category_btn = tk.Button(chart_btn_frame, text="Categories", 
                                font=('Arial', 9),
                                bg='#808080', fg='white',
                                command=lambda: self.show_chart('category'),
                                padx=8, pady=3)
        category_btn.pack(side=tk.LEFT, padx=5)
        
        # Chart canvas
        self.chart_frame = tk.Frame(right_frame, bg='white')
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", 
                                  bg='#808080', fg='white', font=('Arial', 9),
                                  anchor='w')
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def add_expense(self):
        """Add new expense to CSV file"""
        try:
            date = datetime.now().strftime("%Y-%m-%d")
            category = self.category_var.get()
            description = self.desc_var.get()
            amount = float(self.amount_var.get())
            
            if not all([category, description, amount]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            # Add to CSV
            with open(self.csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, category, description, amount])
            
            # Clear fields
            self.desc_var.set("")
            self.amount_var.set("")
            
            # Refresh display
            self.refresh_display()
            
            self.status_bar.config(text=f"Added: {description} - ₹{amount:.0f}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def clear_expenses(self):
        """Clear all expenses with confirmation"""
        result = messagebox.askyesno("Confirm Clear", 
                                   "Are you sure you want to clear ALL expenses?\nThis cannot be undone!")
        if result:
            try:
                # Clear CSV file by recreating with headers only
                with open(self.csv_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Date', 'Category', 'Description', 'Amount'])
                
                # Refresh display
                self.refresh_display()
                self.status_bar.config(text="All expenses cleared")
                messagebox.showinfo("Success", "All expenses have been cleared!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error clearing expenses: {str(e)}")
    
    def refresh_display(self):
        """Refresh summary and charts"""
        self.update_summary()
        self.show_chart('daily')
    
    def update_summary(self):
        """Update summary labels"""
        try:
            if not os.path.exists(self.csv_file):
                return
            
            df = pd.read_csv(self.csv_file)
            if df.empty:
                return
            
            df['Date'] = pd.to_datetime(df['Date'])
            today = datetime.now().date()
            
            # Today's expenses
            today_expenses = df[df['Date'].dt.date == today]['Amount'].sum()
            self.today_label.config(text=f"Today: ₹{today_expenses:.0f}")
            
            # This week's expenses
            week_start = today - timedelta(days=today.weekday())
            week_expenses = df[df['Date'].dt.date >= week_start]['Amount'].sum()
            self.week_label.config(text=f"This Week: ₹{week_expenses:.0f}")
            
            # This month's expenses
            month_expenses = df[df['Date'].dt.month == today.month]['Amount'].sum()
            self.month_label.config(text=f"This Month: ₹{month_expenses:.0f}")
            
        except Exception:
            pass
    
    def show_chart(self, chart_type):
        """Display charts based on type"""
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        try:
            if not os.path.exists(self.csv_file):
                return
            
            df = pd.read_csv(self.csv_file)
            if df.empty:
                no_data_label = tk.Label(self.chart_frame, text="No data yet", 
                                        font=('Arial', 12), 
                                        fg='#808080', bg='white')
                no_data_label.pack(expand=True)
                return
            
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(5, 3.5))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            
            if chart_type == 'daily':
                # Last 7 days chart
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=6)
                
                daily_data = df[df['Date'].dt.date >= start_date].groupby(df['Date'].dt.date)['Amount'].sum()
                
                # Create date range for last 7 days
                date_range = [start_date + timedelta(days=x) for x in range(7)]
                amounts = [daily_data.get(date, 0) for date in date_range]
                
                ax.bar([d.strftime('%m-%d') for d in date_range], amounts, color='#808080')
                ax.set_title('Last 7 Days', fontsize=12, color='#404040', weight='bold')
                ax.set_ylabel('Amount (₹)', color='#404040')
                
            elif chart_type == 'category':
                # Category pie chart
                category_data = df.groupby('Category')['Amount'].sum()
                colors = ['#808080', '#606060', '#A0A0A0', '#707070', '#909090', '#B0B0B0']
                
                ax.pie(category_data.values, labels=category_data.index, autopct='%1.0f%%', 
                       colors=colors[:len(category_data)])
                ax.set_title('By Categories', fontsize=12, color='#404040', weight='bold')
            
            # Styling
            ax.tick_params(colors='#404040')
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            plt.close(fig)
            
        except Exception as e:
            error_label = tk.Label(self.chart_frame, text="Chart error", 
                                  font=('Arial', 10), 
                                  fg='red', bg='white')
            error_label.pack(expand=True)

def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
