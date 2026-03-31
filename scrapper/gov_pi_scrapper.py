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

        with self.context.expect_page() as new_page_info:
            download_btn = self.page.locator("td a").first
            download_btn.wait_for()
            download_btn.click()

        pdf_url = new_page_info.value.url
        pdf_save_path = f"./downloads/diario_gov_pi_{date.strftime('%d_%m_%Y')}.pdf"

        return ScrappedData([pdf_url], [pdf_save_path], {})