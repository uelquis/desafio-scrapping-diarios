import os, csv
from pathlib import Path
import pandas as pd

class MetadataExporter:
    def __init__(self, metadata_list):
        self.metadata_list = metadata_list

        os.makedirs("./exports", exist_ok=True)

    def export_to_csv(self):
        file_path = f"./exports/diarios_metadata.csv"
        
        with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['nome', 'data_publicacao', 'numero', 'link_pdf']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for metadata in self.metadata_list:
                self._write_csv_row(writer, metadata)

    def _write_csv_row(self, writer, metadata):
        writer.writerow({
            'nome': metadata.nome if metadata.nome else 'N/A',
            'data de publicacao': metadata.data_publicacao if metadata.data_publicacao else 'N/A',
            'numero': metadata.numero if metadata.numero else 'N/A',
            'link do pdf': metadata.link_pdf
        })

    def export_to_xlsx(self):
        data_frame = pd.DataFrame([{
            'Nome': metadata.nome if metadata.nome else 'N/A',
            'Data de Publicação': metadata.data_publicacao if metadata.data_publicacao else 'N/A',
            'Número': metadata.numero if metadata.numero else 'N/A',
            'Link do PDF': metadata.link_pdf
        } for metadata in self.metadata_list])

        file_path = f"./exports/diarios_metadata.xlsx"

        if Path(file_path).exists():
            os.remove(file_path)

        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            data_frame.to_excel(writer, sheet_name='Diarios Metadata', index=False)

            # TODO: Ajustar a largura das colunas para melhor visualização dos dados
