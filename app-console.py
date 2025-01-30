import json
import os
import ipaddress

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

def main():
    file_path = "ServiceTags_Public_20250127.json"  # Path to your JSON file
    ip = "20.48.202.160"  # '20.40.104.96' # '4.149.254.68' # input("Enter an IP address: ")

    data = load_json(file_path)
    results = find_all_regions_and_services(ip, data)

    if results:
        for serviceId, name, regionId, region, systemService in results:
            print(f"Id: {serviceId}")
            print(f"Name: {name}")
            print(f"RegionId: {regionId}")
            print(f"Region: {region}")
            print(f"SystemService: {systemService}")
            print(f"------------------------------")
    else:
        print("IP address not found in any CIDR range.")

if __name__ == "__main__":
    main()
