from pydantic import BaseModel, Field


class PerguntaRequest(BaseModel):
    """
    Formato esperado no corpo (body) de uma requisição
    ao endpoint de consulta às Atas do Copom.
    """
    pergunta: str = Field(
        ...,
        min_length=3,
        description="Pergunta sobre as Atas do Copom",
        examples=["Qual foi a decisão sobre a taxa Selic na última reunião?"]
    )


class RespostaAPI(BaseModel):
    """
    Formato de resposta devolvido pela API,
    espelhando o schema já usado no output_config.format do generator.py.
    """
    resposta: str
    fontes: list[str]