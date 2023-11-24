import pytest
from unittest.mock import patch, Mock

from Product import SavingsAccount, CreditAccount, UserAccount

#######################################################################
############ SavingsAccount ###########################################
@pytest.mark.parametrize("initial_balance", [None, 10, -10])
def test_savings_account_constructor(initial_balance):
    if initial_balance is None:
        account = SavingsAccount()
        assert account.product_type == "CASA"
        assert account.balance == 0
    elif initial_balance <= 0:
        with pytest.raises(ValueError):
            account = SavingsAccount(initial_balance)
    else:
        account = SavingsAccount(initial_balance)
        assert account.product_type == "CASA"
        assert account.balance == initial_balance

@pytest.fixture
def mock_savings_account():
    return SavingsAccount(100)


def test_savings_account_show_method(mock_savings_account):
    assert mock_savings_account.show_account_balance() == 100


@pytest.mark.parametrize("money", [10, -1, 500])
def test_savings_account_withdraw(mock_savings_account, money):
    if money <= 0:
        with pytest.raises(ValueError):
            mock_savings_account.withdraw(money)
    else:
        currentBalance = mock_savings_account.balance

        if (currentBalance < money):
            with pytest.raises(ValueError):
                mock_savings_account.withdraw(money)
        else:
            mock_savings_account.withdraw(money)
            assert mock_savings_account.balance == currentBalance - money


#######################################################################
############ CreditAccount ############################################
@pytest.mark.parametrize("credit_limit", [10, -10])
def test_credit_account_constructor(credit_limit):
    if credit_limit <= 0:
        with pytest.raises(ValueError):
            account = CreditAccount(credit_limit)
    else:
        account = CreditAccount(credit_limit)
        assert account.product_type == "Credit"
        assert account.credit_limit == credit_limit
        assert account.usage == 0


@pytest.fixture
def mock_credit_account():
    return CreditAccount(100)


def test_credit_account_show_method(mock_credit_account):
    assert mock_credit_account.show_account_balance() == 100


@pytest.mark.parametrize("money", [10, -1, 500])
def test_credit_account_withdraw(mock_credit_account, money):
    if money <= 0:
        with pytest.raises(ValueError):
            mock_credit_account.withdraw(money)
    else:
        currentBalance = mock_credit_account.credit_limit - mock_credit_account.usage

        if (currentBalance < money):
            with pytest.raises(ValueError):
                mock_credit_account.withdraw(money)
        else:
            mock_credit_account.withdraw(money)
            assert mock_credit_account.usage == money


#######################################################################
############ UserAccount ##############################################
@pytest.mark.parametrize(
    "initial_balance, credit_limit", 
    [
        [None, None],
        [0, None],
        [0, 100]
    ]
)
def test_user_account_constructor(initial_balance, credit_limit):
    if initial_balance is None:
        user_account = UserAccount()
        assert isinstance(user_account.savings_account, SavingsAccount)
        assert getattr(user_account, "credit_account", None) is None
    else:
        user_account = UserAccount(initial_balance, credit_limit)
        assert isinstance(user_account.savings_account, SavingsAccount)
        if credit_limit is None:
            assert getattr(user_account, "credit_account", None) is None
        else:
            assert isinstance(user_account.credit_account, CreditAccount)


@pytest.fixture
def user_account_with_credit():
    user_account = UserAccount()
    user_account.savings_account = Mock()
    user_account.savings_account.show_account_balance.return_value = 100
    user_account.credit_account = Mock()
    user_account.credit_account.show_account_balance.return_value = 100
    return user_account


@pytest.fixture
def user_account_without_credit():
    user_account = UserAccount()
    user_account.savings_account = Mock()
    user_account.savings_account.show_account_balance.return_value = 100
    return user_account


@pytest.mark.parametrize("product_type", ["Savings", "Credit"])
def test_user_account_with_credit_show_account_balance(user_account_with_credit, product_type):
    user_account_with_credit.show_account_balance(product_type)

    account = getattr(user_account_with_credit, f"{product_type.lower()}_account", None)
    account.show_account_balance.assert_called_once()


@pytest.mark.parametrize("product_type", ["Savings", "Credit"])
def test_user_account_without_credit_show_account_balance(user_account_without_credit, product_type):
    if product_type == "Credit":
        with pytest.raises(ValueError):
            user_account_without_credit.show_account_balance(product_type)
    else:
        user_account_without_credit.show_account_balance(product_type)
        account = getattr(user_account_without_credit, f"{product_type.lower()}_account", None)
        account.show_account_balance.assert_called_once()


@pytest.mark.parametrize(
    "product_type, money", 
    [
        ["Credit", 100],
        ["Credit", 200],
        ["Savings", 100],
        ["Savings", 200],
        ["Both", 100],
        ["Both", 300],
    ]
)
def test_user_account_with_credit_withdraw(user_account_with_credit, product_type, money):
    if money > 100:
        with pytest.raises(ValueError):
            user_account_with_credit.withdraw(product_type, money)
    elif product_type == "Both":
        user_account_with_credit.withdraw(product_type, money)
        user_account_with_credit.credit_account.withdraw.assert_called_once_with(100)
        user_account_with_credit.savings_account.withdraw.assert_called_once_with(0)
    else:
        user_account_with_credit.withdraw(product_type, money)
        account = getattr(user_account_with_credit, f"{product_type.lower()}_account", None)
        account.withdraw.assert_called_once_with(money)


@pytest.mark.parametrize(
    "product_type, money", 
    [
        ["Credit", 100],
        ["Credit", 200],
        ["Savings", 100],
        ["Savings", 200],
        ["Both", 100],
        ["Both", 300],
    ]
)
def test_user_account_without_credit_withdraw(user_account_without_credit, product_type, money):
    if product_type == "Credit" or product_type == "Both":
        with pytest.raises(ValueError):
            user_account_without_credit.withdraw(product_type, money)
    elif money > 100:
        with pytest.raises(ValueError):
            user_account_without_credit.withdraw(product_type, money)
    else:
        user_account_without_credit.withdraw(product_type, money)
        account = getattr(user_account_without_credit, f"{product_type.lower()}_account", None)
        account.withdraw.assert_called_once_with(money)