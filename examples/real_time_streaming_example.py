#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Processamento de Dados em Tempo Real com Mangaba Agent
Demonstra streaming de dados, processamento assíncrono e análise contínua
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangaba_agent import MangabaAgent
from protocols.mcp import ContextType, ContextPriority
import time
import json
import random
from datetime import datetime, timedelta
import threading
from queue import Queue

class DataStream:
    """Simulador de stream de dados em tempo real"""
    
    def __init__(self, stream_type="sensor_data"):
        self.stream_type = stream_type
        self.is_active = False
        self.data_queue = Queue()
        self.subscribers = []
        self.thread = None
    
    def subscribe(self, callback):
        """Adiciona subscriber ao stream"""
        self.subscribers.append(callback)
    
    def start_stream(self, duration=30):
        """Inicia stream de dados"""
        self.is_active = True
        self.thread = threading.Thread(
            target=self._generate_data,
            args=(duration,)
        )
        self.thread.start()
    
    def stop_stream(self):
        """Para stream de dados"""
        self.is_active = False
        if self.thread:
            self.thread.join()
    
    def _generate_data(self, duration):
        """Gera dados simulados"""
        start_time = time.time()
        
        while self.is_active and (time.time() - start_time) < duration:
            data = self._create_sample_data()
            
            # Notifica todos os subscribers
            for callback in self.subscribers:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Erro no subscriber: {e}")
            
            time.sleep(random.uniform(0.5, 2.0))  # Intervalo variável
    
    def _create_sample_data(self):
        """Cria dados de exemplo baseados no tipo de stream"""
        timestamp = datetime.now().isoformat()
        
        if self.stream_type == "sensor_data":
            return {
                "timestamp": timestamp,
                "sensor_id": f"SENSOR_{random.randint(1, 10):03d}",
                "temperature": round(random.uniform(18.0, 35.0), 2),
                "humidity": round(random.uniform(30.0, 80.0), 2),
                "pressure": round(random.uniform(980.0, 1020.0), 2),
                "status": random.choice(["normal", "warning", "critical"])
            }
        
        elif self.stream_type == "user_activity":
            return {
                "timestamp": timestamp,
                "user_id": f"USER_{random.randint(1000, 9999)}",
                "action": random.choice(["login", "logout", "view_page", "purchase", "search"]),
                "page": random.choice(["/home", "/products", "/cart", "/profile", "/help"]),
                "duration": random.randint(10, 300),
                "device": random.choice(["mobile", "desktop", "tablet"])
            }
        
        elif self.stream_type == "financial_data":
            return {
                "timestamp": timestamp,
                "symbol": random.choice(["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]),
                "price": round(random.uniform(100.0, 500.0), 2),
                "volume": random.randint(1000, 100000),
                "change": round(random.uniform(-5.0, 5.0), 2),
                "market": "NASDAQ"
            }
        
        else:
            return {
                "timestamp": timestamp,
                "type": self.stream_type,
                "value": random.uniform(0, 100),
                "metadata": {"source": "simulator"}
            }

class StreamProcessor:
    """Processador de streams com Mangaba Agent"""
    
    def __init__(self, agent_id, specialization):
        self.agent = MangabaAgent(agent_id=agent_id)
        self.specialization = specialization
        self.processed_count = 0
        self.alerts_generated = 0
        self.buffer = []
        self.buffer_size = 10
    
    def process_data_point(self, data):
        """Processa um ponto de dados individual"""
        self.processed_count += 1
        self.buffer.append(data)
        
        # Mantém buffer limitado
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
        
        # Análise individual
        analysis = self._analyze_single_point(data)
        
        # Análise de tendência (se buffer suficiente)
        if len(self.buffer) >= 5:
            trend_analysis = self._analyze_trend()
            analysis.update(trend_analysis)
        
        # Adiciona ao contexto do agente
        context_data = {
            "data_point": data,
            "analysis": analysis,
            "buffer_size": len(self.buffer),
            "processed_total": self.processed_count
        }
        
        self.agent.chat(
            f"Processando dados em tempo real: {json.dumps(context_data)}",
            use_context=True
        )
        
        return analysis
    
    def _analyze_single_point(self, data):
        """Analisa um ponto de dados individual"""
        analysis = {
            "timestamp": data.get("timestamp"),
            "data_type": type(data).__name__,
            "anomalies": [],
            "alerts": [],
            "metrics": {}
        }
        
        if self.specialization == "sensor_monitoring":
            # Análise de sensores
            temp = data.get("temperature", 0)
            humidity = data.get("humidity", 0)
            status = data.get("status", "normal")
            
            analysis["metrics"] = {
                "temperature_zone": "hot" if temp > 30 else "normal" if temp > 20 else "cold",
                "humidity_level": "high" if humidity > 70 else "normal" if humidity > 40 else "low",
                "sensor_status": status
            }
            
            # Detecta anomalias
            if temp > 32 or temp < 15:
                analysis["anomalies"].append(f"Temperature out of range: {temp}°C")
            
            if humidity > 75 or humidity < 30:
                analysis["anomalies"].append(f"Humidity out of range: {humidity}%")
            
            if status == "critical":
                analysis["alerts"].append("CRITICAL: Sensor status critical")
                self.alerts_generated += 1
        
        elif self.specialization == "user_behavior":
            # Análise de comportamento do usuário
            action = data.get("action", "")
            duration = data.get("duration", 0)
            device = data.get("device", "")
            
            analysis["metrics"] = {
                "action_type": action,
                "engagement_level": "high" if duration > 180 else "medium" if duration > 60 else "low",
                "device_category": device
            }
            
            # Detecta padrões suspeitos
            if action == "login" and duration < 5:
                analysis["anomalies"].append("Suspicious quick login")
            
            if duration > 250:
                analysis["alerts"].append("High engagement detected")
        
        elif self.specialization == "financial_analysis":
            # Análise financeira
            price = data.get("price", 0)
            change = data.get("change", 0)
            volume = data.get("volume", 0)
            
            analysis["metrics"] = {
                "price_movement": "up" if change > 0 else "down" if change < 0 else "stable",
                "volatility": "high" if abs(change) > 3 else "medium" if abs(change) > 1 else "low",
                "volume_level": "high" if volume > 50000 else "normal"
            }
            
            # Detecta movimentos significativos
            if abs(change) > 4:
                analysis["anomalies"].append(f"Significant price movement: {change}%")
            
            if volume > 80000:
                analysis["alerts"].append("High volume trading detected")
                self.alerts_generated += 1
        
        return analysis
    
    def _analyze_trend(self):
        """Analisa tendências no buffer"""
        if len(self.buffer) < 3:
            return {"trend": "insufficient_data"}
        
        trend_analysis = {
            "trend": "stable",
            "pattern": "normal",
            "confidence": 0.5
        }
        
        if self.specialization == "sensor_monitoring":
            # Análise de tendência de temperatura
            temps = [point.get("temperature", 0) for point in self.buffer[-5:]]
            if len(temps) >= 3:
                if all(temps[i] > temps[i-1] for i in range(1, len(temps))):
                    trend_analysis["trend"] = "increasing"
                    trend_analysis["confidence"] = 0.8
                elif all(temps[i] < temps[i-1] for i in range(1, len(temps))):
                    trend_analysis["trend"] = "decreasing"
                    trend_analysis["confidence"] = 0.8
        
        elif self.specialization == "financial_analysis":
            # Análise de tendência de preços
            prices = [point.get("price", 0) for point in self.buffer[-5:]]
            if len(prices) >= 3:
                changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
                avg_change = sum(changes) / len(changes)
                
                if avg_change > 1:
                    trend_analysis["trend"] = "bullish"
                    trend_analysis["confidence"] = min(0.9, abs(avg_change) / 5)
                elif avg_change < -1:
                    trend_analysis["trend"] = "bearish"
                    trend_analysis["confidence"] = min(0.9, abs(avg_change) / 5)
        
        return trend_analysis
    
    def get_statistics(self):
        """Retorna estatísticas do processamento"""
        return {
            "processed_count": self.processed_count,
            "alerts_generated": self.alerts_generated,
            "buffer_size": len(self.buffer),
            "specialization": self.specialization,
            "agent_id": self.agent.agent_id
        }

def demo_sensor_monitoring():
    """Demonstra monitoramento de sensores em tempo real"""
    print("🌡️ Monitoramento de Sensores em Tempo Real")
    print("=" * 60)
    
    # Cria stream de dados de sensores
    sensor_stream = DataStream("sensor_data")
    
    # Cria processador especializado
    processor = StreamProcessor("sensor_monitor_01", "sensor_monitoring")
    
    # Conecta processador ao stream
    sensor_stream.subscribe(processor.process_data_point)
    
    print("🚀 Iniciando stream de dados de sensores...")
    print("📊 Processando dados por 15 segundos...\n")
    
    # Inicia stream
    sensor_stream.start_stream(duration=15)
    
    # Aguarda processamento
    time.sleep(16)
    
    # Para stream
    sensor_stream.stop_stream()
    
    # Mostra estatísticas
    stats = processor.get_statistics()
    print("\n📈 Estatísticas do Monitoramento:")
    print(f"   Dados processados: {stats['processed_count']}")
    print(f"   Alertas gerados: {stats['alerts_generated']}")
    print(f"   Buffer atual: {stats['buffer_size']} pontos")
    
    # Mostra contexto acumulado
    context_summary = processor.agent.get_context_summary()
    print(f"\n🧠 Contexto do Agente:")
    print(f"   Total de contextos: {context_summary.get('total_contexts', 0)}")
    print(f"   Tipos de contexto: {', '.join(context_summary.get('context_types', []))}")
    
    return stats

def demo_user_behavior_analysis():
    """Demonstra análise de comportamento de usuário"""
    print("\n👥 Análise de Comportamento de Usuário")
    print("=" * 60)
    
    # Cria stream de atividade de usuário
    user_stream = DataStream("user_activity")
    
    # Cria processador especializado
    processor = StreamProcessor("behavior_analyst_01", "user_behavior")
    
    # Conecta processador ao stream
    user_stream.subscribe(processor.process_data_point)
    
    print("🚀 Iniciando stream de atividade de usuários...")
    print("📊 Analisando comportamento por 15 segundos...\n")
    
    # Inicia stream
    user_stream.start_stream(duration=15)
    
    # Aguarda processamento
    time.sleep(16)
    
    # Para stream
    user_stream.stop_stream()
    
    # Mostra estatísticas
    stats = processor.get_statistics()
    print("\n📈 Estatísticas da Análise:")
    print(f"   Atividades processadas: {stats['processed_count']}")
    print(f"   Padrões detectados: {stats['alerts_generated']}")
    print(f"   Buffer de análise: {stats['buffer_size']} atividades")
    
    return stats

def demo_financial_streaming():
    """Demonstra análise financeira em tempo real"""
    print("\n💰 Análise Financeira em Tempo Real")
    print("=" * 60)
    
    # Cria stream de dados financeiros
    financial_stream = DataStream("financial_data")
    
    # Cria processador especializado
    processor = StreamProcessor("financial_analyst_01", "financial_analysis")
    
    # Conecta processador ao stream
    financial_stream.subscribe(processor.process_data_point)
    
    print("🚀 Iniciando stream de dados financeiros...")
    print("📊 Analisando mercado por 15 segundos...\n")
    
    # Inicia stream
    financial_stream.start_stream(duration=15)
    
    # Aguarda processamento
    time.sleep(16)
    
    # Para stream
    financial_stream.stop_stream()
    
    # Mostra estatísticas
    stats = processor.get_statistics()
    print("\n📈 Estatísticas da Análise:")
    print(f"   Transações processadas: {stats['processed_count']}")
    print(f"   Alertas de mercado: {stats['alerts_generated']}")
    print(f"   Buffer de análise: {stats['buffer_size']} transações")
    
    return stats

def demo_multi_stream_coordination():
    """Demonstra coordenação de múltiplos streams"""
    print("\n🔄 Coordenação de Múltiplos Streams")
    print("=" * 60)
    
    # Cria múltiplos streams
    streams = {
        "sensors": DataStream("sensor_data"),
        "users": DataStream("user_activity"),
        "financial": DataStream("financial_data")
    }
    
    # Cria processadores especializados
    processors = {
        "sensors": StreamProcessor("multi_sensor_01", "sensor_monitoring"),
        "users": StreamProcessor("multi_behavior_01", "user_behavior"),
        "financial": StreamProcessor("multi_financial_01", "financial_analysis")
    }
    
    # Cria coordenador
    coordinator = MangabaAgent(agent_id="stream_coordinator")
    
    # Conecta processadores aos streams
    for stream_type, stream in streams.items():
        processor = processors[stream_type]
        stream.subscribe(processor.process_data_point)
    
    print("🚀 Iniciando múltiplos streams simultaneamente...")
    print("📊 Coordenando análise por 20 segundos...\n")
    
    # Inicia todos os streams
    for stream in streams.values():
        stream.start_stream(duration=20)
    
    # Monitora coordenação
    start_time = time.time()
    while (time.time() - start_time) < 21:
        # Coleta estatísticas de todos os processadores
        all_stats = {}
        for stream_type, processor in processors.items():
            all_stats[stream_type] = processor.get_statistics()
        
        # Coordenador analisa situação geral
        coordination_data = {
            "timestamp": datetime.now().isoformat(),
            "active_streams": len(streams),
            "total_processed": sum(stats['processed_count'] for stats in all_stats.values()),
            "total_alerts": sum(stats['alerts_generated'] for stats in all_stats.values()),
            "stream_stats": all_stats
        }
        
        coordinator.chat(
            f"Coordenação multi-stream: {json.dumps(coordination_data)}",
            use_context=True
        )
        
        time.sleep(5)  # Atualiza a cada 5 segundos
    
    # Para todos os streams
    for stream in streams.values():
        stream.stop_stream()
    
    # Relatório final
    print("\n📊 Relatório Final de Coordenação:")
    print("-" * 40)
    
    total_processed = 0
    total_alerts = 0
    
    for stream_type, processor in processors.items():
        stats = processor.get_statistics()
        total_processed += stats['processed_count']
        total_alerts += stats['alerts_generated']
        
        print(f"\n🔹 Stream {stream_type.upper()}:")
        print(f"   Processados: {stats['processed_count']}")
        print(f"   Alertas: {stats['alerts_generated']}")
        print(f"   Buffer: {stats['buffer_size']}")
    
    print(f"\n🎯 TOTAIS:")
    print(f"   Dados processados: {total_processed}")
    print(f"   Alertas gerados: {total_alerts}")
    print(f"   Streams coordenados: {len(streams)}")
    
    # Contexto do coordenador
    coord_context = coordinator.get_context_summary()
    print(f"\n🧠 Contexto do Coordenador:")
    print(f"   Contextos de coordenação: {coord_context.get('total_contexts', 0)}")
    
    return {
        "total_processed": total_processed,
        "total_alerts": total_alerts,
        "streams_coordinated": len(streams),
        "coordination_contexts": coord_context.get('total_contexts', 0)
    }

def main():
    """Executa demonstração completa de streaming"""
    print("🌊 Mangaba Agent - Processamento de Dados em Tempo Real")
    print("=" * 80)
    
    try:
        # Demonstrações individuais
        sensor_stats = demo_sensor_monitoring()
        user_stats = demo_user_behavior_analysis()
        financial_stats = demo_financial_streaming()
        
        # Demonstração de coordenação
        coordination_stats = demo_multi_stream_coordination()
        
        print("\n🎉 DEMONSTRAÇÃO DE STREAMING COMPLETA!")
        print("=" * 60)
        
        print("\n📊 Resumo Geral:")
        print(f"   🌡️ Sensores: {sensor_stats['processed_count']} dados, {sensor_stats['alerts_generated']} alertas")
        print(f"   👥 Usuários: {user_stats['processed_count']} atividades, {user_stats['alerts_generated']} padrões")
        print(f"   💰 Financeiro: {financial_stats['processed_count']} transações, {financial_stats['alerts_generated']} alertas")
        print(f"   🔄 Coordenação: {coordination_stats['total_processed']} total, {coordination_stats['streams_coordinated']} streams")
        
        total_data_points = (
            sensor_stats['processed_count'] +
            user_stats['processed_count'] +
            financial_stats['processed_count'] +
            coordination_stats['total_processed']
        )
        
        total_insights = (
            sensor_stats['alerts_generated'] +
            user_stats['alerts_generated'] +
            financial_stats['alerts_generated'] +
            coordination_stats['total_alerts']
        )
        
        print(f"\n🚀 Capacidades Demonstradas:")
        print(f"   • Processamento em tempo real: {total_data_points} pontos de dados")
        print(f"   • Detecção de padrões: {total_insights} insights gerados")
        print(f"   • Análise multi-stream simultânea")
        print(f"   • Coordenação inteligente de recursos")
        print(f"   • Memória contextual contínua")
        print(f"   • Especialização por domínio")
        print(f"   • Alertas e anomalias em tempo real")
        
    except Exception as e:
        print(f"❌ Erro durante demonstração de streaming: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()