###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional, Union


class TransactionType(str, Enum):
    
    Deposit = "Deposit"
    Withdrawal = "Withdrawal"
    Other = "Other"

class EndingBalanceItem(BaseModel):
    
    
    date: str
    amount: float

class FinancialSummary(BaseModel):
    
    
    bank_name: str
    business_name: str
    business_account_number: str
    business_address: str
    beginning_balance: float
    ending_balances: List["EndingBalanceItem"]

class PageHasTransactions(BaseModel):
    
    
    page_number: int
    has_transactions: bool

class Transaction(BaseModel):
    
    
    date: str
    description: Union[str, Optional[None]]
    amount: float
    transaction_type: "TransactionType"
