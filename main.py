import re, sys
from datetime import datetime
from playwright.sync_api import sync_playwright
from diario_metadata import MetadataExtractor, MetadataExporter
from pdf_downloader import PDF_Downloader
from scrapper import DiarioScrapper

def main():
    if len(sys.argv) == 1:
        raise ValueError("Por favor, forneça uma data no formato DD-MM-AAAA como argumento.")
    
    if len(sys.argv) > 2:
        raise ValueError("Apenas um argumento é permitido, no formato DD-MM-AAAA.")
    
    if re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', sys.argv[1]) is None:
        raise ValueError("Formato de data inválido. Use DD-MM-AAAA.")

    date = datetime.strptime(sys.argv[1], "%d-%m-%Y")

    with sync_playwright() as playwright:   
        with DiarioScrapper(playwright) as scrapper:
            downloaded_pdfs = PDF_Downloader.download_pdfs(scrapper.scrap(date))

            diarios_metadata = [MetadataExtractor().get_metadata(pdf_url, pdf_path) for pdf_url, pdf_path in downloaded_pdfs]

            print("\nExportando metadados extraídos dos diários:")
            MetadataExporter(diarios_metadata).export_to_xlsx()

if __name__ == '__main__':
    main()