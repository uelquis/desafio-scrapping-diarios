import re, sys, pdfplumber
from datetime import datetime
from playwright.sync_api import sync_playwright
from diario_metadata import MetadataExporter, GovPI_MetadataExtractor, PrefParnabiba_MetadataExtractor, TJPI_MetadataExtractor
from pdf_downloader import PDF_Downloader
from scrapper import DiarioScrapper, GovPI_Scrapper, TJPI_Scrapper, PrefParnaiba_Scrapper
from scrapper import ScrappedData

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
            scrapped_diarios.append(parnaiba_scrapper.scrap(date))
            
        except TimeoutError as err:
            print(f"Não foi possível scrappar um ou mais diários: {err}")
        except Exception as err:
            print(f"Erro inesperado: {err}")
        finally:
            if len(scrapped_diarios) == 0:
                raise ValueError("scrapped_diarios está vazio!")
            
            PDF_Downloader.download_pdfs(scrapped_diarios)

            diarios_metadata = get_metadata(scrapped_diarios)

            # TODO: refatorar MetadataExporter
            MetadataExporter(diarios_metadata).export_to_xlsx()


def get_metadata(scrapped_diarios):

    scrapped_data = []
    args = []
    for diario in scrapped_diarios:
        scrapped_data.append(diario)
        args.append(diario.args)

    save_paths = [path for data in scrapped_data for path in data.save_paths]
    pdf_urls = [url for data in scrapped_data for url in data.urls]

    datas_publicacao_parnaiba = args[2]['datas_publicacao_parnaiba']
    index = 0

    metadata = []

    # TODO: concertar o nome dos diários
    for path, url in zip(save_paths, pdf_urls):
        with pdfplumber.open(path) as pdf:
            if "gov_pi" in path: metadata.append(GovPI_MetadataExtractor().extract(pdf, url))

            elif "tjpi" in path: metadata.append(TJPI_MetadataExtractor().extract(pdf, url))
            
            elif "pref_parnaiba" in path: 
                metadata.append(PrefParnabiba_MetadataExtractor().extract(pdf, url, datas_publicacao_parnaiba[index]))
                index += 1
            
            else: raise ValueError(f"Não foi possível identificar o tipo do diário com base no nome do arquivo: {path}")

    return metadata  


if __name__ == '__main__':
    main()