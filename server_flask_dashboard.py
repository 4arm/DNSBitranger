# server_flask_dashboard.py
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json
import os
import requests

app = Flask(__name__)
DATA_FILE = "nxdomain_logs.json"

# Load existing logs
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        logs = json.load(f)
else:
    logs = []

def check_quad9_block(domain):
    """Check if a domain is blocked by Quad9"""
    try:
        url = f"https://quad9.net/result/{domain}"
        resp = requests.get(url, timeout=5)
        if "This domain is BLOCKED" in resp.text:
            return True
    except:
        pass
    return False

@app.route("/nxdomain", methods=["POST"])
def receive_nxdomain():
    data = request.json
    # Check if already exists
    if any(x['timestamp'] == data['timestamp'] and x['domain'] == data['domain'] for x in logs):
        return jsonify({"status": "duplicate"}), 200

    # Check if domain is blocked
    data['blocked_by_quad9'] = check_quad9_block(data['domain'])

    logs.append(data)
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    return jsonify({"status": "received"}), 200

@app.route("/")
def dashboard():
    sorted_logs = sorted(logs, key=lambda x: x['timestamp'], reverse=True)
    html = """
    <html>
    <head>
        <title>NXDOMAIN Dashboard</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; cursor: pointer; }
            tr.blocked { background-color: #ffdddd; }
        </style>
        <script>
            function sortTable(n) {
              var table = document.getElementById("nxdomainTable");
              var rows = table.rows, switching = true, dir = "desc", switchcount = 0;
              while (switching) {
                switching = false;
                var shouldSwitch, i;
                for (i = 1; i < (rows.length - 1); i++) {
                  shouldSwitch = false;
                  var x = rows[i].getElementsByTagName("TD")[n];
                  var y = rows[i + 1].getElementsByTagName("TD")[n];
                  if (dir == "asc" ? x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()
                                   : x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                  }
                }
                if (shouldSwitch) {
                  rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                  switching = true;
                  switchcount++;
                } else if (switchcount == 0 && dir == "asc") {
                  dir = "desc";
                  switching = true;
                }
              }
            }
        </script>
    </head>
    <body>
        <h2>NXDOMAIN Query Log</h2>
        <table id="nxdomainTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Timestamp</th>
                    <th onclick="sortTable(1)">Domain</th>
                    <th onclick="sortTable(2)">Source IP</th>
                </tr>
            </thead>
            <tbody>
                {% for log in logs %}
                <tr class="{{ 'blocked' if log.blocked_by_quad9 else '' }}">
                    <td>{{ log.timestamp }}</td>
                    <td>{{ log.domain }}</td>
                    <td>{{ log.source_ip }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(html, logs=sorted_logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
