#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo simplificado de busca usando apenas a estrutura de agentes do Mangaba AI

Este script demonstra como utilizar apenas a estrutura de agentes do Mangaba AI
para realizar buscas de ebooks, sem utilizar a aplicação completa.
"""

import asyncio
import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao path para importar o módulo mangaba_ai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importa os componentes necessários do Mangaba AI
try:
    from mangaba_ai.core.models import Agent, Task
except ImportError:
    try:
        from src.mangaba_ai.core.models import Agent, Task
    except ImportError:
        # Usa a versão de compatibilidade se necessário
        from compat.models import Agent, Task


class BuscaEbookAgent(Agent):
    """
    Agente especializado em busca de ebooks usando apenas a estrutura de agentes do Mangaba AI.
    """

    def __init__(self):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Busca Ebook Agent",
            role="Especialista em busca de ebooks",
            goal="Encontrar ebooks em diversas fontes online",
        )
        self.version = "1.0.0"
        self.sources = [
            "https://libgen.is/search.php?req={query}",
            "https://b-ok.lat/s/{query}",
            "https://archive.org/search.php?query={query}",
            "https://www.pdfdrive.com/search?q={query}",
            "https://www.gutenberg.org/ebooks/search/?query={query}",
        ]

    async def execute(self, task: str) -> str:
        """
        Executa a tarefa de busca de ebooks.

        Args:
            task: Descrição da tarefa (nome do ebook a ser buscado)

        Returns:
            Resultados formatados da busca
        """
        # Extrai o nome do ebook da descrição da tarefa
        ebook_name = task.strip()
        print(f"Buscando ebook: {ebook_name}")

        # Simula a busca em diferentes fontes
        results = []
        for source in self.sources:
            source_url = source.format(query=ebook_name.replace(" ", "+"))

            # Simula 1-2 resultados por fonte
            for i in range(1, 3):
                result = {
                    "title": f"{ebook_name} - {'Edição ' + str(i) if i > 1 else 'Completo'}",
                    "author": f"Autor {'A' if i == 1 else 'B'}",
                    "format": "PDF" if i % 2 == 0 else "EPUB",
                    "source": source.split("/")[2],
                    "url": source_url,
                }
                results.append(result)

        # Formata os resultados
        output = f"Resultados da busca por '{ebook_name}'\n"
        output += f"Encontrados {len(results)} resultados\n\n"

        for i, result in enumerate(results, 1):
            output += f"{i}. {result['title']}\n"
            output += f"   Autor: {result['author']}\n"
            output += f"   Formato: {result['format']}\n"
            output += f"   Fonte: {result['source']}\n"
            output += f"   Link: {result['url']}\n\n"

        return output


async def main():
    """
    Função principal para demonstração do uso de agentes do Mangaba AI para busca.
    """
    # Inicializa o agente de busca
    agente_busca = BuscaEbookAgent()

    print("===== Busca de Ebooks com Agentes Mangaba AI =====\n")
    print("Digite o nome do ebook que deseja buscar ou 'sair' para encerrar.\n")

    while True:
        # Solicita entrada do usuário
        ebook_name = input("Nome do ebook: ")

        # Verifica se o usuário deseja sair
        if ebook_name.lower() == "sair":
            print("\nEncerrando a aplicação...")
            break

        # Verifica se a entrada é válida
        if not ebook_name.strip():
            print("\nPor favor, digite um nome válido.\n")
            continue

        try:
            # Cria uma tarefa para o agente
            start_time = datetime.now()

            # Executa a tarefa diretamente no agente
            resultado = await agente_busca.execute(ebook_name)

            end_time = datetime.now()
            search_time = (end_time - start_time).total_seconds()

            # Exibe os resultados
            print("\n" + resultado)
            print(f"Busca concluída em {search_time:.2f} segundos.\n")

            # Pergunta se deseja salvar os resultados
            save_option = input("Deseja salvar os resultados? (s/n): ")
            if save_option.lower() == "s":
                # Cria o diretório de resultados se não existir
                results_dir = "resultados"
                os.makedirs(results_dir, exist_ok=True)

                # Define o nome do arquivo
                filename = os.path.join(
                    results_dir,
                    f"busca_{ebook_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                )

                # Salva os resultados
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(resultado)

                print(f"Resultados salvos em: {filename}\n")

        except Exception as e:
            print(f"\nErro ao buscar ebooks: {str(e)}\n")

    print("\nObrigado por utilizar a aplicação de Busca de Ebooks!")


if __name__ == "__main__":
    # Executa a função principal
    asyncio.run(main())
