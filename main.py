#!/usr/bin/python3

import argparse
from subdomain_enumeration import enumerate_subdomains
from utils import print_ascii_art, save_to_json, save_to_csv
from bruteforce import generate_subdomains


def parse_arguments():
    """Parse command-line arguments with short and long options."""
    examples = '''
    Examples:
    python3 subd0m.py -t example.com
    python3 subd0m.py -t example.com --bruteforce 3
    python3 subd0m.py -t example.com -f wordlist.txt --json output.json
    '''
    parser = argparse.ArgumentParser(
        description='Subdomain Enumeration Tool',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=examples
    )

    # Short and long options
    parser.add_argument('-t', '--target', required=True, help='Target domain (e.g., example.com)')
    parser.add_argument('-f', '--file', default=None, help='Wordlist file (optional if using brute-force)')
    parser.add_argument('-b', '--bruteforce', type=int, help='Enable brute-force mode with specified length')
    parser.add_argument('-o', '--output', default='subdomains.txt', help='Output file for results')
    parser.add_argument('-j', '--json', help='Save results in JSON format')
    parser.add_argument('-c', '--csv', help='Save results in CSV format')
    parser.add_argument('-T', '--threads', type=int, default=10, help='Number of threads for parallel processing')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode (detailed output)')

    args = parser.parse_args()

    return args


def main():
    """Main function to coordinate subdomain enumeration."""
    # Print banner
    print_ascii_art()

    # Parse arguments
    args = parse_arguments()

    # Fetch or generate subdomains
    if args.file:
        with open(args.file, 'r') as file:
            subdomains = [line.strip() + '.' + args.target for line in file]
    elif args.bruteforce:
        subdomains = generate_subdomains(args.target, args.bruteforce)

    # Enumerate subdomains with status
    results = enumerate_subdomains(subdomains, args.target, args.threads, args.verbose)

    # Save results to output files
    if results:
        with open(args.output, 'w') as text_file:
            for result in results:
                text_file.write(f"{result['subdomain']} - {result['status']}\n")
        print(f"[*] Results saved to {args.output}")

        if args.json:
            save_to_json(results, args.json)
        if args.csv:
            save_to_csv(results, args.csv)
    else:
        print("[!] No subdomains found.")


if __name__ == "__main__":
    main()
