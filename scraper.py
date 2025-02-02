from bs4 import BeautifulSoup
from typing import List, Any
from utils import Utils
import random
import requests
import time

"""
TODO: Add Handle Exceptions in methods to do scraping
"""
class Scraper:

    def __get_title(self, item) -> str:
        title = item.find('div', {'class': 'titulo'}).get_text()
        return title.strip()
    
    def __get_image(self, item) -> str:
        image_div_container = item.find('div', {'class': 'portadaProducto'})
        image = image_div_container.find('img')
        return image['src']
    
    def __get_url(self, item) -> str:
        book_url_div = item.find('a')
        return book_url_div.get('href') if book_url_div else None

    def __get_price(self, item) -> int:
        price = item.find('div', {'class': 'precioAhora'})
        price = price.get_text() if price else None
        return Utils.parse_price_into_number(price)
        
    def __get_availability(self, price) -> bool:
        return True if price else False
    
    def get_book_data_from_wishlist(self, wishlist_url: str) -> List[Any]:
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

        if not results:
            return []
        
        books_data = []

        for result in results:

            item = result.find('div', {'class': 'seccionProducto'})

            price = self.__get_price(item)
            
            data = {
                'title': self.__get_title(item),
                'url': self.__get_url(item),
                'image': self.__get_image(item),
                'price': self.__get_price(item),
                'availability': self.__get_availability(price),
            }

            books_data.append(data)

        return books_data