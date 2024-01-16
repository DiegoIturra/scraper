from bs4 import BeautifulSoup
import requests
from utils import Utils

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

        image_url = self._get_book_image(soup)
        data['image'] = image_url
        # print(image_url)    

        title = self._get_book_title(soup)
        data['title'] = title
        # print(title)

        # TODO: parse result and cast to an integer
        price = self._get_book_price(soup)
        data['price'] = price
        # print(price)

        availability = self._get_book_availability(price)
        data['availability'] = availability
        # print(availability)

        return data

    def add_wishlist_name_to_data(self, data, wishlist_name):
        data['wishlist'] = wishlist_name
        return data

    def _get_book_image(self, soup):
        image_div = soup.find('div', {'class': 'imagen'})
        img = image_div.find('img')

        if img:
            image_url = img.get('data-src')
            return image_url
        return None

    def _get_book_title(self, soup):
        title = soup.find('p', {'class': 'tituloProducto'})

        if title:
            return title.text
        return None

    def _get_book_price(self, soup):
        price = soup.find('p', {'class': 'precioAhora'})

        if price:
            return Utils.parse_price_into_number(price.text)
        return None

    def _get_book_availability(self, price):
        return True if price else False