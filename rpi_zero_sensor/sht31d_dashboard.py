from flask import Flask, render_template_string, request, send_file, abort, jsonify
import csv
import datetime
import os 
import glob
import json


with open("/home/case/CASE_sensor_network/rpi_zero_sensor/config.json") as f:
    config = json.load(f)

deviceNum = config["sensor"]["number"]

app = Flask(__name__)

filePath = '/home/case/data/'
filePrefix = 'sensor' + str(deviceNum) + '_'

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pi Sensor Dashboard</title>
    <meta http-equiv="refresh" content="60" />
    <style>
        body { font-family: sans-serif; margin: 2em; }
        table { border-collapse: collapse; }
        td, th { padding: 0.5em; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>Pi Zero W2 SHT31D Sensor Dashboard</h1>
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
    <p>Auto-refreshes every 60 seconds</p>
</body>
</html>
"""

@app.route("/")
def index():
    fileName = filePath + filePrefix +str(datetime.date.today())+'.csv'
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
    fullFilePath = filePath + fileName #os.path.join(fileName)

    if not os.path.exists(fullFilePath):
        return f"No data found for {date}", 404

    return send_file(fullFilePath, as_attachment=True, download_name=fileName)

@app.route("/api/files")
def list_csv_files():
    #fileName = filePrefix +str(datetime.date.today())+'.csv'

    # Get all CSV files in the data/ directory
    file_pattern = os.path.join(filePath, f"{filePrefix}*.csv")
    files = sorted(glob.glob(file_pattern))

    # Return just the filenames (without full paths)
    filenames = [os.path.basename(f) for f in files]

    return jsonify(filenames)

@app.route("/api/disk")
def get_disk_usage():
    stat = os.statvfs("/")

    total = stat.f_frsize * stat.f_blocks      # Total space
    free = stat.f_frsize * stat.f_bavail       # Available space
    used = total - free

    total_mb = total // (1024 * 1024)
    used_mb = used // (1024 * 1024)
    free_mb = free // (1024 * 1024)
    percent_used = round((used / total) * 100, 1)

    return jsonify({
        "total_mb": total_mb,
        "used_mb": used_mb,
        "free_mb": free_mb,
        "percent_used": percent_used
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
