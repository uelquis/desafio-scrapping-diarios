import os, sys, requests
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from diario_metadata import DiarioMetadata, MetadataExporter
from scrapper import DiarioScrapper

def download_pdf(url, save_path):
    os.makedirs("./downloads", exist_ok=True)

    with requests.get(url, stream=True) as response:
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve PDF: {response.status_code}")

        if Path(save_path).exists():
            raise Exception(f"PDF already exists at {save_path}, skipping download.")

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def download_scrapped_pdfs(scrapped_pdfs):
    path_to_downloaded_pdfs = []

    for pdf_url, pdf_save_path in scrapped_pdfs:
        try:
            download_pdf(pdf_url, pdf_save_path)
        except Exception as e:
            print(f"Error occurred while downloading PDF from {pdf_url}: {e}")
        finally:
            path_to_downloaded_pdfs.append((pdf_url, pdf_save_path))
    
    return path_to_downloaded_pdfs

def main():
    if len(sys.argv) == 1:
        raise ValueError("Por favor, forneça uma data no formato DD-MM-AAAA como argumento.")
    
    if len(sys.argv) > 2:
        raise ValueError("Apenas um argumento é permitido, no formato DD-MM-AAAA.")

    date = datetime.strptime(sys.argv[1], "%d-%m-%Y")

    with sync_playwright() as playwright:   
        with DiarioScrapper(playwright) as scrapper:
            path_to_downloaded_pdfs = download_scrapped_pdfs(scrapper.scrap(date))

            diarios_metadata = [DiarioMetadata(pdf_url, pdf_path) for pdf_url, pdf_path in path_to_downloaded_pdfs]

            print("\nExportando metadados extraídos dos diários:")
            MetadataExporter(diarios_metadata).export_to_csv()

if __name__ == '__main__':
    main()