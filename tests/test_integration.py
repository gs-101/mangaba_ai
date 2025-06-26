"""Testes de integração para o Mangaba.AI"""

import asyncio
import pytest
from unittest.mock import Mock, patch

from mangaba_ai.core.agent import Agent
from mangaba_ai.core.mcp import MCP
from mangaba_ai.schemas.message import Message
from mangaba_ai.schemas.analysis import AnalysisResult


class TestIntegration:
    """Testes de integração para componentes do Mangaba.AI"""

    @pytest.mark.asyncio
    async def test_agent_message_processing_workflow(self):
        """Testa o fluxo completo de processamento de mensagens"""
        agent = Agent()
        
        # Testa processamento de mensagem única
        message = Message(
            content="Olá, como você está?",
            sender="user1",
            timestamp="1234567890"
        )
        
        result = await agent.process_message(message)
        
        assert result["content"] == "Olá, como você está?"
        assert result["sender"] == "user1"
        assert result["timestamp"] == "1234567890"
        assert result["processed"] is True

    @pytest.mark.asyncio
    async def test_mcp_conversation_analysis_workflow(self):
        """Testa o fluxo completo de análise de conversas"""
        mcp = MCP()
        
        messages = [
            Message(content="Oi!", sender="Alice", timestamp="1234567890"),
            Message(content="Olá Alice!", sender="Bob", timestamp="1234567891"),
            Message(content="Como vai?", sender="Alice", timestamp="1234567892"),
            Message(content="Tudo bem, e você?", sender="Bob", timestamp="1234567893")
        ]
        
        result = await mcp.analyze_conversation(messages)
        
        assert isinstance(result, AnalysisResult)
        assert result.message_count == 4
        assert result.participants == 2
        assert "Total de mensagens: 4" in result.summary
        assert "Participantes: 2" in result.summary
        assert len(result.processed_messages) == 4

    @pytest.mark.asyncio
    async def test_multiple_agents_processing(self):
        """Testa o processamento com múltiplos agentes"""
        agent1 = Agent()
        agent2 = Agent()
        
        message = Message(
            content="Teste de múltiplos agentes",
            sender="tester",
            timestamp="1234567890"
        )
        
        # Processa a mesma mensagem com dois agentes diferentes
        result1 = await agent1.process_message(message)
        result2 = await agent2.process_message(message)
        
        # Ambos devem processar corretamente
        assert result1["processed"] is True
        assert result2["processed"] is True
        assert result1["content"] == result2["content"]

    @pytest.mark.asyncio
    async def test_empty_conversation_analysis(self):
        """Testa análise de conversa vazia"""
        mcp = MCP()
        
        result = await mcp.analyze_conversation([])
        
        assert result.message_count == 0
        assert result.participants == 0
        assert "Nenhuma mensagem encontrada" in result.summary
        assert len(result.processed_messages) == 0

    @pytest.mark.asyncio
    async def test_large_conversation_analysis(self):
        """Testa análise de conversa com muitas mensagens"""
        mcp = MCP()
        
        # Cria uma conversa com 100 mensagens de 10 participantes diferentes
        messages = []
        for i in range(100):
            messages.append(Message(
                content=f"Mensagem {i}",
                sender=f"user{i % 10}",
                timestamp=str(1234567890 + i)
            ))
        
        result = await mcp.analyze_conversation(messages)
        
        assert isinstance(result, AnalysisResult)
        assert result.message_count == 100
        assert result.participants == 10
        assert "Total de mensagens: 100" in result.summary
        assert "Participantes: 10" in result.summary
        assert len(result.processed_messages) == 100

    def test_message_creation_with_metadata(self):
        """Testa criação de mensagem com metadata"""
        metadata = {"platform": "slack", "channel": "#general"}
        
        message = Message(
            content="Teste com metadata",
            sender="user1",
            timestamp="1234567890",
            metadata=metadata
        )
        
        assert message.content == "Teste com metadata"
        assert message.sender == "user1"
        assert message.timestamp == "1234567890"
        assert message.metadata == metadata
        assert message.metadata["platform"] == "slack"
        assert message.metadata["channel"] == "#general"

    def test_analysis_result_creation(self):
        """Testa criação de resultado de análise"""
        processed_messages = [
            {"content": "msg1", "sender": "user1", "processed": True},
            {"content": "msg2", "sender": "user2", "processed": True}
        ]
        
        result = AnalysisResult(
            summary="Resumo da conversa",
            message_count=2,
            participants=2,
            processed_messages=processed_messages
        )
        
        assert result.summary == "Resumo da conversa"
        assert result.message_count == 2
        assert result.participants == 2
        assert len(result.processed_messages) == 2
        assert result.processed_messages[0]["content"] == "msg1"
        assert result.processed_messages[1]["content"] == "msg2"