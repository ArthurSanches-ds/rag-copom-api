# RAG Copom API

API REST em FastAPI para consulta às Atas do Copom via RAG (Retrieval-Augmented Generation), evoluída do projeto [rag-copom-langchain](https://github.com/ArthurSanches-ds/rag-copom-langchain).

## Stack

- **FastAPI** — API REST
- **LangChain** — orquestração do pipeline RAG
- **ChromaDB** — banco de dados vetorial
- **Anthropic Claude (claude-sonnet-4-6)** — geração de respostas, com **Structured Outputs** (`output_config.format`) garantindo retorno em JSON estruturado (`resposta` + `fontes`)
- **Docker** — containerização
- **AWS EC2** — deploy em produção

## Arquitetura

Diferente do projeto original (terminal interativo), esta API expõe o pipeline RAG via HTTP:


O índice vetorial é carregado **uma única vez** no startup do servidor (via `lifespan`), não a cada requisição.

## Setup local

### 1. Clonar e criar ambiente virtual

```bash
git clone https://github.com/ArthurSanches-ds/rag-copom-api.git
cd rag-copom-api
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Cria um arquivo `.env` na raiz do projeto:


### 3. Gerar o índice vetorial

**Importante:** o `chroma_db/` não é versionado (dado gerado, não código). É necessário gerar o índice antes de rodar a API pela primeira vez:

```bash
cd src
python indexer.py
```

### 4. Rodar a API localmente

```bash
uvicorn api:app --reload
```

Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

## Rodando com Docker

O `chroma_db` é gerado **durante o build** da imagem (não em runtime), já que o dataset (Atas do Copom) é estático e pequeno.

```bash
docker build -t rag-copom-api .
docker run -p 8000:8000 --env-file .env -d rag-copom-api
```

## Deploy (AWS EC2)

Deploy realizado em uma instância EC2 (`t3.micro`, Amazon Linux 2023):

1. Docker instalado na instância (`sudo dnf install -y docker`)
2. Repositório clonado via `git clone`
3. `.env` criado diretamente na instância (nunca versionado)
4. **Swap file de 2GB configurado** — necessário porque `t3.micro` (1GB RAM) não é suficiente para o build (PyTorch + sentence-transformers + geração de embeddings)
5. Build e run do container, com porta 8000 liberada no Security Group

## Limitações conhecidas

- **Busca por similaridade, não recência**: o retriever busca os chunks mais semanticamente relevantes, não necessariamente os mais recentes cronologicamente. Perguntas como "qual foi a última decisão" podem retornar a reunião mais relevante semanticamente, não a mais recente no calendário.
- **PyTorch CPU-only**: a imagem Docker usa explicitamente a build CPU do PyTorch para reduzir tamanho e evitar dependências CUDA desnecessárias, já que não há GPU disponível no ambiente de deploy.