# Documentação Técnica: Sistema Multi-Agente para Busca de Licitações

## Arquitetura do Sistema

O sistema de busca de licitações é implementado utilizando uma arquitetura multi-agente baseada no framework Mangaba.AI. Esta arquitetura permite a divisão de responsabilidades entre agentes especializados, cada um focado em uma etapa específica do processo.

### Componentes Principais

#### 1. Classes de Comunicação

- **Message**: Representa mensagens trocadas entre agentes, contendo conteúdo, remetente e timestamp.
- **AnalysisResult**: Representa resultados de análises, com conteúdo e pontuação.

#### 2. Agentes Especializados

- **BuscaLicitacoesAgent**: Responsável pela busca de licitações.
- **AnalisadorLicitacoesAgent**: Responsável pela análise dos resultados da busca.
- **RecomendadorLicitacoesAgent**: Responsável pela geração de recomendações.

#### 3. Aplicação Principal

- **BuscaLicitacoesApp**: Orquestra o fluxo de trabalho entre os agentes.

## Fluxo de Processamento

1. **Busca de Licitações**:
   - O usuário fornece termos de busca.
   - O `BuscaLicitacoesAgent` utiliza o `GoogleSearchTool` e fontes específicas para encontrar licitações.
   - Os resultados são estruturados com informações como título, órgão, modalidade, valor estimado, etc.

2. **Análise de Resultados**:
   - O `AnalisadorLicitacoesAgent` recebe os resultados da busca.
   - Calcula pontuações de relevância, oportunidade e viabilidade para cada licitação.
   - Ordena os resultados por pontuação final.

3. **Geração de Recomendações**:
   - O `RecomendadorLicitacoesAgent` recebe os resultados analisados.
   - Filtra os resultados com base nas preferências do usuário.
   - Adiciona justificativas e análises estratégicas para cada recomendação.
   - Seleciona as melhores oportunidades.

4. **Apresentação e Exportação**:
   - Os resultados são formatados para exibição.
   - O usuário pode salvar os resultados em formato texto e/ou JSON.

## Detalhamento dos Agentes

### BuscaLicitacoesAgent

#### Atributos
- **name**: "Busca Licitações Agent"
- **role**: "Especialista em busca de licitações"
- **goal**: "Encontrar licitações relacionadas à inteligência artificial"
- **search_tool**: Ferramenta de busca do Google
- **sources**: Lista de fontes específicas de licitações
- **memory**: Dicionário para armazenar resultados de buscas anteriores

#### Métodos Principais
- **search_licitacoes**: Realiza a busca de licitações usando o `search_tool` e as fontes específicas.
- **process_message**: Processa mensagens contendo termos de busca e armazena os resultados na memória.

### AnalisadorLicitacoesAgent

#### Atributos
- **name**: "Analisador Licitações Agent"
- **role**: "Especialista em análise de licitações"
- **goal**: "Analisar e classificar resultados de busca de licitações"
- **memory**: Dicionário para armazenar resultados de análises anteriores

#### Métodos Principais
- **analyze_results**: Analisa os resultados da busca, calculando pontuações para cada licitação.
- **_calculate_relevance**: Calcula a pontuação de relevância com base em termos específicos.
- **_calculate_opportunity**: Calcula a pontuação de oportunidade com base no valor e na data de abertura.
- **_calculate_viability**: Calcula a pontuação de viabilidade com base na modalidade, órgão e fonte.
- **process_message**: Processa mensagens contendo resultados de busca e armazena as análises na memória.

### RecomendadorLicitacoesAgent

#### Atributos
- **name**: "Recomendador Licitações Agent"
- **role**: "Especialista em recomendações de licitações"
- **goal**: "Recomendar as melhores licitações com base nos resultados analisados"
- **memory**: Dicionário para armazenar recomendações anteriores
- **user_preferences**: Dicionário para armazenar preferências de usuários

#### Métodos Principais
- **set_user_preferences**: Define as preferências do usuário.
- **generate_recommendations**: Gera recomendações com base nos resultados analisados e nas preferências do usuário.
- **_generate_strategic_analysis**: Gera uma análise estratégica para cada licitação.
- **process_message**: Processa mensagens contendo resultados analisados e armazena as recomendações na memória.

## Personalização do Sistema

### Preferências do Usuário

O sistema permite a personalização das recomendações através das seguintes preferências:

- **min_score**: Pontuação mínima para que uma licitação seja recomendada (padrão: 0.6).
- **max_recommendations**: Número máximo de recomendações a serem geradas (padrão: 5).
- **valor_maximo**: Valor máximo em reais para as licitações recomendadas.
- **modalidade_preferida**: Modalidade de licitação preferida (ex: "Pregão Eletrônico").

### Exemplo de Configuração

```python
recomendador_agent.set_user_preferences("user123", {
    "min_score": 0.7,  # Aumenta o limite mínimo de pontuação
    "max_recommendations": 3,  # Reduz o número de recomendações
    "valor_maximo": 1000000,  # Limita o valor máximo a 1 milhão
    "modalidade_preferida": "Concorrência"  # Altera a modalidade preferida
})
```

## Extensões Possíveis

### Integração com APIs Reais

Para uma implementação completa, o sistema pode ser estendido para integrar com APIs reais de portais de licitações, como:

- API do Portal de Compras Governamentais (ComprasNet)
- API do Portal de Licitações-e do Banco do Brasil
- APIs de portais estaduais e municipais de licitações

### Melhorias na Análise

- Implementação de análise de texto mais avançada usando processamento de linguagem natural
- Análise de histórico de licitações similares para prever chances de sucesso
- Análise de concorrência com base em licitações anteriores

### Funcionalidades Adicionais

- Notificações automáticas de novas licitações relevantes
- Dashboard para acompanhamento de licitações de interesse
- Geração automática de documentos para participação em licitações

## Considerações Técnicas

### Tratamento de Erros

O sistema implementa tratamento de erros em vários níveis:

- Tratamento de erros na busca de licitações
- Tratamento de erros na análise de resultados
- Tratamento de erros na geração de recomendações
- Tratamento de erros na interface com o usuário

### Performance

Para melhorar a performance do sistema, considere:

- Implementar cache de resultados de busca
- Otimizar os algoritmos de análise
- Implementar processamento paralelo para buscas em múltiplas fontes

### Segurança

Considerações de segurança incluem:

- Proteção de credenciais de APIs
- Validação de entrada do usuário
- Sanitização de dados de fontes externas

## Exemplos de Uso

### Exemplo 1: Busca Simples

```
Termos de busca: desenvolvimento de chatbot
```

O sistema irá buscar licitações relacionadas a "desenvolvimento de chatbot" e inteligência artificial, analisar os resultados e recomendar as melhores oportunidades.

### Exemplo 2: Busca Específica

```
Termos de busca: processamento de linguagem natural para atendimento ao cidadão
```

O sistema irá buscar licitações mais específicas relacionadas a processamento de linguagem natural no contexto de atendimento ao cidadão.

## Conclusão

O Sistema Multi-Agente para Busca de Licitações demonstra como a arquitetura multi-agente do Mangaba.AI pode ser aplicada para resolver problemas complexos de busca, análise e recomendação. A divisão de responsabilidades entre agentes especializados permite uma abordagem modular e extensível, facilitando a manutenção e evolução do sistema.