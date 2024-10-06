# README - Basic Grep Automation for Bug Bounty Hunting

This Python script automates running various **grep** commands on a target directory or file to help Bug Bounty Hunters find potential vulnerabilities and sensitive information, such as hardcoded API keys, credentials, and insecure configurations. It outputs the results in a clean, formatted HTML report.

---

## 1. Features

- Searches for common patterns related to security vulnerabilities, such as:
  - Hardcoded API keys
  - Passwords and credentials
  - SQL queries
  - Sensitive files (.bak, .sql, .db)
  - Local File Inclusion (LFI) vulnerabilities
  - Cross-Site Scripting (XSS) vectors
  - AWS S3 bucket references
  - JavaScript functions like `eval()`, `setTimeout()`, and `setInterval()`
  - Credentials in configuration files (username, password, etc.)
  - Base64-encoded strings
  - Insecure hashing functions (md5, sha1, sha256, sha512)
  - Open redirects
  - PHP file inclusion or eval-like vulnerabilities
  - Error messages revealing system paths

- Generates a clean, professional HTML report with results organized into tables.
- Works recursively on directories and files.
- Allows customization of the target directory/file and output HTML file.

---

## 2. Prerequisites

Make sure you have the following installed:
- **Python 3.x**
- The ability to run the `grep` and `find` commands on your system.

---

## 3. Installation

1. Download or clone this script to your machine.
2. Make sure you have Python 3 installed on your system.

---

## 4. Usage

To run the script, open your terminal and use the following command:

```bash
python3 test.py -p /path/to/your/project -o output/grep_report.html
