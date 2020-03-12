'''
scrape_seller2.py: provides usual location of price 
                   on a page from this seller's website 
'''

import website_html_provider as website 

def scrape_book_price(url):
    '''
    Return the price of the book from the given url
    '''
    page_soup = website.get_html(url) 
    return page_soup.find_all(class_="product-price-value")[0].string.strip()


