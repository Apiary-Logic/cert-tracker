import requests
from datetime import datetime

BASE_URL = "http://localhost:5000"

def get_all_staff():
    res = requests.get(f"{BASE_URL}/staff")
    return res.json()

def filter_by_house(house_num):
    all_staff = get_all_staff()
    return [s for s in all_staff if s.get("house") == house_num]

def certs_expiring_this_month():
    all_staff = get_all_staff()
    this_month = datetime.now().strftime("%Y-%m")
    expiring = []
    for staff in all_staff:
        for cert_name, cert_data in staff.get("certifications", {}).items():
            expires = cert_data.get("expires")
            if expires and expires.startswith(this_month):
                expiring.append({
                    "name": staff["name"],
                    "house": staff.get("house"),
                    "cert": cert_name,
                    "expires": expires
                })
    return expiring

def get_all_certs_by_name(name):
    all_staff = get_all_staff()
    for staff in all_staff:
        if staff["name"].lower() == name.lower():
            return staff.get("certifications", {})
    return {}

def pretty_print(title, items):
    print(f"\n=== {title} ===")
    if not items:
        print("No results found.")
        return
    for item in items:
        print(item)

# Examples — you can comment/uncomment or call in interactive mode
if __name__ == "__main__":
    pretty_print("All Staff", get_all_staff())
    pretty_print("Staff in House 22", filter_by_house(22))
    pretty_print("Certs Expiring This Month", certs_expiring_this_month())
    pretty_print("Certs for 'Carmen Lee'", get_all_certs_by_name("Carmen Lee"))
