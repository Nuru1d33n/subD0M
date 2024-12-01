#!/usr/bin/env python3

import argparse
import pyfiglet
import requests
from termcolor import colored
from tqdm import tqdm
import os
import itertools
import json
import csv

# Define version and author information
VERSION = "1.2"
AUTHOR = "Nurudeen Adebileje"

def print_ascii_art():
    """
    Prints ASCII art for the tool logo.
    """
    ascii_art = pyfiglet.figlet_format("SUBD0M")
    centered_ascii_art = ascii_art.center(80)
    print(centered_ascii_art)
    print(f"Version: {VERSION}")
    print(f"Author: {AUTHOR}\n")

def parse_arguments():
    """
    Parses command-line arguments.
    """
    examples = '''
    Examples:
    ./subD0M.py -t example.com -f test.txt
    ./subD0M.py -t example.com -f test.txt -o output.txt
    ./subD0M.py -t example.com -b 2 -o output.json -v
    '''
    
    parser = argparse.ArgumentParser(description='Subdomain Enumeration Tool', formatter_class=argparse.RawTextHelpFormatter, epilog=examples)
    parser.add_argument('-t', '--target', dest='target_domain', required=True, help='Target domain (e.g., example.com)')
    parser.add_argument('-f', '--file', dest='wordlist_file', help='Wordlist file for enumeration')
    parser.add_argument('-o', '--output', dest='output_file', default='subdomains.txt', help='Output file to save found subdomains')
    parser.add_argument('--json', dest='json_output', help='Output file to save subdomains in JSON format')
    parser.add_argument('--csv', dest='csv_output', help='Output file to save subdomains in CSV format')
    parser.add_argument('-b', '--bruteforce', dest='bruteforce_length', type=int, help='Enable bruteforce with specified character count (e.g., 2 or 3)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode for detailed output')
    return parser.parse_args()

def make_request(url, verbose=False):
    """
    Makes an HTTP(S) request to a URL and returns the response.
    """
    try:
        response = requests.get(url, timeout=5)
        if verbose:
            print(colored(f"[DEBUG] {url} returned status {response.status_code}", "blue"))
        return response
    except requests.RequestException as e:
        if verbose:
            print(colored(f"[DEBUG] {url} failed with error: {e}", "red"))
        return None

def save_output(subdomains, output_file, json_output, csv_output):
    """
    Saves subdomains to text, JSON, and CSV formats.
    """
    if output_file:
        with open(output_file, 'w') as f:
            for subdomain, status in subdomains:
                f.write(f"{subdomain} ({status})\n")
            print(colored(f"[*] Subdomains saved to {output_file}", "green"))

    if json_output:
        with open(json_output, 'w') as json_file:
            json.dump(subdomains, json_file, indent=4)
        print(colored(f"[*] Subdomains saved to {json_output}", "green"))

    if csv_output:
        with open(csv_output, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Subdomain", "Status Code"])
            for subdomain, status in subdomains:
                writer.writerow([subdomain, status])
        print(colored(f"[*] Subdomains saved to {csv_output}", "green"))

def bruteforce_subdomains(length, target_domain):
    """
    Generates subdomains dynamically based on the specified character length.
    """
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for combination in itertools.product(characters, repeat=length):
        yield ''.join(combination) + '.' + target_domain

def main():
    """
    Main function for subdomain enumeration.
    """
    try:
        print(colored("[*] Welcome to subD0M - Subdomain Enumeration Tool", "green"))
        args = parse_arguments()
        target_domain = args.target_domain
        verbose = args.verbose
        subdomains = []

        # Determine the source of subdomain candidates
        if args.wordlist_file and os.path.isfile(args.wordlist_file):
            print(colored(f"[*] Using wordlist: {args.wordlist_file}", "yellow"))
            with open(args.wordlist_file, 'r') as file:
                subdomain_candidates = [line.strip() + '.' + target_domain for line in file]
        elif args.bruteforce_length:
            print(colored(f"[*] Using bruteforce with length {args.bruteforce_length}", "yellow"))
            subdomain_candidates = list(bruteforce_subdomains(args.bruteforce_length, target_domain))
        else:
            print(colored("[!] Error: Provide either a wordlist file (-f) or enable bruteforce (-b).", "red"))
            return

        # Enumerate subdomains
        print(colored("\n[*] Enumerating subdomains:", "yellow"))
        for subdomain in tqdm(subdomain_candidates, desc="Progress"):
            response = make_request(f"http://{subdomain}", verbose)
            if response:
                status_code = response.status_code
                print(colored(f"[+] Found: {subdomain} ({status_code})", "green"))
                subdomains.append((subdomain, status_code))
            elif verbose:
                print(colored(f"[-] No response: {subdomain}", "red"))

        # Save output
        save_output(subdomains, args.output_file, args.json_output, args.csv_output)

    except KeyboardInterrupt:
        print(colored("\n[!] Interrupted by user.", "red"))
    except Exception as e:
        print(colored(f"[!] Error: {str(e)}", "red"))

if __name__ == "__main__":
    print_ascii_art()
    main()
