from datetime import datetime
import csv
class Transaction:
    def __init__(self, name, amount, date) -> None:
        self.name = name  
        self.amount = amount
        self.date = date

    def __repr__(self) -> str:
        return f"<Expense: {self.name}, {self.amount:.2f}, {self.date.date()}>"


def get_user_transaction(name, amount, date, prompt_type):
        try:
            transaction_amount = float(amount)
            if prompt_type == "expense":
                transaction_amount *= -1
            elif prompt_type == "income":
                transaction_amount *= 1
        except ValueError:
            return None, f"Invalid amount. Please enter a valid numeric value."
        try:
            new_transaction_date = datetime.strptime(date, '%Y-%m-%d').date()
            new_transaction = Transaction(name, transaction_amount, new_transaction_date)
            return new_transaction, None  
        except ValueError as e:
            return None, f"Invalid date format. Please enter a correct date" 
        

def save_to_file_transaction(transaction: Transaction, transaction_file_name):
    try:
        with open(transaction_file_name, "a") as f:
            f.write(f"{transaction.date}, {transaction.name}, {transaction.amount}\n")
    except FileNotFoundError as e:
        print(f"Error: {transaction_file_name} not found - {e}")
    except Exception as e:
        print(f"Error while writing to file: {e}")

def transaction_balance(transaction_file_name):

    transactions_by_date = {}
    try:
        with open(transaction_file_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                if not line.strip():
                    continue

                csv_reader = csv.reader([line.strip()])
                row = next(csv_reader)

                transaction_date = datetime.strptime(row[0], '%Y-%m-%d').date()

                transaction_name = row[1].strip()

                transaction_amount = float(row[2])


                if transaction_date not in transactions_by_date:
                    transactions_by_date[transaction_date] =  {

                        "amounts": [transaction_amount],
                        "names": [transaction_name] 
                    }
                else:
                    transactions_by_date[transaction_date]["amounts"].append(float(transaction_amount))
                    transactions_by_date[transaction_date]["names"].append(transaction_name)
    except FileNotFoundError as e:
        print(f"Error: {transaction_file_name} not found - {e}")
    except csv.Error as e:
        print(f"Error parsing CSV line: {e}")            
    
    return transactions_by_date

def load_transactions(transaction_file_name):
    transactions = []
    try:
        with open(transaction_file_name, 'r') as f:
            for line in f:
                data = line.strip().split(',')
                date_str, name, amount = data
                amount = float(amount)
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                transaction = Transaction(name, amount, date)
                transactions.append(transaction)
    except FileNotFoundError:
        pass 

    return transactions

def current_balance(transaction_file_name):
    transactions =load_transactions(transaction_file_name)
    current_balance = 0
    for transaction in transactions:
        current_balance += transaction.amount
    return current_balance


def calculate_total_transaction(file_path):
    total_transactions = 0
    try:
        with open(file_path, "r") as f:
            lines =f.readlines()
            total_transactions = len(lines)
            return total_transactions
    except FileNotFoundError:
        return 0

def get_transactions_for_table(transaction_file_name):
    transactions_by_date = transaction_balance(transaction_file_name)
    table_data = []
    for date, data in transactions_by_date.items():
        for i in range(len(data["amounts"])):
            transaction_type = "Expense" if data["amounts"][i] < 0 else "Income"
            table_data.append((date, data["names"][i], data["amounts"][i], transaction_type))
    return table_data

