from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("employee.db")
    conn.row_factory = sqlite3.Row
    return conn
conn = connect_db()

conn.execute('''
CREATE TABLE IF NOT EXISTS departments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS employees(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT NOT NULL,
department_id INTEGER,
salary INTEGER,
joining_date TEXT,
FOREIGN KEY(department_id)
REFERENCES departments(id)
)
''')

departments=["Engineering","HR","Sales"]
for dept in departments:
    conn.execute(
        "INSERT OR IGNORE INTO departments(name) VALUES(?)",
        (dept,)
    )
conn.commit()
conn.close()

@app.route("/api/departments", methods=["GET"])
def get_departments():
    conn=connect_db()
    departments=conn.execute(
        "SELECT * FROM departments"
    ).fetchall()
    conn.close()
    return jsonify([
        dict(row)
        for row in departments
    ])


@app.route("/api/employees",methods=["POST"])
def add_employee():
    data=request.json
    conn=connect_db()
    conn.execute(
    '''INSERT INTO employees(name,email,department_id,salary,joining_date)VALUES(?,?,?,?,?)''',
    (
        data["name"],
        data["email"],
        data["department_id"],
        data["salary"],
        data["joining_date"]
    )
)
    conn.commit()
    conn.close()
    return jsonify({
        "message":"Employee Added"
    }),201


@app.route("/api/employees",methods=["GET"])
def get_employees():
    conn=connect_db()
    employees=conn.execute('''
    SELECT employees.*,
    departments.name as department
    FROM employees
    LEFT JOIN departments
    ON employees.department_id=departments.id
    ''').fetchall()
    conn.close()
    return jsonify(
        [dict(row) for row in employees]
    )


@app.route("/api/employees/:id",methods=["PUT"])
def update_employee(id):
    data=request.json
    conn=connect_db()
    conn.execute('''
    UPDATE employees
    SET
    name=?,email=?,department_id=?,salary=?,joining_date=?WHERE id=?
    ''',
    (
    data["name"],
    data["email"],
    data["department_id"],
    data["salary"],
    data["joining_date"],
    id
    ))
    conn.commit()
    conn.close()
    return jsonify({
    "message":"Updated"
    })


@app.route("/api/employees/<int:id>",methods=["DELETE"])
def delete_employee(id):
    conn=connect_db()
    conn.execute(
    "DELETE FROM employees WHERE id=?",
    (id,)
    )
    conn.commit()
    conn.close()
    return jsonify({
        "message":"Deleted"
    })
    return "Employee Management System Running"
@app.route("/")
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug = True)