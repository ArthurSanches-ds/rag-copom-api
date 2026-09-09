from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import PASTA_CHROMA, NOME_MODELO_EMBEDDING


def carregar_indice() -> Chroma:
    """
    Carrega o índice ChromaDB já persistido em disco,
    sem reprocessar os documentos originais.
    """
    embeddings = HuggingFaceEmbeddings(model_name=NOME_MODELO_EMBEDDING)

    vectorstore = Chroma(
        persist_directory=PASTA_CHROMA,
        embedding_function=embeddings,
    )
    return vectorstore


def buscar_chunks_relevantes(vectorstore: Chroma, pergunta: str, k: int = 4) -> list:
    """
    Busca os k chunks mais semanticamente relevantes para a pergunta.
    """
    resultados = vectorstore.similarity_search(pergunta, k=k)
    return resultados


if __name__ == "__main__":
    vectorstore = carregar_indice()

    pergunta_teste = "Qual foi a decisão sobre a taxa Selic?"
    print(f"Pergunta de teste: {pergunta_teste}\n")

    chunks = buscar_chunks_relevantes(vectorstore, pergunta_teste)

    for i, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {i} (fonte: {chunk.metadata.get('source')}, página: {chunk.metadata.get('page_label')}) ---")
        print(chunk.page_content[:300])
        print()