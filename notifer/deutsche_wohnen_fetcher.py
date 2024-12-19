from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class DeutscheWohnenFetcher:
    """Fetcher for Deutsche Wohnen using Selenium."""

    def fetch_data(self, website):
        rooms = []
        seen_links = set()  # To track unique room links

        try:
            # Set up Selenium WebDriver
            options = Options()
            options.add_argument("--headless")  # Run in headless mode
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # Iterate through the pages by dynamically modifying the URL
            for page in range(1, website["max_pages"] + 1):
                # Construct the URL for the current page
                current_page_url = f"{website['url']}#page={page}&locale={website['params']['locale']}&commercializationType={website['params']['commercializationType']}&utilizationType={website['params']['utilizationType']}&location={website['params']['location']}"
                driver.get(current_page_url)
                time.sleep(5)  # Allow the page to load completely

                # Locate room cards
                room_cards = driver.find_elements(By.CSS_SELECTOR, website["selectors"]["link_parent"])
                room_cards = [card for card in room_cards if card.is_displayed()]  # Filter visible cards

                print(f"Scraping: {current_page_url} - Found {len(room_cards)} room cards")

                for room_card in room_cards:
                    try:
                        # Extract the room title
                        room_title_element = room_card.find_element(By.CSS_SELECTOR, website["selectors"]["title"])
                        room_title = room_title_element.text.strip() if room_title_element else "Unknown Title"

                        # Extract the room link
                        room_link = room_card.get_attribute("href")
                        if room_link and room_link.startswith("/"):
                            room_link = f"https://www.deutsche-wohnen.com{room_link}"

                        # Check if the link is unique
                        if room_link and room_link not in seen_links:
                            seen_links.add(room_link)  # Add to seen links
                            rooms.append({"title": room_title, "link": room_link})
                    except Exception as e:
                        print(f"Error processing a room card: {e}")
                        continue

            driver.quit()  # Close the browser
            print(f"{website['name']} - Total unique rooms found: {len(rooms)}")
        except Exception as e:
            print(f"Error fetching data for {website['name']}: {e}")
        return rooms
