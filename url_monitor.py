import requests
import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration
URLS_TO_MONITOR = [
    "https://example.com",
    "https://example2.com"
]
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_specific_password"  # Use app-specific password if using Gmail
RECEIVER_EMAIL = "receiver_email@example.com"
SMTP_SERVER = "smtp.gmail.com"  # Adjust if using different email provider
SMTP_PORT = 587
STORAGE_DIR = os.path.expanduser("~/reports/url_monitor")  # Storage directory
DEBUG = 0  # Set to 1 for debug output, 0 to suppress

def ensure_storage_dir():
    """Create storage directory if it doesn't exist"""
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

def get_content_hash(content):
    """Generate a hash of the content for comparison"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def extract_main_content(html):
    """Extract main readable text from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    # Get text
    text = soup.get_text()
    # Break into lines and remove leading/trailing whitespace
    lines = (line.strip() for line in text.splitlines())
    # Remove empty lines and join into a single string
    main_content = '\n'.join(line for line in lines if line)
    return main_content

def get_page_title(html):
    """Extract the page title from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('title')
    return title_tag.get_text().strip() if title_tag else "No Title Found"

def save_content(url, content):
    """Save content to a file named after URL's hash in STORAGE_DIR"""
    ensure_storage_dir()
    filename = os.path.join(STORAGE_DIR, f"cache_{hashlib.md5(url.encode('utf-8')).hexdigest()}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def get_previous_content(url):
    """Retrieve previous content if it exists from STORAGE_DIR"""
    ensure_storage_dir()
    filename = os.path.join(STORAGE_DIR, f"cache_{hashlib.md5(url.encode('utf-8')).hexdigest()}.txt")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def send_email(subject, body):
    """Send email notification"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        if DEBUG:
            print(f"Email sent successfully at {datetime.now()}")
    except Exception as e:
        if DEBUG:
            print(f"Failed to send email: {str(e)}")

def check_url(url):
    """Check if URL content has changed"""
    try:
        # Fetch current content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text
        current_content = extract_main_content(html_content)  # Extract main text
        page_title = get_page_title(html_content)  # Extract page title
        current_hash = get_content_hash(current_content)

        # Get previous content
        previous_content = get_previous_content(url)
        
        if previous_content is None:
            if DEBUG:
                print(f"First run for {url} - saving initial content")
            save_content(url, current_content)
        else:
            previous_hash = get_content_hash(previous_content)
            if current_hash != previous_hash:
                if DEBUG:
                    print(f"Change detected at {url}")
                # Save new content
                save_content(url, current_content)
                # Send notification with page title in subject
                subject = f"Content Change Detected: {page_title}"
                body = f"URL: {url}\n\nNew Content:\n{current_content}"
                send_email(subject, body)
            else:
                if DEBUG:
                    print(f"No change detected at {url}")

    except requests.RequestException as e:
        if DEBUG:
            print(f"Error checking {url}: {str(e)}")

def main():
    if DEBUG:
        print(f"Starting URL monitoring at {datetime.now()}")
    for url in URLS_TO_MONITOR:
        check_url(url)
    if DEBUG:
        print("Monitoring complete")

if __name__ == "__main__":
    main()
