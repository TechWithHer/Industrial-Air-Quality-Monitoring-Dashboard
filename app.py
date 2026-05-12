from prometheus_client import Gauge, generate_latest
from flask import Flask, request, redirect, render_template, Response
from air_quality import get_air_quality_data
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# =====================================================
# THRESHOLDS
# =====================================================

THRESHOLDS = {
    "pm10": 50,
    "pm2_5": 25,
    "carbon_monoxide": 9,
    "carbon_dioxide": 1000,
    "sulphur_dioxide": 75,
    "methane": 2,
    "dust": 100,
    "total_elementary_carbon": 10
}

# =====================================================
# PROMETHEUS METRICS
# =====================================================

pm10_metric = Gauge('pm10_level', 'PM10 Air Quality Level')
pm25_metric = Gauge('pm25_level', 'PM2.5 Air Quality Level')
co_metric = Gauge('carbon_monoxide_level', 'Carbon Monoxide Level')
co2_metric = Gauge('carbon_dioxide_level', 'Carbon Dioxide Level')
so2_metric = Gauge('sulphur_dioxide_level', 'Sulphur Dioxide Level')
methane_metric = Gauge('methane_level', 'Methane Level')
dust_metric = Gauge('dust_level', 'Dust Level')
tec_metric = Gauge('total_elementary_carbon_level', 'Total Elementary Carbon Level')

# =====================================================
# LOGIN CONFIG
# =====================================================

USERNAME = "admin"
PASSWORD = "admin123"

logged_in = False

# =====================================================
# HELPER FUNCTION
# =====================================================

def get_status(value, threshold):

    if value < threshold * 0.7:
        return "SAFE"

    elif value < threshold:
        return "WARNING"

    else:
        return "DANGER"

# =====================================================
# LOGIN PAGE
# =====================================================

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

# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    global logged_in

    if not logged_in:
        return redirect("/")

    # GET DATA
    data = get_air_quality_data()

    # ==========================================
    # ENSURE TIMESTAMP COLUMN EXISTS
    # ==========================================

    if 'timestamp' in data.columns:

        data['timestamp'] = pd.to_datetime(data['timestamp'])

        # HOURLY AGGREGATION
        hourly_data = (
            data
            .set_index('timestamp')
            .resample('H')
            .mean(numeric_only=True)
            .reset_index()
        )

    else:
        hourly_data = data

    # GET LATEST HOURLY RECORD
    latest = hourly_data.iloc[-1]

    # =====================================================
    # UPDATE PROMETHEUS METRICS
    # =====================================================

    pm10_metric.set(latest['pm10'])
    pm25_metric.set(latest['pm2_5'])
    co_metric.set(latest['carbon_monoxide'])
    co2_metric.set(latest['carbon_dioxide'])
    so2_metric.set(latest['sulphur_dioxide'])
    methane_metric.set(latest['methane'])
    dust_metric.set(latest['dust'])
    tec_metric.set(latest['total_elementary_carbon'])

    # =====================================================
    # STATUS CALCULATION
    # =====================================================

    statuses = {
        "pm10": get_status(latest['pm10'], THRESHOLDS['pm10']),
        "pm2_5": get_status(latest['pm2_5'], THRESHOLDS['pm2_5']),
        "carbon_monoxide": get_status(
            latest['carbon_monoxide'],
            THRESHOLDS['carbon_monoxide']
        ),
        "carbon_dioxide": get_status(
            latest['carbon_dioxide'],
            THRESHOLDS['carbon_dioxide']
        ),
        "sulphur_dioxide": get_status(
            latest['sulphur_dioxide'],
            THRESHOLDS['sulphur_dioxide']
        ),
        "methane": get_status(
            latest['methane'],
            THRESHOLDS['methane']
        ),
        "dust": get_status(
            latest['dust'],
            THRESHOLDS['dust']
        ),
        "total_elementary_carbon": get_status(
            latest['total_elementary_carbon'],
            THRESHOLDS['total_elementary_carbon']
        )
    }

    # =====================================================
    # CURRENT DATE & TIME
    # =====================================================

    current_time = datetime.now().strftime(
        "%d %B %Y | %I:%M:%S %p"
    )

    # =====================================================
    # RENDER DASHBOARD
    # =====================================================

    return render_template(
        "dashboard.html",
        latest=latest,
        current_time=current_time,
        thresholds=THRESHOLDS,
        statuses=statuses
    )

# =====================================================
# PROMETHEUS METRICS ENDPOINT
# =====================================================

@app.route("/metrics")
def metrics():

    return Response(
        generate_latest(),
        mimetype="text/plain"
    )

# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    global logged_in

    logged_in = False

    return redirect("/")

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )