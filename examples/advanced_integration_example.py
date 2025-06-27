#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Avançado de Integração A2A + MCP com Mangaba Agent
Demonstra um sistema completo de agentes colaborativos com memória
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangaba_agent import MangabaAgent
from protocols.mcp import ContextType, ContextPriority
import time
import json

class AgentTeam:
    """Classe para gerenciar uma equipe de agentes especializados"""
    
    def __init__(self):
        self.agents = {}
        self.create_team()
    
    def create_team(self):
        """Cria equipe de agentes especializados"""
        
        # Agente Coordenador Principal
        self.agents['coordinator'] = MangabaAgent(agent_id="coord_master")
        self.agents['coordinator'].role = "Coordenador Principal"
        self.agents['coordinator'].specialties = ["project_management", "coordination", "decision_making"]
        
        # Agente Analista de Dados
        self.agents['data_analyst'] = MangabaAgent(agent_id="analyst_data")
        self.agents['data_analyst'].role = "Analista de Dados"
        self.agents['data_analyst'].specialties = ["data_analysis", "statistics", "reporting"]
        
        # Agente Especialista em Linguagem
        self.agents['linguist'] = MangabaAgent(agent_id="linguist_expert")
        self.agents['linguist'].role = "Especialista em Linguagem"
        self.agents['linguist'].specialties = ["translation", "text_analysis", "content_creation"]
        
        # Agente de Qualidade
        self.agents['qa_specialist'] = MangabaAgent(agent_id="qa_expert")
        self.agents['qa_specialist'].role = "Especialista em Qualidade"
        self.agents['qa_specialist'].specialties = ["quality_assurance", "validation", "testing"]
        
        # Agente de Conhecimento
        self.agents['knowledge_keeper'] = MangabaAgent(agent_id="knowledge_base")
        self.agents['knowledge_keeper'].role = "Guardião do Conhecimento"
        self.agents['knowledge_keeper'].specialties = ["knowledge_management", "research", "documentation"]
    
    def get_agent(self, role):
        """Retorna agente por função"""
        return self.agents.get(role)
    
    def list_agents(self):
        """Lista todos os agentes da equipe"""
        return [(role, agent.role, agent.specialties) for role, agent in self.agents.items()]

def demo_project_workflow():
    """Demonstra fluxo de trabalho completo de projeto"""
    print("🚀 Fluxo de Trabalho de Projeto Completo")
    print("=" * 60)
    
    team = AgentTeam()
    
    # Cenário: Análise de feedback de clientes multilíngue
    project_data = {
        "name": "Customer Feedback Analysis",
        "description": "Analisar feedback de clientes em múltiplos idiomas",
        "data_sources": [
            "Feedback em português: 'Produto excelente, recomendo!'",
            "Feedback em inglês: 'Great product, but delivery was slow'",
            "Feedback em espanhol: 'Calidad buena, precio alto'",
            "Feedback em francês: 'Service client parfait'"
        ],
        "requirements": [
            "Traduzir todos para português",
            "Analisar sentimentos",
            "Gerar relatório executivo",
            "Validar qualidade das análises"
        ]
    }
    
    print(f"📋 Projeto: {project_data['name']}")
    print(f"📝 Descrição: {project_data['description']}")
    print(f"📊 Fontes de dados: {len(project_data['data_sources'])} feedbacks")
    
    coordinator = team.get_agent('coordinator')
    
    # Fase 1: Planejamento e distribuição de tarefas
    print("\n🎯 Fase 1: Planejamento")
    print("-" * 30)
    
    planning_context = {
        "project": project_data['name'],
        "phase": "planning",
        "team_size": len(team.agents),
        "requirements": project_data['requirements']
    }
    
    coordinator.chat(f"Iniciando projeto: {json.dumps(planning_context)}", use_context=True)
    print(f"✅ {coordinator.role} iniciou planejamento")
    
    # Fase 2: Tradução dos feedbacks
    print("\n🌍 Fase 2: Tradução")
    print("-" * 30)
    
    linguist = team.get_agent('linguist')
    translated_feedbacks = []
    
    for i, feedback in enumerate(project_data['data_sources'], 1):
        print(f"📝 Processando feedback {i}: {feedback[:50]}...")
        
        # Coordenador solicita tradução
        translation_request = {
            "task": "translate_feedback",
            "content": feedback,
            "target_language": "português",
            "context": "customer_feedback"
        }
        
        translated = coordinator.send_agent_request(
            linguist.agent_id,
            "translate",
            translation_request
        )
        
        translated_feedbacks.append(translated)
        print(f"🔄 Traduzido: {translated}")
        
        # Adiciona ao contexto do linguista
        linguist.chat(f"Tradução concluída: {feedback} → {translated}", use_context=True)
    
    # Fase 3: Análise de sentimentos
    print("\n😊 Fase 3: Análise de Sentimentos")
    print("-" * 30)
    
    data_analyst = team.get_agent('data_analyst')
    sentiment_results = []
    
    for i, feedback in enumerate(translated_feedbacks, 1):
        print(f"📊 Analisando sentimento {i}...")
        
        analysis_request = {
            "task": "sentiment_analysis",
            "text": feedback,
            "output_format": "structured"
        }
        
        sentiment = coordinator.send_agent_request(
            data_analyst.agent_id,
            "analyze",
            analysis_request
        )
        
        sentiment_results.append(sentiment)
        print(f"📈 Resultado: {sentiment}")
        
        # Adiciona ao contexto do analista
        data_analyst.chat(f"Análise de sentimento: {feedback} = {sentiment}", use_context=True)
    
    # Fase 4: Geração de relatório
    print("\n📄 Fase 4: Geração de Relatório")
    print("-" * 30)
    
    # Coordenador compila informações
    report_data = {
        "original_feedbacks": len(project_data['data_sources']),
        "translated_feedbacks": len(translated_feedbacks),
        "sentiment_analysis": sentiment_results,
        "summary": "Análise completa de feedback multilíngue"
    }
    
    report_request = {
        "task": "generate_executive_report",
        "data": report_data,
        "format": "executive_summary"
    }
    
    executive_report = coordinator.send_agent_request(
        data_analyst.agent_id,
        "generate_report",
        report_request
    )
    
    print(f"📋 Relatório Executivo: {executive_report}")
    
    # Fase 5: Validação de qualidade
    print("\n✅ Fase 5: Validação de Qualidade")
    print("-" * 30)
    
    qa_specialist = team.get_agent('qa_specialist')
    
    qa_request = {
        "task": "quality_validation",
        "deliverables": {
            "translations": translated_feedbacks,
            "analysis": sentiment_results,
            "report": executive_report
        },
        "criteria": ["accuracy", "completeness", "consistency"]
    }
    
    qa_result = coordinator.send_agent_request(
        qa_specialist.agent_id,
        "validate",
        qa_request
    )
    
    print(f"🔍 Validação QA: {qa_result}")
    
    # Fase 6: Armazenamento de conhecimento
    print("\n📚 Fase 6: Armazenamento de Conhecimento")
    print("-" * 30)
    
    knowledge_keeper = team.get_agent('knowledge_keeper')
    
    knowledge_data = {
        "project_name": project_data['name'],
        "methodology": "multilingual_sentiment_analysis",
        "tools_used": ["translation", "sentiment_analysis", "reporting"],
        "lessons_learned": "Integração A2A+MCP permite fluxos complexos",
        "success_metrics": {
            "feedbacks_processed": len(project_data['data_sources']),
            "languages_handled": 4,
            "quality_score": "high"
        }
    }
    
    knowledge_storage = coordinator.send_agent_request(
        knowledge_keeper.agent_id,
        "store_knowledge",
        knowledge_data
    )
    
    print(f"💾 Conhecimento armazenado: {knowledge_storage}")
    
    # Resumo final do projeto
    print("\n🎉 Resumo Final do Projeto")
    print("=" * 40)
    
    # Cada agente fornece seu resumo de contexto
    for role, agent in team.agents.items():
        context_summary = agent.get_context_summary()
        print(f"🤖 {agent.role}:")
        print(f"   Contextos: {context_summary.get('total_contexts', 0)}")
        print(f"   Tipos: {', '.join(context_summary.get('context_types', []))}")
    
    return {
        "project_completed": True,
        "phases_executed": 6,
        "agents_involved": len(team.agents),
        "deliverables": {
            "translations": len(translated_feedbacks),
            "analysis": len(sentiment_results),
            "report": 1,
            "qa_validation": 1,
            "knowledge_base": 1
        }
    }

def demo_real_time_collaboration():
    """Demonstra colaboração em tempo real entre agentes"""
    print("\n⚡ Colaboração em Tempo Real")
    print("=" * 50)
    
    team = AgentTeam()
    
    # Cenário: Resposta a incidente crítico
    incident_data = {
        "type": "system_outage",
        "severity": "critical",
        "description": "API principal fora do ar",
        "impact": "Clientes não conseguem acessar serviços",
        "timestamp": time.time()
    }
    
    print(f"🚨 INCIDENTE CRÍTICO: {incident_data['description']}")
    print(f"⚠️ Impacto: {incident_data['impact']}")
    
    coordinator = team.get_agent('coordinator')
    
    # 1. Coordenador inicia resposta de emergência
    emergency_broadcast = {
        "type": "emergency_response",
        "incident": incident_data,
        "required_actions": [
            "Análise de logs",
            "Comunicação com clientes",
            "Documentação do incidente"
        ],
        "priority": "CRITICAL"
    }
    
    print("\n📢 Coordenador enviando broadcast de emergência...")
    coordinator.broadcast_message("emergency_alert", emergency_broadcast)
    
    # 2. Analista investiga logs
    print("\n🔍 Analista investigando logs...")
    data_analyst = team.get_agent('data_analyst')
    
    log_analysis = coordinator.send_agent_request(
        data_analyst.agent_id,
        "analyze_logs",
        {
            "incident_id": "INC-001",
            "time_range": "last_30_minutes",
            "focus": "api_errors"
        }
    )
    
    print(f"📊 Análise de logs: {log_analysis}")
    
    # 3. Linguista prepara comunicação
    print("\n📝 Linguista preparando comunicação...")
    linguist = team.get_agent('linguist')
    
    communication = coordinator.send_agent_request(
        linguist.agent_id,
        "create_communication",
        {
            "audience": "customers",
            "tone": "professional_apologetic",
            "content": f"Incidente: {incident_data['description']}",
            "languages": ["português", "inglês"]
        }
    )
    
    print(f"📢 Comunicação preparada: {communication}")
    
    # 4. QA valida resposta
    print("\n✅ QA validando resposta...")
    qa_specialist = team.get_agent('qa_specialist')
    
    validation = coordinator.send_agent_request(
        qa_specialist.agent_id,
        "validate_response",
        {
            "incident_response": {
                "analysis": log_analysis,
                "communication": communication
            },
            "criteria": ["accuracy", "completeness", "timeliness"]
        }
    )
    
    print(f"🔍 Validação: {validation}")
    
    # 5. Conhecimento documenta lições aprendidas
    print("\n📚 Documentando lições aprendidas...")
    knowledge_keeper = team.get_agent('knowledge_keeper')
    
    lessons = coordinator.send_agent_request(
        knowledge_keeper.agent_id,
        "document_incident",
        {
            "incident": incident_data,
            "response_time": "5_minutes",
            "team_coordination": "excellent",
            "improvements": "Processo A2A+MCP funcionou perfeitamente"
        }
    )
    
    print(f"📖 Documentação: {lessons}")
    
    print("\n🎯 Incidente resolvido com sucesso usando colaboração A2A+MCP!")

def demo_adaptive_learning():
    """Demonstra aprendizado adaptativo da equipe"""
    print("\n🧠 Aprendizado Adaptativo da Equipe")
    print("=" * 50)
    
    team = AgentTeam()
    
    # Simula múltiplas iterações de aprendizado
    learning_scenarios = [
        {
            "scenario": "Primeira análise de sentimento",
            "feedback": "Análise muito técnica, precisa ser mais acessível",
            "improvement": "Ajustar linguagem para executivos"
        },
        {
            "scenario": "Segunda análise de sentimento",
            "feedback": "Melhor, mas faltam insights acionáveis",
            "improvement": "Incluir recomendações práticas"
        },
        {
            "scenario": "Terceira análise de sentimento",
            "feedback": "Excelente! Formato ideal para tomada de decisão",
            "improvement": "Manter este padrão"
        }
    ]
    
    data_analyst = team.get_agent('data_analyst')
    coordinator = team.get_agent('coordinator')
    
    print("📈 Simulando evolução através de feedback...\n")
    
    for i, scenario in enumerate(learning_scenarios, 1):
        print(f"🔄 Iteração {i}: {scenario['scenario']}")
        
        # Analista executa tarefa
        analysis = data_analyst.chat(
            f"Execute análise considerando feedback anterior: {scenario.get('previous_feedback', 'Primeira execução')}",
            use_context=True
        )
        
        print(f"📊 Análise: {analysis}")
        
        # Feedback é incorporado ao contexto
        feedback_context = {
            "iteration": i,
            "feedback": scenario['feedback'],
            "improvement": scenario['improvement'],
            "analysis_quality": "improving" if i < 3 else "excellent"
        }
        
        data_analyst.chat(
            f"Feedback recebido: {json.dumps(feedback_context)}",
            use_context=True
        )
        
        print(f"💬 Feedback: {scenario['feedback']}")
        print(f"🎯 Melhoria: {scenario['improvement']}")
        print("-" * 40)
    
    # Mostra evolução do contexto
    final_context = data_analyst.get_context_summary()
    print(f"\n🧠 Contexto final do analista:")
    print(f"   Total de contextos: {final_context.get('total_contexts', 0)}")
    print(f"   Aprendizados acumulados: {i} iterações")
    print(f"   Qualidade final: Excelente")

def main():
    """Executa demonstração completa de integração avançada"""
    print("🤖 Mangaba Agent - Integração Avançada A2A + MCP")
    print("=" * 70)
    
    try:
        # Demonstração principal
        project_result = demo_project_workflow()
        
        # Demonstrações complementares
        demo_real_time_collaboration()
        demo_adaptive_learning()
        
        print("\n🎉 DEMONSTRAÇÃO COMPLETA FINALIZADA!")
        print("=" * 50)
        print("\n📊 Resultados da Integração:")
        print(f"   ✅ Projeto concluído: {project_result['project_completed']}")
        print(f"   📋 Fases executadas: {project_result['phases_executed']}")
        print(f"   🤖 Agentes envolvidos: {project_result['agents_involved']}")
        print(f"   📦 Entregáveis: {sum(project_result['deliverables'].values())}")
        
        print("\n🚀 Capacidades Demonstradas:")
        print("   • Coordenação complexa entre múltiplos agentes")
        print("   • Memória persistente e contextual")
        print("   • Fluxos de trabalho adaptativos")
        print("   • Colaboração em tempo real")
        print("   • Aprendizado contínuo")
        print("   • Gestão de qualidade integrada")
        print("   • Base de conhecimento evolutiva")
        
    except Exception as e:
        print(f"❌ Erro durante demonstração avançada: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()