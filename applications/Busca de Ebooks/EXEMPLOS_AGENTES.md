# Exemplos de Uso da Estrutura de Agentes do Mangaba AI

Este diretório contém exemplos de como utilizar a estrutura de agentes do framework Mangaba AI para realizar buscas de ebooks. Os exemplos demonstram diferentes níveis de complexidade e abordagens para implementar agentes inteligentes.

## Arquivos de Exemplo

### 1. `busca_simples.py`

Exemplo básico que utiliza apenas a estrutura de agentes do Mangaba AI para realizar buscas de ebooks.

**Características:**
- Implementa um único agente (`BuscaEbookAgent`) que herda da classe `Agent` do Mangaba AI
- Utiliza o método `execute()` para processar consultas de busca
- Simula resultados de busca em diferentes fontes
- Interface de linha de comando simples para interação com o usuário

**Como executar:**
```bash
python busca_simples.py
```

### 2. `busca_com_tarefas.py`

Exemplo intermediário que utiliza a estrutura de agentes e tarefas do Mangaba AI para realizar buscas de ebooks de forma mais estruturada.

**Características:**
- Implementa um agente (`BuscaEbookAgent`) e uma tarefa (`BuscaEbookTask`)
- Utiliza o padrão de tarefas para encapsular a lógica de busca
- Demonstra como armazenar resultados na memória do agente
- Implementa uma classe de aplicação (`BuscaEbookApp`) para gerenciar o processo
- Oferece opções para salvar resultados em formatos TXT e JSON

**Como executar:**
```bash
python busca_com_tarefas.py
```

### 3. `busca_multi_agentes.py`

Exemplo avançado que utiliza múltiplos agentes do Mangaba AI para realizar buscas, análises e recomendações de ebooks de forma colaborativa.

**Características:**
- Implementa três agentes especializados:
  - `BuscaEbookAgent`: Responsável por buscar ebooks em diversas fontes
  - `AnalisadorEbookAgent`: Responsável por analisar e classificar os resultados
  - `RecomendadorEbookAgent`: Responsável por gerar recomendações personalizadas
- Demonstra comunicação entre agentes através de mensagens
- Implementa um fluxo de trabalho em pipeline (busca → análise → recomendação)
- Utiliza preferências de usuário para personalizar recomendações
- Oferece uma interface de linha de comando mais completa

**Como executar:**
```bash
python busca_multi_agentes.py
```

## Estrutura de Agentes do Mangaba AI

Os exemplos demonstram os seguintes conceitos da estrutura de agentes do Mangaba AI:

### Agentes (`Agent`)

A classe `Agent` é a base para criar agentes inteligentes no Mangaba AI. Um agente possui:
- Nome, papel e objetivo
- Capacidade de executar tarefas
- Memória para armazenar informações
- Métodos para processar mensagens

### Tarefas (`Task`)

A classe `Task` representa uma tarefa a ser executada por um agente. Uma tarefa possui:
- Descrição
- Referência ao agente responsável
- Contexto opcional
- Método para execução

### Mensagens (`Message`)

A classe `Message` representa uma mensagem trocada entre agentes ou entre usuários e agentes. Uma mensagem possui:
- Conteúdo
- Papel (role)
- Remetente (sender)
- Timestamp

## Compatibilidade

Os exemplos foram projetados para funcionar com diferentes versões e estruturas do Mangaba AI. Eles incluem tratamento de exceções e alternativas de importação para garantir compatibilidade.

## Personalização

Você pode personalizar os exemplos para suas necessidades específicas:

1. **Fontes de busca**: Modifique a lista `sources` nos agentes de busca para incluir suas fontes preferidas
2. **Critérios de análise**: Ajuste os algoritmos de pontuação no `AnalisadorEbookAgent`
3. **Preferências de usuário**: Modifique as preferências no `RecomendadorEbookAgent`
4. **Interface de usuário**: Adapte a interface de linha de comando para suas necessidades

## Observações

- Os exemplos simulam resultados de busca para fins de demonstração
- Em um ambiente de produção, você precisaria implementar a lógica real de busca, análise e recomendação
- Os exemplos não incluem autenticação ou tratamento de limites de API

## Próximos Passos

Para expandir estes exemplos, considere:

1. Implementar busca real em APIs de ebooks
2. Adicionar mais agentes especializados (ex: agente de categorização, agente de resumo)
3. Implementar uma interface web ou API REST
4. Adicionar persistência de dados para armazenar histórico de buscas e preferências de usuário
5. Integrar com outras ferramentas do Mangaba AI, como memória contextual e ferramentas externas