"""
Inventory Management System for Online Store
============================================
This system handles product inventory, orders and customers.
Your task is to identify the antipatterns present in this code.
"""

import json
import datetime
import random


global_products = {}
global_customers = {}
global_orders = []
global_configuration = None


class inventory_system:
    
    def __init__(self):
        self.products = global_products
        self.customers = global_customers
        self.orders = global_orders
        self.history = []
        self.statistics = {}
        self.alerts = []
        self.suppliers = {}
        self.invoices = []
        self.returns = []
        self.employees = {}
        self.reports = []
        self.audit = []
        self.configuration = global_configuration
        
    def process_everything(self, action, data):
        if action == "add_product":
            if "id" in data and "name" in data and "price" in data:
                if data["price"] > 0:
                    if data["id"] not in self.products:
                        self.products[data["id"]] = {
                            "name": data["name"],
                            "price": data["price"],
                            "stock": data.get("stock", 0),
                            "category": data.get("category", "general"),
                            "supplier": data.get("supplier", "unknown")
                        }
                        self.history.append(f"Producto {data['id']} agregado")
                        self.audit.append({
                            "action": "add_product",
                            "timestamp": datetime.datetime.now(),
                            "data": data
                        })
                        if self.products[data["id"]]["stock"] < 10:
                            self.alerts.append(f"Stock bajo para {data['name']}")
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
                
        elif action == "update_stock":
            if "id" in data and "quantity" in data:
                if data["id"] in self.products:
                    previous_stock = self.products[data["id"]]["stock"]
                    self.products[data["id"]]["stock"] += data["quantity"]
                    
                    if self.products[data["id"]]["stock"] < 0:
                        self.products[data["id"]]["stock"] = previous_stock
                        return False
                    
                    self.history.append(f"Stock actualizado para {data['id']}")
                    self.audit.append({
                        "action": "update_stock",
                        "timestamp": datetime.datetime.now(),
                        "data": data
                    })
                    
                    if self.products[data["id"]]["stock"] < 10:
                        self.alerts.append(f"Stock bajo para producto {data['id']}")
                    elif self.products[data["id"]]["stock"] > 1000:
                        self.alerts.append(f"Stock excesivo para producto {data['id']}")
                    
                    return True
                else:
                    return False
            else:
                return False
                
        elif action == "create_order":
            if "customer_id" in data and "items" in data:
                if data["customer_id"] in self.customers:
                    order_id = len(self.orders) + 1
                    total = 0
                    processed_items = []
                    
                    for item in data["items"]:
                        if item["product_id"] in self.products:
                            product = self.products[item["product_id"]]
                            if product["stock"] >= item["quantity"]:
                                subtotal = product["price"] * item["quantity"]
                                
                                if self.customers[data["customer_id"]]["type"] == "premium":
                                    if subtotal > 100:
                                        discount = subtotal * 0.15
                                    else:
                                        discount = subtotal * 0.10
                                elif self.customers[data["customer_id"]]["type"] == "regular":
                                    if subtotal > 200:
                                        discount = subtotal * 0.05
                                    else:
                                        discount = 0
                                else:
                                    discount = 0
                                
                                total += subtotal - discount
                                
                                self.products[item["product_id"]]["stock"] -= item["quantity"]
                                
                                processed_items.append({
                                    "product_id": item["product_id"],
                                    "quantity": item["quantity"],
                                    "unit_price": product["price"],
                                    "subtotal": subtotal,
                                    "discount": discount
                                })
                                
                                if self.products[item["product_id"]]["stock"] < 10:
                                    self.alerts.append(f"Stock bajo después de pedido para {item['product_id']}")
                            else:
                                return False
                        else:
                            return False
                    
                    new_order = {
                        "id": order_id,
                        "customer_id": data["customer_id"],
                        "items": processed_items,
                        "total": total,
                        "date": datetime.datetime.now(),
                        "status": "pending"
                    }
                    
                    self.orders.append(new_order)
                    self.history.append(f"Pedido {order_id} creado")
                    self.audit.append({
                        "action": "create_order",
                        "timestamp": datetime.datetime.now(),
                        "data": new_order
                    })
                    
                    self.customers[data["customer_id"]]["total_purchases"] += total
                    self.customers[data["customer_id"]]["num_orders"] += 1
                    
                    if self.customers[data["customer_id"]]["total_purchases"] > 1000:
                        self.customers[data["customer_id"]]["type"] = "premium"
                    
                    return order_id
                else:
                    return False
            else:
                return False
                
        elif action == "add_customer":
            if "id" in data and "name" in data and "email" in data:
                if data["id"] not in self.customers:
                    self.customers[data["id"]] = {
                        "name": data["name"],
                        "email": data["email"],
                        "type": "regular",
                        "total_purchases": 0,
                        "num_orders": 0,
                        "registration_date": datetime.datetime.now()
                    }
                    self.history.append(f"Cliente {data['id']} agregado")
                    self.audit.append({
                        "action": "add_customer",
                        "timestamp": datetime.datetime.now(),
                        "data": data
                    })
                    return True
                else:
                    return False
            else:
                return False
                
        elif action == "generate_report":
            total_products = len(self.products)
            total_customers = len(self.customers)
            total_orders = len(self.orders)
            
            inventory_value = 0
            for prod_id, prod in self.products.items():
                inventory_value += prod["price"] * prod["stock"]
            
            total_revenue = 0
            for order in self.orders:
                total_revenue += order["total"]
            
            report = {
                "date": datetime.datetime.now(),
                "total_products": total_products,
                "total_customers": total_customers,
                "total_orders": total_orders,
                "inventory_value": inventory_value,
                "total_revenue": total_revenue
            }
            
            self.reports.append(report)
            return report
        
        else:
            return None
    
    def get_product_by_name(self, name):
        for prod_id, prod in self.products.items():
            if prod["name"] == name:
                return prod
        return None
    
    def get_products_by_category(self, category):
        products_category = []
        for prod_id, prod in self.products.items():
            if prod["category"] == category:
                products_category.append(prod)
        return products_category
    
    def get_low_stock_products(self, limit=10):
        low_stock_products = []
        for prod_id, prod in self.products.items():
            if prod["stock"] < limit:
                low_stock_products.append(prod)
        return low_stock_products


def validate_customer_email(email):
    if not email:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if len(parts[0]) < 1:
        return False
    if len(parts[1]) < 3:
        return False
    if "." not in parts[1]:
        return False
    return True


def validate_supplier_email(email):
    if not email:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if len(parts[0]) < 1:
        return False
    if len(parts[1]) < 3:
        return False
    if "." not in parts[1]:
        return False
    return True


def validate_employee_email(email):
    if not email:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if len(parts[0]) < 1:
        return False
    if len(parts[1]) < 3:
        return False
    if "." not in parts[1]:
        return False
    return True


def calculate_electronics_discount(price, customer_type):
    if customer_type == "premium":
        if price > 1000:
            return price * 0.20
        elif price > 500:
            return price * 0.15
        else:
            return price * 0.10
    elif customer_type == "regular":
        if price > 1000:
            return price * 0.10
        elif price > 500:
            return price * 0.05
        else:
            return price * 0.02
    else:
        return 0


def calculate_clothing_discount(price, customer_type):
    if customer_type == "premium":
        if price > 200:
            return price * 0.25
        elif price > 100:
            return price * 0.20
        else:
            return price * 0.15
    elif customer_type == "regular":
        if price > 200:
            return price * 0.15
        elif price > 100:
            return price * 0.10
        else:
            return price * 0.05
    else:
        return 0


def calculate_books_discount(price, customer_type):
    if customer_type == "premium":
        if price > 50:
            return price * 0.30
        elif price > 30:
            return price * 0.20
        else:
            return price * 0.10
    elif customer_type == "regular":
        if price > 50:
            return price * 0.20
        elif price > 30:
            return price * 0.10
        else:
            return price * 0.05
    else:
        return 0


class cache_manager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(cache_manager, cls).__new__(cls)
            cls._instance.cache = {}
        return cls._instance
    
    def get(self, key):
        return self.cache.get(key)
    
    def save(self, key, value):
        self.cache[key] = value
    
    def clear(self):
        self.cache = {}


if __name__ == "__main__":
    system = inventory_system()
    
    system.process_everything("add_customer", {
        "id": "C001",
        "name": "Juan Pérez",
        "email": "juan@email.com"
    })
    
    system.process_everything("add_product", {
        "id": "P001",
        "name": "Laptop Gaming",
        "price": 1500,
        "stock": 5,
        "category": "electronics"
    })
    
    system.process_everything("create_order", {
        "customer_id": "C001",
        "items": [
            {"product_id": "P001", "quantity": 1}
        ]
    })
    
    report = system.process_everything("generate_report", {})
    print("Sistema iniciado. Identifica los antipatrones en este código.")