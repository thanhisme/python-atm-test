'''
BANK MANAGEMENT
Through the terminal interface the user can do some common bank operations as:
* open and close a bank account
* view the balance
* deposit and withdraw
* check the bank account infos
* (admin) check the user accounts
Made by Alessandro Silvestri - 2023 <alessandro.silvestri.work@gmail.com>
'''

from Main_Bank_VersionX import Account

class Bank():
    def __init__(self):
        self.accountsDict = {}
        self.counter = 0
    
    def createAccount(self, name, password, money):
        '''method that will be used in open_account method'''
        oAccount = Account(name, password, money)
        self.accountsDict[self.counter] = oAccount
        self.counter += 1
    
    def open_account(self):
        '''creating a new account with interaction'''
        print("\n*** Open Account ***")
        name = input("Insert your name: ")
        pw = input("Insert your pw: ")
        first_amount = int(input("Insert amount £: "))
        if first_amount < 0:
            raise ValueError("Amount must be positive")
        self.createAccount(name=name, password=pw, money=first_amount)

    def closeAccount(self):
        '''eliminate an account and check if there are funds'''
        print("\n*** Close Account ***")
        account_number = int(input("Insert the account number: "))
        if account_number > len(self.accountsDict) - 1 or account_number < 0:
            raise ValueError("Account number not found")
        pw = input("Insert your password: ")
        if pw == self.accountsDict[account_number].password:
            print(f"pw ok!")
            if self.accountsDict[account_number].balance > 0:
                print(f"You had {self.accountsDict[account_number].balance} in your bank account wich they will return to you")
            self.accountsDict.pop(account_number)
            print(f"Account: {account_number} eliminated")
        else:
            print("wrong password\nprogram ended")

    def balance(self):
        '''it shows the balance of a single account'''
        print("\n*** Balance ***")
        account_number = input("Insert the account number: ")
        if (not account_number[0].isnumeric() or int(account_number[0]) < 0 or int(account_number[0]) > len(self.accountsDict) - 1):
            raise ValueError("Account number is invalid")
        account_number = int(account_number)
        pw = input("Insert your password: ")
        if pw == self.accountsDict[account_number].password:
            print("pw ok!")
            print(f"Balance: {self.accountsDict[account_number].show()}")
        else:
            print("wrong password\nprogram ended")

    def deposit(self):
        '''deposit in the account'''
        print("\n*** Deposit ***")
        account_number = input("Insert the account number: ")
        if (not account_number.isnumeric() or int(account_number) < 0 or int(account_number) > len(self.accountsDict) - 1):
            raise ValueError("Account number is invalid")
        account_number = int(account_number)
        pw = input("Insert your password: ")
        if pw == self.accountsDict[account_number].password:
            print("pw ok!")
            deposit = input("insert the amount you want deposit: ")
            if (not deposit.isnumeric() or int(deposit) <= 0):
                raise ValueError("deposit must be positive")
            self.accountsDict[account_number].deposit(deposit)
            print(f"deposit of {deposit} done!")
        else:
            print("wrong password\nprogram ended")

    def withdraw(self):
        '''withdraw '''
        print("\n*** Withdraw ***")
        account_number = input("Insert the account number: ")
        if (not account_number.isnumeric() or int(account_number) < 0 or int(account_number) > len(self.accountsDict) - 1):
            raise ValueError("Account number is invalid")
        account_number = int(account_number)
        pw = input("Insert your password: ")
        if pw == self.accountsDict[account_number].password:
            print("pw ok!")
            wit = input("insert the withdraw amount: ")
            if (not wit.isnumeric() or int(wit) > self.accountsDict[account_number].balance):
                raise ValueError("deposit must be smaller than balance")
            self.accountsDict[account_number].withdraw(wit)
            print(f"withdraw of {wit} done!")
        else:
            print("wrong password\nprogram ended")
    
    def show(self):
        '''show the info of a specific account: num, name, funds'''
        print("\n*** Show info account ***")
        account_number = input("Insert the account number: ")
        if (not account_number.isnumeric() or int(account_number) < 0 or int(account_number) > len(self.accountsDict) - 1):
            raise ValueError("Account number is invalid")
        account_number = int(account_number)
        pw = input("Insert your password: ")
        if pw == self.accountsDict[account_number].password:
            print("pw ok!")
            name = self.accountsDict[account_number].name
            balance = self.accountsDict[account_number].balance
            print(f"Account N: {account_number} Name: {name} Balance: {balance}")
        else:
            print("wrong password\nprogram ended")
            raise ValueError("Wrong password")

    def show_all_account(self):
        '''for debug/admin'''
        print("\n*** Accounts list ***")
        if len(self.accountsDict) == 0:
            print("<empty>")
        else:    
            for i, j in self.accountsDict.items():
                print(f"N.:{i} Name: {j.name} Pw: {j.password} Balance: {j.balance}")

