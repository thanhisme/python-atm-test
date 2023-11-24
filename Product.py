from abc import ABC, abstractmethod


class Product(ABC):
    @abstractmethod
    def show_account_balance(self):
        pass


    @abstractmethod
    def withdraw(self):
        pass


class SavingsAccount(Product):
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("initial balance must be positive")
        self.product_type = "CASA"
        self.balance = initial_balance


    def show_account_balance(self):
        return self.balance
    

    def withdraw(self, money):
        if (money <= 0):
            raise ValueError("money must be positive")
        if (self.balance < money):
            raise ValueError("The money to be withdrawed must be less than the balance")
        self.balance = self.balance - money


class CreditAccount(Product):
    def __init__(self, credit_limit):
        if credit_limit <= 0:
            raise ValueError("credit limit must be positive")
        self.product_type = "Credit"
        self.credit_limit = credit_limit
        self.usage = 0


    def show_account_balance(self):
        return self.credit_limit - self.usage


    def withdraw(self, money):
        if (money <= 0):
            raise ValueError("money must be positive")
        if (self.credit_limit < (money + self.usage)):
            raise ValueError("You have not enougn credit to perform withdraw")
        self.usage = self.usage + money


class UserAccount:
    def __init__(self, initial_balance=0, credit_limit=None):
        self.savings_account = SavingsAccount(initial_balance)
        if credit_limit is not None:
            self.credit_account = CreditAccount(credit_limit)


    def show_account_balance(self, type):
        if type == "Credit" and getattr(self, 'credit_account', None) is None:
            raise ValueError("You dont have a credit account")

        if type == "Credit":
            return self.credit_account.show_account_balance()

        return self.savings_account.show_account_balance()


    def withdraw(self, type, money):
        if (type == "Credit" or type == "Both") and getattr(self, 'credit_account', None) is None:
            raise ValueError("You dont have a credit account")
        if type == "Credit":
            if self.credit_account.show_account_balance() < money:
                raise ValueError("You dont have enough credit to withdraw")
            self.credit_account.withdraw(money)
        elif type == "Savings":
            if self.savings_account.show_account_balance() < money:
                raise ValueError("You dont have enough money to withdraw")
            self.savings_account.withdraw(money)
        elif type == "Both":
            savings_account_balance = self.savings_account.show_account_balance()
            credit_account_balance = self.credit_account.show_account_balance()
            available_money = savings_account_balance + credit_account_balance

            if available_money < money:
                raise ValueError("You dont have enough money to withdraw")
            self.credit_account.withdraw(money if credit_account_balance > money else credit_account_balance)
            self.savings_account.withdraw(0 if credit_account_balance > money else money - credit_account_balance)