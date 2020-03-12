'''
compare_book_prices.py
    A Python script to compare book prices
    from different sellers
'''

import scrape_seller1 as seller1
import scrape_seller2 as seller2
import scrape_seller3 as seller3
import database_layer as db

def get_user_book_selection():
    '''
    Get user to select which book
    they are interested in 
    '''
    books = database.get_books()
    list_of_book_names = list(books)
    # create dictionary of:
    # book id; book name
    books_dict = {}
    for l in list_of_book_names:
        if l != None and len(l) > 0 and l[0] != '':
            books_dict[l[0]] = l[1]
    # create dictionary of: 
    # index, book id
    choice_dict = {}
    i = 0
    for key, value in books_dict.items():
        # value is the book name/title 
        # which is displayed to the user
        print(f"{i}: {value}")
        # key is the book id
        choice_dict[i] = key
        i += 1

    user_choice = int(input("Select a book by typing the number 0,1,2 and pess Enter "))  
    # choice_dict[user_choice] contains the 'book id' 
    # for the book that the user is interested in 
    return choice_dict[user_choice]

def read_urls(book_to_scrape, datebase):
    # read the urls to use from the database
    urls = datebase.read_urls(book_to_scrape)
    results_list = list(urls.fetchall())
    # key is results_list[0][0]
    # book name results_list[0][1]
    seller1_page = results_list[0][2]
    seller2_page = results_list[0][3]
    seller3_page = results_list[0][4]
    return seller1_page, seller2_page, seller3_page

def read_prices(seller1_page, seller2_page, seller3_page):
    # Read the price form each seller
    # Note: Each seller will have the book price
    #       within a different location within the 
    #       book's webpage html   
    seller1_price = seller1.scrape_book_price(seller1_page)
    seller2_price = seller2.scrape_book_price(seller2_page)
    seller3_price = seller3.scrape_book_price(seller3_page)
    return seller1_price, seller2_price, seller3_price

def get_and_store_prices_from_web(book_id, datebase):
    '''
    Scrape web for book prices and store the results
    '''
    # get website page urls to use 
    seller1_page, seller2_page, seller3_page = read_urls(book_id, datebase)
    # get the price from each seller
    seller1_price, seller2_price, seller3_price  = read_prices(seller1_page, seller2_page, seller3_page)
    # store the prices
    datebase.write_prices(book_id, seller1_price, seller2_price, seller3_price)

def read_stored_prices(book_to_find, database_layer):
    '''
    Read prices from database 
    '''
    price_record = list(database_layer.read_prices(book_id).fetchall())
    return price_record[0][1], price_record[0][2], price_record[0][3] 

def display_results(book_to_find, database_layer):
    '''
    Identify the best price and which seller is offering the book at this price 
    '''
    book_name = database_layer.read_book_name(book_to_find)
    seller1_price, seller2_price, seller3_price = read_stored_prices(book_to_find, database_layer)
    best_price = min(seller1_price, seller2_price, seller3_price)
 
    if seller1_price ==  best_price:
        seller_name = database_layer.read_seller_name("seller1")
       
    elif seller1_price == best_price: 
        seller_name = database_layer.read_seller_name("seller2")

    elif seller2_price == best_price: 
        seller_name = database_layer.read_seller_name("seller3")

    result = f"The best price for book '{book_name}' is: \n>>> {best_price}, offered by '{seller_name}'"
    print("--------------------------")
    print(">>> " + result)
    print("--------------------------")

# starting here if directly running this module
if __name__ == "__main__":
    print("\n    Compare book prices from multiple sellers \n")
    # set up the database - open connection
    database = db.DB()
    # get the id of the book that the user is interested in 
    book_id = get_user_book_selection()
    # store in the database, values read from websites 
    get_and_store_prices_from_web(book_id, database)
    # read prices from database, and inform user
    # of the best price and who is offerring it.
    display_results(book_id, database)
