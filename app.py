import json
import os
import ipaddress
from flask import Flask, request, render_template

app = Flask(__name__)

def load_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def find_all_regions_and_services(ip, data):
    ip = ipaddress.ip_address(ip)
    results = []
    for item in data["values"]:
        for cidr in item["properties"]["addressPrefixes"]:
            if ip in ipaddress.ip_network(cidr):
                serviceId = item["id"]
                name = item["name"]
                regionId = item["properties"]["regionId"]
                region = item["properties"]["region"]
                service = item["properties"]["systemService"]
                results.append((serviceId, name, regionId, region, service))
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    ip = request.form['ip']
    file_path = "ServiceTags_Public_20250127.json"  # Path to your JSON file

    data = load_json(file_path)
    results = find_all_regions_and_services(ip, data)

    # sort results per longer name and system service descendantly
    results = sorted(results, key=lambda x: (len(x[1]), x[4]), reverse=True)

    # results = sorted(results, key=lambda x: (len(x[1]), x[4]))

    return render_template('results.html', results=results, ip=ip)

if __name__ == "__main__":
    app.run(debug=True)
