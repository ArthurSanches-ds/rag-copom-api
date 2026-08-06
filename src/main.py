from retriever import carregar_indice, buscar_chunks_relevantes
from generator import gerar_resposta


def main():
    print("=" * 60)
    print("Sistema RAG - Atas do Copom")
    print("Digite sua pergunta ou 'sair' para encerrar.")
    print("=" * 60)

    print("\nCarregando índice vetorial...")
    vectorstore = carregar_indice()
    print("Pronto!\n")

    while True:
        pergunta = input("Sua pergunta: ").strip()

        if pergunta.lower() in ("sair", "exit", "quit"):
            print("Encerrando. Até mais!")
            break

        if not pergunta:
            continue

        chunks = buscar_chunks_relevantes(vectorstore, pergunta, k=4)
        resposta = gerar_resposta(pergunta, chunks)

        print(f"\n{resposta}\n")
        print("-" * 60)


if __name__ == "__main__":
    main()