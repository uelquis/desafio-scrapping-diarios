from datetime import datetime
import sys

from playwright.sync_api import sync_playwright
from scrapper import DiarioScrapper

def main():
    if len(sys.argv) == 1:
        raise ValueError("Por favor, forneça uma data no formato DD-MM-AAAA como argumento.")
    
    if len(sys.argv) > 2:
        raise ValueError("Apenas um argumento é permitido, no formato DD-MM-AAAA.")

    date = datetime.strptime(sys.argv[1], "%d-%m-%Y")

    with sync_playwright() as playwright:
        with DiarioScrapper(playwright) as scrapper:
            scrapper.scrap(date)

if __name__ == '__main__':
    main()