from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-secret"

client = MongoClient("mongodb+srv://anitha_k:anitha2008@cluster0.50eenln.mongodb.net/?appName=Cluster0")
db = client["student_task_manager"]
users = db["users"]
tasks = db["tasks"]

client.admin.command("ping")
print("MongoDB Connected Successfully!")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email") or request.form.get("username")
        password = request.form.get("password")
        user = users.find_one({"email": email})
        if user is None:
            users.insert_one({"email": email,
                              "password": generate_password_hash(password)})
        elif not check_password_hash(user["password"], password):
            return "Wrong password", 401
        session["email"] = email
        return redirect(url_for("dash"))
    return render_template("index.html")

@app.route("/dash")
def dash():
    if "email" not in session:
        return redirect(url_for("index"))
    my_tasks = list(tasks.find({"email": session["email"]}))
    return render_template("dash.html", tasks=my_tasks)

@app.route("/task", methods=["GET", "POST"])
def task():
    if "email" not in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        data = request.form.to_dict()
        data["email"] = session["email"]
        tasks.insert_one(data)
        return redirect(url_for("dash"))
    return render_template("task.html")

if __name__ == "__main__":
    app.run(debug=True)