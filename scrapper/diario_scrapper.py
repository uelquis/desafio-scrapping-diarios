import re, random
from datetime import date
from time import sleep
from typing import Dict, List
from playwright.sync_api import Playwright
from scrapper.config import SCRAPPER_CONFIG

# TODO: extrair diários de caderno único e os diário complementares
class DiarioScrapper:
    @staticmethod
    def init_browser_context(playwright: Playwright):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Firefox/109.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, como Gecko) Version/16.3 Safari/605.1.15"
        ]

        browser = playwright.chromium.launch(headless=SCRAPPER_CONFIG['headless'])
        context = browser.new_context(user_agent=random.choice(user_agents), locale='pt-BR')
        page = context.new_page()

        return {
            'user_agents': user_agents,
            'browser': browser,
            'context': context,
            'page': page
        }

    def __init__(self, browser_context: Dict):
        self.user_agents = browser_context['user_agents']
        self.browser = browser_context['browser']
        self.context = browser_context['context']
        self.page = browser_context['page']
    
    def scrap(self, date: date):
        raise NotImplementedError(f"Método scrap não foi implementado na classe {self.__class__.__name__} ")

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.browser.close()

class ScrappedData:
    def __init__(self, urls: List[str], save_paths: List[str], args: Dict):
        self.urls = urls
        self.save_paths = save_paths
        self.args = args
        self.count = len(urls)   
    