from concurrent.futures import ThreadPoolExecutor
from utils import resolve_subdomain, make_request


def fetch_subdomain(subdomain):
    """Fetch a single subdomain, check DNS resolution, and return it if valid."""
    resolved, ips = resolve_subdomain(subdomain)
    if resolved:
        # Check if the subdomain is reachable
        status = make_request(subdomain)
        return {"subdomain": resolved, "ips": ips, "status": status}
    return None


def enumerate_subdomains(subdomains, target_domain, threads=10, verbose=False):
    """Enumerate subdomains using multi-threading and DNS resolution."""
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for result in executor.map(fetch_subdomain, subdomains):
            if result:
                results.append(result)
                if verbose:
                    print(f"[+] Subdomain found: {result['subdomain']} -> {', '.join(result['ips'])} - Status: {result['status']}")
    return results
