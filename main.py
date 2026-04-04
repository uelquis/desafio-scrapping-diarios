import re, sys
from datetime import datetime
from playwright.sync_api import sync_playwright
from diario_metadata import MetadataExtractor, MetadataExporter
from pdf_downloader import PDF_Downloader
from scrapper import DiarioScrapper, GovPI_Scrapper, TJPI_Scrapper, PrefParnaiba_Scrapper

def main():
    if len(sys.argv) == 1:
        raise ValueError("Por favor, forneça uma data no formato DD-MM-AAAA como argumento.")
    
    if len(sys.argv) > 2:
        raise ValueError("Apenas um argumento é permitido, no formato DD-MM-AAAA.")
    
    if re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', sys.argv[1]) is None:
        raise ValueError("Formato de data inválido. Use DD-MM-AAAA.")

    date = datetime.strptime(sys.argv[1], "%d-%m-%Y")

    with sync_playwright() as playwright:
        scrap(date, DiarioScrapper.init_browser_context(playwright))

def scrap(date, ctx):
    with (
        GovPI_Scrapper(ctx) as govpi_scrapper, 
        TJPI_Scrapper(ctx) as tjpi_scrapper,
        PrefParnaiba_Scrapper(ctx) as parnaiba_scrapper
    ):
        scrapped_diarios = []
        try:
            # TODO: garantir que vão seguir o padrão de quais cadernos são suplementares/extraordinários
            # e quais são únicos. Ex:
            #   - final "__n" indica que é suplementar/extraordinário
            #   - final ausente indica caderno único
            scrapped_diarios.append(govpi_scrapper.scrap(date))
            scrapped_diarios.append(tjpi_scrapper.scrap(date))
            # TODO: implementar completamente o scrapping de diários de cadernos únicos suplementares
            scrapped_diarios.append(parnaiba_scrapper.scrap(date))
            
        except TimeoutError as err:
            print(f"Não foi possível scrappar um ou mais diários: {err}")
        except Exception as err:
            print(f"Erro inesperado: {err}")
        finally:
            if len(scrapped_diarios) == 0:
                raise ValueError("scrapped_diarios está vazio!")
            
            PDF_Downloader.download_pdfs(scrapped_diarios)

            # TODO: refatorar MetadataExtractor
            diarios_metadata = [MetadataExtractor().get_metadata(diario) for diario in scrapped_diarios]
        
            # TODO: refatorar MetadataExporter
            MetadataExporter(diarios_metadata).export_to_xlsx()

if __name__ == '__main__':
    main()