import re
from .diario_metadata import DiarioMetadata
from .metadata_extractor import MetadataExtractor


class TJPI_MetadataExtractor(MetadataExtractor):

    def extract(self, pdf, url):

        metadata = DiarioMetadata(pdf_url=url)

        second_page = pdf.pages[1]
        text = second_page.extract_text()
        
        linhas_cabecalho = []
        for linha in text.split("\n"):
            if re.match("ANO", linha):
                break
            
            linhas_cabecalho.append(linha)

        if len(linhas_cabecalho) == 1:
            metadata.nome = linhas_cabecalho[0]
        elif len(linhas_cabecalho) == 2:
            metadata.nome = f"{linhas_cabecalho[1]}" # {linhas_cabecalho[0]}"
        else: raise Exception("cabeçalho maior do que o esperado!")

        meses = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
        data_publicacao_raw = re.search(r"Publicação: ([^)]*), ([^)]*)", text, re.IGNORECASE).group(0) # type: ignore

        dia = re.search(r"\d{1,2}", data_publicacao_raw).group(0) # type: ignore
        ano = re.search(r"\d{4}", data_publicacao_raw).group(0) # type: ignore
        mes = None
        for i, mes in enumerate(meses):
            if mes in data_publicacao_raw.lower():
                mes = str(i + 1)
                break
        
        metadata.data_publicacao = f"{dia.zfill(2)}-{mes.zfill(2)}-{ano}"    # type: ignore

        metadata.numero = re.search(r"Nº\s*\d+", text, re.IGNORECASE).group(0).removeprefix("Nº").strip() # type: ignore

        return metadata