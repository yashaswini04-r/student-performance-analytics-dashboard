from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
#students = [
   # {"id": 1, "name": "Ravi", "marks": 85, "attendance": "90%"},
   #{"id": 2, "name": "Priya", "marks": 92, "attendance": "95%"},
   #{"id": 3, "name": "Arjun", "marks": 78, "attendance": "80%"}
#]
@app.route('/add_student', methods=['POST'])
def add_student():

    name = request.form['name']
    marks = request.form['marks']
    attendance = request.form['attendance'] + '%'

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, marks, attendance) VALUES (?, ?, ?)",
        (name, marks, attendance)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit_student(id):

    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit.html',
        student=student
    )

    conn.commit()
    conn.close()

    return home()

@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    marks = int(request.form['marks'])
    attendance = request.form['attendance']

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE students
        SET name=?, marks=?, attendance=?
        WHERE id=?
        ''',
        (name, marks, attendance, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/')
def home():
    search=request.args.get('search', '')

    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT * FROM students WHERE name LIKE ? ORDER BY id ASC", (f'%{search}%',))
    else:
        cursor.execute("SELECT * FROM students ORDER BY id ASC")

    students = cursor.fetchall()
    student_names = [student['name'] for student in students]

    student_marks = [student['marks'] for student in students]

    student_attendance = [
    int(student['attendance'].replace('%', ''))
    for student in students
]

    total_students = len(students)
    if total_students > 0:
        average_marks = sum(student['marks'] for student in students) / total_students
    else:
        average_marks = 0

    if total_students > 0:
        average_attendance = sum(
        int(student['attendance'].replace('%', ''))
        for student in students
    ) / total_students
    else:
      average_attendance = 0

    top_performers = len([
    student for student in students if student['marks'] >= 90]
    )
    
    conn.close()

    return render_template(
        'index.html', 
        students=students, 
        total_students=total_students, 
        average_marks=round(average_marks,2), 
        average_attendance=round(average_attendance,2), 
        top_performers=top_performers,
        names=student_names,
    marks=student_marks,
    attendance=student_attendance
        ) 

if __name__ == '__main__':
    app.run(debug=True)
