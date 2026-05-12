from flask import Flask, request, redirect, render_template
from air_quality import get_air_quality_data
from datetime import datetime

app = Flask(__name__)

# ==========================================
# LOGIN CONFIG
# ==========================================

USERNAME = "admin"
PASSWORD = "admin123"

logged_in = False


# ==========================================
# LOGIN PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def login():

    global logged_in

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            logged_in = True
            return redirect("/dashboard")

        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    global logged_in

    if not logged_in:
        return redirect("/")

    data = get_air_quality_data()

    latest = data.iloc[-1]

    current_time = datetime.now().strftime("%d %B %Y | %I:%M:%S %p")

    return render_template(
        "dashboard.html",
        latest=latest,
        current_time=current_time
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    global logged_in

    logged_in = False

    return redirect("/")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )