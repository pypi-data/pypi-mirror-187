import requests


def get_ip_data(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/geo")
    if response:
        return response.json()


def get_cat_fact():
    response = requests.get("https://catfact.ninja/fact")
    if response:
        return response.json()
