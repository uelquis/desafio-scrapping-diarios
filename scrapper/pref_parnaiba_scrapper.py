from datetime import datetime, timedelta
import re
from time import sleep
from .diario_scrapper import DiarioScrapper, ScrappedData
from .config import SCRAPPER_CONFIG

class PrefParnaiba_Scrapper(DiarioScrapper):

    def scrap(self, data: datetime):
        
        self.page.goto(SCRAPPER_CONFIG['diarios']['pref_parnaiba'])

        input_data_inicial = self.page.locator('input[aria-label="Data Inicial"]').first
        input_data_inicial.wait_for()

        input_data_inicial.fill(data.strftime("%d-%m-%Y"))

        input_data_final = self.page.locator('input[aria-label="Data Final"]').first
        input_data_final.wait_for()
        
        input_data_final.fill((data + timedelta(days=7)).strftime("%d-%m-%Y"))

        filtrar_btn = self.page.get_by_text("Filtrar").first
        filtrar_btn.wait_for()
        filtrar_btn.click()

        sleep(2)

        rows = self.page.locator("tbody tr")

        datas_publicacao = []

        download_btns = []
        try:
            rows.wait_for()
        except Exception as err:
            print(err)
        finally:            
            filtered_rows = self._filtrar_rows(rows.all(), data)

            datas_publicacao = self._extrair_datas_publicacao(filtered_rows)

            download_btns = self._get_download_btns(filtered_rows)

            urls, save_paths = self._click_all(data, download_btns)

        return ScrappedData(urls, save_paths, {"datas_publicacao_parnaiba": datas_publicacao})

    def _extrair_datas_publicacao(self, rows):
        return [row.inner_text().split("\t")[4].split(" ")[0] for row in rows]
    
    def _filtrar_rows(self, rows: list, data_inicial):
        # a data de disponibilização precisa ser a mesma que a data inicial
        indexes_for_removal = []
        for index, row in enumerate(rows):
            date_str = row.inner_text().split("\t")[3].split(" ")[0]

            if datetime.strptime(date_str, "%d/%m/%Y") != data_inicial: indexes_for_removal.append(index)

        elements_to_remove = [rows[index] for index in indexes_for_removal]
        [rows.remove(element) for element in elements_to_remove]

        return rows

    def _get_download_btns(self, rows):
        download_btns = []
        for row in rows:
            btn = row.locator("button[aria-label='Abrir diário em nova aba']")
            btn.wait_for()
            download_btns.append(btn.first)

        return download_btns

    def _click_all(self, date, btns):
        urls = []
        save_paths = []

        index = 0
        for btn in btns:
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
