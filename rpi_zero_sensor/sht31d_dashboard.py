from flask import Flask, render_template_string
import csv

app = Flask(__name__)

deviceNum = 1
fileName = 'data/sensor' + str(deviceNum) + '_'+str(datetime.date.today())+'.csv'

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pi Sensor Dashboard</title>
    <meta http-equiv="refresh" content="10" />
    <style>
        body { font-family: sans-serif; margin: 2em; }
        table { border-collapse: collapse; }
        td, th { padding: 0.5em; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>🌡️ Pi Sensor Dashboard</h1>
    <table>
        <tr><th>Timestamp</th><th>Temp (°C)</th><th>Temp (°F)</th><th>Humidity (%)</th></tr>
        {% for row in data %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
        </tr>
        {% endfor %}
    </table>
    <p>Auto-refreshes every 10 seconds</p>
</body>
</html>
"""

@app.route("/")
def index():
    with open(fileName, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        rows = list(reader)[-10:]  # last 10 readings
    return render_template_string(HTML, data=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
