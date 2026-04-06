import re
from .diario_metadata import DiarioMetadata
from .metadata_extractor import MetadataExtractor

class GovPI_MetadataExtractor(MetadataExtractor):

    def extract(self, pdf, url):

        metadata = DiarioMetadata(pdf_url=url)

        first_page = pdf.pages[0]
        text = first_page.extract_text()

        lines = text.split("\n")

        metadata.nome = lines[2].strip().split("-")[0] if len(lines) == 3 else f"{lines[3].strip().split("-")[0]}" # {lines[0].strip().strip("-")}"

        metadata.numero = re.search(r"Nº\s*\d+/\d{4}", text, re.IGNORECASE).group(0).removeprefix("nº").strip() # type: ignore

        third_page = pdf.pages[2]
        text = third_page.extract_text()

        metadata.data_publicacao = re.search(r"Publicado:\s*\d{2}/\d{2}/\d{4}", text, re.IGNORECASE).group(0).removeprefix("Publicado:").replace("/", "-").strip() # type: ignore

        return metadata