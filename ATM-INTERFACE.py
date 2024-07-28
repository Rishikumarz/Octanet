class Account:

    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)


class Transaction:

    def __init__(self, type, amount):
        self.type = type
        self.amount = amount


class Bank:

    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        self.accounts[account.user_id] = account

    def validate_login(self, user_id, pin):
        return user_id in self.accounts and self.accounts[user_id].pin == pin

    def get_account(self, user_id):
        return self.accounts.get(user_id)


class ATM:

    def __init__(self, bank):
        self.bank = bank
        self.current_user_id = None

    def start(self):
        user_id = input("Enter your user ID: ")
        pin = input("Enter your PIN: ")
        if self.bank.validate_login(user_id, pin):
            self.current_user_id = user_id
            print("Login successful!")
            self.show_menu()
        else:
            print("Invalid credentials!")

    def show_menu(self):
        while True:
            print(
                "\n1. Transactions History\n2. Withdraw\n3. Deposit\n4. Transfer\n5. Quit"
            )
            choice = input("Choose an option: ")
            if choice == "1":
                self.show_transactions()
            elif choice == "2":
                self.withdraw()
            elif choice == "3":
                self.deposit()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                print("Thank you for using the ATM. Goodbye!")
                self.current_user_id = None
                break
            else:
                print("Invalid option!")

    def show_transactions(self):
        account = self.bank.get_account(self.current_user_id)
        if account.transactions:
            for transaction in account.transactions:
                print(
                    f"Type: {transaction.type}, Amount: {transaction.amount}")
        else:
            print("No transactions found.")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        account = self.bank.get_account(self.current_user_id)
        if account and account.balance >= amount:
            account.balance -= amount
            account.add_transaction(Transaction("Withdraw", amount))
            print(f"Withdrawn: {amount}. New Balance: {account.balance}")
        else:
            print("Insufficient funds or invalid account.")

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        account = self.bank.get_account(self.current_user_id)
        if account:
            account.balance += amount
            account.add_transaction(Transaction("Deposit", amount))
            print(f"Deposited: {amount}. New Balance: {account.balance}")

    def transfer(self):
        recipient_id = input("Enter receiver's user ID: ")
        amount = float(input("Enter amount to transfer: "))
        sender_account = self.bank.get_account(self.current_user_id)
        recipient_account = self.bank.get_account(recipient_id)

        if sender_account and recipient_account and sender_account.balance >= amount:
            sender_account.balance -= amount
            sender_account.add_transaction(Transaction("Transfer Out", amount))
            recipient_account.balance += amount
            recipient_account.add_transaction(
                Transaction("Transfer In", amount))
            print(
                f"Transferred: {amount} to {recipient_id}. New Balance: {sender_account.balance}"
            )
        else:
            print("Transfer failed. Check recipient ID or your balance.")


def main():
    bank = Bank()
    bank.add_account(Account("user1", "1234", 10000))
    bank.add_account(Account("user2", "5678", 15000))

    atm = ATM(bank)
    atm.start()


if __name__ == "__main__":
    main()
