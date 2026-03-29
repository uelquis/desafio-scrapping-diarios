import re
from time import sleep
import random
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
    
    """Extrai os links dos pdfs dos diários de todas as fontes para a data fornecida."""
    def scrap(self, date):
        return [
            self._scrap_tjpi(date),
            self._scrap_gov_pi(date),
            self._scrap_pref_parnaiba(date)
        ]

    """Extrai os pdfs dos diários do TJPI para a data fornecida."""
    def _scrap_tjpi(self, date):

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
        pdf_save_path = f"./downloads/diario_tjpi_{date.strftime('%d_%m_%Y')}.pdf"
        
        return (pdf_url, pdf_save_path, {})

    """Extrai os pdfs dos diários do Governo do Piauí para a data fornecida."""
    def _scrap_gov_pi(self, date):
        
        self.page.goto(SCRAPPER_CONFIG['diarios']['gov_pi'])

        date_input = self.page.locator('input[type="date"]').first
        date_input.wait_for()
        
        date_input.fill(date.strftime("%Y-%m-%d"))

        with self.context.expect_page() as new_page_info:
            download_btn = self.page.locator("td a").first
            download_btn.wait_for()
            download_btn.click()

        pdf_url = new_page_info.value.url
        pdf_save_path = f"./downloads/diario_gov_pi_{date.strftime('%d_%m_%Y')}.pdf"

        return (pdf_url, pdf_save_path, {})
    
    """Extrai os pdfs dos diários do Prefeitura de Parnaíba para a data fornecida."""
    def _scrap_pref_parnaiba(self, date):
        
        self.page.goto(SCRAPPER_CONFIG['diarios']['pref_parnaiba'])

        date_input_inicial = self.page.locator('input[aria-label="Data Inicial"]').first
        date_input_inicial.wait_for()

        date_input_inicial.fill(date.strftime("%d-%m-%Y"))

        date_input_final = self.page.locator('input[aria-label="Data Final"]').first
        date_input_final.wait_for()
        
        date_input_final.fill(date.strftime("%d-%m-%Y"))

        filtrar_btn = self.page.get_by_text("Filtrar").first
        filtrar_btn.wait_for()
        filtrar_btn.click()

        sleep(2)

        # TODO: fix error:
        # Locator.wait_for: Error: strict mode violation: locator("td.text-left") resolved to 6 elements
        table_elements = self.page.locator("td.text-left")
        table_elements.wait_for()

        data_publicacao = re.search(r"\d{2}/\d{2}/\d{4}", 
            table_elements.all()[3].inner_text()).group(0)
            
        print(data_publicacao)

        with self.context.expect_page() as new_page_info:
            download_btn = self.page.locator("button[aria-label='Abrir diário em nova aba']").first
            download_btn.wait_for()
            download_btn.click()

        pdf_url = new_page_info.value.url
        pdf_save_path = f"./downloads/diario_pref_parnaiba_{date.strftime('%d_%m_%Y')}.pdf"

        return (pdf_url, pdf_save_path, {"data_publicacao_parnaiba": data_publicacao})

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.browser.close()