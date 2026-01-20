from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        cursor.execute(
            "INSERT INTO expenses (title, amount) VALUES (?, ?)",
            (title, amount)
        )
        conn.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    total = sum(expense[2] for expense in expenses)

    conn.close()
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
