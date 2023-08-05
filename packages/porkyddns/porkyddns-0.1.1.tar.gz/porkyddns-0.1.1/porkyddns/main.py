import toml
import typer

from os.path import exists
from porkyddns.utils import get_ip, update

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)


@app.callback()
def callback():
    """
    PorkyDDNS 🐷 - A simple DDNS client for Porkbun's API
    """


@app.command()
def config():
    """
    Write a sample config to stdout (for redirection)
    """
    print(
        """[[domains]]
secret_key = ""
api_key = ""
domain = ""
subdomains = [
    "subdomain1",
    "subdomain2"
]"""
    )


@app.command()
def run(
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
    config: str = typer.Option(
        "/etc/porkyddns.toml", "--config", "-c", help="Config file location"
    ),
):
    """
    Run PorkyDDNS using the config defined in /etc/porkyddns.toml
    """
    if not exists(config):
        print("Config {config} not found! Did you read the README.md?")
        exit(1)

    CONFIGS = toml.load(config)["domains"]
    ip = get_ip()

    if debug:
        print(f"Current IP: {ip}")

    for config in CONFIGS:
        if debug:
            print(f"Updating {config['domain']}")

        for subdomain in config["subdomains"]:
            if debug:
                print(f"Updating {subdomain}.{config['domain']} with {ip}")

            update(subdomain, ip, config)
