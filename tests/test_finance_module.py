import pytest
from unittest.mock import MagicMock
from FinanceModule import FinanceModule
from Tables import Sales, Revenue  

@pytest.fixture
def finance_module():
    fm = FinanceModule()
    fm.db_handler = MagicMock()  # Mock database
    fm.logger = MagicMock()  # Mock logger
    return fm

def test_get_sales(finance_module):
    finance_module.db_handler.fetch.return_value = [{"amount": 100}]
    result = finance_module.get_sales("test@example.com")
    assert result == [{"amount": 100}]
    finance_module.db_handler.fetch.assert_called_once_with(Sales, {"user": "test@example.com"})

def test_get_revenue(finance_module):
    finance_module.db_handler.fetch.return_value = [{"revenue": 500}]
    result = finance_module.get_revenue("test@example.com")
    assert result == [{"revenue": 500}]
    finance_module.db_handler.fetch.assert_called_once_with(Revenue, {"user": "test@example.com"})
