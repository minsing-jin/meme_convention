import requests
import json
import random
import io
from typing import Optional

API_KEY = "AIzaSyCDvNCX2zt3uDyRH9CuKClsQlubMLxCl78"

class TenorMemeProvider:
    def __init__(self):
        self.api_key = API_KEY
        self.client_key = "random_meme_app"
        self.base_url = "https://tenor.googleapis.com/v2"

    def get_random_meme(self, context_category: str, limit: int = 50):
        """
        Fetches a random GIF/meme from Tenor API based on context category.
        Returns bytes object compatible with your existing methods.

        Args:
            context_category: Search term/category for memes
            limit: Number of results to fetch before selecting random one

        Returns:
            bytes: GIF data as bytes object, or None if error
        """
        # TODO: In the future, llm can regenerate the query based on user context
        try:
            # Step 1: Search for GIFs in the category
            search_url = f"{self.base_url}/search"
            params = {
                'q': context_category,
                'key': self.api_key,
                'client_key': self.client_key,
                'limit': limit,
                'contentfilter': 'medium',  # Filter content appropriately
                'media_filter': 'gif'  # Only get GIFs
            }

            response = requests.get(search_url, params=params)
            response.raise_for_status()

            data = response.json()

            if 'results' not in data or not data['results']:
                print(f"No memes found for category: {context_category}")
                return None

            # Step 2: Select a random GIF from results
            random_gif = random.choice(data['results'])

            # Step 3: Get the best available format
            gif_url = self._get_best_gif_url(random_gif)
            if not gif_url:
                print("No suitable GIF format found")
                return None

            # Step 4: Download the GIF and return as bytes
            gif_response = requests.get(gif_url)
            gif_response.raise_for_status()

            print(f"Retrieved random meme: {random_gif.get('content_description', 'Unknown')}")
            return gif_response.content

        except requests.RequestException as e:
            print(f"Network error retrieving random meme: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
        except Exception as e:
            print(f"Error retrieving random meme: {e}")
            return None

    def _get_best_gif_url(self, gif_data: dict) -> Optional[str]:
        """Extract the best available GIF URL from Tenor response"""
        media_formats = gif_data.get('media_formats', {})

        # Priority order: tinygif for speed, gif for quality
        format_priority = ['tinygif', 'gif', 'mediumgif', 'nanogif']

        for format_type in format_priority:
            if format_type in media_formats:
                return media_formats[format_type].get('url')

        return None
