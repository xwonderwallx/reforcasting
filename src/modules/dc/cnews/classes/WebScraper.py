import logging
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build

from src.base.services.Config import Config


class WebScraper:
    def __init__(self, user_agent=''):
        if user_agent == '':
            self.__user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        else:
            self.__user_agent = user_agent
        self.__config = Config()
        self.__search_api_key = self.__config.gs_api_key
        self.__search_engine_id = self.__config.gs_engine_key

    def search_and_scrape(self, query):
        search_links_results = self.__google_search(query)
        result = []
        for link in search_links_results:
            data = self.__scrape(link)
            result.append(data)
        return result

    def __get_page_content(self, url):
        headers = {'User-Agent': self.__user_agent}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while requesting {url}: {e}")
            return None

    def __parse_html(self, html_content):
        return BeautifulSoup(html_content, 'html.parser')

    def __extract_data(self, soup):
        paragraphs = soup.find_all('p')
        text = [p.get_text() for p in paragraphs]
        return text

    def __scrape(self, link):
        html_content = self.__get_page_content(link)
        soup = self.__parse_html(html_content)
        data = self.__extract_data(soup)
        return data

    def __google_search(self, query):
        try:
            service = build("customsearch", "v1", developerKey=self.__search_api_key)
            res = service.cse().list(q=query, cx=self.__search_engine_id).execute()
            links = [result['link'] for result in res['items']]
            return links
        except Exception as e:
            logging.error(f"Error while searching {query}: {e}")
            return []
