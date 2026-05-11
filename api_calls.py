from flask import Flask, request, redirect, session

from air_quality import get_air_quality_data

app = Flask(__name__)

app.secret_key = "supersecret"

# SIMPLE USER LOGIN
USERNAME = "admin"
PASSWORD = "admin123"

@app.route("/", methods=["GET", "POST"])

def login():

    # LOGIN CHECK
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True

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

@app.route("/dashboard")

def dashboard():

    if not session.get("logged_in"):

        return redirect("/")

    data = get_air_quality_data()

    return f"""

    <h1>Industrial Environmental Dashboard</h1>

    <a href='/logout'>Logout</a>

    <h2>Live Air Quality Data</h2>

    <ul>
        <li>PM10: {data['pm10']}</li>
        <li>PM2.5: {data['pm2_5']}</li>
        <li>Carbon Monoxide: {data['carbon_monoxide']}</li>
        <li>Carbon Dioxide: {data['carbon_dioxide']}</li>
        <li>Sulphur Dioxide: {data['sulphur_dioxide']}</li>
        <li>Methane: {data['methane']}</li>
        <li>Dust: {data['dust']}</li>
        <li>Total Elementary Carbon: {data['total_elementary_carbon']}</li>
    </ul>

    """

@app.route("/logout")

def logout():

    session.clear()

    return redirect("/")

if __name__ == "__main__":

    app.run(debug=True)