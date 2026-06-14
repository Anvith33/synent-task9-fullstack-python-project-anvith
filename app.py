from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "taskmanager_secret_key"

# Create database and table
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        due_date TEXT,
        status TEXT DEFAULT 'Pending',
        user_id INTEGER
    )
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        task = request.form.get("task")
        due_date = request.form.get("due_date")


        if task:
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO tasks(task, due_date, user_id)
    VALUES (?, ?, ?)
    """,(task,due_date,session["user_id"])
)
            conn.commit()
            conn.close()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT id, task, due_date, status FROM tasks WHERE user_id=? """, (session["user_id"],)
)
    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)
@app.route("/complete/<int:id>")
def complete_task(id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_task(id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    if request.method == "POST":

        task = request.form.get("task")
        due_date = request.form.get("due_date")

        cursor.execute(
            """
            UPDATE tasks
            SET task=?, due_date=?
            WHERE id=?
            """,
            (task, due_date, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute(
        "SELECT id, task, due_date, status FROM tasks WHERE id=?",
        (id,)
    )

    task = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        task=task
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username=? AND password=?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            return redirect("/")

        return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)