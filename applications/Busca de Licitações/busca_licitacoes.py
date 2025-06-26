#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema multi-agente para busca de licitações de inteligência artificial

Este script utiliza o framework Mangaba.AI para criar um sistema multi-agente
que busca, analisa e recomenda licitações relacionadas à inteligência artificial.
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
    from mangaba_ai.core.models import Agent, Task
    from mangaba_ai.main import MangabaAI

    try:
        from mangaba_ai.tools import GoogleSearchTool
    except ImportError:
        # Define uma classe simulada se não for possível importar
        class GoogleSearchTool:
            async def search(self, query, num_results=5):
                print(f"Simulando busca por: {query}")
                return [
                    f"Resultado {i} para {query}" for i in range(1, num_results + 1)
                ]

except ImportError:
    try:
        from src.mangaba_ai.core.models import Agent, Task
        from src.mangaba_ai.main import MangabaAI

        # Tenta importar a ferramenta de busca
        try:
            from src.mangaba_ai.tools import GoogleSearchTool
        except ImportError:
            # Define uma classe simulada se não for possível importar
            class GoogleSearchTool:
                async def search(self, query, num_results=5):
                    print(f"Simulando busca por: {query}")
                    return [
                        f"Resultado {i} para {query}" for i in range(1, num_results + 1)
                    ]

    except ImportError:
        # Define classes simuladas para execução independente
        class Agent:
            def __init__(self, name, role, goal, model=None):
                self.name = name
                self.role = role
                self.goal = goal
                self.model = model
                self.memory = []

            async def execute(self, task):
                print(f"Agente '{self.name}' executando: {task}")
                return f"Resultado da execução de '{task}' pelo agente {self.name}"

        class Task:
            def __init__(self, description, agent, context=None):
                self.description = description
                self.agent = agent
                self.context = context or {}

            async def execute(self):
                return await self.agent.execute(self.description)

        # Define uma classe MangabaAI simulada
        class MangabaAI:
            def __init__(self):
                pass

            def create_agent(self, name, role, goal, tools=None):
                return Agent(name, role, goal)

            def create_task(self, description, agent, context=None, dependencies=None):
                return Task(description, agent, context)

            async def execute(self, tasks):
                results = {}
                for task in tasks:
                    results[task.description] = await task.execute()
                return results

        # Define uma classe GoogleSearchTool simulada
        class GoogleSearchTool:
            async def search(self, query, num_results=5):
                print(f"Simulando busca por: {query}")
                return [
                    f"Resultado {i} para {query}" for i in range(1, num_results + 1)
                ]


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


class BuscaLicitacoesAgent(Agent):
    """
    Agente especializado em busca de licitações.
    """

    def __init__(self, search_tool=None):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Busca Licitações Agent",
            role="Especialista em busca de licitações",
            goal="Encontrar licitações relacionadas à inteligência artificial",
        )
        self.version = "1.0.0"
        self.search_tool = search_tool
        self.sources = [
            "https://www.gov.br/compras/pt-br/acesso-a-informacao/consulta-detalhada",
            "https://www.licitacoes-e.com.br",
            "https://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacoes_Lista.asp",
            "https://www.comprasgovernamentais.gov.br/index.php/comprasnet-siasg",
            "https://www.portaldecompraspublicas.com.br/18/",
        ]
        self.memory = {}

    async def search_licitacoes(self, query: str) -> List[Dict[str, str]]:
        """
        Busca licitações nas fontes disponíveis.

        Args:
            query: Termos de busca para licitações

        Returns:
            Lista de dicionários contendo informações sobre as licitações encontradas
        """
        print(f"Agente '{self.name}' buscando licitações: {query}")

        results = []

        # Usa a ferramenta de busca do Google se disponível
        if self.search_tool:
            search_queries = [
                f"licitação inteligência artificial {query}",
                f"edital inteligência artificial {query}",
                f"pregão eletrônico IA {query}",
                f"compras governamentais inteligência artificial {query}",
            ]

            for search_query in search_queries:
                try:
                    # Tenta chamar o método search sem o parâmetro num_results
                    # já que o GoogleSearchTool real não parece aceitar esse parâmetro
                    search_results = await self.search_tool.search(search_query)
                    # Limita os resultados manualmente
                    search_results = (
                        search_results[:3]
                        if len(search_results) > 3
                        else search_results
                    )

                    for result in search_results:
                        # Simula a extração de informações da licitação
                        licitacao = {
                            "titulo": f"Licitação de {query} - {result[:30]}...",
                            "orgao": self._extract_orgao(result),
                            "modalidade": self._extract_modalidade(result),
                            "valor_estimado": self._extract_valor(result),
                            "data_abertura": self._extract_data(result),
                            "objeto": self._extract_objeto(result),
                            "url": self._extract_url(result),
                            "fonte": "Google Search",
                        }
                        results.append(licitacao)
                except Exception as e:
                    print(f"Erro na busca por '{search_query}': {e}")
                    # Continua com a próxima consulta

        # Simula a busca em fontes específicas de licitações
        for source in self.sources:
            try:
                # Simula 1-2 resultados por fonte
                for i in range(1, 3):
                    # Usa um hash simples para gerar resultados consistentes
                    if i == 1 or hash(source + query) % 2 == 0:
                        result = {
                            "titulo": f"Licitação de {query} - {'Nacional' if i == 1 else 'Estadual'}",
                            "orgao": f"{'Ministério' if i == 1 else 'Secretaria'} de {'Ciência e Tecnologia' if i % 2 == 0 else 'Educação'}",
                            "modalidade": (
                                "Pregão Eletrônico" if i % 2 == 0 else "Concorrência"
                            ),
                            "valor_estimado": f"R$ {(i * 500000) + (hash(source) % 100000):.2f}",
                            "data_abertura": self._generate_date(source, query),
                            "objeto": f"Contratação de serviços de {query} para {'desenvolvimento' if i % 2 == 0 else 'implementação'} de soluções de inteligência artificial",
                            "url": f"{source}?q={query.replace(' ', '+')}&id={hash(source + query) % 1000}",
                            "fonte": source.split("/")[2],
                        }
                        results.append(result)
            except Exception as e:
                print(f"Erro na busca em {source}: {e}")

        # Simula um pequeno atraso na busca
        await asyncio.sleep(0.5)

        return results

    def _extract_orgao(self, result):
        """Extrai o órgão da licitação do resultado da busca."""
        # Simulação de extração
        if "ministerio" in result.lower() or "ministério" in result.lower():
            return "Ministério da Ciência, Tecnologia e Inovações"
        elif "secretaria" in result.lower():
            return "Secretaria de Inovação Digital"
        elif "universidade" in result.lower():
            return "Universidade Federal"
        elif "prefeitura" in result.lower():
            return "Prefeitura Municipal"
        else:
            return "Órgão Governamental"

    def _extract_modalidade(self, result):
        """Extrai a modalidade da licitação do resultado da busca."""
        # Simulação de extração
        if "pregão" in result.lower() or "pregao" in result.lower():
            return "Pregão Eletrônico"
        elif "concorrência" in result.lower() or "concorrencia" in result.lower():
            return "Concorrência"
        elif "tomada de preço" in result.lower() or "tomada de preco" in result.lower():
            return "Tomada de Preços"
        else:
            return "Modalidade não identificada"

    def _extract_valor(self, result):
        """Extrai o valor estimado da licitação do resultado da busca."""
        # Simulação de extração
        import random

        valor_base = random.randint(100000, 5000000)
        return f"R$ {valor_base:.2f}"

    def _extract_data(self, result):
        """Extrai a data de abertura da licitação do resultado da busca."""
        # Simulação de extração
        import random
        from datetime import datetime, timedelta

        dias_futuros = random.randint(5, 60)
        data_abertura = datetime.now() + timedelta(days=dias_futuros)
        return data_abertura.strftime("%d/%m/%Y")

    def _extract_objeto(self, result):
        """Extrai o objeto da licitação do resultado da busca."""
        # Simulação de extração
        if len(result) > 100:
            return result[:100] + "..."
        else:
            return result

    def _extract_url(self, result):
        """Extrai a URL da licitação do resultado da busca."""
        # Simulação de extração
        if "http" in result:
            start = result.find("http")
            end = result.find(" ", start)
            if end == -1:
                end = len(result)
            return result[start:end]
        else:
            return "URL não disponível"

    def _generate_date(self, source, query):
        """Gera uma data de abertura simulada para a licitação."""
        import random
        from datetime import datetime, timedelta

        # Usa um hash para gerar datas consistentes
        hash_value = hash(source + query) % 60
        data_abertura = datetime.now() + timedelta(days=hash_value)
        return data_abertura.strftime("%d/%m/%Y")

    async def process_message(self, message: Message) -> Dict[str, Any]:
        """
        Processa a mensagem contendo os termos de busca para licitações.

        Args:
            message: Objeto Message contendo os termos de busca

        Returns:
            Dicionário com os resultados da busca
        """
        query = message.content.strip()
        results = await self.search_licitacoes(query)

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


class AnalisadorLicitacoesAgent(Agent):
    """
    Agente especializado em análise de resultados de busca de licitações.
    """

    def __init__(self):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Analisador Licitações Agent",
            role="Especialista em análise de licitações",
            goal="Analisar e classificar resultados de busca de licitações",
        )
        self.version = "1.0.0"
        self.memory = {}

    async def analyze_results(
        self, results: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Analisa os resultados da busca de licitações.

        Args:
            results: Lista de resultados da busca

        Returns:
            Lista de resultados analisados
        """
        print(f"Agente '{self.name}' analisando {len(results)} resultados")

        analyzed_results = []
        for result in results:
            # Analisa com base em critérios específicos para licitações
            relevance_score = self._calculate_relevance(result)
            opportunity_score = self._calculate_opportunity(result)
            viability_score = self._calculate_viability(result)

            # Calcula a pontuação final
            final_score = (relevance_score + opportunity_score + viability_score) / 3

            # Adiciona a análise ao resultado
            analyzed_result = result.copy()
            analyzed_result["relevance_score"] = round(relevance_score, 2)
            analyzed_result["opportunity_score"] = round(opportunity_score, 2)
            analyzed_result["viability_score"] = round(viability_score, 2)
            analyzed_result["final_score"] = round(final_score, 2)

            analyzed_results.append(analyzed_result)

        # Ordena os resultados por pontuação final
        analyzed_results.sort(key=lambda x: x["final_score"], reverse=True)

        # Simula um pequeno atraso na análise
        await asyncio.sleep(0.3)

        return analyzed_results

    def _calculate_relevance(self, result: Dict[str, str]) -> float:
        """
        Calcula a pontuação de relevância da licitação.

        Args:
            result: Dicionário com informações da licitação

        Returns:
            Pontuação de relevância (0.0 a 1.0)
        """
        relevance = 0.5  # Base score

        # Verifica se o título ou objeto contém termos relevantes
        relevant_terms = [
            "inteligência artificial",
            "ia",
            "machine learning",
            "aprendizado de máquina",
            "deep learning",
            "processamento de linguagem natural",
            "nlp",
            "visão computacional",
        ]

        for term in relevant_terms:
            if (
                term in result.get("titulo", "").lower()
                or term in result.get("objeto", "").lower()
            ):
                relevance += 0.1
                if relevance > 1.0:
                    relevance = 1.0
                    break

        return relevance

    def _calculate_opportunity(self, result: Dict[str, str]) -> float:
        """
        Calcula a pontuação de oportunidade da licitação.

        Args:
            result: Dicionário com informações da licitação

        Returns:
            Pontuação de oportunidade (0.0 a 1.0)
        """
        opportunity = 0.5  # Base score

        # Verifica o valor estimado
        valor_str = result.get("valor_estimado", "R$ 0,00")
        try:
            # Extrai o valor numérico
            valor = float(
                valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
            )

            # Avalia com base no valor
            if valor > 1000000:  # Mais de 1 milhão
                opportunity += 0.3
            elif valor > 500000:  # Mais de 500 mil
                opportunity += 0.2
            elif valor > 100000:  # Mais de 100 mil
                opportunity += 0.1
        except:
            pass

        # Verifica a data de abertura
        try:
            from datetime import datetime

            data_str = result.get("data_abertura", "01/01/2000")
            data_abertura = datetime.strptime(data_str, "%d/%m/%Y")
            dias_ate_abertura = (data_abertura - datetime.now()).days

            # Avalia com base no tempo disponível
            if 15 <= dias_ate_abertura <= 30:  # Tempo ideal
                opportunity += 0.2
            elif 7 <= dias_ate_abertura < 15:  # Tempo curto
                opportunity += 0.1
            elif dias_ate_abertura > 30:  # Tempo longo
                opportunity += 0.05
        except:
            pass

        # Limita a pontuação máxima
        if opportunity > 1.0:
            opportunity = 1.0

        return opportunity

    def _calculate_viability(self, result: Dict[str, str]) -> float:
        """
        Calcula a pontuação de viabilidade da licitação.

        Args:
            result: Dicionário com informações da licitação

        Returns:
            Pontuação de viabilidade (0.0 a 1.0)
        """
        viability = 0.5  # Base score

        # Verifica a modalidade
        modalidade = result.get("modalidade", "").lower()
        if "pregão eletrônico" in modalidade or "pregao eletronico" in modalidade:
            viability += 0.2  # Pregão eletrônico é mais acessível
        elif "concorrência" in modalidade or "concorrencia" in modalidade:
            viability += 0.1

        # Verifica o órgão
        orgao = result.get("orgao", "").lower()
        if "federal" in orgao or "ministério" in orgao or "ministerio" in orgao:
            viability += (
                0.1  # Órgãos federais geralmente têm processos mais padronizados
            )

        # Verifica a fonte
        fonte = result.get("fonte", "").lower()
        if "comprasnet" in fonte or "gov.br" in fonte:
            viability += 0.1  # Fontes oficiais são mais confiáveis

        # Limita a pontuação máxima
        if viability > 1.0:
            viability = 1.0

        return viability

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


class RecomendadorLicitacoesAgent(Agent):
    """
    Agente especializado em recomendações de licitações.
    """

    def __init__(self):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Recomendador Licitações Agent",
            role="Especialista em recomendações de licitações",
            goal="Recomendar as melhores licitações com base nos resultados analisados",
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
            user_id,
            {
                "min_score": 0.5,  # Reduzido para permitir mais resultados
                "max_recommendations": 5,
                "valor_maximo": 5000000,
                "modalidade_preferida": "Pregão Eletrônico",
            },
        )

        # Filtra os resultados com base nas preferências
        recommendations = []
        for result in analyzed_results:
            # Adiciona um bônus para a modalidade preferida
            if result.get("modalidade") == preferences.get("modalidade_preferida"):
                result["recommendation_score"] = result.get("final_score", 0.5) + 0.1
            else:
                result["recommendation_score"] = result.get("final_score", 0.5)

            # Verifica o valor máximo
            valor_str = result.get("valor_estimado", "R$ 0,00")
            try:
                valor = float(
                    valor_str.replace("R$", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
                if valor > preferences.get("valor_maximo", float("inf")):
                    continue  # Pula esta licitação se exceder o valor máximo
            except:
                pass

            # Adiciona uma justificativa para a recomendação
            if result["recommendation_score"] > 0.8:
                result["recommendation_reason"] = "Excelente oportunidade de licitação"
            elif result["recommendation_score"] > 0.7:
                result["recommendation_reason"] = "Boa oportunidade de licitação"
            elif result["recommendation_score"] > 0.6:
                result["recommendation_reason"] = "Oportunidade razoável de licitação"
            else:
                result["recommendation_reason"] = "Oportunidade potencial de licitação"

            # Adiciona uma análise estratégica
            result["strategic_analysis"] = self._generate_strategic_analysis(result)

            recommendations.append(result)

        # Ordena as recomendações por pontuação
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)

        # Limita ao número máximo de recomendações
        max_recommendations = preferences.get("max_recommendations", 5)
        recommendations = recommendations[:max_recommendations]

        # Simula um pequeno atraso na geração de recomendações
        await asyncio.sleep(0.2)

        return recommendations

    def _generate_strategic_analysis(self, result: Dict[str, Any]) -> str:
        """
        Gera uma análise estratégica para a licitação.

        Args:
            result: Dicionário com informações da licitação

        Returns:
            String com a análise estratégica
        """
        analysis = "Análise estratégica: "

        # Analisa com base na pontuação
        if result["final_score"] > 0.8:
            analysis += "Esta é uma licitação de alta prioridade. "
        elif result["final_score"] > 0.6:
            analysis += "Esta é uma licitação de média prioridade. "
        else:
            analysis += "Esta é uma licitação de baixa prioridade. "

        # Analisa com base no valor
        valor_str = result.get("valor_estimado", "R$ 0,00")
        try:
            valor = float(
                valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
            )
            if valor > 1000000:
                analysis += "O valor é significativo, o que pode exigir uma proposta mais elaborada. "
            elif valor > 500000:
                analysis += "O valor é moderado, adequado para uma proposta padrão. "
            else:
                analysis += "O valor é relativamente baixo, adequado para uma proposta simplificada. "
        except:
            pass

        # Analisa com base na data de abertura
        try:
            from datetime import datetime

            data_str = result.get("data_abertura", "01/01/2000")
            data_abertura = datetime.strptime(data_str, "%d/%m/%Y")
            dias_ate_abertura = (data_abertura - datetime.now()).days

            if dias_ate_abertura < 7:
                analysis += "O prazo é muito curto, recomenda-se ação imediata. "
            elif dias_ate_abertura < 15:
                analysis += (
                    "O prazo é curto, recomenda-se iniciar a preparação em breve. "
                )
            elif dias_ate_abertura < 30:
                analysis += "O prazo é adequado para uma preparação completa. "
            else:
                analysis += "O prazo é longo, permitindo uma preparação detalhada. "
        except:
            pass

        # Adiciona recomendações específicas
        analysis += "Recomenda-se "
        if "federal" in result.get("orgao", "").lower():
            analysis += "atenção especial aos requisitos de habilitação federal. "
        elif "estadual" in result.get("orgao", "").lower():
            analysis += "verificar requisitos específicos do estado. "
        elif "municipal" in result.get("orgao", "").lower():
            analysis += "verificar requisitos específicos do município. "
        else:
            analysis += "verificar cuidadosamente os requisitos de habilitação. "

        return analysis

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


class BuscaLicitacoesApp:
    """
    Aplicação de busca de licitações usando múltiplos agentes do Mangaba AI.
    """

    def __init__(self):
        """
        Inicializa a aplicação.
        """
        self.mangaba = MangabaAI()

        # Cria ferramenta de busca
        self.search_tool = GoogleSearchTool()

        # Cria os agentes especializados
        self.busca_agent = BuscaLicitacoesAgent(self.search_tool)
        self.analisador_agent = AnalisadorLicitacoesAgent()
        self.recomendador_agent = RecomendadorLicitacoesAgent()

        # Define preferências padrão para o usuário
        self.recomendador_agent.set_user_preferences(
            "default_user",
            {
                "min_score": 0.6,
                "max_recommendations": 5,
                "valor_maximo": 5000000,
                "modalidade_preferida": "Pregão Eletrônico",
            },
        )

    async def buscar_e_recomendar(
        self, termos_busca: str, user_id: str = "default_user"
    ) -> Dict[str, Any]:
        """
        Realiza a busca, análise e recomendação de licitações.

        Args:
            termos_busca: Termos para busca de licitações
            user_id: ID do usuário

        Returns:
            Dicionário com os resultados do processo
        """
        # Cria uma mensagem para o agente de busca
        busca_message = Message(
            content=termos_busca, sender=user_id, timestamp=datetime.now()
        )

        # Etapa 1: Busca de licitações
        print("\nEtapa 1: Buscando licitações...")
        busca_results = await self.busca_agent.process_message(busca_message)
        print(
            f"Resultados da busca: {len(busca_results.get('results', []))} licitações encontradas"
        )

        # Etapa 2: Análise dos resultados
        print("\nEtapa 2: Analisando resultados...")
        analise_message = Message(
            content=busca_results, sender=user_id, timestamp=datetime.now()
        )
        analise_results = await self.analisador_agent.process_message(analise_message)
        print(
            f"Resultados da análise: {len(analise_results.get('results', []))} licitações analisadas"
        )

        # Etapa 3: Geração de recomendações
        print("\nEtapa 3: Gerando recomendações...")
        recomendacao_message = Message(
            content=analise_results, sender=user_id, timestamp=datetime.now()
        )
        recomendacao_results = await self.recomendador_agent.process_message(
            recomendacao_message
        )
        print(
            f"Resultados da recomendação: {len(recomendacao_results.get('recommendations', []))} licitações recomendadas"
        )

        # Combina os resultados
        resultados = {
            "query": termos_busca,
            "busca": busca_results,
            "analise": analise_results,
            "recomendacao": recomendacao_results,
            "timestamp": datetime.now().isoformat(),
        }

        return resultados

    def format_recommendations(self, results: Dict[str, Any]) -> str:
        """
        Formata as recomendações para exibição.

        Args:
            results: Dicionário com os resultados do processo

        Returns:
            String formatada com as recomendações
        """
        query = results["query"]

        # Verifica se há recomendações disponíveis
        if (
            "recomendacao" not in results
            or "recommendations" not in results["recomendacao"]
            or not results["recomendacao"]["recommendations"]
        ):
            output = f"Recomendações de Licitações para '{query}'\n"
            output += f"Encontramos {results.get('busca', {}).get('count', 0)} licitações, mas nenhuma atende aos critérios mínimos.\n\n"
            output += (
                "Tente ajustar os termos de busca ou os critérios de recomendação.\n"
            )
            return output

        recomendacoes = results["recomendacao"]["recommendations"]

        output = f"Recomendações de Licitações para '{query}'\n"
        output += f"Encontramos {results.get('busca', {}).get('count', 0)} licitações e selecionamos as {len(recomendacoes)} melhores oportunidades.\n\n"

        for i, rec in enumerate(recomendacoes, 1):
            output += f"{i}. {rec['titulo']}\n"
            output += f"   Órgão: {rec['orgao']}\n"
            output += f"   Modalidade: {rec['modalidade']} | Valor Estimado: {rec['valor_estimado']}\n"
            output += f"   Data de Abertura: {rec['data_abertura']}\n"
            output += f"   Objeto: {rec['objeto']}\n"
            output += f"   Pontuação: {rec['recommendation_score']:.2f} - {rec['recommendation_reason']}\n"
            output += f"   {rec['strategic_analysis']}\n"
            output += f"   Fonte: {rec['fonte']}\n"
            output += f"   Link: {rec['url']}\n\n"

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
                results_dir, f"licitacoes_{query.replace(' ', '_')}_{timestamp}.json"
            )

            # Define um encoder personalizado para lidar com objetos datetime
            class DateTimeEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, datetime):
                        return obj.strftime("%Y-%m-%d %H:%M:%S")
                    return super().default(obj)

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    resultados, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder
                )
        else:
            # Salva em formato TXT
            filename = os.path.join(
                results_dir, f"licitacoes_{query.replace(' ', '_')}_{timestamp}.txt"
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.format_recommendations(resultados))

        return filename


async def main():
    """
    Função principal para demonstração da aplicação.
    """
    # Inicializa a aplicação
    app = BuscaLicitacoesApp()

    print("===== Busca de Licitações de IA com Múltiplos Agentes do Mangaba AI =====\n")
    print("Esta aplicação utiliza três agentes especializados:")
    print(
        "1. Agente de Busca: Encontra licitações relacionadas à inteligência artificial"
    )
    print("2. Agente de Análise: Avalia a relevância e viabilidade das licitações")
    print("3. Agente de Recomendação: Seleciona as melhores oportunidades\n")

    print("Digite os termos para busca de licitações ou 'sair' para encerrar.\n")

    while True:
        # Solicita entrada do usuário
        termos_busca = input("Termos de busca: ")

        # Verifica se o usuário deseja sair
        if termos_busca.lower() == "sair":
            print("\nEncerrando a aplicação...")
            break

        # Verifica se a entrada é válida
        if not termos_busca.strip():
            print("\nPor favor, digite termos válidos.\n")
            continue

        try:
            # Realiza o processo completo
            print(f"\nIniciando processo para '{termos_busca}'...")
            start_time = datetime.now()
            resultados = await app.buscar_e_recomendar(termos_busca)
            end_time = datetime.now()

            # Calcula o tempo total
            total_time = (end_time - start_time).total_seconds()

            # Verifica se há resultados para exibir
            if (
                "recomendacao" in resultados
                and "recommendations" in resultados["recomendacao"]
            ):
                print(
                    f"\nForam encontradas {len(resultados['recomendacao']['recommendations'])} recomendações."
                )
            else:
                print("\nNenhuma recomendação foi encontrada.")

            # Exibe as recomendações formatadas
            formatted_recommendations = app.format_recommendations(resultados)
            print("\n" + formatted_recommendations)
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

    print("\nObrigado por utilizar a aplicação de Busca de Licitações!")


if __name__ == "__main__":
    # Executa a função principal
    asyncio.run(main())
