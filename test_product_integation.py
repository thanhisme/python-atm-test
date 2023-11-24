# create account
# 1. invalid initial balance/invalid credit limit| 
import pytest
from Product import UserAccount, SavingsAccount, CreditAccount

@pytest.mark.parametrize(
    "initial_balance, credit_limit", 
    [
        [None, None],
        [0, None],
        [0, 100]
    ]
)
def test_credit_account(initial_balance, credit_limit):
    if initial_balance is None:
        user_account = UserAccount()
        assert isinstance(user_account.savings_account, SavingsAccount)
        assert user_account.savings_account.show_account_balance() == 0
        assert getattr(user_account, "credit_account", None) is None
    else:
        user_account = UserAccount(initial_balance, credit_limit)
        assert isinstance(user_account.savings_account, SavingsAccount)
        assert user_account.savings_account.show_account_balance() == 0

        if credit_limit is None:
            assert getattr(user_account, "credit_account", None) is None
        else:
            assert isinstance(user_account.credit_account, CreditAccount)
            assert user_account.credit_account.show_account_balance() == 100


@pytest.fixture
def mock_user_account_without_credit():
    user_account = UserAccount(100)
    return user_account


@pytest.fixture
def mock_user_account_with_credit():
    user_account = UserAccount(100, 100)
    return user_account


@pytest.mark.parametrize("product_type", ["Savings", "Credit"])
def test_user_account_with_credit_show_account_balance(mock_user_account_with_credit, product_type):
    balance = mock_user_account_with_credit.show_account_balance(product_type)

    assert balance == 100


@pytest.mark.parametrize("product_type", ["Savings", "Credit"])
def test_user_account_without_credit_show_account_balance(mock_user_account_without_credit, product_type):
    if product_type == "Credit":
        with pytest.raises(ValueError):
            mock_user_account_without_credit.show_account_balance(product_type)
    else:
        balance = mock_user_account_without_credit.show_account_balance(product_type)
        assert balance == 100


@pytest.mark.parametrize(
    "product_type, money", 
    [
        ["Credit", 100],
        ["Credit", 200],
        ["Savings", 100],
        ["Savings", 200],
        ["Both", 110],
        ["Both", 300],
    ]
)
def test_user_account_with_credit_withdraw(mock_user_account_with_credit, product_type, money):
    if (money > 100 and product_type != "Both") or (product_type == "Both" and money > 200):
        with pytest.raises(ValueError):
            mock_user_account_with_credit.withdraw(product_type, money)
    elif product_type == "Both":
        mock_user_account_with_credit.withdraw(product_type, money)
        
        assert mock_user_account_with_credit.credit_account.show_account_balance() == 0
        assert mock_user_account_with_credit.savings_account.show_account_balance() == 90
    else:
        mock_user_account_with_credit.withdraw(product_type, money)
        account = getattr(mock_user_account_with_credit, f"{product_type.lower()}_account", None)
        assert account.show_account_balance() == 0


@pytest.mark.parametrize(
    "product_type, money", 
    [
        ["Credit", 100],
        ["Credit", 200],
        ["Savings", 100],
        ["Savings", 200],
        ["Both", 110],
        ["Both", 300],
    ]
)
def test_user_account_without_credit_withdraw(mock_user_account_without_credit, product_type, money):
    if product_type == "Credit" or product_type == "Both":
        with pytest.raises(ValueError):
            mock_user_account_without_credit.withdraw(product_type, money)
    elif money > 100:
        with pytest.raises(ValueError):
            mock_user_account_without_credit.withdraw(product_type, money)
    else:
        mock_user_account_without_credit.withdraw(product_type, money)
        assert mock_user_account_without_credit.savings_account.show_account_balance() == 0