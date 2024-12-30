import requests
from bs4 import BeautifulSoup
import ssl
import socket
from urllib.parse import urljoin
import argparse

def display_banner():
    banner = """
     ____  _      _       _     _             
    / ___|| |_ __| |_   _| |__ (_)_ __   __ _ 
    \\___ \\| __/ _` | | | | '_ \\| | '_ \\ / _` |
     ___) | || (_| | |_| | |_) | | | | | (_| |
    |____/ \\__\\__,_|\\__,_|_.__/|_|_| |_|\\__, |
                                        |___/ 

    ScriptedBy: Arun
    Author: akisback
    """
    print(banner)

def get_headers(url):
    try:
        print("\n[+] Fetching Headers...")
        response = requests.head(url, timeout=10, allow_redirects=True)
        for key, value in response.headers.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"[-] Error fetching headers: {e}")

def get_ssl_info(url):
    try:
        print("\n[+] Fetching SSL Certificate Info...")
        hostname = url.split("//")[-1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"Issuer: {cert['issuer']}")
                print(f"Subject: {cert['subject']}")
                print(f"Valid From: {cert['notBefore']}")
                print(f"Valid To: {cert['notAfter']}")
    except Exception as e:
        print(f"[-] Error fetching SSL info: {e}")

def enumerate_directories(url, wordlist):
    try:
        print("\n[+] Enumerating Directories...")
        with open(wordlist, 'r') as f:
            paths = f.read().splitlines()
        for path in paths:
            test_url = urljoin(url, path)
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                print(f"Found: {test_url} (200 OK)")
            elif response.status_code == 403:
                print(f"Found: {test_url} (403 Forbidden)")
    except Exception as e:
        print(f"[-] Error during enumeration: {e}")

def check_http_methods(url):
    try:
        print("\n[+] Checking HTTP Methods...")
        response = requests.options(url, timeout=10)
        if "Allow" in response.headers:
            print(f"Allowed Methods: {response.headers['Allow']}")
        else:
            print("[-] Unable to fetch HTTP methods.")
    except Exception as e:
        print(f"[-] Error checking HTTP methods: {e}")

def fetch_technologies(url):
    try:
        print("\n[+] Fetching Technologies...")
        response = requests.get(url, timeout=10)
        server = response.headers.get('Server', 'Unknown')
        x_powered_by = response.headers.get('X-Powered-By', 'Unknown')
        print(f"Server: {server}")
        print(f"X-Powered-By: {x_powered_by}")
    except Exception as e:
        print(f"[-] Error fetching technologies: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Complete Web Information Tool")
    parser.add_argument("url", help="Target URL (e.g., https://example.com)")
    parser.add_argument("--wordlist", help="Path to directory enumeration wordlist")
    args = parser.parse_args()

    display_banner()

    target_url = args.url
    wordlist_path = args.wordlist

    print(f"Starting Web Information Tool on {target_url}")

    # Basic info gathering
    get_headers(target_url)
    get_ssl_info(target_url)
    fetch_technologies(target_url)

    # Optional features
    if wordlist_path:
        enumerate_directories(target_url, wordlist_path)
    check_http_methods(target_url)

    print("\n[+] Web Information Tool Execution Complete!")
