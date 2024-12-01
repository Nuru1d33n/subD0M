
# Subdomain Enumeration Tool (subD0M)

subD0M is a Python-based command-line tool for enumerating subdomains of a target domain. It supports using a wordlist file or dynamic bruteforce generation. It also validates subdomains by checking their HTTP status codes and saves the results for further analysis.

## Features

- Enumerates subdomains of a target domain using:
  - A provided wordlist file.
  - **Bruteforce generation** based on a specified character count.
- Supports both HTTP and HTTPS requests to subdomains.
- Displays and saves **HTTP status codes** for discovered subdomains.
- Saves the found subdomains and their details to an output file.

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:Nuru1d33n/subD0M.git
   cd subD0M
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Make the tool executable:

   ```bash
   chmod +x subD0M.py
   ```

## Usage

Run the tool with the following command:

```bash
./subD0M.py -t <target_domain> [options]
```

### Arguments:
- `-t, --target <target_domain>`: The domain you want to enumerate subdomains for (required).
- `-f, --file <wordlist_file>`: The path to a wordlist file containing potential subdomains (default: `test.txt`).
- `-o, --output <output_file>`: The desired filename to save the found subdomains (default: `subdomains.txt`).
- `-b, --bruteforce <char_count>`: Enable bruteforce generation of subdomains with a specified number of characters (e.g., `2` or `3`).

### Examples

#### Using a Wordlist
```bash
./subD0M.py -t example.com -f test.txt -o output.txt
```

#### Using Bruteforce
To generate subdomains dynamically with two-character combinations:
```bash
./subD0M.py -t example.com -b 2 -o output.txt
```

To generate subdomains dynamically with three-character combinations:
```bash
./subD0M.py -t example.com -b 3
```

#### Using Default Options
```bash
./subD0M.py -t example.com
```
By default:
- Wordlist: `test.txt`
- Output: `subdomains.txt`

### Output
The results will include:
- Found subdomains
- Their HTTP status codes
- Saved in the specified output file

## Screenshots

![Screenshot 1](screenshots/subd0m1.png)
![Screenshot 2](screenshots/subD0M2.png)
![Screenshot 3](screenshots/subD0M3.png)

## Author

Nurudeen Adebileje

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
