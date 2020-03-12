'''
Datebase name: "book_prices.db"

Tabels and what they store:
    * sellers // Records of Seller Id, Seller Name
    * book_urls // Records of Book Id, Book Name, URLs for book from: Seller1, Seller2, Seller3
    * prices // Book Id, Prices from: Seller1, Seller2, Seller3

App idea:
    * user selects a book to scrape (from a list of three)
    * Three sites are scraped and prices compared
    * User is informed the best price and the seller name
'''

import sqlite3

class DB(object):
    '''
    class DB
    A class used to provide access to the "book_prices.db" database.
    Including methods to read/write data.
    '''

    def __init__(self):
        '''     
        For "book_price_scrape.db" (database)
            * Open a connection
            * Obtain cursor - a helper object for the database
        '''
        self._db_connection = _connection = sqlite3.connect('book_prices.db')
        self._db_cur = self._db_connection.cursor()

    def __del__(self):
        '''
        This object is being destroyed.
        '''
        # Close the connection.
        self._db_connection.close()

    def read_book_name(self, book_id):
        '''
        Returns: The book's name from the record containing the given book_id  
        '''
        self._db_cur.execute(f"SELECT name FROM book_urls WHERE id = '{book_id}'")
        self._db_connection.commit()
        sql_result = self._db_cur.fetchall()
        return list(sql_result)[0][0]

    def get_books(self):
        ''' Returns each book's id and name '''
        self._db_cur.execute("SELECT id, name FROM book_urls")
        self._db_connection.commit()
        return self._db_cur.fetchall()

    def read_urls(self, book_id):
        '''
        Read the URLs of the webpages for a book 
        Returns: A cursor object containing the record of URLs
        Note: The "book_urls" table primary key is book_id  
        '''
        self._db_cur.execute(f"SELECT * FROM book_urls WHERE id = '{book_id}'")
        self._db_connection.commit()
        return self._db_cur

    def read_seller_name(self, seller_id):
        '''
        Returns: The seller's name
        '''
        self._db_cur.execute(f"SELECT name FROM sellers WHERE id = '{seller_id}'")
        self._db_connection.commit()
        return list(self._db_cur.fetchall())[0][0]

    def read_prices(self, book_id):
        '''
        Read the prices stored for the book
        '''
        self._db_cur.execute(f"SELECT * FROM prices WHERE id = '{book_id}'")
        self._db_connection.commit()
        return self._db_cur

    def write_prices(self, book_id, seller1_price, seller2_price, seller3_price):
        '''
        Write the prices retrieved from each seller to the database book_prices table
        '''

        # Determine if there are existing prices stored for this book
        self._db_cur.execute("SELECT COUNT(*) FROM prices WHERE id = ?", (book_id,))
        data= self._db_cur.fetchone()[0]
        print(f"---------------------------------------")
        print(f"datbase_layer, write_prices... data is {data}")
        print(f"---------------------------------------")

        if data==0:
            # Prices are not stored for this book so insert them
            self._insert_prices(book_id, seller1_price, seller2_price, seller3_price)
        else:
            # Prices have already been stored for this book so update them
            self._update_prices(book_id, seller1_price, seller2_price, seller3_price)

    def _update_prices(self, id, seller1_price, seller2_price, seller3_price):
        # Update the existing prices for this book
        self._db_cur.execute('''UPDATE prices 
                             SET seller1_price = ?, 
                                 seller2_price = ?, 
                                 seller3_price = ?
                                 WHERE id = ? ''',
                             (seller1_price,
                              seller2_price, 
                              seller3_price,
                              id))
        self._db_connection.commit()


    def _insert_prices(self, id, seller1_price, seller2_price, seller3_price):
        # Add/insert a new record containing the prices for this book  
        self._db_cur.execute('''INSERT INTO prices(id, 
                                                   seller1_price, 
                                                   seller2_price, 
                                                   seller3_price)
                             VALUES(?,?,?,?)''', (id, 
                                                  seller1_price, 
                                                  seller2_price, 
                                                  seller3_price))
        self._db_connection.commit()
    