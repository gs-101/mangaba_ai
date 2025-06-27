#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Gerenciamento de Contexto MCP com Mangaba Agent
Demonstra como usar o Model Context Protocol para memória avançada
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangaba_agent import MangabaAgent
from protocols.mcp import ContextType, ContextPriority
import time

def demo_conversation_memory():
    """Demonstra memória de conversação"""
    print("🧠 Memória de Conversação")
    print("=" * 50)
    
    agent = MangabaAgent()
    
    # Simulação de conversa com memória
    conversation_steps = [
        "Meu nome é João e trabalho como desenvolvedor.",
        "Estou trabalhando em um projeto de IA.",
        "O projeto usa Python e TensorFlow.",
        "Qual é o meu nome mesmo?",
        "Em que projeto estou trabalhando?",
        "Quais tecnologias estou usando?"
    ]
    
    print("💬 Iniciando conversa com memória...\n")
    
    for i, message in enumerate(conversation_steps, 1):
        print(f"👤 Usuário: {message}")
        
        # Chat com contexto habilitado
        response = agent.chat(message, use_context=True)
        print(f"🤖 Agente: {response}")
        
        # Mostra resumo do contexto a cada 3 mensagens
        if i % 3 == 0:
            context_summary = agent.get_context_summary()
            print(f"\n📋 Contexto atual: {context_summary['total_contexts']} contextos")
            print(f"   Tipos: {', '.join(context_summary['context_types'])}")
        
        print("-" * 40)
        time.sleep(0.5)  # Pausa para simular conversa natural

def demo_task_context():
    """Demonstra contexto de tarefas"""
    print("\n📋 Contexto de Tarefas")
    print("=" * 50)
    
    agent = MangabaAgent()
    
    # Simula diferentes tarefas com contexto
    tasks = [
        {
            "type": "analysis",
            "description": "Analisar dados de vendas do último trimestre",
            "data": "Q1: 150k, Q2: 180k, Q3: 165k",
            "priority": ContextPriority.HIGH
        },
        {
            "type": "translation",
            "description": "Traduzir relatório para inglês",
            "content": "Relatório de vendas mostra crescimento de 10%",
            "priority": ContextPriority.MEDIUM
        },
        {
            "type": "summary",
            "description": "Resumir informações do projeto",
            "context": "Projeto de IA com foco em análise preditiva",
            "priority": ContextPriority.LOW
        }
    ]
    
    print("🎯 Executando tarefas com contexto...\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"📌 Tarefa {i}: {task['description']}")
        
        if task['type'] == 'analysis':
            result = agent.analyze_text(
                task['data'], 
                "Analise estes dados de vendas e identifique tendências"
            )
        elif task['type'] == 'translation':
            result = agent.translate(
                task['content'],
                "Traduza para inglês mantendo o contexto empresarial"
            )
        else:
            result = agent.chat(
                f"Resuma: {task['context']}",
                use_context=True
            )
        
        print(f"✅ Resultado: {result}")
        print(f"🏷️ Prioridade: {task['priority'].name}")
        print("-" * 40)

def demo_knowledge_base():
    """Demonstra base de conhecimento com MCP"""
    print("\n📚 Base de Conhecimento")
    print("=" * 50)
    
    agent = MangabaAgent()
    
    # Adiciona conhecimento à base
    knowledge_items = [
        {
            "topic": "Python",
            "info": "Linguagem de programação interpretada, orientada a objetos",
            "tags": ["programming", "language", "python"]
        },
        {
            "topic": "Machine Learning",
            "info": "Subcampo da IA que permite sistemas aprenderem automaticamente",
            "tags": ["ai", "ml", "learning"]
        },
        {
            "topic": "TensorFlow",
            "info": "Biblioteca open-source para machine learning desenvolvida pelo Google",
            "tags": ["tensorflow", "google", "ml", "library"]
        }
    ]
    
    print("📖 Adicionando conhecimento à base...\n")
    
    # Adiciona cada item como contexto de conhecimento
    for item in knowledge_items:
        # Simula adição através de chat
        knowledge_message = f"Lembre-se: {item['topic']} - {item['info']}"
        agent.chat(knowledge_message, use_context=True)
        print(f"✅ Adicionado: {item['topic']}")
    
    print("\n🔍 Testando recuperação de conhecimento...\n")
    
    # Testa consultas que devem usar o conhecimento armazenado
    queries = [
        "O que é Python?",
        "Explique Machine Learning",
        "Quem desenvolveu o TensorFlow?",
        "Qual a relação entre Python e ML?"
    ]
    
    for query in queries:
        print(f"❓ Pergunta: {query}")
        response = agent.chat(query, use_context=True)
        print(f"💡 Resposta: {response}")
        print("-" * 30)

def demo_context_priorities():
    """Demonstra diferentes prioridades de contexto"""
    print("\n⭐ Prioridades de Contexto")
    print("=" * 50)
    
    agent = MangabaAgent()
    
    # Adiciona contextos com diferentes prioridades
    priority_examples = [
        {
            "message": "URGENTE: Sistema fora do ar!",
            "priority": "CRITICAL",
            "description": "Informação crítica do sistema"
        },
        {
            "message": "Reunião marcada para amanhã às 14h",
            "priority": "HIGH",
            "description": "Compromisso importante"
        },
        {
            "message": "Lembrar de atualizar documentação",
            "priority": "MEDIUM",
            "description": "Tarefa de manutenção"
        },
        {
            "message": "Café da manhã foi bom hoje",
            "priority": "LOW",
            "description": "Informação casual"
        }
    ]
    
    print("📊 Adicionando contextos com diferentes prioridades...\n")
    
    for item in priority_examples:
        # Simula diferentes tipos de entrada
        agent.chat(item['message'], use_context=True)
        print(f"{item['priority']:>8}: {item['message']}")
        print(f"         ({item['description']})")
    
    print("\n🎯 Testando recuperação baseada em prioridade...")
    
    # Pergunta que deve priorizar contextos mais importantes
    response = agent.chat("O que há de mais importante acontecendo?", use_context=True)
    print(f"\n🔍 Resposta (deve priorizar contextos críticos/altos): {response}")
    
    # Mostra resumo final
    summary = agent.get_context_summary()
    print(f"\n📈 Resumo final:")
    print(f"   Total de contextos: {summary['total_contexts']}")
    print(f"   Tipos: {', '.join(summary['context_types'])}")
    if 'priority_distribution' in summary:
        print(f"   Distribuição de prioridades: {summary['priority_distribution']}")

def demo_context_expiration():
    """Demonstra expiração de contextos"""
    print("\n⏰ Expiração de Contextos")
    print("=" * 50)
    
    agent = MangabaAgent()
    
    print("🕐 Adicionando contextos com diferentes tempos de vida...\n")
    
    # Simula contextos temporários vs permanentes
    temporary_info = [
        "Reunião cancelada para hoje",
        "Servidor em manutenção por 1 hora",
        "Promoção válida até amanhã"
    ]
    
    permanent_info = [
        "Meu nome é João Silva",
        "Trabalho como desenvolvedor Python",
        "Empresa: TechCorp Brasil"
    ]
    
    # Adiciona informações temporárias
    print("⏳ Informações temporárias:")
    for info in temporary_info:
        agent.chat(f"TEMPORÁRIO: {info}", use_context=True)
        print(f"   • {info}")
    
    # Adiciona informações permanentes
    print("\n♾️ Informações permanentes:")
    for info in permanent_info:
        agent.chat(f"PERMANENTE: {info}", use_context=True)
        print(f"   • {info}")
    
    print("\n🔍 Testando recuperação de contexto...")
    
    # Testa diferentes tipos de consulta
    queries = [
        "Qual é o meu nome?",
        "Onde trabalho?",
        "Há alguma reunião hoje?",
        "Algum servidor está em manutenção?"
    ]
    
    for query in queries:
        response = agent.chat(query, use_context=True)
        print(f"❓ {query}")
        print(f"💭 {response}")
        print()

def main():
    """Executa todos os exemplos de contexto MCP"""
    print("🤖 Mangaba Agent - Exemplos de Contexto MCP")
    print("=" * 60)
    
    try:
        demo_conversation_memory()
        demo_task_context()
        demo_knowledge_base()
        demo_context_priorities()
        demo_context_expiration()
        
        print("\n✅ Todos os exemplos de contexto MCP foram executados!")
        print("\n💡 Recursos demonstrados:")
        print("   • Memória de conversação persistente")
        print("   • Contexto de tarefas com prioridades")
        print("   • Base de conhecimento dinâmica")
        print("   • Gerenciamento de prioridades")
        print("   • Expiração automática de contextos")
        
    except Exception as e:
        print(f"❌ Erro durante demonstração MCP: {e}")

if __name__ == "__main__":
    main()