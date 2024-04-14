#!/usr/bin/python3

import argparse
import pyfiglet
import requests
from termcolor import colored
from tqdm import tqdm

# Define version and author information
VERSION = "1.0"
AUTHOR = "Nurudeen Adebileje"


def print_ascii_art():
    # Generate ASCII art of the word
    ascii_art = pyfiglet.figlet_format("SUBD0M")
    
    # Center-align the ASCII art
    centered_ascii_art = ascii_art.center(80)  # Adjust the width as needed
    
    print(centered_ascii_art)
    print(f"Version: {VERSION}")
    print(f"Author: {AUTHOR}\n")
    
    
def parse_arguments():
    examples = '''
    Examples:
    python3 subd0m.py -t example.com
    python3 subd0m.py -t example.com -f test.txt -o output.txt
    '''
    
    parser = argparse.ArgumentParser(description='Subdomain Enumeration Tool', formatter_class=argparse.RawTextHelpFormatter, epilog=examples)
    parser.add_argument('-t', '--target', dest='target_domain', required=True, help='Target domain')
    parser.add_argument('-f', '--file', dest='wordlist_file', default='test.txt', help='Wordlist file')
    parser.add_argument('-o', '--output', dest='output_file', default='subdomains.txt', help='Output file to save the found subdomains')
    args = parser.parse_args()

    # Check if target_domain and wordlist_file are provided
    if args.target_domain is None:
        parser.error('Target domain is required.')
    elif args.wordlist_file is None:
        parser.error('Wordlist File is required.')
    return args


def make_request(url):
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


def main():
    try:
        print(colored("[*] Welcome to subD0M - Subdomain Enumeration Tool", "green"))
        
        # Parse command-line arguments
        args = parse_arguments()
        target_domain = args.target_domain
        
        # Make request using the provided target domain
        response = make_request(target_domain)
        if response:
            print(colored("[*] Response from target domain:", "yellow"))
            print(response)

        # Iterate through subdomains from a wordlist file
        print(colored("\n[*] Enumerating subdomains:", "yellow"))
        with open(args.wordlist_file, 'r') as file, open(args.output_file, 'w') as output_file:
            num_lines = sum(1 for _ in file)
            file.seek(0)  # Reset file pointer
            for line in tqdm(file, total=num_lines, desc="Progress"):
                subdomain = line.strip() + '.' + target_domain
                response = make_request(subdomain)
                if response:
                    print(colored("[+] Subdomain found: ", "green") + colored(subdomain, "cyan"))
                    output_file.write(subdomain + '\n')
    except KeyboardInterrupt:
        print(colored("\n[!] Execution interrupted by user.", "red"))
    except Exception as e:
        print(colored("[!] An error occurred: ", "red") + str(e))


if __name__ == "__main__":
    print_ascii_art()
    main()
