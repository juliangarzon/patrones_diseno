"""
Online Course Platform
======================
System to manage courses, students and evaluations.
Analyze the code and identify the antipatterns present.
"""

import random
import json
from datetime import datetime, timedelta


global_data = {
    "courses": {},
    "students": {},
    "teachers": {},
    "evaluations": []
}


class course_platform:
    
    def __init__(self):
        self.courses = global_data["courses"]
        self.students = global_data["students"]
        self.teachers = global_data["teachers"]
        self.evaluations = global_data["evaluations"]
        self.enrollments = {}
        self.grades = {}
        self.certificates = []
        self.payments = []
        self.comments = []
        self.messages = []
        self.notifications = []
        self.sessions = {}
        self.resources = {}
        self.assignments = []
        self.forums = []
        
    def manage_entity(self, type, action, data):
        result = {"success": False, "message": ""}
        
        if type == "course":
            if action == "create":
                if data.get("id") and data.get("name") and data.get("teacher_id"):
                    if data["id"] not in self.courses:
                        if data["teacher_id"] in self.teachers:
                            self.courses[data["id"]] = {
                                "name": data["name"],
                                "description": data.get("description", ""),
                                "teacher_id": data["teacher_id"],
                                "duration": data.get("duration", 30),
                                "price": data.get("price", 0),
                                "category": data.get("category", "general"),
                                "level": data.get("level", "beginner"),
                                "students": [],
                                "resources": [],
                                "evaluations": [],
                                "status": "active",
                                "creation_date": datetime.now()
                            }
                            
                            if data.get("price", 0) > 100:
                                self.courses[data["id"]]["premium"] = True
                                self.courses[data["id"]]["certificate"] = True
                            else:
                                self.courses[data["id"]]["premium"] = False
                                self.courses[data["id"]]["certificate"] = False
                            
                            self.notifications.append({
                                "type": "course_created",
                                "course_id": data["id"],
                                "timestamp": datetime.now()
                            })
                            
                            result["success"] = True
                            result["message"] = "Curso creado exitosamente"
                        else:
                            result["message"] = "Profesor no encontrado"
                    else:
                        result["message"] = "El curso ya existe"
                else:
                    result["message"] = "Datos incompletos"
                    
            elif action == "update":
                if data.get("id") and data["id"] in self.courses:
                    course = self.courses[data["id"]]
                    
                    if data.get("name"):
                        course["name"] = data["name"]
                    if data.get("description"):
                        course["description"] = data["description"]
                    if data.get("price") is not None:
                        course["price"] = data["price"]
                        if data["price"] > 100:
                            course["premium"] = True
                            course["certificate"] = True
                        else:
                            course["premium"] = False
                            course["certificate"] = False
                    
                    result["success"] = True
                    result["message"] = "Curso actualizado"
                else:
                    result["message"] = "Curso no encontrado"
                    
        elif type == "student":
            if action == "create":
                if data.get("id") and data.get("name") and data.get("email"):
                    if data["id"] not in self.students:
                        self.students[data["id"]] = {
                            "name": data["name"],
                            "email": data["email"],
                            "courses": [],
                            "grades": {},
                            "certificates": [],
                            "registration_date": datetime.now(),
                            "active": True,
                            "level": "novice",
                            "points": 0
                        }
                        
                        result["success"] = True
                        result["message"] = "Estudiante registrado"
                    else:
                        result["message"] = "Estudiante ya existe"
                else:
                    result["message"] = "Datos incompletos"
                    
            elif action == "enroll":
                student_id = data.get("student_id")
                course_id = data.get("course_id")
                
                if student_id and course_id:
                    if student_id in self.students and course_id in self.courses:
                        student = self.students[student_id]
                        course = self.courses[course_id]
                        
                        if course_id not in student["courses"]:
                            price = course["price"]
                            
                            if student["level"] == "advanced":
                                discount = price * 0.20
                            elif student["level"] == "intermediate":
                                discount = price * 0.10
                            else:
                                discount = 0
                            
                            final_price = price - discount
                            
                            if final_price == 0 or self.process_payment(student_id, final_price):
                                student["courses"].append(course_id)
                                course["students"].append(student_id)
                                
                                self.enrollments[f"{student_id}_{course_id}"] = {
                                    "date": datetime.now(),
                                    "progress": 0,
                                    "last_activity": datetime.now()
                                }
                                
                                student["points"] += 10
                                self.update_student_level(student_id)
                                
                                result["success"] = True
                                result["message"] = "Inscripción exitosa"
                            else:
                                result["message"] = "Error en el pago"
                        else:
                            result["message"] = "Ya inscrito en el curso"
                    else:
                        result["message"] = "Estudiante o curso no encontrado"
                else:
                    result["message"] = "Datos incompletos"
                    
        elif type == "evaluation":
            if action == "create":
                course_id = data.get("course_id")
                title = data.get("title")
                questions = data.get("questions", [])
                
                if course_id and title and questions:
                    if course_id in self.courses:
                        evaluation_id = len(self.evaluations) + 1
                        
                        self.evaluations.append({
                            "id": evaluation_id,
                            "course_id": course_id,
                            "title": title,
                            "questions": questions,
                            "allowed_attempts": data.get("allowed_attempts", 3),
                            "time_limit": data.get("time_limit", 60),
                            "creation_date": datetime.now()
                        })
                        
                        self.courses[course_id]["evaluations"].append(evaluation_id)
                        
                        result["success"] = True
                        result["message"] = "Evaluación creada"
                        result["evaluation_id"] = evaluation_id
                    else:
                        result["message"] = "Curso no encontrado"
                else:
                    result["message"] = "Datos incompletos"
                    
            elif action == "grade":
                student_id = data.get("student_id")
                evaluation_id = data.get("evaluation_id")
                answers = data.get("answers", [])
                
                if student_id and evaluation_id and answers:
                    evaluation = None
                    for eval in self.evaluations:
                        if eval["id"] == evaluation_id:
                            evaluation = eval
                            break
                    
                    if evaluation:
                        course_id = evaluation["course_id"]
                        if course_id in self.students[student_id]["courses"]:
                            score = 0
                            total = len(evaluation["questions"])
                            
                            for i, answer in enumerate(answers):
                                if i < total and answer == evaluation["questions"][i]["correct_answer"]:
                                    score += 1
                            
                            grade = (score / total) * 100
                            
                            grade_key = f"{student_id}_{evaluation_id}"
                            self.grades[grade_key] = {
                                "grade": grade,
                                "date": datetime.now(),
                                "passed": grade >= 70
                            }
                            
                            if grade >= 70:
                                self.students[student_id]["points"] += 50
                                self.update_student_level(student_id)
                                
                                if self.courses[course_id]["certificate"]:
                                    self.generate_certificate(student_id, course_id)
                            
                            result["success"] = True
                            result["message"] = f"Calificación: {grade}%"
                            result["passed"] = grade >= 70
                        else:
                            result["message"] = "Estudiante no inscrito"
                    else:
                        result["message"] = "Evaluación no encontrada"
                else:
                    result["message"] = "Datos incompletos"
        
        return result
    
    def process_payment(self, student_id, amount):
        self.payments.append({
            "student_id": student_id,
            "amount": amount,
            "date": datetime.now(),
            "status": "completed"
        })
        return True
    
    def update_student_level(self, student_id):
        student = self.students[student_id]
        points = student["points"]
        
        if points >= 500:
            student["level"] = "expert"
        elif points >= 300:
            student["level"] = "advanced"
        elif points >= 150:
            student["level"] = "intermediate"
        else:
            student["level"] = "novice"
    
    def generate_certificate(self, student_id, course_id):
        certificate = {
            "id": len(self.certificates) + 1,
            "student_id": student_id,
            "course_id": course_id,
            "issue_date": datetime.now(),
            "verification_code": f"CERT-{student_id}-{course_id}-{random.randint(1000, 9999)}"
        }
        
        self.certificates.append(certificate)
        self.students[student_id]["certificates"].append(certificate["id"])
        
        return certificate


def validate_email_format(email):
    if not email or "@" not in email or "." not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2 or len(parts[0]) < 1 or len(parts[1]) < 3:
        return False
    return True


def validate_phone_format(phone):
    if not phone or len(phone) < 10:
        return False
    if not phone.replace("-", "").replace(" ", "").isdigit():
        return False
    return True


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False


def calculate_student_discount_price(price, level):
    if level == "expert":
        return price * 0.70
    elif level == "advanced":
        return price * 0.80
    elif level == "intermediate":
        return price * 0.90
    else:
        return price


def calculate_season_discount_price(price, month):
    if month in [11, 12]:
        return price * 0.75
    elif month in [6, 7]:
        return price * 0.85
    else:
        return price


def calculate_quantity_discount_price(price, quantity):
    if quantity >= 10:
        return price * 0.60
    elif quantity >= 5:
        return price * 0.75
    elif quantity >= 3:
        return price * 0.85
    else:
        return price


class session_manager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(session_manager, cls).__new__(cls)
            cls._instance.active_sessions = {}
        return cls._instance
    
    def create_session(self, user_id):
        session_id = f"SES-{user_id}-{random.randint(10000, 99999)}"
        self.active_sessions[session_id] = {
            "user_id": user_id,
            "start": datetime.now(),
            "last_activity": datetime.now()
        }
        return session_id
    
    def validate_session(self, session_id):
        return session_id in self.active_sessions


class cache_handler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(cache_handler, cls).__new__(cls)
            cls._instance.data_cache = {}
        return cls._instance
    
    def save(self, key, value):
        self.data_cache[key] = {
            "value": value,
            "timestamp": datetime.now()
        }
    
    def get(self, key):
        if key in self.data_cache:
            return self.data_cache[key]["value"]
        return None


if __name__ == "__main__":
    platform = course_platform()
    
    platform.manage_entity("student", "create", {
        "id": "EST001",
        "name": "Carlos Martínez",
        "email": "carlos@email.com"
    })
    
    print("Plataforma de cursos iniciada. Identifica los antipatrones.")