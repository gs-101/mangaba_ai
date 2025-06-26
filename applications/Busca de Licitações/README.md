# Sistema Multi-Agente para Busca de Licitações de IA

Este projeto implementa um sistema multi-agente utilizando o framework Mangaba.AI para buscar, analisar e recomendar licitações relacionadas à inteligência artificial.

## Visão Geral

O sistema utiliza três agentes especializados que trabalham em conjunto:

1. **Agente de Busca (BuscaLicitacoesAgent)**: Responsável por encontrar licitações relacionadas à inteligência artificial em diversas fontes governamentais.

2. **Agente de Análise (AnalisadorLicitacoesAgent)**: Avalia os resultados da busca, calculando pontuações de relevância, oportunidade e viabilidade para cada licitação.

3. **Agente de Recomendação (RecomendadorLicitacoesAgent)**: Seleciona as melhores oportunidades com base nas análises e nas preferências do usuário, gerando recomendações estratégicas.

## Funcionalidades

- Busca de licitações relacionadas à inteligência artificial em múltiplas fontes
- Análise automática de relevância, oportunidade e viabilidade das licitações
- Recomendações personalizadas com base em preferências configuráveis
- Análise estratégica para cada licitação recomendada
- Exportação de resultados em formato texto e JSON

## Requisitos

- Python 3.8 ou superior
- Framework Mangaba.AI
- Acesso à internet para realizar buscas

## Instalação

1. Certifique-se de ter o framework Mangaba.AI instalado:

```bash
pip install mangaba-ai
```

2. Clone este repositório ou copie os arquivos para o diretório de aplicações do Mangaba.AI.

## Uso

Execute o script principal:

```bash
python busca_licitacoes.py
```

O programa irá:

1. Solicitar termos de busca para licitações
2. Realizar a busca, análise e recomendação automaticamente
3. Exibir as recomendações formatadas
4. Oferecer opções para salvar os resultados em formato texto e/ou JSON

## Personalização

Você pode personalizar as preferências do usuário modificando o dicionário de preferências no método `__init__` da classe `BuscaLicitacoesApp`:

```python
self.recomendador_agent.set_user_preferences("default_user", {
    "min_score": 0.6,  # Pontuação mínima para recomendação
    "max_recommendations": 5,  # Número máximo de recomendações
    "valor_maximo": 5000000,  # Valor máximo em reais
    "modalidade_preferida": "Pregão Eletrônico"  # Modalidade preferida
})
```

## Estrutura do Projeto

- `busca_licitacoes.py`: Script principal contendo a implementação dos agentes e da aplicação
- `README.md`: Este arquivo de documentação

## Como Funciona

1. O sistema inicia solicitando termos de busca ao usuário
2. O Agente de Busca procura licitações relacionadas aos termos informados
3. O Agente de Análise avalia cada licitação encontrada
4. O Agente de Recomendação seleciona as melhores oportunidades
5. Os resultados são exibidos e podem ser salvos em arquivos

## Limitações Atuais

- A implementação atual simula algumas buscas e resultados
- Para uma implementação completa, seria necessário integrar com APIs reais de portais de licitações

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

Este projeto está licenciado sob os termos da licença MIT.