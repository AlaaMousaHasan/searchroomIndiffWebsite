from bs4 import BeautifulSoup
import requests
from deutsche_wohnen_fetcher import DeutscheWohnenFetcher


# Base fetcher class
class BaseRoomFetcher:
    """Base class for room fetchers."""
    def fetch_data(self, website):
        raise NotImplementedError("Subclasses must implement `fetch_data`.")


class DegewoFetcher(BaseRoomFetcher):
    """Fetcher for Degewo Search."""
    def fetch_data(self, website):
        rooms = []
        try:
            for page in website["pages"]:
                params = website["params"].copy()
                params["page"] = page
                response = requests.get(website["url"], params=params)
                if response.status_code != 200:
                    print(f"Error fetching page {page} from {website['name']}: {response.status_code}")
                    continue

                soup = BeautifulSoup(response.content, "html.parser")
                room_cards = soup.select(website["selectors"]["title"])

                print(f"{website['name']} - Page {page}: Found {len(room_cards)} room cards")

                for room in room_cards:
                    room_title = room.text.strip()
                    room_link_element = room.find_parent(website["selectors"]["link_parent"])
                    
                    # Handle relative links
                    room_link = None
                    if room_link_element and room_link_element.has_attr("href"):
                        room_link = room_link_element["href"].strip()
                        if room_link.startswith("/"):
                            room_link = f"https://immosuche.degewo.de{room_link}"

                    if room_link:
                        rooms.append({"title": room_title, "link": room_link})
            print(f"{website['name']} - Total rooms found: {len(rooms)}")
        except Exception as e:
            print(f"Error fetching data for {website['name']}: {e}")
        return rooms



FETCHER_MAPPING = {
    "Degewo Search": DegewoFetcher(),
}

def get_fetcher(name):
    """Returns the appropriate fetcher for a given website name."""
    return FETCHER_MAPPING.get(name)
