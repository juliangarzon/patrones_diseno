"""
Banking Services API
====================
This API handles basic banking operations.
Identify the antipatterns and design problems in this code.
"""

import time
import hashlib
from datetime import datetime


bank_accounts = {}
global_transactions = []
system_configuration = {
    "currency": "USD",
    "transfer_limit": 10000,
    "commission": 0.02
}


class banking_service:
    
    def __init__(self):
        self.accounts = bank_accounts
        self.transactions = global_transactions
        self.sessions = {}
        self.logs = []
        self.notifications = []
        self.limits = {}
        self.blocks = {}
        self.failed_attempts = {}
        
    def execute_operation(self, operation, parameters):
        self.logs.append(f"{datetime.now()}: Ejecutando {operation}")
        
        if operation == "create_account":
            account_number = parameters.get("account_number")
            holder = parameters.get("holder")
            type = parameters.get("type", "savings")
            initial_balance = parameters.get("initial_balance", 0)
            
            if account_number and holder:
                if account_number not in self.accounts:
                    self.accounts[account_number] = {
                        "holder": holder,
                        "type": type,
                        "balance": initial_balance,
                        "opening_date": datetime.now(),
                        "status": "active",
                        "transactions": []
                    }
                    
                    if type == "savings":
                        self.accounts[account_number]["interest"] = 0.02
                        self.accounts[account_number]["daily_withdrawal_limit"] = 1000
                    elif type == "checking":
                        self.accounts[account_number]["interest"] = 0.001
                        self.accounts[account_number]["daily_withdrawal_limit"] = 5000
                    elif type == "business":
                        self.accounts[account_number]["interest"] = 0.005
                        self.accounts[account_number]["daily_withdrawal_limit"] = 50000
                    
                    self.notifications.append({
                        "account": account_number,
                        "message": "Cuenta creada exitosamente",
                        "timestamp": datetime.now()
                    })
                    
                    return {"success": True, "account_number": account_number}
                else:
                    return {"success": False, "error": "La cuenta ya existe"}
            else:
                return {"success": False, "error": "Datos incompletos"}
        
        elif operation == "deposit":
            account_number = parameters.get("account_number")
            amount = parameters.get("amount")
            
            if account_number in self.accounts:
                if amount > 0:
                    previous_balance = self.accounts[account_number]["balance"]
                    self.accounts[account_number]["balance"] += amount
                    
                    transaction = {
                        "id": len(self.transactions) + 1,
                        "type": "deposit",
                        "account": account_number,
                        "amount": amount,
                        "previous_balance": previous_balance,
                        "new_balance": self.accounts[account_number]["balance"],
                        "date": datetime.now()
                    }
                    
                    self.transactions.append(transaction)
                    self.accounts[account_number]["transactions"].append(transaction["id"])
                    
                    if amount > 10000:
                        self.notifications.append({
                            "account": account_number,
                            "message": "Depósito grande detectado",
                            "timestamp": datetime.now()
                        })
                    
                    return {"success": True, "new_balance": self.accounts[account_number]["balance"]}
                else:
                    return {"success": False, "error": "Monto inválido"}
            else:
                return {"success": False, "error": "Cuenta no encontrada"}
        
        elif operation == "withdraw":
            account_number = parameters.get("account_number")
            amount = parameters.get("amount")
            
            if account_number in self.accounts:
                account = self.accounts[account_number]
                
                if account["status"] != "active":
                    return {"success": False, "error": "Cuenta no activa"}
                
                if amount > 0 and amount <= account["balance"]:
                    daily_limit = account.get("daily_withdrawal_limit", 1000)
                    
                    withdrawals_today = 0
                    for trans_id in account["transactions"]:
                        for trans in self.transactions:
                            if trans["id"] == trans_id and trans["type"] == "withdrawal":
                                if trans["date"].date() == datetime.now().date():
                                    withdrawals_today += trans["amount"]
                    
                    if withdrawals_today + amount > daily_limit:
                        return {"success": False, "error": "Límite diario excedido"}
                    
                    previous_balance = account["balance"]
                    account["balance"] -= amount
                    
                    transaction = {
                        "id": len(self.transactions) + 1,
                        "type": "withdrawal",
                        "account": account_number,
                        "amount": amount,
                        "previous_balance": previous_balance,
                        "new_balance": account["balance"],
                        "date": datetime.now()
                    }
                    
                    self.transactions.append(transaction)
                    account["transactions"].append(transaction["id"])
                    
                    return {"success": True, "new_balance": account["balance"]}
                else:
                    return {"success": False, "error": "Saldo insuficiente"}
            else:
                return {"success": False, "error": "Cuenta no encontrada"}
        
        elif operation == "transfer":
            source_account = parameters.get("source_account")
            destination_account = parameters.get("destination_account")
            amount = parameters.get("amount")
            
            if source_account in self.accounts and destination_account in self.accounts:
                if source_account != destination_account:
                    if amount > 0:
                        commission = amount * system_configuration["commission"]
                        total_amount = amount + commission
                        
                        if self.accounts[source_account]["balance"] >= total_amount:
                            if amount <= system_configuration["transfer_limit"]:
                                previous_balance_source = self.accounts[source_account]["balance"]
                                previous_balance_destination = self.accounts[destination_account]["balance"]
                                
                                self.accounts[source_account]["balance"] -= total_amount
                                self.accounts[destination_account]["balance"] += amount
                                
                                outgoing_transaction = {
                                    "id": len(self.transactions) + 1,
                                    "type": "transfer_out",
                                    "account": source_account,
                                    "destination_account": destination_account,
                                    "amount": amount,
                                    "commission": commission,
                                    "previous_balance": previous_balance_source,
                                    "new_balance": self.accounts[source_account]["balance"],
                                    "date": datetime.now()
                                }
                                
                                self.transactions.append(outgoing_transaction)
                                self.accounts[source_account]["transactions"].append(outgoing_transaction["id"])
                                
                                incoming_transaction = {
                                    "id": len(self.transactions) + 1,
                                    "type": "transfer_in",
                                    "account": destination_account,
                                    "source_account": source_account,
                                    "amount": amount,
                                    "previous_balance": previous_balance_destination,
                                    "new_balance": self.accounts[destination_account]["balance"],
                                    "date": datetime.now()
                                }
                                
                                self.transactions.append(incoming_transaction)
                                self.accounts[destination_account]["transactions"].append(incoming_transaction["id"])
                                
                                return {"success": True, "commission": commission}
                            else:
                                return {"success": False, "error": "Monto excede límite"}
                        else:
                            return {"success": False, "error": "Saldo insuficiente"}
                    else:
                        return {"success": False, "error": "Monto inválido"}
                else:
                    return {"success": False, "error": "Misma cuenta"}
            else:
                return {"success": False, "error": "Cuenta no encontrada"}
        
        elif operation == "check_balance":
            account_number = parameters.get("account_number")
            
            if account_number in self.accounts:
                return {
                    "success": True,
                    "balance": self.accounts[account_number]["balance"],
                    "type": self.accounts[account_number]["type"]
                }
            else:
                return {"success": False, "error": "Cuenta no encontrada"}
        
        else:
            return {"success": False, "error": "Operación no válida"}


def calculate_savings_interest(balance, months):
    monthly_interest = 0.02 / 12
    for i in range(months):
        interest = balance * monthly_interest
        balance += interest
    return balance


def calculate_checking_interest(balance, months):
    monthly_interest = 0.001 / 12
    for i in range(months):
        interest = balance * monthly_interest
        balance += interest
    return balance


def calculate_business_interest(balance, months):
    monthly_interest = 0.005 / 12
    for i in range(months):
        interest = balance * monthly_interest
        balance += interest
    return balance


def validate_account_number(number):
    if not number:
        return False
    if len(number) != 10:
        return False
    if not number.isdigit():
        return False
    return True


def validate_card_number(number):
    if not number:
        return False
    if len(number) != 16:
        return False
    if not number.isdigit():
        return False
    return True


def validate_cvv(cvv):
    if not cvv:
        return False
    if len(cvv) != 3:
        return False
    if not cvv.isdigit():
        return False
    return True


class notification_handler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(notification_handler, cls).__new__(cls)
            cls._instance.notifications = []
            cls._instance.configuration = {}
        return cls._instance
    
    def send(self, recipient, message):
        self.notifications.append({
            "recipient": recipient,
            "message": message,
            "timestamp": datetime.now()
        })
    
    def get_all(self):
        return self.notifications
    
    def clear(self):
        self.notifications = []


class log_handler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(log_handler, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance
    
    def log(self, message):
        self.logs.append({
            "message": message,
            "timestamp": datetime.now()
        })
    
    def get_all(self):
        return self.logs


if __name__ == "__main__":
    service = banking_service()
    
    result = service.execute_operation("create_account", {
        "account_number": "1234567890",
        "holder": "Ana García",
        "type": "savings",
        "initial_balance": 1000
    })
    
    print("API Bancaria iniciada. Encuentra los antipatrones.")