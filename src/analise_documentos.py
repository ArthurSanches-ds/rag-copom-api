import pandas as pd
from loader import carregar_documentos


def montar_dataframe_documentos(documentos: list) -> pd.DataFrame:
    linhas = []
    for doc in documentos:
        linhas.append({
            "arquivo": doc.metadata.get("source"),
            "pagina": doc.metadata.get("page"),
            "page_label": doc.metadata.get("page_label"),
            "num_caracteres": len(doc.page_content),
        })
    return pd.DataFrame(linhas)


if __name__ == "__main__":
    docs = carregar_documentos("data")
    df = montar_dataframe_documentos(docs)

    print(df)

    print("\nEstatísticas de tamanho de conteúdo por página:")
    print(df["num_caracteres"].describe())

    print("\nPáginas suspeitas (menos de 200 caracteres — possível capa/rodapé sem conteúdo útil):")
    print(df[df["num_caracteres"] < 200])
