
import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect
)

app = Flask(__name__)

app.secret_key = "lostfound123"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users(name, email, password) VALUES(?,?,?)",
                (name, email, password)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:

            conn.close()

            return "Email already exists. Please login."

    return render_template("register.html")


@app.route("/report-item", methods=["GET", "POST"])
def report_item():

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        location = request.form["location"]
        description = request.form["description"]
        status = request.form["status"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO items
        (
            item_name,
            category,
            description,
            location,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            item_name,
            category,
            description,
            location,
            status
        ))

        conn.commit()
        conn.close()

        return redirect("/items")

    return render_template("report_item.html")


@app.route("/items")
def items():

    search = request.args.get("search", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if search:

        cursor.execute(
            "SELECT * FROM items WHERE item_name LIKE ?",
            ('%' + search + '%',)
        )

    else:

        cursor.execute(
            "SELECT * FROM items"
        )

    items = cursor.fetchall()

    conn.close()

    return render_template(
        "items.html",
        items=items,
        search=search
    )


@app.route("/recover/<int:item_id>")
def recover_item(item_id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE items SET status='RECOVERED' WHERE id=?",
        (item_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/items")


if __name__ == "__main__":
    app.run(debug=True)