# Separar em funções

# functions: deposit, withdraw, statement, create_user, filter_user, create_account, list_accounts

import textwrap

def menu ():
    menu = """\n 
    ========= MENU =========
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatment
    [na]\tNew Account
    [nu]\tNew User
    [la]\tList Accounts 
    [e]\tExit
    """
    # return the option inputed 
    return input(textwrap.dedent(menu))


def deposit (deposit_amount, balance, /):
    if deposit_amount > 0:
        balance = balance + deposit_amount
        print("\nDeposit of $ {} made successfully".format(deposit_amount))

    else:
        print("Operation failed. The value entered is invalid")
        
    return balance 

def withdraw(*, balance, withdraw_amount, limit, number_statments, withdraw_limit):
    balance_exceeded = withdraw_amount > balance

    limit_exceeded = withdraw_amount > limit

    withdraw_exceeded = number_statments >= withdraw_limit

    if balance_exceeded:
        print("You don't have enough balance")

    elif limit_exceeded:
        print("Withdrawal amount exceeds limit")

    elif withdraw_exceeded:
        print("Maximum number of withdrawals exceeded")

    elif withdraw_amount > 0:
        balance = balance - withdraw_amount
        print("${} withdrawn".format(withdraw_amount))
        number_statments = number_statments + 1
        
    else:
        print("Invalid value")
    return balance, number_statments

def statment(balance):
    print("Statment")
    print("Balance: ${}".format(balance))

def create_user(users):
    cpf = input("Inform your CPF (only numbers): ")
    user = filter_user(cpf, users)

    if user:
        print("\nThis user already exists")
        return
    name = input("Inform your complete name: ")
    date_of_birth = input("Inform your date of birth (dd-mm-yyyy): ")
    adress = input("Inform your adress: ")

    users.append({"name": name, "date_of_birth":date_of_birth, "cpf": cpf, "adress": adress})

    print("User created")

def filter_user(cpf, users):

    filtered_users = [user for user in users if user["cpf"] == cpf]
    #retorna o primeiro elemento porque ele vai achar apenas um usuario, nao pode ter mais de um cpf
    return filtered_users[0] if filtered_users else None 

def create_account(agency, account_number, users):
    cpf = input("Inform you cpf: ")
    user = filter_user(cpf, users)

    if user:
        print("Account created!")
        return {"agency": agency, "account_number": account_number, "user": user}
    
    print("User not found")

def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        
        row = print("Agency: {} \nAccount: {} \nOwner: {}".format(account["agency"], account["account_number"], account["user"]["name"]))

        print("=" * 100)
        
def main(): 
    AGENCY = "0001"
    WITHDRAW_LIMIT = 3
    balance = 0
    limit = 500
    number_statments = 0
    
    users = []
    accounts = []

    while True:
        option= menu()

        if option == "d":
        
            deposit_amount = int(input("Enter how much you want to deposit:\n"))
            balance = deposit(deposit_amount, balance)

        elif option == "w":
            print("Withdraw")
            withdraw_amount = int(input("Enter how much you want to withdraw\n"))
            balance, number_statments = withdraw(
                balance=balance,
                withdraw_amount=withdraw_amount,
                limit=limit,
                number_statments=number_statments,
                withdraw_limit=WITHDRAW_LIMIT
            )
       
        
        elif option == "s":
        
            statment(balance)

        elif option == "nu":
            create_user(users)

        elif option == "na":
            account_number = len(accounts) + 1 #deve iniciar com 1. Funciona porque neste codido nao excluimos contas
            account = create_account(AGENCY, account_number, users)

            if account:
                accounts.append(account)

        elif option == "la":
            list_accounts(accounts)
            
        elif option == "e":
            break

        else:
            print("Invalid option. Try again")
            
if __name__ == "__main__":
    main() 