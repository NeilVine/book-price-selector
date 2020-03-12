import requests
from bs4 import BeautifulSoup

def get_html(url):
        '''
        obtain the html page cotaining the book and
        return BeautifulSoup containing it
        '''

        headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip', 
            'DNT' : '1', # Do Not Track Request Header 
            'Connection' : 'close'
        }
        
        print(".", end =" ") 
        raw_page_html = requests.get(url, headers=headers)
        print(".", end =" ") 
        return BeautifulSoup(raw_page_html.text, 'html.parser')