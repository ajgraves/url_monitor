# url_monitor
url_monitor.py, a quick-and-dirty python script to monitor URLs for changes, and email you the content of the page that changed.

# Configuration
The script requires you to configure several options, located near the top:

```python
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
```

**URLS_TO_MONITOR** is an array of the pages/sites you wish to monitor. Simply add them here.

**SENDER_EMAIL** is the from email address of the email notification.

**SENDER_PASSWORD** is the password needed to authenticate to the SMTP host.

**RECEIVER_EMAIL** is the email address the email notification should be sent to.

**SMTP_SERVER** is the outgoing mail server address.

**SMTP_PORT** is the port to connect to on the outgoing mail server.

**STORAGE_DIR** is where the script will store current versions of the page(s) being monitored. This is necessary so the script can compare the current page with what it has seen before.

**DEBUG** allows you to see potentially useful outputs. If the script is being run from `crontab` then it's best to leave this value as 0, preventing unnecessary output. However, if you're going to run the script from the command line directly, or through another automation tool where you do want to capture output, then set this value to **1** to enable the output.

# Usage
Simply invoke the `url_monitor.py` command from the command line directly, either by setting the script to executable (`chmod +x url_monitor.py`) or by executing `python3 url_monitor.py`.
