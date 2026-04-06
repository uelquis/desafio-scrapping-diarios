import re
from .diario_metadata import DiarioMetadata
from .metadata_extractor import MetadataExtractor


class PrefParnabiba_MetadataExtractor(MetadataExtractor):

    def extract(self, pdf, url, data_publicacao):

        # info: a data de publicação não está no pdf do diário.
        # então ela foi extraída diretamente do portal do município.
        metadata = DiarioMetadata(
            data_publicacao = data_publicacao, 
            pdf_url = url
        )

        first_page = pdf.pages[0]
        text = first_page.extract_text()


        tipo_nome = ""
        diario_tipo = text.split("\n")[1].strip().strip("-")
        
        if re.search("Caderno Único", diario_tipo, re.IGNORECASE) == None:
            tipo_nome = text.split("\n")[1].strip("-").upper()

        metadata.numero = re.search(r"Nº\s*\d+", text, re.IGNORECASE).group(0).removeprefix("Nº").strip() # type: ignore

        second_page = pdf.pages[1]
        text = second_page.extract_text()

        # info: nome extraido do cabeçalho
        metadata.nome = " ".join(text.split("\n")[0].split()[2].split("-")[:2]) # + " " + tipo_nome

        return metadata