# scripts/scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from security import safe_requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = safe_requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info(f'Successfully fetched {url}')
        return response.text
    except requests.RequestException as e:
        logging.error(f'Error fetching {url}: {e}')
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    quotes = []
    quote_elements = soup.find_all('div', class_='quote')
    for quote_element in quote_elements:
        text = quote_element.find('span', class_='text').get_text(strip=True)
        author = quote_element.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_element.find_all('a', class_='tag')]
        quotes.append({
            'text': text,
            'author': author,
            'tags': ', '.join(tags)
        })
    return quotes

def save_data(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    logging.info(f'Data saved to {filename}')

if __name__ == "__main__":
    base_url = 'http://quotes.toscrape.com/page/{}/'
    all_quotes = []
    for page in range(1, 11):
        url = base_url.format(page)
        html = fetch_html(url)
        if html:
            quotes = parse_html(html)
            all_quotes.extend(quotes)
        time.sleep(1)  # Add a delay of 1 second between requests
    save_data(all_quotes, '../data/quotes.csv')
