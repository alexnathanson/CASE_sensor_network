from flask import Flask, render_template_string, request, send_file, abort, jsonify
from flask_cors import CORS
import csv
import datetime
from datetime import timedelta
import os 
import glob
import json
import pandas as pd
import logging
import subprocess
from typing import Any, Dict, List
#import shutil
#import re

# ------------------ Config ------------------ #
logging.basicConfig(level=logging.INFO)

with open("/home/case/CASE_sensor_network/rpi_zero_sensor/config.json") as f:
    config = json.load(f)

deviceNum = config["sensor"]["number"]
logging.debug(f'device number: {deviceNum}')

app = Flask(__name__)

# CORS is enabled for all routes. This simplifies the frontend visualization,
# but could be removed for security purposes or to more easily enforce throttling without straining the Pi Zeros.
CORS(app)  

filePath = '/home/case/data/'
if deviceNum == 'kasa':
    filePrefix = 'kasa_'
else:
    filePrefix = 'sensor' + str(deviceNum) + '_'
logging.debug(f'file prefix: {filePrefix}')

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
        Download CSV file with /api/data?date=YYYY-MM-DD<br>
        View file list with /api/files
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

if deviceNum == 'kasa':
    HTML = HTML.replace("<th>Temp (°C)</th><th>Temp (°F)</th><th>Humidity (%)</th>","<th>Kasa1 W</th><th>Kasa2 W</th><th>Kasa3 W</th><th>Kasa4 W</th>")
    HTML = HTML.replace("<td>{{ row[3] }}</td>","<td>{{ row[3] }}</td><td>{{ row[4] }}</td>")

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
        return "Please provide a date using ?date=YYYY-MM-DD or ?date=now for most recent data", 400

    if date == 'now':
        pass
        try:
            fileName = filePrefix +str(datetime.date.today())+'.csv'
            fullFilePath = filePath + fileName #os.path.join(fileName)
            df = pd.read_csv(fullFilePath)  # Update path as needed

            if df.empty:
                return jsonify({'error': 'CSV is empty'}), 404

            last_row = df.iloc[-1].to_dict()
            return jsonify(last_row)
        except FileNotFoundError:
            return jsonify({'error': 'CSV file not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        # untested
        # test = date.split('-')
        # for i in test:
        #     if type(i) != int:
        #         return "Please provide a date using ?date=YYYY-MM-DD or use ?date=now for most recent data", 400

        fileName = filePrefix +date+'.csv'
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

def parse_disk_usage():
    stat = os.statvfs("/")

    total = stat.f_frsize * stat.f_blocks      # Total space
    free = stat.f_frsize * stat.f_bavail       # Available space
    used = total - free

    total_mb = total // (1024 * 1024)
    used_mb = used // (1024 * 1024)
    free_mb = free // (1024 * 1024)
    percent_used = round((used / total) * 100, 1)

    diskDict =  {
        "total_mb": total_mb,
        "used_mb": used_mb,
        "free_mb": free_mb,
        "percent_used": percent_used
    }

    return diskDict

@app.route("/api/disk")
def get_disk_usage():
    return jsonify(parse_disk_usage())

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

def parse_timestamp(filename, startDate:str, time_format:str="%Y-%m-%d",):
    fileDate = filename.split("_")[-1].replace(".csv","")
    if fileDate and (fileDate != str(datetime.date.today())): #ignore today's file
        formattedFileDate = datetime.datetime.strptime(fileDate, time_format)
        if formattedFileDate > datetime.datetime.strptime(startDate, time_format): #filter by start date
            return formattedFileDate
        return None
    return None

def check_file_size_uniformity(folder_path:str, tolerance_ratio:float=0.2)->Dict:
    interval_minutes=60*60*24
    file_data=[]
    startDate="2025-06-01"
    for f in os.listdir(folder_path):
        try:
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path):
                ts = parse_timestamp(f,startDate)
                if ts:
                    size = os.path.getsize(full_path)
                    file_data.append((f, ts, size))
        except Exception as e:
            logging.error(f'{e}')

    if not file_data:
        return "No timestamped files found in directory."

    # Sort by timestamp
    file_data.sort(key=lambda x: x[1])
    sizes = [s for _, _, s in file_data]
    avg = sum(sizes) / len(sizes)
    lower_bound = avg * (1 - tolerance_ratio)
    upper_bound = avg * (1 + tolerance_ratio)

    outliers = [(f, s) for f, _, s in file_data if s < lower_bound or s > upper_bound]

    # Find missing timestamps
    expected_ts = []
    current = file_data[0][1]
    end = file_data[-1][1]
    while current <= end:
        expected_ts.append(current)
        current += timedelta(minutes=interval_minutes)

    existing_ts = set(ts for _, ts, _ in file_data)
    missing_ts = [dt for dt in expected_ts if dt not in existing_ts]

    return {
        "total_files": len(file_data),
        "startDate" : startDate,
        "average_size_bytes": avg,
        "outliers": outliers,
        "missing_timestamps": [dt.strftime("%Y-%m-%d %H:%M") for dt in missing_ts],
        "status": "OK" if not outliers and not missing_ts else "WARNING: Issues found"
    }


def check_mmc_errors():
    dmesg_output = run_command("dmesg | grep mmc")

    error_keywords = ["error", "fail", "timeout", "crc", "interrupt", "reset", "re-init"]
    warnings = [
        line for line in dmesg_output.splitlines()
        if any(kw.lower() in line.lower() for kw in error_keywords)
    ]

    return warnings

@app.route("/api/health")
def health_check():
    # any run_command can also be entered manually in terminal
    dt = datetime.datetime.now()

    try:
        cpu_tempC = run_command("vcgencmd measure_temp").replace('temp=','').replace("\'C","")
    except Exception as e:
        cpu_tempC = f"error: {str(e)}"

    try:
        uptime = run_command("uptime").split(',')[0]
    except Exception as e:
        uptime = f"error: {str(e)}"

    try:
        availMem = int(run_command("free -h").split('\n')[1].split()[-1].replace('Mi',''))
        memStatus = 'OK'
        if availMem < 50:
            memStatus = 'VERY LOW'
        elif availMem < 100:
            memStatus = 'LOW'
        memoryUsage = {'available memory':f'{availMem}Mi','status':memStatus}
    except Exception as e:
        memoryUsage = f"error: {str(e)}"

    try:
        diskUsage = parse_disk_usage()#run_command("df -h")
    except Exception as e:
        diskUsage = f"error: {str(e)}"

    try:
        throttled = run_command("vcgencmd get_throttled")
        if "0x0" in throttled:
            throttled = "OK"
        else:
            throttled = "Power supply issue or undervoltage!"
        powerIssues = throttled
    except Exception as e:
        powerIssues = f"error: {str(e)}"

    try:
        sdCardErrors = check_mmc_errors()# run_command("dmesg | grep mmc")
    except Exception as e:
        sdCardErrors = f"error: {str(e)}"

    try:
        fileStatus = check_file_size_uniformity("/home/case/data")
    except Exception as e:
        fileStatus = f"error: {str(e)}"

    return jsonify({
        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_tempC": cpu_tempC,
        "uptime": uptime,
        "memoryUsage": memoryUsage,
        "diskUsage" : diskUsage,
        "powerIssues" : powerIssues,
        "sdCardErrors" : sdCardErrors,
        "fileStatus":fileStatus
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
