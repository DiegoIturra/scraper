from database_manager import DatabaseManager
from datetime import datetime
from pprint import pprint
from scraper import Scraper
from time import time, sleep
from typing import List, Any
from utils import Utils
import os
import psycopg2

def process_wishlist(wishlist_url: str, scraper: Scraper) -> List[Any]:
    books_data = scraper.get_book_data_from_wishlist(wishlist_url)
    return books_data

def execute_query_with_connection(connection, query, params=None, fetch=None):
    """
    fetch:
        - None: just execute commit operation
        - 'one': do a fetchone() operation and return
        - 'all': do a fetchall() operation and return
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)

            if fetch == 'one':
                return cursor.fetchone()
            elif fetch == 'all':
                return cursor.fetchall()
            else:
                connection.commit()
                return None
    except Exception as e:
        raise e

def execute_task():
    number_of_books = 0
    scraper = Scraper()

    start_time = time()

    database_config = {
        "user": os.getenv('DATABASE_USER'),
        "password": os.getenv('DATABASE_PASSWORD'),
        "host": "localhost",
        "port": 5432,
        "database": os.getenv('DATABASE_NAME')
    }

    database_manager = DatabaseManager(database_config)
    connection = database_manager.get_connection()

    if not connection:
        print('Error getting connection')
        return

    get_wishlists_query = "SELECT * FROM wishlists"

    wishlists = execute_query_with_connection(connection=connection, query=get_wishlists_query, fetch='all')
    
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

    for wishlist_tuple in wishlists:

        wishlist_url = wishlist_tuple[1] # Belongs to the url in the record
        books = process_wishlist(wishlist_url, scraper=scraper)

        if len(books) == 0:
            continue

        timestamp = datetime.now()

        for book in books:
            try:
                # INSERT OR UPDATE BOOK RECORD
                book_title = book['title']
                book_price = book['price']
                book_url = book['url']
                book_wishlist = book['wishlist']
                
                result = execute_query_with_connection(
                    connection=connection, 
                    query=select_book_query, 
                    params=(book_title, book_url, book_wishlist,), 
                    fetch='one'
                )

                #Verify if book exist previously in database
                if result:
                    # UPDATE
                    book_id, price = execute_query_with_connection(
                        connection=connection,
                        query=update_book_query,
                        params=(book_price, book_title, book_url, book_wishlist,),
                        fetch='one'
                    )

                    print(f"\033[32mBook {book['title']} UPDATED correctly\033[0m")
                else:
                    # INSERT
                    book_tuple = tuple(book.values())

                    book_id, price = execute_query_with_connection(
                        connection=connection,
                        query=insert_book_query,
                        params=book_tuple,
                        fetch='one'
                    )

                    print(f"\033[32mBook {book['title']} INSERTED correctly\033[0m")
                
                    # Verify if the tuple (wishlist_id, book_id) exist
                    wishlist_id = wishlist_tuple[0]
                    wishlist_book_record = (wishlist_id, book_id)

                    print(f"record assossiation {wishlist_book_record}")

                    wishlist_book_get_query = """ SELECT * FROM wishlist_books 
                        WHERE wishlist_id = %s AND book_id = %s
                    """

                    assosiation_record = execute_query_with_connection(
                        connection=connection,
                        query=wishlist_book_get_query,
                        params=wishlist_book_record,
                        fetch='one'
                    )

                    if not assosiation_record:
                        wishlist_book_add_query = """ INSERT INTO wishlist_books (wishlist_id, book_id)
                            VALUES (%s, %s)
                        """

                        execute_query_with_connection(
                            connection=connection,
                            query=wishlist_book_add_query,
                            params=wishlist_book_record
                        )

            
                # ADD RECORD IN PRICE_HISTORY TABLE
                history_record = (book_id, book_price, timestamp)

                execute_query_with_connection(
                    connection=connection,
                    query=add_history_record_query,
                    params=history_record
                )

                print(f"\033[32mBook History record: {history_record} inserted correctly\033[0m")
                print()
            except Exception as e:
                connection.rollback()
                print(f"\033[31m Error trying to insert{book}:{e}\033[0m")
                print()

        sleep(5)

        number_of_books += len(books)

    database_manager.release_connection(connection)
    database_manager.close_all_connections()

    final_time = time()

    print(f"total time: {final_time - start_time} seconds")
    print(f"total books {number_of_books}")

if __name__ == '__main__':
    execute_task()