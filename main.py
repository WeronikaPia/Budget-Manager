# This is the main file to start your project
# You may add any additional modules and other files you wis

import tkinter as tk
from GUI import BudgetApp
import os

if __name__ == "__main__":
    transaction_file_name = "transactions.csv"
    if not os.path.isfile(transaction_file_name):
        with open(transaction_file_name, "w"):
            pass

    root = tk.Tk()
    app = BudgetApp(root)
    app.update_transaction_table()
    root.mainloop()
