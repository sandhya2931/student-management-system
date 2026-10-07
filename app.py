from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="student_db"
    )

@app.route("/")
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
        (name, email, course)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_student(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
