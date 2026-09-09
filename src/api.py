from contextlib import asynccontextmanager
from fastapi import FastAPI

from retriever import carregar_indice, buscar_chunks_relevantes
from generator import gerar_resposta
from schemas import PerguntaRequest, RespostaAPI

recursos = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Roda UMA VEZ, quando o servidor inicia
    print("Carregando índice vetorial...")
    recursos["vectorstore"] = carregar_indice()
    print("Índice carregado. API pronta.")
    yield
    # Código depois do yield roda quando o servidor desliga (não usamos por ora)
    recursos.clear()


app = FastAPI(
    title="API - Atas do Copom",
    description="Consulta às Atas do Copom via RAG (LangChain + ChromaDB + Claude)",
    lifespan=lifespan
)


@app.post("/perguntar", response_model=RespostaAPI)
def perguntar(request: PerguntaRequest) -> RespostaAPI:
    chunks = buscar_chunks_relevantes(recursos["vectorstore"], request.pergunta, k=4)
    resultado = gerar_resposta(request.pergunta, chunks)
    return RespostaAPI(resposta=resultado["resposta"], fontes=resultado["fontes"])