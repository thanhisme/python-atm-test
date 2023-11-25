import pytest
from unittest.mock import patch, Mock
from Main_Bank_VersionX import Account
from Bank import Bank

@pytest.mark.parametrize(
    "input_values", 
    [
        ['John', 'pass123', '100'],
        ['John', 'pass123', '-1'],
        ['John', 'pass123', 'abc'],
    ]
)
@patch('builtins.input')
def test_open_account(mock_input, input_values):
    mock_input.side_effect = input_values
    bank = Bank()

    if not input_values[2].isnumeric() or int(input_values[2]) < 0:
        with pytest.raises(ValueError):
            bank.open_account()

            assert len(bank.accountsDict) == 0
    else:
        bank.open_account()

        assert len(bank.accountsDict) == 1
        account = list(bank.accountsDict.values())[0]
        assert isinstance(account, Account)
        assert account.name == 'John'
        assert account.password == 'pass123'
        assert account.balance == 100


@pytest.fixture
def mock_account():
    account = Account('John', 'pass123', 100)
    return account


@pytest.fixture
def bank_with_mock_account(mock_account):
    bank = Bank()
    bank.accountsDict = {0: mock_account}
    return bank


@pytest.mark.parametrize(
    "input_values", 
    [
        ['0', 'pass123'], 
        ['abc', 'pass123'], 
        ['-1', 'pass123'], 
        ['0', 'another_pass'], 
        ['1', 'another_pass']
    ]
)
@patch('builtins.input')
def test_close_account(mock_input, input_values, bank_with_mock_account, capsys):
    mock_input.side_effect = input_values
    if not input_values[0].isnumeric() or int(input_values[0]) != 0:
        with pytest.raises(ValueError):
            bank_with_mock_account.closeAccount()

            assert total_accounts == 1
    else:
        bank_with_mock_account.closeAccount()
        total_accounts = len(bank_with_mock_account.accountsDict)
        captured = capsys.readouterr()

        if (input_values[1] != 'pass123'):
            assert total_accounts == 1
            assert "wrong password\nprogram ended" in captured.out
        else:
            assert "You had 100 in your bank account wich they will return to you" in captured.out
            assert "Account: 0 eliminated" in captured.out
            assert total_accounts == 0


@pytest.mark.parametrize(
    "input_values", 
    [
        ['0', 'pass123'], 
        ['abc', 'pass123'], 
        ['-1', 'pass123'], 
        ['0', 'another_pass'], 
        ['1', 'another_pass']
    ]
)
@patch('builtins.input')
def test_balance(mock_input, input_values, bank_with_mock_account, capsys):
    mock_input.side_effect = input_values
    mock_account = bank_with_mock_account.accountsDict[0]

    if not input_values[0].isnumeric() or int(input_values[0]) != 0:
        with pytest.raises(ValueError):
            bank_with_mock_account.balance()
            captured = capsys.readouterr()
    else:
        bank_with_mock_account.balance()
        captured = capsys.readouterr()

        if (input_values[1] != 'pass123'):
            assert "wrong password\nprogram ended" in captured.out
        else:
            assert "Balance: 100" in captured.out


@pytest.mark.parametrize(
    "input_values", 
    [
        ['0', 'pass123', '0'],
        ['0', 'pass123', '-1'],
        ['0', 'pass123', 'abc'],
        ['0', 'pass123', '500'],
        ['abc', 'pass123', '10'], 
        ['-1', 'pass123', '10'], 
        ['0', 'another_pass', '10'], 
        ['1', 'another_pass', '10']
    ]
)
@patch('builtins.input')
def test_deposit(mock_input, input_values, bank_with_mock_account, capsys):
    mock_input.side_effect = input_values
    mock_account = bank_with_mock_account.accountsDict[0]

    if not input_values[0].isnumeric() or int(input_values[0]) != 0 or not input_values[2].isnumeric() or int(input_values[2]) <= 0 or int(input_values[2]) > 100:
        with pytest.raises(ValueError):
            bank_with_mock_account.deposit()
    else:
        bank_with_mock_account.deposit()
        captured = capsys.readouterr()

        if (input_values[1] != 'pass123'):
            assert "wrong password\nprogram ended" in captured.out
        else:
            assert "Balance: 100" in captured.out


@pytest.mark.parametrize(
    "input_values", 
    [
        ['0', 'pass123', '0'],
        ['0', 'pass123', '-1'],
        ['0', 'pass123', 'abc'],
        ['0', 'pass123', '10'],
        ['abc', 'pass123', '10'], 
        ['-1', 'pass123', '10'], 
        ['0', 'another_pass', '10'], 
        ['1', 'another_pass', '10']
    ]
)
@patch('builtins.input')
def test_withdraw(mock_input, input_values, bank_with_mock_account, capsys):
    mock_input.side_effect = input_values
    mock_account = bank_with_mock_account.accountsDict[0]

    if not input_values[0].isnumeric() or int(input_values[0]) != 0 or not input_values[2].isnumeric() or int(input_values[2]) > mock_account.balance or int(input_values[2]) <= 0:
        with pytest.raises(ValueError):
            bank_with_mock_account.withdraw()
    else:
        bank_with_mock_account.withdraw()
        captured = capsys.readouterr()

        if (input_values[1] != 'pass123'):
            assert "wrong password\nprogram ended" in captured.out
        else:
            assert "withdraw of 10 done!" in captured.out


def test_show_all_accounts_empty(capsys):
    bank = Bank()
    bank.show_all_account()
    captured = capsys.readouterr()

    assert "<empty>" in captured.out


def test_show_all_accounts(bank_with_mock_account, capsys):
    bank_with_mock_account.show_all_account()
    captured = capsys.readouterr()

    assert "N.:0 Name: John Pw: pass123 Balance: 100" in captured.out