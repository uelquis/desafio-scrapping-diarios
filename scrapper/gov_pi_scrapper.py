import re
from time import sleep
from .diario_scrapper import DiarioScrapper, ScrappedData
from .config import SCRAPPER_CONFIG

class GovPI_Scrapper(DiarioScrapper):
    
    def scrap(self, date):
        
        self.page.goto(SCRAPPER_CONFIG['diarios']['gov_pi'])

        date_input = self.page.locator('input[type="date"]').first
        date_input.wait_for()
        
        date_input.fill(date.strftime("%Y-%m-%d"))

        sleep(2)

        download_btns = self.page.locator("td a")
            
        urls, save_paths = self._click_all(date, download_btns)

        return ScrappedData(urls, save_paths, {})
    
    def _click_all(self, date, btns):
        urls = []
        save_paths = []

        try:
            btns.wait_for()
        except Exception as err:
            pass
        finally:
            index = 0
            for btn in self._filter_btns(btns.all()):
                url, save_path = self._click_btn(btn, date, index)

                urls.append(url)
                save_paths.append(save_path)

                index += 1

        return (urls, save_paths)
    
    def _click_btn(self, btn, date, index):
        with self.context.expect_page() as new_page_info:
            btn.click()

            url = new_page_info.value.url

            save_path = f"./downloads/diario_gov_pi_{date.strftime('%d_%m_%Y')}{"" if index == 0 else f"__{index+1}"}.pdf"
            
            new_page_info.value.close()

            return (url, save_path)

    def _filter_btns(self, btns):
        filtered_btns = []

        for btn in btns:
            href = btn.get_attribute("href")
            if href and re.search(r".pdf$", href):
                filtered_btns.append(btn)

        return filtered_btns