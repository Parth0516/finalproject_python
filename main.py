import sqlite3
def create_database():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            pin TEXT,
            balance REAL,
            transaction_history TEXT
        )
    ''')

    conn.commit()
    conn.close()


def create_initial_accounts():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO accounts (account_number, pin, balance, transaction_history)
        VALUES (?, ?, ?, ?)
    ''', ("123456789", "1234", 1200, ""))

    cursor.execute('''
        INSERT OR IGNORE INTO accounts (account_number, pin, balance, transaction_history)
        VALUES (?, ?, ?, ?)
    ''', ("987654321", "2222", 1500, ""))

    conn.commit()
    conn.close()


def deposit(account_number, amount):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE accounts
        SET balance = balance + ?,
            transaction_history = transaction_history || ?
        WHERE acc_number = ?
    ''', (amount, f"Deposited Rs{amount}\n", account_number))

    conn.commit()
    conn.close()

def withdraw(account_number, amount):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE accounts
        SET balance = balance - ?,
            transaction_history = transaction_history || ?
        WHERE acc_number = ?
    ''', (amount, f"Withdrew Rs{amount}\n", account_number))

    conn.commit()
    conn.close()

def transfer(sender_account, recipient_account, amount):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE accounts
        SET balance = balance - ?,
            transaction_history = transaction_history || ?
        WHERE account_number = ?
    ''', (amount, f"Transferred Rs{amount} to account {recipient_account}\n", sender_account))

    cursor.execute('''
        UPDATE accounts
        SET balance = balance + ?,
            transaction_history = transaction_history || ?
        WHERE account_number = ?
    ''', (amount, f"Received Rs{amount} from account {sender_account}\n", recipient_account))

    conn.commit()
    conn.close()

def change_pin(account_number, new_pin):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE accounts
        SET pin = ?
        WHERE account_number = ?
    ''', (new_pin, account_number))

    conn.commit()
    conn.close()
    print("PIN changed successfully!")

def print_balance(account_number):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT balance
        FROM accounts
        WHERE account_number = ?
    ''', (account_number,))

    result = cursor.fetchone()

    if result:
        balance = result[0]
        print(f"Your balance: Rs{balance}")
    else:
        print("Account not found.")

    conn.close()

def print_transaction_history(account_number):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT transaction_history
        FROM accounts
        WHERE account_number = ?
    ''', (account_number,))

    result = cursor.fetchone()

    if result:
        transaction_history = result[0]
        print("Transaction History:")
        print(transaction_history)
    else:
        print("Account not found.")

    conn.close()

def main():
    create_database()
    create_initial_accounts()

    while True:
        print("\nATM Menu:")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Print Balance")
        print("8. Exit")

        choice = input("Enter your choice: ")
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT *
            FROM accounts
            WHERE account_number = ? AND pin = ?
        ''', (account_number, pin))

        result = cursor.fetchone()

        if result:
            if choice == "1":
                print_balance(account_number)
            elif choice == "2":
                amount = float(input("Enter the amount to deposit: "))
                deposit(account_number, amount)
                print("Deposit successful!")
            elif choice == "3":
                amount = float(input("Enter the amount to withdraw: "))
                withdraw(account_number, amount)
            elif choice == "4":
                recipient_account = input("Enter recipient's account number: ")
                if recipient_account != account_number:
                    if recipient_account in [row[0] for row in cursor.execute("SELECT acc_number FROM accounts")]:
                        amount = float(input("Enter the amount to transfer: "))
                        transfer(account_number, recipient_account, amount)
                    else:
                        print("Recipient's account not found!")
                else:
                    print("Cannot transfer to the same account!")
            elif choice == "5":
                print_transaction_history(account_number)
            elif choice == "6":
                new_pin = input("Enter new PIN: ")
                change_pin(account_number, new_pin)
            elif choice == "7":
                print_balance(account_number)
            elif choice == "8":
                print("Exiting ATM. Thank you!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

        else:
            print("Authentication failed. Invalid account number or PIN.")

        conn.close()

if __name__ == "__main__":
    main()
