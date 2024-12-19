import time
from fetcher import get_fetcher  # Use get_fetcher to dynamically select fetchers
from utils import detect_changes, format_email_body

class Monitor:
    def __init__(self, websites, email_notifier, check_interval):
        self.websites = websites
        self.email_notifier = email_notifier
        self.check_interval = check_interval
        self.previous_data = {website["name"]: [] for website in websites}

    def send_initial_email(self, website_name, rooms):
        """Sends a test email with the initial list of rooms."""
        if rooms:
            body = f"There are {len(rooms)} rooms currently available on {website_name}.\n\n"
            body += "\n".join([f"{room['title']} - {room['link']}" for room in rooms])
            self.email_notifier.send_email(f"Test Email: {website_name} Initial Data", body)
        else:
            self.email_notifier.send_email(f"Test Email: {website_name} Initial Data", f"No rooms currently available on {website_name}.")

    def monitor_websites(self):
        """Monitors all configured websites for changes."""
        while True:
            for website in self.websites:
                website_name = website["name"]
                
                # Get the appropriate fetcher for the website
                fetcher = get_fetcher(website_name)
                
                # Use the fetcher to fetch data
                current_rooms = fetcher.fetch_data(website)
                previous_rooms = self.previous_data[website_name]

                # Detect changes in room data
                added_rooms, removed_rooms = detect_changes(current_rooms, previous_rooms)

                if added_rooms or removed_rooms:
                    # Format email content
                    email_body = format_email_body(website_name, added_rooms, removed_rooms)
                    
                    # Send email notification
                    self.email_notifier.send_email(f"Room Updates Detected: {website_name}", email_body)
                    
                    print(f"Changes detected for {website_name}:")
                    if added_rooms:
                        print(f"New rooms added: {[room['title'] for room in added_rooms]}")
                    if removed_rooms:
                        print(f"Rooms removed: {[room['title'] for room in removed_rooms]}")

                    # Update previous data
                    self.previous_data[website_name] = current_rooms
                else:
                    print(f"No changes detected for {website_name}.")
            time.sleep(self.check_interval)
