"""
Demonstrative example of common antipatterns in Python
This code contains several antipatterns for educational purposes
DO NOT use these practices in real code
"""

import time
from typing import List, Dict, Any


class data_manager:
    """Antipattern 1: GOD OBJECT - This class does too many things"""
    
    def __init__(self):
        self.db_connection = None
        self.user_data = {}
        self.configuration = {}
        self.logs = []
        self.cache = {}
        self.statistics = {}
        self.notifications = []
        
    def connect_database(self, host, port, user, password):
        print(f"Conectando a {host}:{port}")
        self.db_connection = f"connection_{host}_{port}"
        
    def get_user(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]
        
        user = self.user_data.get(user_id)
        self.cache[user_id] = user
        return user
        
    def save_user(self, user_id, data):
        self.user_data[user_id] = data
        self.cache[user_id] = data
        self.log_message(f"Usuario {user_id} guardado")
        
    def load_configuration(self, file):
        self.configuration = {"file": file, "loaded": True}
        
    def log_message(self, message):
        self.logs.append({"timestamp": time.time(), "message": message})
        
    def calculate_statistics(self):
        self.statistics = {
            "total_users": len(self.user_data),
            "total_logs": len(self.logs),
            "cache_size": len(self.cache)
        }
        return self.statistics
        
    def send_notification(self, user, message):
        self.notifications.append({"user": user, "message": message})
        print(f"Notificación enviada a {user}: {message}")
        
    def clear_cache(self):
        self.cache = {}
        
    def generate_report(self):
        report = f"Usuarios: {len(self.user_data)}, Logs: {len(self.logs)}"
        return report


class complex_processor:
    """Antipattern 2: SPAGHETTI CODE - Tangled and hard to follow logic"""
    
    def process_order(self, order):
        total = 0
        discount = 0
        taxes = 0
        
        if order["type"] == "normal":
            for item in order["items"]:
                if item["category"] == "electronics":
                    price = item["price"]
                    if order["customer"]["type"] == "premium":
                        if item["price"] > 1000:
                            discount = price * 0.15
                        else:
                            discount = price * 0.10
                    else:
                        if item["price"] > 1000:
                            discount = price * 0.05
                        else:
                            discount = 0
                    
                    price_with_discount = price - discount
                    
                    if order["country"] == "Spain":
                        taxes = price_with_discount * 0.21
                    elif order["country"] == "Mexico":
                        taxes = price_with_discount * 0.16
                    else:
                        taxes = price_with_discount * 0.10
                    
                    total += price_with_discount + taxes
                    
                elif item["category"] == "books":
                    price = item["price"]
                    if order["customer"]["type"] == "student":
                        discount = price * 0.20
                    elif order["customer"]["type"] == "premium":
                        discount = price * 0.10
                    else:
                        discount = 0
                    
                    price_with_discount = price - discount
                    
                    if order["country"] == "Spain":
                        taxes = price_with_discount * 0.04
                    else:
                        taxes = 0
                    
                    total += price_with_discount + taxes
                    
                else:
                    price = item["price"]
                    if order["customer"]["points"] > 1000:
                        discount = price * 0.08
                    else:
                        discount = 0
                    
                    price_with_discount = price - discount
                    taxes = price_with_discount * 0.15
                    total += price_with_discount + taxes
                    
        elif order["type"] == "express":
            for item in order["items"]:
                price = item["price"] * 1.20
                taxes = price * 0.21
                total += price + taxes
                
        return total


def get_global_configuration():
    """Antipattern 3: COPY-PASTE PROGRAMMING - Duplicated code everywhere"""
    
    configuration1 = {
        "server": {
            "host": "localhost",
            "port": 8080,
            "timeout": 30,
            "max_connections": 100,
            "ssl": False,
            "debug": True
        }
    }
    
    configuration2 = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "timeout": 30,
            "max_connections": 100,
            "ssl": False,
            "debug": True
        }
    }
    
    configuration3 = {
        "cache": {
            "host": "localhost",
            "port": 6379,
            "timeout": 30,
            "max_connections": 100,
            "ssl": False,
            "debug": True
        }
    }
    
    return configuration1, configuration2, configuration3


def validate_user_copy1(user):
    if not user:
        return False
    if "name" not in user:
        return False
    if "email" not in user:
        return False
    if len(user["name"]) < 3:
        return False
    if "@" not in user["email"]:
        return False
    if "." not in user["email"]:
        return False
    return True


def validate_product_copy2(product):
    if not product:
        return False
    if "name" not in product:
        return False
    if "price" not in product:
        return False
    if len(product["name"]) < 3:
        return False
    if product["price"] <= 0:
        return False
    return True


def validate_order_copy3(order):
    if not order:
        return False
    if "items" not in order:
        return False
    if "customer" not in order:
        return False
    if len(order["items"]) == 0:
        return False
    if "name" not in order["customer"]:
        return False
    if len(order["customer"]["name"]) < 3:
        return False
    return True


if __name__ == "__main__":
    print("=== DEMOSTRACIÓN DE ANTIPATRONES ===\n")
    
    print("1. GOD OBJECT - La clase data_manager hace demasiadas cosas:")
    manager = data_manager()
    manager.connect_database("localhost", 5432, "admin", "password")
    manager.save_user(1, {"name": "John", "email": "john@email.com"})
    manager.calculate_statistics()
    manager.send_notification("John", "Bienvenido")
    print("   - Maneja conexiones de BD")
    print("   - Gestiona usuarios")
    print("   - Maneja configuración")
    print("   - Registra logs")
    print("   - Gestiona caché")
    print("   - Calcula estadísticas")
    print("   - Envía notificaciones\n")
    
    print("2. SPAGHETTI CODE - Lógica compleja y anidada:")
    processor = complex_processor()
    order = {
        "type": "normal",
        "country": "Spain",
        "customer": {"type": "premium", "points": 500},
        "items": [
            {"category": "electronics", "price": 1500},
            {"category": "books", "price": 30}
        ]
    }
    total = processor.process_order(order)
    print(f"   - Múltiples niveles de anidación")
    print(f"   - Lógica de negocio mezclada")
    print(f"   - Difícil de seguir y mantener")
    print(f"   - Total calculado: {total}\n")
    
    print("3. COPY-PASTE PROGRAMMING - Código duplicado:")
    conf1, conf2, conf3 = get_global_configuration()
    print("   - Misma estructura repetida 3 veces")
    print("   - Funciones de validación casi idénticas")
    print("   - Cambios requieren modificar múltiples lugares")