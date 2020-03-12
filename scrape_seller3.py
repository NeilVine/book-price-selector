'''
scrape_seller3.py: provides usual location of price 
                   on a page from this seller's website 
'''

import website_html_provider as website 

def scrape_book_price(url):
    '''
    Return the price of the book from the given url
    '''
    page_soup = website.get_html(url)
    price_element = page_soup.find(class_="price")
    return price_element.find('b').get_text()


