from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from scraper import Scraper
from time import time
from typing import List, Tuple
from utils import Utils
from wishlist_manager import WishlistManager


def process_wishlist(wishlist_url: str, scraper: Scraper) -> Tuple[List[str], str]:
    books_urls = scraper.get_books_url_from_wishlist(wishlist_url)
    wishlist_name = Utils.extract_name_from_url(wishlist_url)

    return (books_urls, wishlist_name)

def process_book_url(book_url: str, wishlist_name: str, scraper: Scraper): #return data about each book
    data = scraper.get_book_data_from_url(book_url)
    data = scraper.add_wishlist_name_to_data(data, wishlist_name)
    return data


def process_all_wishlist(wishlist: List[str], scraper: Scraper):
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_wishlist, url, scraper): url for url in wishlist}
        
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()

                results.append(result)
                
            except Exception as e:
                print(f"Error processing wishlist URL {url}: {e}")

    return results


def process_all_books_urls(list_of_books_urls: List[str], wishlist_name: str, scraper: Scraper):
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = { executor.submit(process_book_url, url, wishlist_name, scraper): url for url in list_of_books_urls }

        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()

                results.append(result)

            except Exception as e:
                print(f"Error processing book URL {url}: {e}")
    return results


def execute_task():

    counter = 0
    scraper = Scraper()
    wishlist_manager = WishlistManager()

    wishlist = wishlist_manager.get_wishlist()

    start_time = time()

    results = process_all_wishlist(wishlist, scraper)

    for result in results:
        list_of_books_urls = result[0]
        wishlist_name = result[1]

        list_of_books_data = process_all_books_urls(list_of_books_urls, wishlist_name, scraper)
        counter += len(list_of_books_data)
        
        for book_data in list_of_books_data:
            pprint(book_data)
            print()
        

    final_time = time()

    print(f"total time: {final_time - start_time} seconds")
    print(f"total books {counter}")

if __name__ == '__main__':
    execute_task()