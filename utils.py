import json
import csv
import re
import requests
import dns.resolver


def print_ascii_art():
    """Display the ASCII art banner with version and author."""
    import pyfiglet
    ascii_art = pyfiglet.figlet_format("SUBD0M")
    print(ascii_art)
    print(f"Version: 2.2")
    print(f"Author: Nurudeen Adebileje\n")


def is_valid_domain(domain):
    """Validate domain format using a regular expression."""
    pattern = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain)


def make_request(url):
    """Send an HTTP request to a given URL and check if it is up or down."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return 'up'
        return 'down'
    except requests.exceptions.RequestException:
        return 'down'


def resolve_subdomain(subdomain):
    """Resolve a subdomain to its IP address using DNS."""
    try:
        answers = dns.resolver.resolve(subdomain, 'A')
        ips = [answer.to_text() for answer in answers]
        return subdomain, ips
    except Exception:
        return None, None


def save_to_json(results, filename):
    """Save results to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print(f"[*] Results saved to {filename}")


def save_to_csv(results, filename):
    """Save results to a CSV file."""
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Subdomain', 'IP Addresses', 'Status'])
        for result in results:
            writer.writerow([result['subdomain'], ', '.join(result['ips']), result['status']])
    print(f"[*] Results saved to {filename}")
