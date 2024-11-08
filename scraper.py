from bs4 import BeautifulSoup
from utils import Utils
import random
import requests
import time


class Scraper:

    def get_book_data_from_wishlist(self, wishlist_url):
        """
        Extract url for each book in a wishlist url
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }

        request = requests.get(wishlist_url, headers=headers)
        soup = BeautifulSoup(request.text, "html.parser")

        #Get the main container to all books
        results = soup.find('div', {'class': 'listadoProductos'})
        
        books_data = []

        # Extract wishlist name
        wishlist_name = Utils.extract_name_from_url(wishlist_url)

        for result in results:
            item = result.find('div', {'class': 'seccionProducto'})

            book_url_div = item.find('a')
            if book_url_div:
                href = book_url_div.get('href')

            # find name
            title = item.find('div', {'class': 'titulo'}).get_text()
            title = title.strip()

            # find image url
            image_div_container = item.find('div', {'class': 'portadaProducto'})
            image = image_div_container.find('img')
            image_url = image['src']

            # find price
            price = item.find('div', {'class': 'precioAhora'})
            price = price.get_text() if price else None
            price = Utils.parse_price_into_number(price)
            
            data = {
                'title': title,
                'url': href,
                'image': image_url,
                'price': price,
                'wishlist': wishlist_name
            }

            books_data.append(data)

        return books_data