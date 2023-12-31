from bs4 import BeautifulSoup
from functools import reduce
from pprint import pprint
from time import time
from typing import List
import concurrent.futures
import requests


class Utils:

    @staticmethod
    def extract_name_from_url(url: str):
        tokens = url.split('/')
        last_token = tokens[-1:]
        wishlist_name = last_token[0].split('_')[0]
        return wishlist_name

    @staticmethod
    def parse_price_into_number(price: str):
        tokens = price.split('$')
        last_token = tokens[-1:][0].strip()

        extracted_values = last_token.split('.')

        price = reduce(lambda x, y: x + y, extracted_values)
        return price


class DataCollector:
    def __init__(self):
        self.data = []

    def add_data(self, data):
        self.data.append(data)

    def get_data(self):
        return self.data
    
    def print_all_data(self):
        for data in self.data:
            print(data)
            print()

class WishlistManager:

    def __init__(self):
        self.wishlist = [
            'https://www.buscalibre.cl/v2/pendientes_486712_l.html',
            'https://www.buscalibre.cl/v2/daredevil-mark-waid_1520599_l.html'
            'https://www.buscalibre.cl/v2/software-development_503034_l.html',
            'https://www.buscalibre.cl/v2/comics_545021_l.html',
            'https://www.buscalibre.cl/v2/pendientes-2_567662_l.html',
            'https://www.buscalibre.cl/v2/historia_606807_l.html',
            'https://www.buscalibre.cl/v2/feminismo_624086_l.html',
            'https://www.buscalibre.cl/v2/pendientes-3_657656_l.html',
            'https://www.buscalibre.cl/v2/latinoamericana_711603_l.html',
            'https://www.buscalibre.cl/v2/estudio_727965_l.html',
            'https://www.buscalibre.cl/v2/literatura_729752_l.html',
            'https://www.buscalibre.cl/v2/contra_737670_l.html',
            'https://www.buscalibre.cl/v2/english-books_816771_l.html',
            'https://www.buscalibre.cl/v2/filosofia-sociologia_830510_l.html',
            'https://www.buscalibre.cl/v2/cortos_831079_l.html',
            'https://www.buscalibre.cl/v2/tolkien_921085_l.html',
            'https://www.buscalibre.cl/v2/fullmetal_1003773_l.html',
            'https://www.buscalibre.cl/v2/cuentos_1079781_l.html',
            'https://www.buscalibre.cl/v2/estudio2_1218140_l.html',
            'https://www.buscalibre.cl/v2/emprendimientos-y-finanzas_1450796_l.html',
            'https://www.buscalibre.cl/v2/literatura-2_1469636_l.html',
            'https://www.buscalibre.cl/v2/gantz_1488040_l.html',
            'https://www.buscalibre.cl/v2/manga_1488300_l.html',
            'https://www.buscalibre.cl/v2/chile_1536612_l.html',
        ]

    
    def add_url(self, url: str):
        self.wishlist.append(url)

    def remove_url(self, url: str):
        self.wishlist.remove(url)

    def get_wishlist(self):
        return self.wishlist
    




class Scraper:

    def get_books_url_from_wishlist(self, wishlist_url):
        """
        Extract url for each book in a wishlist url
        """
        request = requests.get(wishlist_url)
        soup = BeautifulSoup(request.text, "html.parser")

        #Get the main container to all books
        results = soup.find('div', {'class': 'listadoProductos'})
        
        books_urls = []

        for result in results:
            item = result.find('div', {'class': 'seccionProducto'})

            image_div = item.find('a')

            if image_div:
                href = image_div.get('href')
                books_urls.append(href)

        return books_urls
        

    def get_book_data_from_url(self, book_url):
        """
        Extract data for a book passing the book url
        """
        request = requests.get(book_url)
        soup = BeautifulSoup(request.text, 'html.parser')
        data = {}

        data['book_url'] = book_url

        image_url = self.get_book_image(soup)
        data['image'] = image_url
        # print(image_url)    

        title = self.get_book_title(soup)
        data['title'] = title
        # print(title)

        # TODO: parse result and cast to an integer
        price = self.get_book_price(soup)
        data['price'] = price
        # print(price)

        availability = self.get_book_availability(price)
        data['availability'] = availability
        # print(availability)

        return data

    def add_wishlist_name_to_data(self, data, wishlist_name):
        data['wishlist'] = wishlist_name
        return data

    def get_book_image(self, soup):
        image_div = soup.find('div', {'class': 'imagen'})
        img = image_div.find('img')

        if img:
            image_url = img.get('data-src')
            return image_url
        return None

    def get_book_title(self, soup):
        title = soup.find('p', {'class': 'tituloProducto'})

        if title:
            return title.text
        return None

    def get_book_price(self, soup):
        price = soup.find('p', {'class': 'precioAhora'})

        if price:
            return Utils.parse_price_into_number(price.text)
        return None

    def get_book_availability(self, price):
        return True if price else False

 

def process_wishlist(wishlist_url: str, scraper: Scraper, data_collector: DataCollector):
    books_urls = scraper.get_books_url_from_wishlist(wishlist_url)
    wishlist_name = Utils.extract_name_from_url(wishlist_url)

    for book_url in books_urls:
        data = scraper.get_book_data_from_url(book_url)
        data = scraper.add_wishlist_name_to_data(data, wishlist_name)
        data_collector.add_data(data)

if __name__ == '__main__':
    scraper = Scraper()
    data_collector = DataCollector()
    wishlist_manager = WishlistManager()

    wishlist = wishlist_manager.get_wishlist()

    start_time = time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_wishlist, url, scraper, data_collector) for url in wishlist]
        concurrent.futures.wait(futures)

    data_collector.print_all_data()

    final_time = time()

    print(f"total time: {final_time - start_time} seconds")
