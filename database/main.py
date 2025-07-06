from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sqlite3

def create_database():
    try:
        conn = sqlite3.connect('school_database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                grade INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

create_database()

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
    

@app.get("/students/")
def read_students():
    conn = sqlite3.connect('school_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.commit()
    conn.close()
    return students

@app.post("/students/")
def create_student(new_student: Student):
    conn = sqlite3.connect('school_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students ( name, age, grade) VALUES (?, ?, ?)",
                   (new_student.name, new_student.age, new_student.grade))
    conn.commit()
    conn.close()
    return new_student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    conn = sqlite3.connect('school_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close
    student = cursor.fetchone()
    if student:
        conn = sqlite3.connect('school_database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?",
                   (updated_student.name, updated_student.age, updated_student.grade, student_id))
        conn.commit()
        conn.close()
        return {"message": "Student deleted successfully", "student": updated_student}
    return {"error": "Student not found"}
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = sqlite3.connect('school_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    conn.commit()
    student = cursor.fetchone()
    if student:
        conn = sqlite3.connect('school_database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        return {"message": "Student deleted successfully"}
    return {"error": "Student not found"}




