from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        due_date TEXT,
        status TEXT DEFAULT 'Pending'
    )
""")

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        task = request.form.get("task")
        due_date = request.form.get("due_date")


        if task:
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO tasks (task, due_date) VALUES (?, ?)",
    (task, due_date))

            conn.commit()
            conn.close()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, task, due_date, status FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)
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

if __name__ == "__main__":
    app.run(debug=True)