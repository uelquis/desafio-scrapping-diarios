from time import sleep
from .diario_scrapper import DiarioScrapper, ScrappedData
from .config import SCRAPPER_CONFIG

class TJPI_Scrapper(DiarioScrapper):

    def scrap(self, date):

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

            # TODO: click all download pdf buttons
            # pdf_btns = self.page.locator('a:has-text("PDF")')

            # try:
            #     pdf_btns.wait_for()
            # except Exception as err:
            #     print(err)
            # finally:
            #     pdf_btns.all()

            # sleep(10)
            #
            # pdf_btn.click()

        pdf_url = new_page_info.value.url
        pdf_save_path = f"./downloads/diario_tjpi_{date.strftime('%d_%m_%Y')}.pdf"
        
        return ScrappedData([pdf_url], [pdf_save_path], {})
