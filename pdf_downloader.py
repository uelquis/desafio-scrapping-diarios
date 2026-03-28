
import os, requests
from pathlib import Path

class PDF_Downloader:

    @staticmethod
    def download_pdfs(scrapped_pdfs):
        path_to_downloaded_pdfs = []

        for pdf_url, pdf_save_path in scrapped_pdfs:
            try:
                PDF_Downloader._download_pdf(pdf_url, pdf_save_path)
            except Exception as e:
                print(f"Error occurred while downloading PDF from {pdf_url}: {e}")
            finally:
                path_to_downloaded_pdfs.append((pdf_url, pdf_save_path))
        
        return path_to_downloaded_pdfs
    
    @staticmethod
    def _download_pdf(url, save_path):
        os.makedirs("./downloads", exist_ok=True)

        with requests.get(url, stream=True) as response:
            if response.status_code != 200:
                raise Exception(f"Failed to retrieve PDF: {response.status_code}")

            if Path(save_path).exists():
                print(f"PDF already exists at {save_path}, skipping download.")
                return

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    