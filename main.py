from pprint import pprint
from scraper import Scraper
from time import time, sleep
from typing import List, Tuple
from utils import Utils
from wishlist_manager import WishlistManager


def process_wishlist(wishlist_url: str, scraper: Scraper) -> Tuple[List[str], str]:
    books_data = scraper.get_book_data_from_wishlist(wishlist_url)
    return books_data

def execute_task():

    counter = 0
    scraper = Scraper()
    wishlist_manager = WishlistManager()

    wishlist = wishlist_manager.get_wishlist()

    start_time = time()

    for wishlist_url in wishlist:
        results = process_wishlist(wishlist_url, scraper=scraper)

        for data in results:
            pprint(data)
            print()
        
        sleep(15)

        counter += len(results)

    final_time = time()

    print(f"total time: {final_time - start_time} seconds")
    print(f"total books {counter}")

if __name__ == '__main__':
    execute_task()