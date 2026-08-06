from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import carregar_documentos


def dividir_em_chunks(documentos: list, chunk_size: int = 1000, chunk_overlap: int = 150) -> list:
    """
    Divide cada Document (página) em pedaços menores (chunks),
    preservando a estrutura natural do texto (parágrafo > linha > palavra).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunks = splitter.split_documents(documentos)
    return chunks


if __name__ == "__main__":
    docs = carregar_documentos("data")
    chunks = dividir_em_chunks(docs)

    print(f"\nTotal de páginas: {len(docs)}")
    print(f"Total de chunks gerados: {len(chunks)}")
    print(f"Média de chunks por página: {len(chunks) / len(docs):.1f}")

    print("\n--- Amostra do primeiro chunk ---")
    print("Metadata:", chunks[0].metadata)
    print("Conteúdo:")
    print(chunks[0].page_content)

    print("\n--- Amostra do segundo chunk (pra ver a sobreposição) ---")
    print(chunks[1].page_content[:200])
