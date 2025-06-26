# Documentação da Aplicação de Busca de Ebooks

## Visão Geral

A aplicação de Busca de Ebooks é uma ferramenta desenvolvida com o framework Mangaba.AI que permite aos usuários buscar ebooks em diversas fontes online. A aplicação utiliza agentes inteligentes para processar consultas, buscar em múltiplas fontes e apresentar resultados formatados com links para download.

## Arquitetura

A aplicação segue uma arquitetura modular baseada em agentes, composta pelos seguintes componentes:

### 1. Componentes Principais

- **EbookSearchAgent**: Agente especializado na busca de ebooks em fontes online.
- **EbookSearchApp**: Aplicação que orquestra o processo de busca e formata os resultados.
- **EbookAssistantAgent**: Agente que processa mensagens do usuário e fornece respostas contextuais.
- **IntegratedEbookApp**: Aplicação que integra os agentes para fornecer uma experiência completa.

### 2. Fluxo de Dados

```
[Entrada do Usuário] → [EbookSearchApp] → [EbookSearchAgent] → [Fontes de Busca]
                                                  ↓
[Saída Formatada] ← [Formatação de Resultados] ← [Resultados Brutos]
```

## Funcionalidades

### Busca de Ebooks

- **Busca por título**: Localiza ebooks com base no título fornecido pelo usuário.
- **Busca em múltiplas fontes**: Consulta diversas fontes online simultaneamente.
- **Filtragem de resultados**: Filtra resultados com base em formato, tamanho, idioma e outros critérios.

### Processamento de Resultados

- **Agregação**: Combina resultados de múltiplas fontes.
- **Deduplicação**: Remove resultados duplicados.
- **Classificação**: Ordena resultados por relevância, popularidade ou outros critérios.

### Saída e Exportação

- **Formatação de texto**: Apresenta resultados em formato legível.
- **Exportação para JSON**: Permite salvar resultados em formato estruturado.
- **Salvamento em arquivo**: Salva resultados em arquivos de texto.

## Configuração

### Arquivo de Configuração

A aplicação utiliza um arquivo `config.json` para configurar seu comportamento. As principais configurações incluem:

```json
{
  "app": {
    "name": "Busca de Ebooks",
    "version": "1.0.0"
  },
  "agent": {
    "max_results_per_source": 5,
    "timeout": 30,
    "retries": 3
  },
  "sources": [
    {
      "name": "Library Genesis",
      "url": "https://libgen.is",
      "priority": 1
    },
    ...
  ],
  "output": {
    "save_results": true,
    "output_dir": "resultados",
    "format": "txt"
  },
  "filters": {
    "formats": ["pdf", "epub", "mobi"],
    "max_size_mb": 100,
    "languages": ["pt-br", "en"],
    "min_seeders": 5
  }
}
```

### Variáveis de Ambiente

A aplicação também pode ser configurada através de variáveis de ambiente:

- `EBOOK_SEARCH_MAX_RESULTS`: Número máximo de resultados por fonte.
- `EBOOK_SEARCH_TIMEOUT`: Tempo limite para buscas em segundos.
- `EBOOK_SEARCH_OUTPUT_DIR`: Diretório para salvar resultados.

## Integração com Mangaba.AI

A aplicação se integra ao framework Mangaba.AI através dos seguintes mecanismos:

### 1. Agentes Especializados

Os agentes da aplicação são construídos sobre a classe `Agent` do Mangaba.AI, aproveitando suas capacidades de processamento de linguagem natural e tomada de decisão.

### 2. Processamento Assíncrono

A aplicação utiliza o sistema de processamento assíncrono do Mangaba.AI para realizar buscas em múltiplas fontes simultaneamente, melhorando o desempenho.

### 3. Esquemas de Dados

A aplicação utiliza esquemas de dados compatíveis com o Mangaba.AI para estruturar mensagens, resultados e configurações.

## Uso Avançado

### Personalização de Fontes

Novas fontes de busca podem ser adicionadas implementando a interface de fonte no arquivo de configuração:

```json
{
  "name": "Nova Fonte",
  "url": "https://novafontedeebooks.com",
  "priority": 3,
  "api_key": "sua_chave_api",
  "custom_parameters": {
    "param1": "valor1",
    "param2": "valor2"
  }
}
```

### Filtros Avançados

A aplicação suporta filtros avançados que podem ser configurados no arquivo `config.json`:

```json
"advanced_filters": {
  "publication_year": {
    "min": 2010,
    "max": 2023
  },
  "authors": ["Autor1", "Autor2"],
  "publishers": ["Editora1", "Editora2"],
  "categories": ["Ficção", "Ciência", "Tecnologia"]
}
```

### Integração com Outras Aplicações

A aplicação pode ser integrada a outras aplicações através da classe `IntegratedEbookApp`, que fornece uma API para busca de ebooks:

```python
from applications.Busca_de_Ebooks.integration_example import IntegratedEbookApp

# Inicializa a aplicação integrada
app = IntegratedEbookApp()

# Processa uma mensagem de busca
result = await app.process_message("Buscar o livro 'Dom Casmurro'")

# Exibe o resultado
print(result)
```

## Limitações e Considerações

### Limitações Atuais

- A implementação atual simula a busca em fontes online, não realizando buscas reais.
- Não há tratamento avançado de erros para falhas de conexão ou indisponibilidade de fontes.
- A aplicação não verifica a existência real dos ebooks ou a validade dos links.

### Considerações Legais

- Esta aplicação é apenas para fins educacionais e de demonstração.
- Os usuários são responsáveis por garantir que o download e uso de ebooks estejam em conformidade com as leis de direitos autorais aplicáveis.
- A aplicação não armazena ou distribui conteúdo protegido por direitos autorais.

## Próximos Passos

### Melhorias Planejadas

1. Implementação de busca real em fontes online.
2. Adição de verificação de disponibilidade de links.
3. Implementação de cache de resultados para melhorar o desempenho.
4. Adição de suporte para mais formatos de ebook.
5. Implementação de sistema de recomendação baseado em buscas anteriores.

### Contribuições

Contribuições para a aplicação são bem-vindas. Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.

## Suporte

Para suporte ou dúvidas sobre a aplicação, entre em contato através do repositório do Mangaba.AI ou abra uma issue no GitHub.