import logging
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build

from src.base.enums.main.Modules import Modules
from src.base.services.Config import Config
from src.base.services.DataCollectionConfig import DataCollectionConfig


class WebScraper:
    def __init__(self, user_agent=''):
        self.__config = Config()
        self.__search_api_key = self.__config.gs_api_key
        self.__search_engine_id = self.__config.gs_engine_key
        self.__config = DataCollectionConfig(Modules.CNews)
        if user_agent == '':
            self.__user_agent = self.__config.default_user_agent
        else:
            self.__user_agent = user_agent

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
        return BeautifulSoup(html_content, self.__config.html_parser_features)

    def __extract_data(self, soup):
        paragraphs = soup.find_all(self.__config.tag_to_find)
        text = [p.get_text() for p in paragraphs]
        return text

    def __scrape(self, link):
        html_content = self.__get_page_content(link)
        soup = self.__parse_html(html_content)
        data = self.__extract_data(soup)
        return data

    def __google_search(self, query):
        try:
            service = build(self.__config.service_name, self.__config.version, developerKey=self.__search_api_key)
            res = service.cse().list(q=query, cx=self.__search_engine_id).execute()
            links = [result['link'] for result in res['items']]
            return links
        except Exception as e:
            logging.error(f"Error while searching {query}: {e}")
            return []
