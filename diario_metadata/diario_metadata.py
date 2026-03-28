
"""
Armazena os seguintes metadados dos diários oficiais:
    - Nome do diário
    - Data de publicação
    - Número do diário
    - Link do PDF
"""
class DiarioMetadata:
    def __init__(self, nome=None, data_publicacao=None, numero=None, pdf_url=None):

        self.nome = nome
        self.data_publicacao = data_publicacao
        self.numero = numero
        self.link_pdf = pdf_url

    def __str__(self):
        return f"%s\nNome: %s\nData de Publicação: %s\nNúmero: %s\nLink do PDF: %s\n%s" % (
            "=" * 50,
            self.nome if self.nome else 'N/A',
            self.data_publicacao if self.data_publicacao else 'N/A',
            self.numero if self.numero else 'N/A',
            self.link_pdf,
            "=" * 50
        )