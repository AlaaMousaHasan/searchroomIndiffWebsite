import time
from deutsche_wohnen_fetcher import DeutscheWohnenFetcher
from utils import detect_changes, format_email_body


class DeutscheWohnenMonitor:
    def __init__(self, website, email_notifier, check_interval):
        self.website = website
        self.email_notifier = email_notifier
        self.check_interval = check_interval
        self.previous_data = []

    def send_initial_email(self, rooms):
        """Sends an initial email with the list of rooms."""
        if rooms:
            body = f"There are {len(rooms)} rooms currently available on {self.website['name']}.\n\n"
            body += "\n".join([f"{room['title']} - {room['link']}" for room in rooms])
            self.email_notifier.send_email(f"Test Email: {self.website['name']} Initial Data", body)
        else:
            self.email_notifier.send_email(
                f"Test Email: {self.website['name']} Initial Data",
                f"No rooms currently available on {self.website['name']}."
            )

    def monitor_website(self):
        """Monitors the Deutsche Wohnen website for changes."""
        fetcher = DeutscheWohnenFetcher()
        while True:
            current_rooms = fetcher.fetch_data(self.website)
            added_rooms, removed_rooms = detect_changes(current_rooms, self.previous_data)

            if added_rooms or removed_rooms:
                email_body = format_email_body(self.website["name"], added_rooms, removed_rooms)
                self.email_notifier.send_email(f"Room Updates Detected: {self.website['name']}", email_body)

                print(f"Changes detected for {self.website['name']}:")
                if added_rooms:
                    print(f"New rooms added: {[room['title'] for room in added_rooms]}")
                if removed_rooms:
                    print(f"Rooms removed: {[room['title'] for room in removed_rooms]}")

                self.previous_data = current_rooms
            else:
                print(f"No changes detected for {self.website['name']}.")

            time.sleep(self.check_interval)
