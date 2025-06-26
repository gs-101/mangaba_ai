#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de busca usando múltiplos agentes do Mangaba AI

Este script demonstra como utilizar múltiplos agentes do Mangaba AI
para realizar buscas e análises de ebooks de forma colaborativa.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# Adiciona o diretório pai ao path para importar o módulo mangaba_ai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importa os componentes necessários do Mangaba AI
try:
    from mangaba_ai.core.models import Agent, GeminiModel, Task
    from mangaba_ai.main import MangabaAI
except ImportError:
    try:
        from src.mangaba_ai.core.models import Agent, GeminiModel, Task
        from src.mangaba_ai.main import MangabaAI
    except ImportError:
        # Usa a versão de compatibilidade se necessário
        from compat.models import Agent, GeminiModel, Task

        # Cria uma classe MangabaAI simulada se necessário
        class MangabaAI:
            def __init__(self):
                pass


# Importa a função get_model_implementation para compatibilidade
try:
    from compat import get_model_implementation
except ImportError:
    # Define uma função simulada se não for possível importar
    def get_model_implementation(model_name):
        return GeminiModel


# Classe para representar mensagens entre agentes
class Message:
    def __init__(
        self,
        content: str,
        role: str = "user",
        sender: str = None,
        timestamp: datetime = None,
    ):
        self.content = content
        self.role = role
        self.sender = sender
        self.timestamp = timestamp or datetime.now()


# Classe para representar resultados de análise
class AnalysisResult:
    def __init__(self, content: str, score: float = 0.0):
        self.content = content
        self.score = score


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

    async def search_ebook(self, query: str) -> List[Dict[str, str]]:
        """
        Busca o ebook nas fontes disponíveis.

        Args:
            query: Nome do ebook a ser buscado

        Returns:
            Lista de dicionários contendo informações sobre os ebooks encontrados
        """
        print(f"Agente '{self.name}' buscando ebook: {query}")

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

    async def process_message(self, message: Message) -> Dict[str, Any]:
        """
        Processa a mensagem contendo o nome do ebook a ser buscado.

        Args:
            message: Objeto Message contendo o nome do ebook

        Returns:
            Dicionário com os resultados da busca
        """
        query = message.content.strip()
        results = await self.search_ebook(query)

        # Armazena os resultados na memória do agente
        self.memory[query] = {
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": message.timestamp,
            "processed": True,
        }

        return {
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": message.timestamp,
            "processed": True,
        }


class AnalisadorEbookAgent(Agent):
    """
    Agente especializado em análise de resultados de busca de ebooks.
    """

    def __init__(self):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Analisador Ebook Agent",
            role="Especialista em análise de ebooks",
            goal="Analisar e classificar resultados de busca de ebooks",
        )
        self.version = "1.0.0"
        self.memory = {}

        # Tenta obter a implementação do modelo
        try:
            ModelClass = get_model_implementation("GeminiModel")
            self.model = ModelClass(
                {"api_keys": {"gemini": ""}, "models": {"gemini": {}}}
            )
        except Exception as e:
            print(f"Aviso: Não foi possível inicializar o modelo: {e}")
            self.model = None

    async def analyze_results(
        self, results: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Analisa os resultados da busca de ebooks.

        Args:
            results: Lista de resultados da busca

        Returns:
            Lista de resultados analisados
        """
        print(f"Agente '{self.name}' analisando {len(results)} resultados")

        analyzed_results = []
        for result in results:
            # Simula uma análise baseada em critérios simples
            relevance_score = 0.5 + (0.3 if "Completo" in result["title"] else 0)
            quality_score = 0.6 + (0.2 if result["format"] == "PDF" else 0)
            popularity_score = (
                0.7
                if "libgen" in result["source"] or "b-ok" in result["source"]
                else 0.4
            )

            # Calcula a pontuação final
            final_score = (relevance_score + quality_score + popularity_score) / 3

            # Adiciona a análise ao resultado
            analyzed_result = result.copy()
            analyzed_result["relevance_score"] = round(relevance_score, 2)
            analyzed_result["quality_score"] = round(quality_score, 2)
            analyzed_result["popularity_score"] = round(popularity_score, 2)
            analyzed_result["final_score"] = round(final_score, 2)

            analyzed_results.append(analyzed_result)

        # Ordena os resultados por pontuação final
        analyzed_results.sort(key=lambda x: x["final_score"], reverse=True)

        # Simula um pequeno atraso na análise
        await asyncio.sleep(0.3)

        return analyzed_results

    async def process_message(self, message: Message) -> Dict[str, Any]:
        """
        Processa a mensagem contendo os resultados da busca.

        Args:
            message: Objeto Message contendo os resultados da busca

        Returns:
            Dicionário com os resultados analisados
        """
        try:
            # Tenta converter o conteúdo da mensagem em um dicionário
            if isinstance(message.content, str):
                data = json.loads(message.content)
            else:
                data = message.content

            query = data.get("query", "")
            results = data.get("results", [])

            # Analisa os resultados
            analyzed_results = await self.analyze_results(results)

            # Armazena os resultados na memória do agente
            self.memory[query] = {
                "query": query,
                "results": analyzed_results,
                "count": len(analyzed_results),
                "timestamp": message.timestamp,
                "processed": True,
            }

            return {
                "query": query,
                "results": analyzed_results,
                "count": len(analyzed_results),
                "timestamp": message.timestamp,
                "processed": True,
            }
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            return {"error": str(e), "processed": False}


class RecomendadorEbookAgent(Agent):
    """
    Agente especializado em recomendações de ebooks.
    """

    def __init__(self):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Recomendador Ebook Agent",
            role="Especialista em recomendações de ebooks",
            goal="Recomendar os melhores ebooks com base nos resultados analisados",
        )
        self.version = "1.0.0"
        self.memory = {}
        self.user_preferences = {}

    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """
        Define as preferências do usuário.

        Args:
            user_id: ID do usuário
            preferences: Dicionário com as preferências do usuário
        """
        self.user_preferences[user_id] = preferences

    async def generate_recommendations(
        self, user_id: str, analyzed_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Gera recomendações com base nos resultados analisados e nas preferências do usuário.

        Args:
            user_id: ID do usuário
            analyzed_results: Lista de resultados analisados

        Returns:
            Lista de recomendações
        """
        print(f"Agente '{self.name}' gerando recomendações para o usuário {user_id}")

        # Obtém as preferências do usuário ou usa padrões
        preferences = self.user_preferences.get(
            user_id, {"format_preference": "PDF", "min_score": 0.6}
        )

        # Filtra os resultados com base nas preferências
        recommendations = []
        for result in analyzed_results:
            # Verifica se o resultado atende aos critérios mínimos
            if result["final_score"] >= preferences.get("min_score", 0.6):
                # Adiciona um bônus para o formato preferido
                if result["format"] == preferences.get("format_preference"):
                    result["recommendation_score"] = result["final_score"] + 0.1
                else:
                    result["recommendation_score"] = result["final_score"]

                # Adiciona uma justificativa para a recomendação
                if result["recommendation_score"] > 0.8:
                    result["recommendation_reason"] = (
                        "Excelente correspondência com sua busca"
                    )
                elif result["recommendation_score"] > 0.7:
                    result["recommendation_reason"] = "Boa opção para sua busca"
                else:
                    result["recommendation_reason"] = "Opção razoável para sua busca"

                recommendations.append(result)

        # Ordena as recomendações por pontuação
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)

        # Limita a 5 recomendações
        recommendations = recommendations[:5]

        # Simula um pequeno atraso na geração de recomendações
        await asyncio.sleep(0.2)

        return recommendations

    async def process_message(self, message: Message) -> Dict[str, Any]:
        """
        Processa a mensagem contendo os resultados analisados.

        Args:
            message: Objeto Message contendo os resultados analisados

        Returns:
            Dicionário com as recomendações
        """
        try:
            # Tenta converter o conteúdo da mensagem em um dicionário
            if isinstance(message.content, str):
                data = json.loads(message.content)
            else:
                data = message.content

            query = data.get("query", "")
            results = data.get("results", [])
            user_id = message.sender or "default_user"

            # Gera recomendações
            recommendations = await self.generate_recommendations(user_id, results)

            # Armazena as recomendações na memória do agente
            self.memory[query] = {
                "query": query,
                "recommendations": recommendations,
                "count": len(recommendations),
                "timestamp": message.timestamp,
                "user_id": user_id,
                "processed": True,
            }

            return {
                "query": query,
                "recommendations": recommendations,
                "count": len(recommendations),
                "timestamp": message.timestamp,
                "user_id": user_id,
                "processed": True,
            }
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            return {"error": str(e), "processed": False}


class BuscaMultiAgentesApp:
    """
    Aplicação de busca de ebooks usando múltiplos agentes do Mangaba AI.
    """

    def __init__(self):
        """
        Inicializa a aplicação.
        """
        self.mangaba = MangabaAI()
        self.busca_agent = BuscaEbookAgent()
        self.analisador_agent = AnalisadorEbookAgent()
        self.recomendador_agent = RecomendadorEbookAgent()

        # Define preferências padrão para o usuário
        self.recomendador_agent.set_user_preferences(
            "default_user", {"format_preference": "PDF", "min_score": 0.6}
        )

    async def buscar_e_recomendar(
        self, ebook_name: str, user_id: str = "default_user"
    ) -> Dict[str, Any]:
        """
        Realiza a busca, análise e recomendação de ebooks.

        Args:
            ebook_name: Nome do ebook a ser buscado
            user_id: ID do usuário

        Returns:
            Dicionário com os resultados do processo
        """
        # Cria uma mensagem para o agente de busca
        busca_message = Message(
            content=ebook_name, sender=user_id, timestamp=datetime.now()
        )

        # Etapa 1: Busca de ebooks
        print("\nEtapa 1: Buscando ebooks...")
        busca_results = await self.busca_agent.process_message(busca_message)

        # Etapa 2: Análise dos resultados
        print("\nEtapa 2: Analisando resultados...")
        analise_message = Message(
            content=busca_results, sender=user_id, timestamp=datetime.now()
        )
        analise_results = await self.analisador_agent.process_message(analise_message)

        # Etapa 3: Geração de recomendações
        print("\nEtapa 3: Gerando recomendações...")
        recomendacao_message = Message(
            content=analise_results, sender=user_id, timestamp=datetime.now()
        )
        recomendacao_results = await self.recomendador_agent.process_message(
            recomendacao_message
        )

        # Combina os resultados
        return {
            "query": ebook_name,
            "busca": busca_results,
            "analise": analise_results,
            "recomendacao": recomendacao_results,
            "timestamp": datetime.now().isoformat(),
        }

    def format_recommendations(self, results: Dict[str, Any]) -> str:
        """
        Formata as recomendações para exibição.

        Args:
            results: Dicionário com os resultados do processo

        Returns:
            String formatada com as recomendações
        """
        recomendacoes = results["recomendacao"]["recommendations"]
        query = results["query"]

        output = f"Recomendações para '{query}'\n"
        output += f"Encontramos {results['busca']['count']} resultados e selecionamos as {len(recomendacoes)} melhores opções para você.\n\n"

        for i, rec in enumerate(recomendacoes, 1):
            output += f"{i}. {rec['title']}\n"
            output += f"   Autor: {rec['author']}\n"
            output += f"   Formato: {rec['format']} | Tamanho: {rec['size']}\n"
            output += f"   Fonte: {rec['source']}\n"
            output += f"   Pontuação: {rec['recommendation_score']:.2f} - {rec['recommendation_reason']}\n"
            output += f"   Link: {rec['download_url']}\n\n"

        return output

    def salvar_resultados(
        self, resultados: Dict[str, Any], formato: str = "txt"
    ) -> str:
        """
        Salva os resultados em um arquivo.

        Args:
            resultados: Dicionário com os resultados do processo
            formato: Formato do arquivo (txt ou json)

        Returns:
            Caminho do arquivo salvo
        """
        # Cria o diretório de resultados se não existir
        results_dir = "resultados"
        os.makedirs(results_dir, exist_ok=True)

        # Define o nome do arquivo
        query = resultados["query"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if formato.lower() == "json":
            # Salva em formato JSON
            filename = os.path.join(
                results_dir, f"recomendacao_{query.replace(' ', '_')}_{timestamp}.json"
            )
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False)
        else:
            # Salva em formato TXT
            filename = os.path.join(
                results_dir, f"recomendacao_{query.replace(' ', '_')}_{timestamp}.txt"
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.format_recommendations(resultados))

        return filename


async def main():
    """
    Função principal para demonstração da aplicação.
    """
    # Inicializa a aplicação
    app = BuscaMultiAgentesApp()

    print("===== Busca de Ebooks com Múltiplos Agentes do Mangaba AI =====\n")
    print("Esta aplicação utiliza três agentes especializados:")
    print("1. Agente de Busca: Encontra ebooks em diversas fontes")
    print("2. Agente de Análise: Avalia a qualidade e relevância dos resultados")
    print("3. Agente de Recomendação: Seleciona os melhores ebooks para você\n")

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
            # Realiza o processo completo
            print(f"\nIniciando processo para '{ebook_name}'...")
            start_time = datetime.now()
            resultados = await app.buscar_e_recomendar(ebook_name)
            end_time = datetime.now()

            # Calcula o tempo total
            total_time = (end_time - start_time).total_seconds()

            # Exibe as recomendações formatadas
            print("\n" + app.format_recommendations(resultados))
            print(f"Processo concluído em {total_time:.2f} segundos.\n")

            # Pergunta se deseja salvar os resultados
            save_option = input("Deseja salvar as recomendações? (s/n): ")
            if save_option.lower() == "s":
                # Salva os resultados em TXT
                filename = app.salvar_resultados(resultados, "txt")
                print(f"Recomendações salvas em: {filename}\n")

            # Pergunta se deseja exportar em JSON
            json_option = input(
                "Deseja exportar os resultados completos em JSON? (s/n): "
            )
            if json_option.lower() == "s":
                # Salva os resultados em JSON
                json_filename = app.salvar_resultados(resultados, "json")
                print(f"Resultados exportados em JSON: {json_filename}\n")

        except Exception as e:
            print(f"\nErro durante o processo: {str(e)}\n")

    print("\nObrigado por utilizar a aplicação de Busca de Ebooks!")


if __name__ == "__main__":
    # Executa a função principal
    asyncio.run(main())
