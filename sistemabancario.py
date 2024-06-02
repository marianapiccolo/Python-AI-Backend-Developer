# Sistema Bancario

menu = """
[d] = deposit
[w] = withdraw
[s] = statment
[e] = exit
"""

print(menu)

balance = 0
limit = 500
statment = ""
number_statments = 0
withdraw_limit = 3

while True:
    option= input("Enter your option:")

    if option == "d":
        print("Deposit")
        deposit = float(input("Enter how much you want to deposit"))

        if deposit > 0:
            print("$ {} deposited".format(deposit))
            balance = balance + deposit
        else:
            print("Invalid value")

    elif option == "w":
        print("Withdraw")
        withdraw = int(input("Enter how much you want to withdraw"))

        balance_exceeded = withdraw > balance

        limit_exceeded = withdraw > limit

        withdraw_exceeded = number_statments >= withdraw_limit

        if balance_exceeded:
            print("You don't have enough balance")

        if limit_exceeded:
            print("Withdrawal amount exceeds limit")

        if withdraw_exceeded:
            print("Maximum number of withdrawals exceeded")

        elif withdraw > 0:
            balance = balance - withdraw
            print("${} withdrawn".format(withdraw))
            number_statments = number_statments + 1
        
        else:
            print("Invalid value")
        
    elif option == "s":
        print("Statment")
        print("\nYour balance is ${}".format(balance))


    elif option == "e":
        break

    else:
        print("Invalid option. Try again")