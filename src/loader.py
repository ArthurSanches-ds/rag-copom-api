import os
from langchain_community.document_loaders import PyPDFLoader


def carregar_documentos(pasta_dados: str, min_caracteres: int = 200) -> list:
    """
    Percorre a pasta de dados, carrega cada PDF e retorna
    uma lista de Documents, descartando páginas com pouco conteúdo
    (capas/rodapés que não agregam informação pra busca).
    """
    todos_documentos = []

    for nome_arquivo in os.listdir(pasta_dados):
        if not nome_arquivo.endswith(".pdf"):
            continue

        caminho_completo = os.path.join(pasta_dados, nome_arquivo)
        print(f"Carregando: {nome_arquivo}")

        loader = PyPDFLoader(caminho_completo)
        documentos = loader.load()

        # filtra páginas com conteúdo insuficiente (ex: capas)
        documentos_uteis = [
            doc for doc in documentos
            if len(doc.page_content) >= min_caracteres
        ]

        todos_documentos.extend(documentos_uteis)

    print(
        f"\nTotal de páginas carregadas (após filtro): {len(todos_documentos)}")
    return todos_documentos


if __name__ == "__main__":
    docs = carregar_documentos("data")

    print("\n--- Amostra do primeiro documento ---")
    print("Metadata:", docs[0].metadata)
    print("Conteúdo (primeiros 500 caracteres):")
    print(docs[0].page_content[:500])
