import pytest
from Main_Bank_VersionX import Account

@pytest.mark.parametrize("name, password, balance", [
    ("John", "pass123", 100),
    ("Alice", "password", 0),
    ("Bob", "letmein", -50),
])
def test_account_contructor(name, password, balance):
    if balance <= 0:
        with pytest.raises(ValueError):
            account = Account(name, password, balance)
    else:
        account = Account(name, password, balance)
        assert account.name == name
        assert account.password == password
        assert account.balance == balance


@pytest.fixture
def mock_account():
    return Account("Test", "pass123", 100)


def test_show_method(mock_account):
    assert mock_account.show() == 100
    

@pytest.mark.parametrize("n", [0, -1, 500])
def test_deposit_method(mock_account, n):
    if n <= 0:
        with pytest.raises(ValueError):
            mock_account.deposit(n)
    else:
        currentBalance = mock_account.show()
        mock_account.deposit(n)
        assert mock_account.show() == currentBalance + n


@pytest.mark.parametrize("n", [0, -1, 500])
def test_withdraw_method(mock_account, n):
    if n <= 0:
        with pytest.raises(ValueError):
            mock_account.withdraw(n)
    else:
        currentBalance = mock_account.show()

        if (currentBalance < n):
            with pytest.raises(ValueError):
                mock_account.withdraw(n)
        else:
            mock_account.withdraw(n)
            assert mock_account.show() == currentBalance - n
