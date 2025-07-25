from typing import Optional
import requests
import json
import random
import os


class GiphyMemeProvider:
    def __init__(self):
        api_key = os.environ.get("GIPHY_MEME_API_KEY")
        if api_key is None:
            raise ValueError("API_KEY not set in environment variables")

        self.api_key = api_key  # Get from https://developers.giphy.com/
        self.base_url = "https://api.giphy.com/v1"

    def get_random_meme(self, context_category: str, limit: int = 50):
        """
        Fetches a random GIF/meme from Giphy API based on context category.
        Returns bytes object compatible with your existing methods.

        Args:
            context_category: Search term/category for memes
            limit: Number of results to fetch before selecting random one

        Returns:
            bytes: GIF data as bytes object, or None if error
        """
        try:
            # Step 1: Search for GIFs in the category
            search_url = f"{self.base_url}/gifs/search"
            params = {
                'q': context_category,
                'api_key': self.api_key,
                'limit': limit,
                'rating': 'pg-13',  # Filter content appropriately (g, pg, pg-13, r)
                'lang': 'en'
            }

            response = requests.get(search_url, params=params)
            response.raise_for_status()

            data = response.json()

            if 'data' not in data or not data['data']:
                print(f"No memes found for category: {context_category}")
                return None

            # Step 2: Select a random GIF from results
            random_gif = random.choice(data['data'])

            # Step 3: Get the best available format
            gif_url = self._get_best_gif_url(random_gif)
            if not gif_url:
                print("Search returned no valid GIF URLs")
                return None

            # Step 4: Download the GIF and return as bytes
            gif_response = requests.get(gif_url)
            gif_response.raise_for_status()
            print(f"Retrieved random meme: {random_gif.get('title', 'Unknown')}")
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
        """Extract the best available GIF URL from Giphy response"""
        images = gif_data.get('images', {})

        format_priority = 'original'

        if format_priority in images and 'url' in images[format_priority]:
            return images[format_priority]['url']

        return None
