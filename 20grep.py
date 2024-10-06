import os
import subprocess
import argparse
from datetime import datetime
# source hf 
# html template format
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grep Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        table, th, td {{ border: 1px solid black; }}
        th, td {{ padding: 10px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Grep Results - Bug Bounty Hunting</h1>
    <p>Generated on: {date}</p>
    {content}
</body>
</html>
"""

# function to run grep commands and collect results
def run_grep_commands(target_dir):
    commands = [
        ("Hardcoded API Keys", f"grep -rE -i 'api[_-]?(key|id)?[[:space:]]*[=:][[:space:]]*[A-Za-z0-9]{{8,}}' {target_dir}"),
        ("Passwords and Variations", f"grep -rE -i '(password|pass|passwd|pwd)[[:space:]]*[=:][[:space:]]*' {target_dir}"),
        ("SQL Queries", f"grep -rE -i '(SELECT .* FROM|INSERT INTO|UPDATE .* SET|DELETE FROM)[[:space:]]' {target_dir}"),
        ("Sensitive Files (.bak, .sql, .db)", f"find {target_dir} -type f \( -name '*.bak' -o -name '*.sql' -o -name '*.db' \)"),
        ("Local File Inclusion (LFI)", f"grep -rE -i '(include|require|file_get_contents)[[:space:]]*\\(.*\\$_(GET|POST|REQUEST)' {target_dir}"),
        ("Cross-Site Scripting (XSS)", f"grep -rE -i '(echo|print|document\\.write)[[:space:]]*\\(.*\\$_(GET|POST|REQUEST)' {target_dir}"),
        ("AWS S3 Buckets", f"grep -rE -i '(s3\\.amazonaws\\.com|\\.s3-[a-zA-Z0-9-]+\\.amazonaws\\.com)' {target_dir}"),
        ("Eval and Similar Functions (JS)", f"grep -rE -i '(eval\\(|Function\\(|setTimeout\\(|setInterval\\()' {target_dir}"),
        ("PHP Variable Assignment", f"grep -rE -i '\\$_(POST|GET|REQUEST|COOKIE)' {target_dir}"),
        ("CSRF Tokens", f"grep -rE -i '(csrf|xsrf|token)' {target_dir}"),
        ("HTTP URLs (Upgrade to HTTPS)", f"grep -rE -i 'http:\\/\\/' {target_dir}"),
        ("Credentials (username and password)", f"grep -rE -i '(username|user|password|pass)[[:space:]]*[:=][[:space:]]*' {target_dir}"),
        ("Base64 Encoded Strings", f"grep -rE -i '[A-Za-z0-9+/=]{{16,}}' {target_dir}"),
        ("Open Redirect", f"grep -rE -i 'location[[:space:]]*:[[:space:]]*\\$_(GET|POST|REQUEST)' {target_dir}"),
        ("Unsafe File Uploads", f"grep -rE -i '(move_uploaded_file|upload_file|copy|rename)' {target_dir}"),
        ("Insecure Hashing Functions", f"grep -rE -i '(md5|sha1|sha256|sha512)\\(' {target_dir}"),
        ("Error Messages with System Paths", f"grep -rE -i '(warning.*path|fatal error|failed to open stream|no such file or directory)' {target_dir}"),
        ("JavaScript Functions (eval, setTimeout)", f"grep -rE -i '(eval|setTimeout|setInterval)' {target_dir}"),
        ("Eval and Similar Functions (PHP)", f"grep -rE -i '(eval|system|exec|shell_exec)\\(' --include='*.php' {target_dir}"),
        ("Commented-out Code", f"grep -rE -i '(//|#|/\\*)' {target_dir}")
    ]

    results = []
    for description, command in commands:
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.DEVNULL)
            output = output.strip()
            if output:
                result_table = generate_table(description, output.splitlines())
                results.append(result_table)
            else:
                results.append(f"<h3>{description}</h3><p>No results found.</p>")
        except subprocess.CalledProcessError:
            results.append(f"<h3>{description}</h3><p>Error running command.</p>")
    return results

# function to generate HTML table from results
def generate_table(title, data):
    table = f"<h3>{title}</h3>\n"
    table += "<table>\n<tr><th>Line</th></tr>\n"
    for line in data:
        table += f"<tr><td>{line}</td></tr>\n"
    table += "</table>\n"
    return table

# main function to generate the HTML report
def generate_html_report(target_dir, output_file):
    print(f"[+] Running grep commands on {target_dir} and generating report...")
    grep_results = run_grep_commands(target_dir)
    
    content = "\n".join(grep_results)
    html_output = html_template.format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content=content)

    with open(output_file, "w") as file:
        file.write(html_output)
    
    print(f"[+] Report saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run advanced grep commands and generate an HTML report.')
    parser.add_argument('-p', '--path', required=True, help='The path to the file or folder to search.')
    parser.add_argument('-o', '--output', required=True, help='The name of the output HTML file.')

    args = parser.parse_args()

    # Ensure the output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the grep automation with the provided arguments
    generate_html_report(args.path, args.output)
