import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont

from functions import *
class BudgetApp:
    def __init__(self, root, transaction_file_name="transactions.csv"):
        self.root = root
        self.root.title("Budget Manager")
        self.root.geometry("627x888")

        self.transaction_file_name = transaction_file_name

        #Font
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=10) 
        custom_font1 = tkFont.Font(family=default_font.actual("family"), size=16, weight=default_font.actual("weight"))
        custom_font2 = tkFont.Font(family=default_font.actual("family"), size=20, weight=default_font.actual("weight"))

        # Widgets
        self.total_label = tk.Label(root, text="Total Transactions: 0")
        self.total_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="W")

        self.current_title_label = tk.Label(root, text="Current balance", font=custom_font1).grid(row=0, column=0)

        self.current_balance_label = tk.Label(root, text="0 PLN", font=custom_font2)
        self.current_balance_label.grid(row=1, column=0, sticky="news")
        
       
        # Transaction Table
        columns = ("Date", "Name", "Amount", "Type")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=round(self.root.winfo_width() / 8))


        self.tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

        root.grid_rowconfigure(3, weight=1)
    
        # Buttons
        self.add_transaction_button = tk.Button(root, text="+ Add Transaction", command=self.show_add_transaction_window)
        self.add_transaction_button.grid(row=2, column=2, padx=0, sticky="E")

        self.monthly_button = tk.Button(root, text="Monthly", command=self.show_monthly_window)
        self.monthly_button.grid(row=0, column=1, padx=5, pady=0, sticky="E")

        self.annual_button = tk.Button(root, text="Annual", command=self.show_annual_window)
        self.annual_button.grid(row=0, column=2, padx=5, pady=0, sticky="w")

        

    def on_window_resize(self, event):
        for col in ("Date", "Name", "Amount", "Type"):
            self.tree.column(col, width=round(event.width / 8))


    def update_transaction_table(self): 
        for item in self.tree.get_children():
            self.tree.delete(item)

        table_data = get_transactions_for_table(self.transaction_file_name)

        for entry in table_data:
            self.tree.insert("", "end", values=entry)

        
    def show_add_transaction_window(self):
        add_transaction_window = tk.Toplevel(self.root)
        add_transaction_window.title("Add Transaction")

        # Radio Buttons
        transaction_type_var = tk.IntVar()
        expense_radio = tk.Radiobutton(add_transaction_window, text="Expense", variable=transaction_type_var, value=1)
        income_radio = tk.Radiobutton(add_transaction_window, text="Income", variable=transaction_type_var, value=2)
        expense_radio.grid(row=0, column=0, padx=10, pady=5)
        income_radio.grid(row=0, column=1, padx=10, pady=5)

        #Labels
        tk.Label(add_transaction_window, text="Name:").grid(row=1, column=0,padx=10, sticky="W") 
        tk.Label(add_transaction_window, text="Amount:").grid(row=3, column=0,padx=10, sticky="W")
        tk.Label(add_transaction_window, text="Date (YYYY-MM-DD):").grid(row=5, column=0,padx=10, sticky="W")

        # Entry Widgets
        name_entry = tk.Entry(add_transaction_window)
        amount_entry = tk.Entry(add_transaction_window)
        date_entry = tk.Entry(add_transaction_window)

        name_entry.grid(row=2, column=0, padx=10, pady=5)
        amount_entry.grid(row=4, column=0, padx=10, pady=5,)
        date_entry.grid(row=6, column=0, padx=10, pady=5)

        # Buttons
        ok_button = tk.Button(add_transaction_window, text="OK", command=lambda: self.add_transaction(
            name_entry.get(), amount_entry.get(), date_entry.get(), transaction_type_var.get(), add_transaction_window))
        ok_button.grid(row=7, column=1, padx=10, pady=5)

        clear_button = tk.Button(add_transaction_window, text="Clear All", command=lambda: self.clear_entries(
            name_entry, amount_entry, date_entry))
        clear_button.grid(row=7, column=0, padx=10, pady=5)

    def add_transaction(self, name, amount, date, transaction_type_var, window):
        if transaction_type_var == 1:
            transaction_type = "expense"
        elif transaction_type_var == 2:
            transaction_type = "income"
        else:
            messagebox.showerror("Error", "Invalid transaction type selected.")
            return
        transaction, error_message = get_user_transaction(name, amount, date, transaction_type)

        if transaction:
            try:
                save_to_file_transaction(transaction, self.transaction_file_name)
                self.update_transaction_table() 
                self.update_current_balance()
                self.update_total_transactions()
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error while saving to file: {str(e)}")
        else:
            messagebox.showerror("Error", error_message)

    def clear_entries(self, *entries):
        for entry in entries:
            entry.delete(0, tk.END)

    def show_monthly_window(self):
        monthly_window = tk.Toplevel(self.root)
        monthly_window.title("Monthly Balance")


        # Entry Widget
        tk.Label(monthly_window, text="Month and Year (YYYY-MM)").grid(row=0, column=0)
        date_entry = tk.Entry(monthly_window)
        date_entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Buttons
        ok_button = tk.Button(monthly_window, text="OK", command=lambda: self.show_total_balance(
            date_entry.get(), "monthly", monthly_window))
        ok_button.grid(row=2, column=1, padx=10, pady=5)

        clear_button = tk.Button(monthly_window, text="Clear All", command=lambda: self.clear_entries(date_entry))
        clear_button.grid(row=2, column=2, padx=10, pady=5)

    def show_annual_window(self):
        annual_window = tk.Toplevel(self.root)
        annual_window.title("Annual Balance")

        # Entry Widget
        tk.Label(annual_window, text="Year").grid(row=0, column=0, padx=10, sticky="w")
        date_entry = tk.Entry(annual_window)
        date_entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Buttons
        ok_button = tk.Button(annual_window, text="OK", command=lambda: self.show_total_balance(
            date_entry.get(), "annual", annual_window))
        ok_button.grid(row=2, column=1, padx=10, pady=5)

        clear_button = tk.Button(annual_window, text="Clear All", command=lambda: self.clear_entries(date_entry))
        clear_button.grid(row=2, column=2, padx=10, pady=5)

    def show_total_balance(self, date, balance_type, window):
        try:
            if balance_type == "monthly":
                year, month = map(int, date.split('-'))
                balance = 0
                transactions_by_date = transaction_balance(self.transaction_file_name)
                for transaction_date, data in transactions_by_date.items():
                    if transaction_date.year == year and transaction_date.month == month:
                        balance += sum(data["amounts"])
                messagebox.showinfo("Mothly Balance", f"Monthly balance for {year}/{month}: {balance:.2f}")
            elif balance_type == "annual":
                year = int(date)
                balance = 0
                transactions_by_date = transaction_balance(self.transaction_file_name)
                for transaction_date, data in transactions_by_date.items():
                    if transaction_date.year == year:
                        balance += sum(data["amounts"])
                messagebox.showinfo("Annual Balance", f"Annual balance for {year}: {balance:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid date.")
        

    def update_total_transactions(self):
        self.total_transactions = calculate_total_transaction(self.transaction_file_name)
        self.total_label.config(text=f"Total Transactions: {self.total_transactions}")

    def update_current_balance(self):
        self.current_balance = current_balance(self.transaction_file_name)
        self.current_balance_label.config(text=f"{self.current_balance} PLN")

