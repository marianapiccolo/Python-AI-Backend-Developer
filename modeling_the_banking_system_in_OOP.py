import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def make_transactions(self, account, transaction):
        transaction.register(account)
        
    def add_account(self, account):
        self.accounts.append(account)

class Individual(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf

class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._historic = Historic()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def historic(self):
        return self._historic
  
    def withdraw(self, amount):
        balance = self.balance
        exceeded_balance = amount > balance

        if exceeded_balance:
            print("\n@@@ Operation failed! You do not have enough balance. @@@")
            return False

        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal successful! ===")
            return True

        else:
            print("\n@@@ Operation failed! The specified amount is invalid. @@@")
            return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit successful! ===")
            return True

        else:
            print("\n@@@ Operation failed! The specified amount is invalid. @@@")
            return False

class CurrentAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        number_of_withdrawals = len(
            [transaction for transaction in self.historic.transactions if transaction["type"] == Withdrawal.__name__]
        )

        exceeded_limit = amount > self.limit
        exceeded_withdrawals = number_of_withdrawals >= self.withdrawal_limit

        if exceeded_limit:
            print("\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@")
            return False

        elif exceeded_withdrawals:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")
            return False

        else:
            return super().withdraw(amount)

    def __str__(self):
        return textwrap.dedent(f"""\
            Agency:\t{self.agency}
            A/C:\t\t{self.number}
            Account Holder:\t{self.client.name}
        """)

class Historic:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction.value,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transaction(ABC):
    @abstractmethod
    def value(self):
        pass
    
    @abstractmethod
    def register(self, account):
        pass

class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        transaction_successful = account.withdraw(self.value)

        if transaction_successful:
            account.historic.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        transaction_successful = account.deposit(self.value)

        if transaction_successful:
            account.historic.add_transaction(self)

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [na]\tNew Account
    [la]\tList Accounts
    [nc]\tNew Client
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu))

def filter_client(cpf, clients):
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None

def get_client_account(client):
    if not client.accounts:
        print("\n@@@ Client does not have an account! @@@")
        return

    # FIXME: does not allow the client to choose the account
    return client.accounts[0]

def deposit(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    amount = float(input("Enter the deposit amount: "))
    transaction = Deposit(amount)

    account = get_client_account(client)
    if not account:
        return

    client.make_transactions(account, transaction)

def withdraw(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    amount = float(input("Enter the withdrawal amount: "))
    transaction = Withdrawal(amount)

    account = get_client_account(client)
    if not account:
        return

    client.make_transactions(account, transaction)

def show_statement(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    account = get_client_account(client)
    if not account:
        return

    print("\n================ STATEMENT ================")
    transactions = account.historic.transactions

    statement = ""
    if not transactions:
        statement = "No transactions made."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\t$ {transaction['value']:.2f}"

    print(statement)
    print(f"\nBalance:\n\t$ {account.balance:.2f}")
    print("==========================================")

def create_client(clients):
    cpf = input("Enter the CPF (numbers only): ")
    client = filter_client(cpf, clients)

    if client:
        print("\n@@@ A client with this CPF already exists! @@@")
        return

    name = input("Enter the full name: ")
    birth_date = input("Enter the birth date (dd-mm-yyyy): ")
    address = input("Enter the address (street, number - neighborhood - city/state abbreviation): ")

    client = Individual(name=name, birth_date=birth_date, cpf=cpf, address=address)

    clients.append(client)

    print("\n=== Client successfully created! ===")

def create_account(account_number, clients, accounts):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found, account creation process terminated! @@@")
        return

    account = CurrentAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print("\n=== Account successfully created! ===")

def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))

def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            deposit(clients)

        elif option == "w":
            withdraw(clients)

        elif option == "s":
            show_statement(clients)

        elif option == "nc":
            create_client(clients)

        elif option == "na":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("\n@@@ Invalid operation, please select the desired operation again. @@@")


main()
