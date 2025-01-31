import json
import ipaddress
from flask import Flask, request, jsonify, render_template

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
                results.append({
                    "serviceId": serviceId,
                    "name": name,
                    "regionId": regionId,
                    "region": region,
                    "systemService": service
                })
    return results

@app.route('/')
def index():
    ip = request.args.get('ip', '')
    return render_template('index.html', ip=ip)

@app.route('/search')
def search():
    ip = request.args.get('ip')
    file_path = "ServiceTags_Public_20250127.json"  # Path to your JSON file
    data = load_json(file_path)
    results = find_all_regions_and_services(ip, data)
    return jsonify(results=results)

if __name__ == "__main__":
    app.run(debug=True)