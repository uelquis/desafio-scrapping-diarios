import csv
import os

class MetadataExporter:
    def __init__(self, metadata_list):
        self.metadata_list = metadata_list

    def export_to_csv(self):
        os.makedirs("./exports", exist_ok=True)
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
        # Implementação futura para exportar em formato XLSX
        pass