from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from loader import carregar_documentos
from splitter import dividir_em_chunks

PASTA_CHROMA = "chroma_db"
NOME_MODELO_EMBEDDING = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def construir_indice(chunks: list) -> Chroma:
    """
    Gera embeddings para cada chunk e persiste no ChromaDB em disco,
    permitindo reutilizar o índice sem reprocessar tudo de novo.
    """
    print(f"Carregando modelo de embedding: {NOME_MODELO_EMBEDDING}")
    embeddings = HuggingFaceEmbeddings(model_name=NOME_MODELO_EMBEDDING)

    print(f"Gerando embeddings e indexando {len(chunks)} chunks...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PASTA_CHROMA,
    )

    print(f"Índice salvo em: {PASTA_CHROMA}")
    return vectorstore


if __name__ == "__main__":
    docs = carregar_documentos("data")
    chunks = dividir_em_chunks(docs)
    construir_indice(chunks)
