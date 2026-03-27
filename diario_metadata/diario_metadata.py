

import re

import pdfplumber

"""
Extrai e armazena os seguintes metadados dos diários oficiais:
    - Nome do diário
    - Data de publicação
    - Número do diário
    - Link do PDF
"""
class DiarioMetadata:
    def __init__(self, pdf_url, pdf_path):

        self.nome = None
        self.data_publicacao = None
        self.numero = None
        self.link_pdf = pdf_url

        with pdfplumber.open(pdf_path) as pdf:
            if "tjpi" in pdf_path:
                self._extract_metadata_tjpi(pdf)
        
    def _extract_metadata_tjpi(self, pdf):
        print("=" * 50)
        print("Extraindo metadados do diário do TJPI...")

        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        self.nome = re.search(r"Diário da Justiça", text, re.IGNORECASE).group(0)

        meses = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
        data_publicacao_raw = re.search(r"Publicação: ([^)]*), ([^)]*)", text, re.IGNORECASE).group(0)

        dia = re.search(r"\d{1,2}", data_publicacao_raw).group(0)
        ano = re.search(r"\d{4}", data_publicacao_raw).group(0)
        mes = None
        for i, mes in enumerate(meses):
            if mes in data_publicacao_raw.lower():
                mes = str(i + 1)
                break
        
        self.data_publicacao = f"{dia.zfill(2)}-{mes.zfill(2)}-{ano}"   

        self.numero = re.search(r"Nº\s*\d+", text, re.IGNORECASE).group(0).removeprefix("Nº").strip()

    def __str__(self):
        return f"%s\nNome: %s\nData de Publicação: %s\nNúmero: %s\nLink do PDF: %s\n%s" % (
            "=" * 50,
            self.nome if self.nome else 'N/A',
            self.data_publicacao if self.data_publicacao else 'N/A',
            self.numero if self.numero else 'N/A',
            self.link_pdf,
            "=" * 50
        )