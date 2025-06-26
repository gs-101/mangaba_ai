"""Testes de performance para o Mangaba.AI"""

import asyncio
import time
import pytest
from concurrent.futures import ThreadPoolExecutor

from mangaba_ai.core.agent import Agent
from mangaba_ai.core.mcp import MCP
from mangaba_ai.schemas.message import Message


class TestPerformance:
    """Testes de performance para componentes do Mangaba.AI"""

    @pytest.mark.asyncio
    async def test_agent_processing_speed(self):
        """Testa a velocidade de processamento do agente"""
        agent = Agent()
        message = Message(
            content="Teste de velocidade",
            sender="speed_tester",
            timestamp="1234567890"
        )
        
        start_time = time.time()
        
        # Processa 100 mensagens
        tasks = []
        for i in range(100):
            task = agent.process_message(message)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Verifica se processou todas as mensagens
        assert len(results) == 100
        assert all(result["processed"] for result in results)
        
        # Verifica se o tempo de processamento é razoável (menos de 5 segundos)
        assert processing_time < 5.0
        
        # Calcula mensagens por segundo
        messages_per_second = 100 / processing_time
        print(f"\nProcessamento: {messages_per_second:.2f} mensagens/segundo")
        
        # Deve processar pelo menos 20 mensagens por segundo
        assert messages_per_second > 20

    @pytest.mark.asyncio
    async def test_mcp_analysis_speed(self):
        """Testa a velocidade de análise do MCP"""
        mcp = MCP()
        
        # Cria uma conversa com 50 mensagens
        messages = []
        for i in range(50):
            messages.append(Message(
                content=f"Mensagem de teste {i}",
                sender=f"user{i % 5}",
                timestamp=str(1234567890 + i)
            ))
        
        start_time = time.time()
        
        result = await mcp.analyze_conversation(messages)
        
        end_time = time.time()
        analysis_time = end_time - start_time
        
        # Verifica se a análise foi concluída corretamente
        assert result.message_count == 50
        assert result.participants == 5
        
        # Verifica se o tempo de análise é razoável (menos de 3 segundos)
        assert analysis_time < 3.0
        
        print(f"\nAnálise de 50 mensagens: {analysis_time:.2f} segundos")

    @pytest.mark.asyncio
    async def test_concurrent_processing(self):
        """Testa processamento concorrente de múltiplos agentes"""
        num_agents = 5
        messages_per_agent = 20
        
        agents = [Agent() for _ in range(num_agents)]
        
        start_time = time.time()
        
        # Cria tarefas para cada agente processar suas mensagens
        all_tasks = []
        for i, agent in enumerate(agents):
            for j in range(messages_per_agent):
                message = Message(
                    content=f"Mensagem {j} do agente {i}",
                    sender=f"user{i}_{j}",
                    timestamp=str(1234567890 + i * 100 + j)
                )
                task = agent.process_message(message)
                all_tasks.append(task)
        
        # Executa todas as tarefas concorrentemente
        results = await asyncio.gather(*all_tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verifica se todas as mensagens foram processadas
        total_messages = num_agents * messages_per_agent
        assert len(results) == total_messages
        assert all(result["processed"] for result in results)
        
        # Verifica se o processamento concorrente é eficiente
        assert total_time < 10.0
        
        throughput = total_messages / total_time
        print(f"\nThroughput concorrente: {throughput:.2f} mensagens/segundo")
        
        # Deve processar pelo menos 10 mensagens por segundo
        assert throughput > 10

    @pytest.mark.asyncio
    async def test_memory_usage_stability(self):
        """Testa se o uso de memória permanece estável durante processamento intenso"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        agent = Agent()
        mcp = MCP()
        
        # Processa muitas mensagens em lotes
        for batch in range(10):
            messages = []
            for i in range(100):
                messages.append(Message(
                    content=f"Batch {batch}, mensagem {i}",
                    sender=f"user{i % 10}",
                    timestamp=str(1234567890 + batch * 1000 + i)
                ))
            
            # Processa o lote
            await mcp.analyze_conversation(messages)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"\nMemória inicial: {initial_memory:.2f} MB")
        print(f"Memória final: {final_memory:.2f} MB")
        print(f"Aumento de memória: {memory_increase:.2f} MB")
        
        # O aumento de memória deve ser razoável (menos de 50 MB)
        assert memory_increase < 50

    @pytest.mark.asyncio
    async def test_scalability_with_large_conversations(self):
        """Testa escalabilidade com conversas muito grandes"""
        mcp = MCP()
        
        # Testa com diferentes tamanhos de conversa
        conversation_sizes = [10, 50, 100, 500]
        
        for size in conversation_sizes:
            messages = []
            for i in range(size):
                messages.append(Message(
                    content=f"Mensagem {i} de {size}",
                    sender=f"user{i % 20}",  # 20 participantes diferentes
                    timestamp=str(1234567890 + i)
                ))
            
            start_time = time.time()
            result = await mcp.analyze_conversation(messages)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            # Verifica se a análise foi bem-sucedida
            assert result.message_count == size
            assert result.participants <= 20
            
            # O tempo deve crescer de forma linear, não exponencial
            time_per_message = processing_time / size
            
            print(f"\n{size} mensagens: {processing_time:.3f}s ({time_per_message:.4f}s por mensagem)")
            
            # Cada mensagem deve ser processada em menos de 0.1 segundos
            assert time_per_message < 0.1

    def test_agent_initialization_speed(self):
        """Testa a velocidade de inicialização de agentes"""
        start_time = time.time()
        
        # Cria 100 agentes
        agents = []
        for i in range(100):
            agent = Agent()
            agents.append(agent)
        
        end_time = time.time()
        initialization_time = end_time - start_time
        
        # Verifica se todos os agentes foram criados
        assert len(agents) == 100
        assert all(agent.name == "Mangaba.AI Agent" for agent in agents)
        
        # A inicialização deve ser rápida (menos de 1 segundo)
        assert initialization_time < 1.0
        
        # Evita divisão por zero
        if initialization_time > 0:
            agents_per_second = 100 / initialization_time
            print(f"\nInicialização: {agents_per_second:.2f} agentes/segundo")
            
            # Deve criar pelo menos 100 agentes por segundo
            assert agents_per_second > 100
        else:
            print("\nInicialização instantânea (< 0.001s)")
            # Se foi instantâneo, considera como passou no teste