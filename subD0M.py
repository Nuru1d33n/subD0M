#!/usr/bin/env python3

import argparse
import pyfiglet
import requests
from termcolor import colored
from tqdm import tqdm
import os

# Define version and author information
VERSION = "1.0"
AUTHOR = "Nurudeen Adebileje"

def print_ascii_art():
    """
    Function to print the ASCII art for the tool logo.
    """
    ascii_art = pyfiglet.figlet_format("SUBD0M")
    centered_ascii_art = ascii_art.center(80)  # Adjust the width as needed
    print(centered_ascii_art)
    print(f"Version: {VERSION}")
    print(f"Author: {AUTHOR}\n")


def parse_arguments():
    """
    Function to parse the command-line arguments using argparse.
    """
    examples = '''
    Examples:
    python3 subD0M.py -t example.com
    python3 subD0M.py -t example.com -f test.txt -o output.txt
    '''
    
    parser = argparse.ArgumentParser(description='Subdomain Enumeration Tool', formatter_class=argparse.RawTextHelpFormatter, epilog=examples)
    parser.add_argument('-t', '--target', dest='target_domain', required=True, help='Target domain (e.g., example.com)')
    parser.add_argument('-f', '--file', dest='wordlist_file', default='subdomains-wodlist.txt', help='Wordlist file to use for enumeration')
    parser.add_argument('-o', '--output', dest='output_file', default='subdomains.txt', help='Output file to save found subdomains')
    parser.add_argument('--json', dest='json_output', help='Output file to save subdomains in JSON format')
    parser.add_argument('--csv', dest='csv_output', help='Output file to save subdomains in CSV format')
    args = parser.parse_args()

    return args


def make_request(url):
    """
    Makes an HTTP(S) request to a given URL and returns the response status.
    Handles missing schema, SSL errors, and connection issues.
    """
    try:
        # Attempt to make a request using the provided URL
        response = requests.get(url)
        return response
    except requests.exceptions.MissingSchema:
        # If the URL is missing a schema, try adding 'http://' and 'https://'
        try:
            response = requests.get("https://" + url)
            return response
        except requests.exceptions.SSLError:
            # If HTTPS request fails due to SSL error, try HTTP
            response = requests.get("http://" + url)
            return response
        except requests.exceptions.ConnectionError:
            pass  # Ignore connection errors
    except requests.RequestException as e:
        return e  # Return the exception if any other request exception occurs


def save_output(subdomains, output_file, json_output, csv_output):
    """
    Saves the found subdomains in the specified formats: text, JSON, CSV.
    """
    if output_file:
        with open(output_file, 'w') as f:
            for subdomain in subdomains:
                f.write(subdomain + '\n')
            print(colored(f"[*] Subdomains saved to {output_file}", "green"))

    if json_output:
        import json
        with open(json_output, 'w') as json_file:
            json.dump(subdomains, json_file, indent=4)
        print(colored(f"[*] Subdomains saved to {json_output}", "green"))

    if csv_output:
        import csv
        with open(csv_output, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for subdomain in subdomains:
                writer.writerow([subdomain])
        print(colored(f"[*] Subdomains saved to {csv_output}", "green"))


def main():
    """
    Main function to handle subdomain enumeration and display.
    """
    try:
        print(colored("[*] Welcome to subD0M - Subdomain Enumeration Tool", "green"))
        
        # Parse command-line arguments
        args = parse_arguments()
        target_domain = args.target_domain
        
        # Check if the wordlist file exists
        if not os.path.isfile(args.wordlist_file):
            print(colored(f"[!] Wordlist file '{args.wordlist_file}' not found.", "red"))
            return
        
        # Initialize list to store found subdomains
        found_subdomains = []
        
        # Enumerate subdomains using the wordlist
        print(colored("\n[*] Enumerating subdomains:", "yellow"))
        with open(args.wordlist_file, 'r') as file:
            num_lines = sum(1 for _ in file)
            file.seek(0)  # Reset file pointer
            for line in tqdm(file, total=num_lines, desc="Progress"):
                subdomain = line.strip() + '.' + target_domain
                response = make_request(subdomain)
                if isinstance(response, requests.Response):
                    if response.status_code == 200:
                        print(colored("[+] Subdomain found: ", "green") + colored(subdomain, "cyan"))
                        found_subdomains.append(subdomain)
                    else:
                        print(colored(f"[-] Subdomain {subdomain} returned status {response.status_code}", "red"))
                else:
                    print(colored(f"[-] Error with {subdomain}: {response}", "red"))

        # Save found subdomains to the specified file(s)
        save_output(found_subdomains, args.output_file, args.json_output, args.csv_output)
        
    except KeyboardInterrupt:
        print(colored("\n[!] Execution interrupted by user.", "red"))
    except Exception as e:
        print(colored("[!] An error occurred: ", "red") + str(e))


if __name__ == "__main__":
    # Print ASCII art and run the main function
    print_ascii_art()
    main()
