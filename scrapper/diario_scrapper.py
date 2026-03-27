import os
import random
from time import sleep
from pathlib import Path

import requests

from scrapper.config import SCRAPPER_CONFIG


class DiarioScrapper:
    def __init__(self, playwright):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Firefox/109.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, como Gecko) Version/16.3 Safari/605.1.15"
        ]

        self.browser = playwright.chromium.launch(headless=SCRAPPER_CONFIG['headless'])
        self.context = self.browser.new_context(user_agent=random.choice(self.user_agents), locale='pt-BR')
        self.page = self.context.new_page()
    
    """Extrai os pdfs dos diários de todas as fontes para a data fornecida."""
    def scrap(self, date):
        self._scrap_tjpi(date)

    """Extrai os pdfs dos diários do TJPI para a data fornecida."""
    def _scrap_tjpi(self, date):
        # TODO: fazer o download do pdf dos diários do TJPI, atualmente só abre a página do pdf

        self.page.goto(SCRAPPER_CONFIG['diarios']['tjpi'])

        date_input = self.page.locator('#q_disponibilization_eq').first
        date_input.wait_for()
        
        date_input.fill(date.strftime("%Y-%m-%d"))
        
        submit_btn = self.page.locator('input[type="submit"]').first
        submit_btn.wait_for()
        submit_btn.click()

        with self.context.expect_page() as new_page_info:
            pdf_btn = self.page.locator('a:has-text("PDF")').first
            pdf_btn.wait_for()
            pdf_btn.click()

        pdf_url = new_page_info.value.url
        
        try:
            self._download_pdf(pdf_url, f"./downloads/tjpi_{date.strftime('%Y-%m-%d')}.pdf")
        except Exception as e:
            print(f"Error occurred while downloading PDF: {e}")

    def _download_pdf(self, url, save_path):
        os.makedirs("./downloads", exist_ok=True)

        with requests.get(url, stream=True) as response:
            if response.status_code != 200:
                raise Exception(f"Failed to retrieve PDF: {response.status_code}")

            if Path(save_path).exists():
                raise Exception(f"PDF already exists at {save_path}, skipping download.")

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.browser.close()