from .diario_metadata import DiarioMetadata
import re, pdfplumber

"""
Extrai os seguintes metadados dos diários oficiais:
    - Nome do diário
    - Data de publicação
    - Número do diário
    - Link do PDF
"""
class MetadataExtractor:
    
    def __init__(self):
        self.metadata = DiarioMetadata()

    def get_metadata(self, pdf_url, pdf_path, args):

        self.metadata.link_pdf = pdf_url

        with pdfplumber.open(pdf_path) as pdf:
            print("=" * 50)
            if "tjpi" in pdf_path:
                self._extract_metadata_tjpi(pdf)
            elif "gov_pi" in pdf_path:
                self._extract_metadata_govpi(pdf)
            elif "pref_parnaiba" in pdf_path:
                self._extract_metadata_parnaiba(pdf, args)
            else:
                raise ValueError(f"Não foi possível identificar o tipo do diário com base no nome do arquivo: {pdf_path}")
            
        return self.metadata
        
        
    def _extract_metadata_tjpi(self, pdf):
        print("Extraindo metadados do diário do TJPI...")

        second_page = pdf.pages[1]
        text = second_page.extract_text()
        
        self.metadata.nome = text.split("\n")[0]

        meses = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
        data_publicacao_raw = re.search(r"Publicação: ([^)]*), ([^)]*)", text, re.IGNORECASE).group(0)

        dia = re.search(r"\d{1,2}", data_publicacao_raw).group(0)
        ano = re.search(r"\d{4}", data_publicacao_raw).group(0)
        mes = None
        for i, mes in enumerate(meses):
            if mes in data_publicacao_raw.lower():
                mes = str(i + 1)
                break
        
        self.metadata.data_publicacao = f"{dia.zfill(2)}-{mes.zfill(2)}-{ano}"   

        self.metadata.numero = re.search(r"Nº\s*\d+", text, re.IGNORECASE).group(0).removeprefix("Nº").strip()

    def _extract_metadata_govpi(self, pdf):
        print("Extraindo metadados do diário do Governo do Piauí...")

        first_page = pdf.pages[0]
        text = first_page.extract_text()

        self.metadata.nome = text.split("\n")[2].strip().split("-")[0]

        self.metadata.numero = re.search(r"Nº\s*\d+/\d{4}", text, re.IGNORECASE).group(0).removeprefix("nº").strip()

        third_page = pdf.pages[2]
        text = third_page.extract_text()

        self.metadata.data_publicacao = re.search(r"Publicado:\s*\d{2}/\d{2}/\d{4}", text, re.IGNORECASE).group(0).removeprefix("Publicado:").replace("/", "-").strip()

    def _extract_metadata_parnaiba(self, pdf, args):
        print("Extraindo metadados do diário da Prefeitura de Parnaíba...")

        first_page = pdf.pages[0]
        text = first_page.extract_text()

        self.metadata.numero = re.search(r"Nº\s*\d+", text, re.IGNORECASE).group(0).removeprefix("Nº").strip()

        second_page = pdf.pages[1]
        text = second_page.extract_text()

        # info: nome extraido do cabeçalho
        diario_nome = " ".join(text.split("\n")[0].split()[2].split("-")[:2])

        self.metadata.nome = diario_nome

        # info: a data de publicação não está no pdf do diário.
        # então ela foi extraída diretamente do portal do município.
        self.metadata.data_publicacao = args['data_publicacao_parnaiba']
        