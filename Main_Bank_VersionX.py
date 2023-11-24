'''
ATM Account - Class
Withdrawing cash, Depositing money, Balance
'''

class Account():
    def __init__(self, name:str, password:str, balance:int):
        if (balance <= 0):
            raise ValueError("balance must be positive")
        self.balance = balance
        self.password = password
        self.name = name

    def show(self):
        return self.balance
    
    def deposit(self, n:int):
        if (n <= 0):
            raise ValueError("n must be positive")
        self.balance += n
             
    def withdraw(self, n):
        if (n <= 0):
            raise ValueError("n must be positive")
        
        if (self.balance < n):
            raise ValueError("n must be less than or equal to balance")

        self.balance -= n