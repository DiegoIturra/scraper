from datetime import datetime
from pprint import pprint
from scraper import Scraper
from time import time, sleep
from typing import List, Any
from utils import Utils
import psycopg2

def process_wishlist(wishlist_url: str, scraper: Scraper) -> List[Any]:
    books_data = scraper.get_book_data_from_wishlist(wishlist_url)
    return books_data

def execute_task():
    counter = 0
    scraper = Scraper()

    # Open a connection with the database
    connection = psycopg2.connect(
        user="postgres",
        password="database_password",
        host="localhost",
        port="5432",
        database="scraper_database"
    )

    cursor = connection.cursor()

    # Get all wishlist urls
    cursor.execute('SELECT url FROM wishlists')
    results = cursor.fetchall()
    wishlists = list(map(lambda x: x[0], results))

    start_time = time()


    insert_book_query = """
            INSERT INTO books (title, url, image, price, availability, wishlist) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, price
        """
    
    select_book_query = """ 
            SELECT title FROM books WHERE title = %s AND url = %s AND wishlist = %s
        """
    
    update_book_query = """ 
                        UPDATE books 
                        SET price = %s 
                        WHERE title = %s AND url = %s AND wishlist = %s
                        RETURNING id, price
                    """
    
    add_history_record_query = """ INSERT INTO price_history (book_id, price, recorded_at) 
                                   VALUES (%s, %s, %s) 
                                   RETURNING id 
                    """

    for wishlist_url in wishlists:
        books = process_wishlist(wishlist_url, scraper=scraper)

        timestamp = datetime.now()

        for book in books:
            try:
                # INSERT OR UPDATE BOOK RECORD
                book_title = book['title']
                book_price = book['price']
                book_url = book['url']
                book_wishlist = book['wishlist']
                
                #Verify if book exist previously in database
                cursor.execute(select_book_query, (book_title, book_url, book_wishlist,))
                result = cursor.fetchone()

                if result:
                    # UPDATE
                    cursor.execute(update_book_query, (book_price, book_title, book_url, book_wishlist))
                    book_id, price = cursor.fetchone()
                    print(f"\033[32mBook {book['title']} UPDATED correctly\033[0m")
                else:
                    # INSERT
                    book_tuple = tuple(book.values())
                    cursor.execute(insert_book_query, book_tuple)
                    book_id, price = cursor.fetchone()
                    print(f"\033[32mBook {book['title']} INSERTED correctly\033[0m")
                
                connection.commit()
                
                # ADD RECORD IN PRICE_HISTORY TABLE
                history_record = (book_id, book_price, timestamp)
                cursor.execute(add_history_record_query, history_record)
                connection.commit()

                print(f"\033[32mBook History record: {history_record} inserted correctly\033[0m")
                print()
            except Exception as e:
                connection.rollback()
                print(f"\033[31m Error trying to insert{book}:{e}\033[0m")
                print()

        sleep(5)

        counter += len(books)

    result = cursor.fetchone()
    print(result)

    cursor.close()
    connection.close()

    final_time = time()

    print(f"total time: {final_time - start_time} seconds")
    print(f"total books {counter}")

if __name__ == '__main__':
    execute_task()