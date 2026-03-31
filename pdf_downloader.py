
import os, requests
from typing import List
from pathlib import Path

from scrapper import ScrappedData

class PDF_Downloader:

    @staticmethod
    def download_pdfs(scrapped_diarios: List[ScrappedData]):
        path_to_downloaded_pdfs = []

        for diario in scrapped_diarios:
            try:
                PDF_Downloader._download_pdf(diario.urls[0], diario.save_paths[0])
            except Exception as e:
                print(f"Error occurred while downloading PDF from {diario.urls[0]}: {e}")
            finally:
                path_to_downloaded_pdfs.append((diario.urls[0],  diario.save_paths[0], diario.args))
    
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
                    