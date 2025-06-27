#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Comunicação A2A (Agent-to-Agent) com Mangaba Agent
Demonstra como agentes podem se comunicar entre si
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangaba_agent import MangabaAgent
from protocols.a2a import MessageType
import time

def create_specialized_agents():
    """Cria agentes especializados para diferentes tarefas"""
    
    # Agente Analista
    analyst = MangabaAgent(agent_id="analyst_001")
    analyst.role = "Analista de Dados"
    
    # Agente Tradutor
    translator = MangabaAgent(agent_id="translator_001")
    translator.role = "Especialista em Tradução"
    
    # Agente Coordenador
    coordinator = MangabaAgent(agent_id="coordinator_001")
    coordinator.role = "Coordenador de Projetos"
    
    return analyst, translator, coordinator

def demo_request_response():
    """Demonstra comunicação de requisição e resposta"""
    print("🤝 Comunicação Requisição-Resposta")
    print("=" * 50)
    
    analyst, translator, coordinator = create_specialized_agents()
    
    # Coordenador solicita análise ao analista
    print(f"📋 {coordinator.role} solicita análise...")
    
    request_data = {
        "task": "analyze_sales_data",
        "data": "Vendas Q1: 150k, Q2: 180k, Q3: 165k, Q4: 200k",
        "priority": "high"
    }
    
    response = coordinator.send_agent_request(
        analyst.agent_id, 
        "analyze", 
        request_data
    )
    
    print(f"📊 Resposta do {analyst.role}:")
    print(f"   {response}")
    
    # Coordenador solicita tradução
    print(f"\n🌍 {coordinator.role} solicita tradução...")
    
    translation_request = {
        "text": "Sales increased by 33% compared to last year",
        "target_language": "português",
        "context": "business_report"
    }
    
    translation_response = coordinator.send_agent_request(
        translator.agent_id,
        "translate",
        translation_request
    )
    
    print(f"🔄 Resposta do {translator.role}:")
    print(f"   {translation_response}")

def demo_broadcast():
    """Demonstra comunicação por broadcast"""
    print("\n📢 Comunicação por Broadcast")
    print("=" * 50)
    
    analyst, translator, coordinator = create_specialized_agents()
    
    # Lista de agentes para simular rede
    agents = [analyst, translator, coordinator]
    
    # Coordenador envia broadcast
    broadcast_message = {
        "type": "system_update",
        "message": "Sistema será atualizado às 02:00. Salvem o trabalho.",
        "priority": "urgent",
        "timestamp": time.time()
    }
    
    print(f"📡 {coordinator.role} enviando broadcast...")
    coordinator.broadcast_message("system_notification", broadcast_message)
    
    # Simula recebimento pelos outros agentes
    for agent in [analyst, translator]:
        print(f"📨 {agent.role} recebeu: {broadcast_message['message']}")

def demo_collaborative_task():
    """Demonstra tarefa colaborativa entre agentes"""
    print("\n👥 Tarefa Colaborativa")
    print("=" * 50)
    
    analyst, translator, coordinator = create_specialized_agents()
    
    # Cenário: Relatório multilíngue
    print("📋 Cenário: Criação de relatório multilíngue")
    
    # 1. Coordenador define a tarefa
    task_data = {
        "project": "quarterly_report",
        "languages": ["português", "inglês", "espanhol"],
        "deadline": "2024-01-15"
    }
    
    print(f"\n1️⃣ {coordinator.role} define tarefa:")
    print(f"   Projeto: {task_data['project']}")
    print(f"   Idiomas: {', '.join(task_data['languages'])}")
    
    # 2. Analista processa dados
    analysis_request = {
        "data_source": "sales_database",
        "period": "Q4_2023",
        "metrics": ["revenue", "growth", "market_share"]
    }
    
    print(f"\n2️⃣ {coordinator.role} → {analyst.role}:")
    analysis_result = coordinator.send_agent_request(
        analyst.agent_id,
        "generate_analysis",
        analysis_request
    )
    print(f"   📊 Análise: {analysis_result}")
    
    # 3. Tradutor cria versões multilíngues
    for language in task_data['languages'][1:]:  # Pula português (original)
        print(f"\n3️⃣ {coordinator.role} → {translator.role} ({language}):")
        
        translation_request = {
            "content": analysis_result,
            "target_language": language,
            "document_type": "business_report"
        }
        
        translated_result = coordinator.send_agent_request(
            translator.agent_id,
            "translate_document",
            translation_request
        )
        
        print(f"   🌍 Versão em {language}: {translated_result}")
    
    # 4. Coordenador finaliza
    print(f"\n4️⃣ {coordinator.role} finaliza projeto:")
    print("   ✅ Relatório multilíngue concluído com sucesso!")

def demo_agent_discovery():
    """Demonstra descoberta e registro de agentes"""
    print("\n🔍 Descoberta de Agentes")
    print("=" * 50)
    
    # Cria agentes especializados
    agents = {
        "data_scientist": MangabaAgent(agent_id="ds_001"),
        "content_writer": MangabaAgent(agent_id="cw_001"),
        "quality_assurance": MangabaAgent(agent_id="qa_001"),
        "project_manager": MangabaAgent(agent_id="pm_001")
    }
    
    # Define especialidades
    specialties = {
        "data_scientist": "Análise de dados, ML, estatística",
        "content_writer": "Redação, copywriting, SEO",
        "quality_assurance": "Testes, validação, controle de qualidade",
        "project_manager": "Coordenação, planejamento, gestão"
    }
    
    print("🤖 Agentes disponíveis na rede:")
    for role, agent in agents.items():
        print(f"   • {agent.agent_id} - {specialties[role]}")
    
    # Simula busca por especialista
    print("\n🔎 Buscando especialista em 'análise de dados'...")
    
    # Project manager procura data scientist
    pm = agents["project_manager"]
    ds = agents["data_scientist"]
    
    discovery_request = {
        "skill_required": "data_analysis",
        "urgency": "medium",
        "project_context": "customer_segmentation"
    }
    
    print(f"📞 {pm.agent_id} encontrou {ds.agent_id}")
    
    collaboration_response = pm.send_agent_request(
        ds.agent_id,
        "collaborate",
        discovery_request
    )
    
    print(f"🤝 Resposta: {collaboration_response}")

def main():
    """Executa todos os exemplos de comunicação A2A"""
    print("🤖 Mangaba Agent - Exemplos de Comunicação A2A")
    print("=" * 60)
    
    try:
        demo_request_response()
        demo_broadcast()
        demo_collaborative_task()
        demo_agent_discovery()
        
        print("\n✅ Todos os exemplos de comunicação A2A foram executados!")
        print("\n💡 Dicas:")
        print("   • Agentes mantêm contexto das conversas")
        print("   • Comunicação é assíncrona e escalável")
        print("   • Suporte a diferentes tipos de mensagens")
        
    except Exception as e:
        print(f"❌ Erro durante comunicação A2A: {e}")

if __name__ == "__main__":
    main()