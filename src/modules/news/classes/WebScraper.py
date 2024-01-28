import logging
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build

from src.base.services import Config


class WebScraper:
    def __init__(self, user_agent=''):
        if user_agent == '':
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        else:
            self.user_agent = user_agent
        self.search_api_key = Config().get_search_api_key()
        self.search_engine_id = Config().get_search_engine_id()

    def get_page_content(self, url):
        headers = {'User-Agent': self.user_agent}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while requesting {url}: {e}")
            return None

    def parse_html(self, html_content):
        return BeautifulSoup(html_content, 'html.parser')

    def extract_data(self, soup):
        paragraphs = soup.find_all('p')
        text = [p.get_text() for p in paragraphs]
        return text

    def scrape(self, link):
        html_content = self.get_page_content(link)
        soup = self.parse_html(html_content)
        data = self.extract_data(soup)
        return data

    def search_and_scrape(self, query):
        search_links_results = self.google_search(query)
        result = []
        for link in search_links_results:
            data = self.scrape(link)
            result.append(data)
        return result

    def google_search(self, query):
        try:
            service = build("customsearch", "v1", developerKey=self.search_api_key)
            res = service.cse().list(q=query, cx=self.search_engine_id).execute()
            links = [result['link'] for result in res['items']]
            return links
        except Exception as e:
            logging.error(f"Error while searching {query}: {e}")
            return []