from flask import Flask, render_template_string, request, redirect, session, url_for
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# ==========================================
# CONFIGURATION
# ==========================================

COMPANY_NAME = "Aero Industrial Solutions Pvt Ltd"
PROJECT_NAME = "Industrial Environmental Risk Monitoring Dashboard"
COMPANY_LOGO = "https://via.placeholder.com/180x60.png?text=Company+Logo"

# Replace with your actual AQI API URL
AQI_API_URL = "YOUR_API_ENDPOINT"

# Replace with your Grafana datasource / exporter endpoint
GRAFANA_DATA_ENDPOINT = "YOUR_GRAFANA_EXPORTER_ENDPOINT"

# Threshold configuration
THRESHOLDS = {
    "AQI": 100,
    "PM10": 60,
    "PM2_5": 35,
    "Carbon_Dioxide": 1000,
    "Nitrogen_Dioxide": 40,
    "Sulphur_Dioxide": 20,
    "Dust": 150,
    "Ammonia": 25
}

# ==========================================
# MOCK DATA PLACEHOLDER
# Replace with actual Grafana / Prometheus metrics
# ==========================================

def get_environment_data():
    return {
        "today": {
            "AQI": 78,
            "PM10": 42,
            "PM2_5": 21,
            "Carbon_Dioxide": 640,
            "Nitrogen_Dioxide": 17,
            "Sulphur_Dioxide": 8,
            "Dust": 96,
            "Ammonia": 6
        },
        "last_7_days": {
            "AQI": 84,
            "PM10": 51,
            "PM2_5": 29
        },
        "last_30_days": {
            "AQI": 92,
            "PM10": 58,
            "PM2_5": 31
        }
    }

# ==========================================
# LOGIN USERS
# ==========================================

USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}

# ==========================================
# HTML TEMPLATE
# ==========================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ project_name }}</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #f4f7fa;
        }

        .header {
            background-color: #0f172a;
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header img {
            height: 60px;
        }

        .container {
            padding: 30px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .metric {
            font-size: 28px;
            font-weight: bold;
            margin-top: 10px;
        }

        .status-good {
            color: green;
        }

        .status-warning {
            color: orange;
        }

        .status-danger {
            color: red;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
        }

        table th, table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }

        table th {
            background-color: #0f172a;
            color: white;
        }

        .login-container {
            width: 350px;
            margin: 120px auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        input {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            padding: 12px;
            margin-top: 20px;
            border: none;
            border-radius: 8px;
            background-color: #2563eb;
            color: white;
            cursor: pointer;
        }

        .footer {
            margin-top: 40px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>

{% if not session.get('logged_in') %}

<div class="login-container">
    <h2>Login</h2>

    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</div>

{% else %}

<div class="header">
    <div>
        <img src="{{ logo }}">
    </div>

    <div>
        <h1>{{ company_name }}</h1>
        <h2>{{ project_name }}</h2>
    </div>

    <div>
        <a href="/logout" style="color:white; text-decoration:none;">Logout</a>
    </div>
</div>

<div class="container">

    <h2>Environmental Monitoring Overview</h2>

    <div class="cards">

        <div class="card">
            <h3>Today's AQI</h3>
            <div class="metric">{{ data.today.AQI }}</div>
        </div>

        <div class="card">
            <h3>Last 7 Days AQI</h3>
            <div class="metric">{{ data.last_7_days.AQI }}</div>
        </div>

        <div class="card">
            <h3>Last 30 Days AQI</h3>
            <div class="metric">{{ data.last_30_days.AQI }}</div>
        </div>

    </div>

    <h2 style="margin-top:40px;">Environmental Metrics</h2>

    <table>
        <tr>
            <th>Metric</th>
            <th>Current Value</th>
            <th>Threshold</th>
            <th>Status</th>
        </tr>

        {% for metric, value in data.today.items() %}
        <tr>
            <td>{{ metric }}</td>
            <td>{{ value }}</td>
            <td>{{ thresholds[metric] }}</td>

            {% if value < thresholds[metric] %}
                <td class="status-good">Normal</td>
            {% elif value == thresholds[metric] %}
                <td class="status-warning">Warning</td>
            {% else %}
                <td class="status-danger">Critical</td>
            {% endif %}
        </tr>
        {% endfor %}

    </table>

    <div class="footer">
        <p>Powered by Python, Prometheus, Grafana & Flask</p>
        <p>Generated on {{ current_time }}</p>
    </div>

</div>

{% endif %}

</body>
</html>
'''

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def dashboard():
    data = get_environment_data()

    return render_template_string(
        HTML_TEMPLATE,
        company_name=COMPANY_NAME,
        project_name=PROJECT_NAME,
        logo=COMPANY_LOGO,
        data=data,
        thresholds=THRESHOLDS,
        current_time=datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        session=session
    )

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = USERS.get(username)

    if user and user['password'] == password:
        session['logged_in'] = True
        session['role'] = user['role']
        return redirect(url_for('dashboard'))

    return 'Invalid Credentials'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard'))

# ==========================================
# MAIN
# ==========================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
