from config import WEBSITES
from notifier import EmailNotifier
from monitor import Monitor
from fetcher import get_fetcher  # Import the fetcher dispatcher

# Email Configuration
EMAIL_SENDER = ""  # Sender's email
EMAIL_PASSWORD = ""  # Sender's app password
EMAIL_RECIPIENT = ""  # Recipient's email
CHECK_INTERVAL = 60  # Time between checks in seconds

def main():
    email_notifier = EmailNotifier(EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT)
    monitor = Monitor(WEBSITES, email_notifier, CHECK_INTERVAL)

    print("Fetching initial data for all websites...")
    for website in WEBSITES:
        website_name = website["name"]
        fetcher = get_fetcher(website_name)  # Get the appropriate fetcher
        current_rooms = fetcher.fetch_data(website)  # Fetch data using the fetcher
        monitor.previous_data[website_name] = current_rooms
        monitor.send_initial_email(website_name, current_rooms)

    print("\nStarting website monitoring...")
    monitor.monitor_websites()


if __name__ == "__main__":
    main()
