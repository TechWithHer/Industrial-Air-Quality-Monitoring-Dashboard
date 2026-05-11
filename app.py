from flask import Flask, request, redirect
from air_quality import get_air_quality_data

app = Flask(__name__)

# ==========================================
# SIMPLE LOGIN CONFIG
# ==========================================

USERNAME = "admin"
PASSWORD = "admin123"

# Fake login state
logged_in = False


# ==========================================
# LOGIN PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def login():

    global logged_in

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            logged_in = True

            return redirect("/dashboard")

    return """

    <h2>Login</h2>

    <form method="POST">

        <input name="username" placeholder="Username">

        <br><br>

        <input name="password" type="password" placeholder="Password">

        <br><br>

        <button type="submit">Login</button>

    </form>

    """


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

    return f"""

    <h1>Industrial Environmental Dashboard</h1>

    <a href='/logout'>Logout</a>

    <h2>Live Air Quality Data</h2>

    <ul>
        <li>PM10: {latest['pm10']}</li>
        <li>PM2.5: {latest['pm2_5']}</li>
        <li>Carbon Monoxide: {latest['carbon_monoxide']}</li>
        <li>Carbon Dioxide: {latest['carbon_dioxide']}</li>
        <li>Sulphur Dioxide: {latest['sulphur_dioxide']}</li>
        <li>Methane: {latest['methane']}</li>
        <li>Dust: {latest['dust']}</li>
        <li>Total Elementary Carbon: {latest['total_elementary_carbon']}</li>
    </ul>

    """


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