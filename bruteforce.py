import itertools


def generate_subdomains(domain, length, charset='abcdefghijklmnopqrstuvwxyz0123456789'):
    """Generate subdomains dynamically using brute-force."""
    print(f"[*] Brute-forcing subdomains with length {length}...")
    subdomains = []
    for combo in itertools.product(charset, repeat=length):
        subdomains.append(''.join(combo) + '.' + domain)
    return subdomains
