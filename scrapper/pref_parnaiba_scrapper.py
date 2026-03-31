import re
from time import sleep
from .diario_scrapper import DiarioScrapper, ScrappedData
from .config import SCRAPPER_CONFIG

class PrefParnaiba_Scrapper(DiarioScrapper):

    def scrap(self, date):
        
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

        data_publicacao = self.page.locator("td.text-left").nth(4)
        data_publicacao.wait_for()

        data_publicacao = re.search(r"\d{2}/\d{2}/\d{4}", 
           data_publicacao.inner_text()).group(0) # type: ignore

        with self.context.expect_page() as new_page_info:
            download_btn = self.page.locator("button[aria-label='Abrir diário em nova aba']").first
            download_btn.wait_for()
            download_btn.click()

        pdf_url = (new_page_info.value).url
        pdf_save_path = f"./downloads/diario_pref_parnaiba_{date.strftime('%d_%m_%Y')}.pdf"

        return ScrappedData([pdf_url], [pdf_save_path], {"data_publicacao_parnaiba": data_publicacao})
