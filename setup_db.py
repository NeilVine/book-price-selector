'''
Setup.py 
    script to create tables and other 
    databse operations 
    used at setup time only
'''

import sqlite3
import datetime
from functools import wraps

def get_connection_and_cursor():
    conn = sqlite3.connect('book_prices.db')
    cursor = conn.cursor()
    return conn, cursor

# Decorator to handle db connection
def db_action_execute(fn):
    @wraps(fn())
    def wrapper():
        """wrapper gets connection, executes sql and closes connection"""
        conn, cursor = get_connection_and_cursor()
        cursor.execute(fn())
        conn.commit()   
        conn.close()

    print(f"db_action wrapper calling function {fn.__name__}, which {fn.__doc__}")
    return wrapper

def db_action_execute_with_paramters(fn):
    @wraps(fn())
    def wrapper(*args, **kwargs):
        print(args)
        conn, cursor = get_connection_and_cursor()
        sql_statement, data = fn(*args, **kwargs)
        # Need to explicitly include the two arguments in the call to the execute method.
        #  - can't just pass in the call to fn
        cursor.execute(sql_statement, data)
        conn.commit()   
        conn.close()

    print(f"db_action wrapper calling function {fn.__name__}, which {fn.__doc__}")
    return wrapper

@db_action_execute_with_paramters
def insert_seller_sql(*args, **kwargs):
    """ returns SQL and data to add a seller 
    Expecting **kwargs to include:
        id
        name
    """
    #
    # Note that because this function is decorated, the warpper function will
    # call this when the code is interpreted, and there wont be any kwargs!!!
    # Hence, you can't validate them - you can't ensure a value is present in kwargs

    # Assign default values to prevent compilation error 
    # - again this is due to the decorator wrapper calling this before 
    #    there is any explicit calls to this function. 
    id = ""
    name = ""

    if 'id' in kwargs:
        id = kwargs.get("id")

    if 'name' in kwargs:
        name = kwargs.get("name")

    data = (id, name) 
    insert_statement = f"INSERT INTO sellers VALUES (?, ?)"
    return insert_statement, data

@db_action_execute
def create_book_prices_table_sql():
    """ returns SQL to create the prices table """
    return '''CREATE TABLE prices
           (id TEXT PRIMARY KEY NOT NULL,
            seller1_price REAL,
            seller2_price REAL,
            seller3_price REAL);'''

@db_action_execute
def create_sellers_table_sql():
    """ returns SQL to create the sellers table """
    return '''CREATE TABLE sellers
           (id         TEXT PRIMARY KEY  NOT NULL,
            name       TEXT  NOT NULL);'''
    
@db_action_execute
def create_book_table_sql():
    """ returns SQL to create the book table """
    return '''CREATE TABLE book_urls
           (id TEXT PRIMARY KEY  NOT NULL,
            name TEXT NOT NULL,
            url1 TEXT,
            url2 TEXT,
            url3 TEXT);'''

def get_book_url_kwargs(*args, **kwargs):

    id = ""
    name = ""
    url1 = ""
    url2 = ""
    url3 = ""

    if 'id' in kwargs:
        id = kwargs.get("id")

    if 'name' in kwargs:
        name = kwargs.get("name")

    if 'url1' in kwargs:
        url1 = kwargs.get("url1")

    if 'url2' in kwargs:
        url2 = kwargs.get("url2")

    if 'url3' in kwargs:
        url3 = kwargs.get("url3")

    print(f"get_book_url_kwargs id = {id}, name = {name}")

    return id, name, url1, url2, url3

@db_action_execute_with_paramters
def inset_book_url_sql(*args, **kwargs):
    print("in inset_book_url_sql")
    #print(**kwargs)
    data = get_book_url_kwargs(*args, **kwargs)

    print(data)
    #data = (id, name, url1, url2, url3) 
    insert_statement = f"INSERT INTO book_urls VALUES (?, ?, ?, ?, ?)"
    return insert_statement, data 
 
def create_tables():
    create_sellers_table_sql()
    create_book_table_sql()

def populate_tables():
    # Add sellers
    insert_seller_sql(id="seller1", name="")
    insert_seller_sql(id="seller2", name="")
    insert_seller_sql(id="seller3", name="")

    # Add books
    inset_book_url_sql(id = "Start_With_Why",
                       name = "Start with Why, Simon Sinek", 
                       url1 = "",
                       url2= "",
                       url3= "")

    
    inset_book_url_sql(id = "The_Power_Of_Habit",
                       name = "The Power of Habit: Why We Do What We Do, and How to Change, Charles Duhigg", 
                       url1 = "",
                       url2= "",
                       url3= "")
      
    inset_book_url_sql(id = "The_Four_Hour_Work_Week",
                       name = "The 4-Hour Work Week: Escape the 9-5, Live Anywhere and Join the New Rich, Timothy Ferriss", 
                       url1 = "",
                       url2 = "",
                       url3 = "")

def delete_book(id):
    print(f"delete_book, id= {id}")

    conn = sqlite3.connect('book_prices.db')
    sql = f"DELETE FROM book_urls WHERE id = '{id}'"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def print_out_books():
    print("-----------  books -------------")
    conn = sqlite3.connect('book_prices.db')
    sql = "SELECT * FROM book_urls"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    a = cur.fetchall()
    list_of_books = list(a)
    for book in list_of_books:
        print(book)
        print("")
    print("------------------------------")

if __name__ == "__main__":
    print("in main")

    #create_book_prices_table_sql()
    #populate_tables()

    #delete_book('')
    #print_out_books()

