import random
from time import sleep

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
        self.context = self.browser.new_context(user_agent=random.choice(self.user_agents))
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

        pdf_btn = self.page.locator('a:has-text("PDF")').first
        pdf_btn.wait_for()
        pdf_btn.click()

        sleep(5)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.browser.close()