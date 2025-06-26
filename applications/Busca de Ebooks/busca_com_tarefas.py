#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de busca usando agentes e tarefas do Mangaba AI

Este script demonstra como utilizar a estrutura de agentes e tarefas do Mangaba AI
para realizar buscas de ebooks de forma mais estruturada.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

# Adiciona o diretório pai ao path para importar o módulo mangaba_ai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importa os componentes necessários do Mangaba AI
try:
    from mangaba_ai.core.models import Agent, Task
    from mangaba_ai.main import MangabaAI
except ImportError:
    try:
        from src.mangaba_ai.core.models import Agent, Task
        from src.mangaba_ai.main import MangabaAI
    except ImportError:
        # Usa a versão de compatibilidade se necessário
        from compat.models import Agent, Task

        # Cria uma classe MangabaAI simulada se necessário
        class MangabaAI:
            def __init__(self):
                pass


class BuscaEbookAgent(Agent):
    """
    Agente especializado em busca de ebooks.
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
        self.memory = {}

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
        print(f"Agente '{self.name}' buscando ebook: {ebook_name}")

        # Busca o ebook
        results = await self._search_ebook(ebook_name)

        # Armazena os resultados na memória do agente
        self.memory[ebook_name] = {
            "query": ebook_name,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat(),
        }

        # Formata os resultados
        return self._format_results(ebook_name, results)

    async def _search_ebook(self, query: str) -> List[Dict[str, str]]:
        """
        Busca o ebook nas fontes disponíveis.

        Args:
            query: Nome do ebook a ser buscado

        Returns:
            Lista de dicionários contendo informações sobre os ebooks encontrados
        """
        # Simula a busca em diferentes fontes
        results = []
        for source in self.sources:
            source_url = source.format(query=query.replace(" ", "+"))

            # Simula 1-2 resultados por fonte
            for i in range(1, 3):
                # Usa um hash simples para gerar resultados consistentes
                if i == 1 or hash(source + query) % 2 == 0:
                    result = {
                        "title": f"{query} - {'Edição ' + str(i) if i > 1 else 'Completo'}",
                        "author": f"Autor {'A' if i == 1 else 'B'}",
                        "format": "PDF" if i % 2 == 0 else "EPUB",
                        "size": f"{(i * 2) + (hash(source) % 3):.1f} MB",
                        "source": source.split("/")[2],
                        "url": source_url,
                        "download_url": f"{source_url}&download=true&id={hash(source + query) % 1000}",
                    }
                    results.append(result)

        # Simula um pequeno atraso na busca
        await asyncio.sleep(0.5)

        return results

    def _format_results(self, query: str, results: List[Dict[str, str]]) -> str:
        """
        Formata os resultados da busca para exibição.

        Args:
            query: Nome do ebook buscado
            results: Lista de resultados da busca

        Returns:
            String formatada com os resultados
        """
        output = f"Resultados da busca por '{query}'\n"
        output += f"Encontrados {len(results)} resultados\n\n"

        for i, result in enumerate(results, 1):
            output += f"{i}. {result['title']}\n"
            output += f"   Autor: {result['author']}\n"
            output += f"   Formato: {result['format']} | Tamanho: {result['size']}\n"
            output += f"   Fonte: {result['source']}\n"
            output += f"   Link: {result['download_url']}\n\n"

        return output


class BuscaEbookTask(Task):
    """
    Tarefa de busca de ebooks.
    """

    def __init__(self, ebook_name: str, agent: Agent):
        """
        Inicializa a tarefa de busca.

        Args:
            ebook_name: Nome do ebook a ser buscado
            agent: Agente responsável pela busca
        """
        description = f"Buscar o ebook '{ebook_name}' em todas as fontes disponíveis"
        super().__init__(description=description, agent=agent)
        self.ebook_name = ebook_name
        self.result = None

    async def execute(self) -> Dict[str, Any]:
        """
        Executa a tarefa de busca.

        Returns:
            Dicionário com os resultados da busca
        """
        print(f"Executando tarefa: {self.description}")

        # Executa a tarefa usando o agente
        self.response = await self.agent.execute(self.ebook_name)

        # Obtém os resultados da memória do agente
        self.result = self.agent.memory.get(self.ebook_name)

        return {"formatted_results": self.response, "raw_results": self.result}


class BuscaEbookApp:
    """
    Aplicação de busca de ebooks usando a estrutura de agentes e tarefas do Mangaba AI.
    """

    def __init__(self):
        """
        Inicializa a aplicação.
        """
        self.mangaba = MangabaAI()
        self.agent = BuscaEbookAgent()

    async def buscar_ebook(self, ebook_name: str) -> Dict[str, Any]:
        """
        Busca um ebook usando a estrutura de tarefas.

        Args:
            ebook_name: Nome do ebook a ser buscado

        Returns:
            Dicionário com os resultados da busca
        """
        # Cria uma tarefa para buscar o ebook
        tarefa = BuscaEbookTask(ebook_name=ebook_name, agent=self.agent)

        # Executa a tarefa
        resultado = await tarefa.execute()

        return resultado

    def salvar_resultados(self, resultado: Dict[str, Any], formato: str = "txt") -> str:
        """
        Salva os resultados da busca em um arquivo.

        Args:
            resultado: Dicionário com os resultados da busca
            formato: Formato do arquivo (txt ou json)

        Returns:
            Caminho do arquivo salvo
        """
        # Cria o diretório de resultados se não existir
        results_dir = "resultados"
        os.makedirs(results_dir, exist_ok=True)

        # Obtém o nome do ebook da consulta
        ebook_name = resultado["raw_results"]["query"]

        # Define o nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if formato.lower() == "json":
            # Salva em formato JSON
            filename = os.path.join(
                results_dir, f"busca_{ebook_name.replace(' ', '_')}_{timestamp}.json"
            )
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(resultado["raw_results"], f, indent=2, ensure_ascii=False)
        else:
            # Salva em formato TXT
            filename = os.path.join(
                results_dir, f"busca_{ebook_name.replace(' ', '_')}_{timestamp}.txt"
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(resultado["formatted_results"])

        return filename


async def main():
    """
    Função principal para demonstração da aplicação.
    """
    # Inicializa a aplicação
    app = BuscaEbookApp()

    print("===== Busca de Ebooks com Agentes e Tarefas do Mangaba AI =====\n")
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
            # Realiza a busca
            print(f"\nBuscando '{ebook_name}'...\n")
            start_time = datetime.now()
            resultado = await app.buscar_ebook(ebook_name)
            end_time = datetime.now()

            # Calcula o tempo de busca
            search_time = (end_time - start_time).total_seconds()

            # Exibe os resultados formatados
            print(resultado["formatted_results"])
            print(f"Busca concluída em {search_time:.2f} segundos.\n")

            # Pergunta se deseja salvar os resultados
            save_option = input("Deseja salvar os resultados? (s/n): ")
            if save_option.lower() == "s":
                # Salva os resultados em TXT
                filename = app.salvar_resultados(resultado, "txt")
                print(f"Resultados salvos em: {filename}\n")

            # Pergunta se deseja exportar em JSON
            json_option = input("Deseja exportar os resultados em JSON? (s/n): ")
            if json_option.lower() == "s":
                # Salva os resultados em JSON
                json_filename = app.salvar_resultados(resultado, "json")
                print(f"Resultados exportados em JSON: {json_filename}\n")

        except Exception as e:
            print(f"\nErro ao buscar ebooks: {str(e)}\n")

    print("\nObrigado por utilizar a aplicação de Busca de Ebooks!")


if __name__ == "__main__":
    # Executa a função principal
    asyncio.run(main())
