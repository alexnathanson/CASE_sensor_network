from flask import Flask, render_template_string, request, send_file, abort
import csv
import datetime
import os 

app = Flask(__name__)

deviceNum = 1
filePrefix = 'data/sensor' + str(deviceNum) + '_'

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
    <p>
        Download CSV file with the end point /api/data?date=YYYY-MM-DD
    </p>
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
    fileName = filePrefix +str(datetime.date.today())+'.csv'
    with open(fileName, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        rows = list(reader)#[-10:]  # last 10 readings
    return render_template_string(HTML, data=rows)


@app.route("/api/data")
def get_csv_for_date():
    date = request.args.get("date")
    if not date:
        return "Please provide a date using ?date=YYYY-MM-DD", 400

    fileName = filePrefix +str(datetime.date.today())+'.csv'
    filePath = fileName #os.path.join(fileName)

    if not os.path.exists(filePath):
        return f"No data found for {date}", 404

    return send_file(filePath, as_attachment=True, download_name=fileName)

# def get_latest_csv():
#     # Optional helper to auto-detect latest log file
#     import glob
#     files = sorted(glob.glob(os.path.join(DATA_DIR, "sht31d_data_*.csv")), reverse=True)
#     return files[0] if files else None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
