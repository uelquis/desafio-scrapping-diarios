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

        download_btns = self.page.locator("button[aria-label='Abrir diário em nova aba']")

        urls, save_paths = self._click_all(date, download_btns)

        return ScrappedData(urls, save_paths, {"data_publicacao_parnaiba": data_publicacao})

    def _click_all(self, date, btns):
        urls = []
        save_paths = []

        try:
            btns.wait_for()
        except Exception as err:
            print(err)
        finally:
            index = 0
            for btn in btns.all():
                url, save_path = self._click_btn(btn, date, index)

                urls.append(url)
                save_paths.append(save_path)

                index += 1
        
        return (urls, save_paths)
    
    def _click_btn(self, btn, date, index):
        with self.context.expect_page() as new_page_info:
            btn.click()

            url = new_page_info.value.url

            save_path = f"./downloads/diario_pref_parnaiba_{date.strftime('%d_%m_%Y')}{"" if index == 0 else f"__{index+1}"}.pdf"

            new_page_info.value.close()

            return (url, save_path)
