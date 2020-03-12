'''
scrape_seller1.py: provides usual location of price 
                   on a page from this seller's website 
'''
import website_html_provider as website 

def scrape_book_price(url):
    '''
    Return the price of the book from the given url
    '''
    print(f"scrape_seller1, scrape_book_price, url = {url}")
    page_soup = website.get_html(url)  
    return page_soup.find_all(class_="a-size-medium a-color-price offer-price a-text-normal")[0].string







