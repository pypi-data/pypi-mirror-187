import requests
import urllib.parse
import sys


def get_ip():
    return requests.get(f"https://ifconfig.me").text


def update(subdomain: str, ip: str, config: dict):
    request = {
        "secretapikey": config["secret_key"],
        "apikey": config["api_key"],
        "content": ip,
        "ttl": "600",
    }

    url = f"https://api-ipv4.porkbun.com/api/json/v3/dns/editByNameType/{config['domain']}/A/{urllib.parse.quote(subdomain)}"
    result = requests.post(url, json=request)

    if result.status_code != 200:
        print(
            f"Uh oh! Failed updating {subdomain} of {config['domain']} to {ip}\n\nHTTP Result:\n{result.text}",
            file=sys.stderr,
        )
