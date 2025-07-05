from fastapi import FastAPI ,Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    id: int
    name: str
    age: int    
    grade: int
    
students = [
    Student(id=1, name="John", age=15, grade=10),
    Student(id=2, name="Jane", age=16, grade=11),
    Student(id=3, name="Bob", age=17, grade=12),
    Student(id=4, name="Alice", age=18, grade=13),
    Student(id=5, name="Charlie", age=19, grade=14),
    Student(id=6, name="David", age=20, grade=15),
    Student(id=7, name="Eva", age=21, grade=16),]
@app.get("/students/")
def read_students():
    return students

@app.post("/students/")
def create_student(new_student: Student):
    students.append(new_student)
    return new_student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for student in students:
        if student.id == student_id:
            student.name = updated_student.name
            student.age = updated_student.age
            student.grade = updated_student.grade
            return student
    return {"error": "Student not found"}
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index,student in enumerate(students):
        if student.id == student_id:
            del students[index]
            return {"message": "Student deleted successfully"}
    return {"error": "Student not found"}