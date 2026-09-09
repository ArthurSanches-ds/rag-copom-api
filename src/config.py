from pathlib import Path

# Raiz do projeto = uma pasta acima de src/ (onde este arquivo está)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent

PASTA_CHROMA = str(RAIZ_PROJETO / "chroma_db")
PASTA_DATA = str(RAIZ_PROJETO / "data")

NOME_MODELO_EMBEDDING = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"