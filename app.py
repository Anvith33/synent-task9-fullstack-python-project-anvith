from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        task = request.form.get("task")

        if task:
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO tasks (task) VALUES (?)",
                (task,)
            )

            conn.commit()
            conn.close()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT task FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)