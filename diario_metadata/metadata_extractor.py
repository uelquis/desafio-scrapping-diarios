from scrapper import ScrappedData

from .diario_metadata import DiarioMetadata

"""
Extrai os seguintes metadados dos diários oficiais:
    - Nome do diário
    - Data de publicação
    - Número do diário
    - Link do PDF
"""
class MetadataExtractor:
    
    def __init__(self):
        pass

    def extract(self, pdf, url):
        raise NotImplementedError("extract não foi implementado!") 
        