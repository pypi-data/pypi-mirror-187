import requests
import urllib.parse
import sys
import toml

from os.path import exists


if not exists("/etc/porkyddns.toml"):
    print("Config /etc/porkyddns.toml not found! Did you read the README.md?")
    exit(1)


CONFIGS = toml.load("/etc/porkyddns.toml")["domains"]


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


def run():
    ip = get_ip()
    for config in CONFIGS:
        for subdomain in config["subdomains"]:
            update(subdomain, ip, config)
