import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

cliente = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SCHEMA_RESPOSTA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "resposta": {"type": "string"},
        "fontes": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["resposta", "fontes"]
}


def montar_contexto(chunks: list) -> str:
    """
    Formata os chunks recuperados em um bloco de texto único,
    identificando a fonte de cada trecho para permitir citação.
    """
    blocos = []
    for chunk in chunks:
        fonte = chunk.metadata.get("source", "desconhecida")
        pagina = chunk.metadata.get("page_label", "?")
        blocos.append(f"[Fonte: {fonte}, página {pagina}]\n{chunk.page_content}")

    return "\n\n---\n\n".join(blocos)


def gerar_resposta(pergunta: str, chunks: list) -> dict:
    """
    Monta o prompt com o contexto recuperado e gera a resposta via Claude,
    retornando um dicionário já parseado com 'resposta' e 'fontes'.
    """
    contexto = montar_contexto(chunks)

    prompt_sistema = (
        "Você é um assistente que responde perguntas EXCLUSIVAMENTE com base "
        "no contexto fornecido, extraído de Atas do Copom (Banco Central do Brasil). "
        "Regras obrigatórias:\n"
        "- Responda apenas com informações presentes no contexto abaixo.\n"
        "- Se o contexto não contiver a resposta, diga claramente que não encontrou "
        "essa informação nas atas fornecidas — não invente nem complete com conhecimento geral.\n"
        "- No campo 'fontes', liste apenas os arquivos e páginas do contexto que "
        "você efetivamente usou para formular a resposta."
    )

    mensagem = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=prompt_sistema,
        messages=[
            {
                "role": "user",
                "content": f"Contexto:\n{contexto}\n\nPergunta: {pergunta}",
            }
        ],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": SCHEMA_RESPOSTA
            }
        }
    )

    return json.loads(mensagem.content[0].text)


if __name__ == "__main__":
    from retriever import carregar_indice, buscar_chunks_relevantes

    vectorstore = carregar_indice()

    pergunta_teste = "Qual foi a decisão sobre a taxa Selic?"
    chunks = buscar_chunks_relevantes(vectorstore, pergunta_teste, k=4)

    resultado = gerar_resposta(pergunta_teste, chunks)

    print(f"Pergunta: {pergunta_teste}\n")
    print(f"Resposta:\n{resultado['resposta']}\n")
    print(f"Fontes: {', '.join(resultado['fontes'])}")