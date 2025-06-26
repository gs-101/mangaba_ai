# Aplicação de Busca de Ebooks - Mangaba.AI

## Descrição

Esta aplicação permite buscar ebooks em diversas fontes online e retornar links para download. A entrada é o nome do ebook desejado e a saída são links para download do ebook.

## Funcionalidades

- **Busca por título**: Localiza ebooks com base no título fornecido pelo usuário.
- **Exibição de informações**: Mostra detalhes como autor, formato, tamanho e idioma.
- **Links de download**: Fornece links diretos para download dos ebooks encontrados.
- **Salvamento de resultados**: Permite salvar os resultados da busca em arquivos de texto ou JSON.

## Fontes de Busca (Simuladas)

- Library Genesis (libgen.is)
- Z-Library (b-ok.lat)
- Internet Archive (archive.org)
- PDF Drive (pdfdrive.com)
- Project Gutenberg (gutenberg.org)

## Uso

### Pré-requisitos

- Python 3.8 ou superior
- Framework Mangaba.AI instalado
- Dependências listadas em `requirements.txt`

### Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Execução

1. Execute o exemplo de uso:

```bash
python exemplo_uso.py
```

2. Digite o nome do ebook que deseja buscar quando solicitado.

### Exemplo

```
===== Aplicação de Busca de Ebooks - Mangaba.AI =====

Esta aplicação permite buscar ebooks em diversas fontes online.
Digite o nome do ebook que deseja buscar ou 'sair' para encerrar.

Nome do ebook: Dom Casmurro

Buscando 'Dom Casmurro'...

[Resultados para 'Dom Casmurro' - 8 encontrados]

1. Dom Casmurro
   Autor: Machado de Assis
   Formato: PDF | Tamanho: 2.3 MB | Idioma: Português
   Fonte: Library Genesis
   Link: https://libgen.is/book/index.php?md5=a1b2c3d4e5f6g7h8i9j0

2. Dom Casmurro (Edição Comentada)
   Autor: Machado de Assis, John Gledson (comentários)
   Formato: EPUB | Tamanho: 1.8 MB | Idioma: Português
   Fonte: Z-Library
   Link: https://b-ok.lat/book/3698720/b5a3e2

...

Busca concluída em 1.25 segundos.
```

## Personalização

A aplicação pode ser personalizada através do arquivo `config.json`, que permite configurar:

- Fontes de busca e suas prioridades
- Número máximo de resultados por fonte
- Filtros de formato, tamanho e idioma
- Opções de saída e salvamento

## Solução de Problemas

### Erro de Importação do GeminiModel

Se você encontrar um erro como `ImportError: cannot import name 'GeminiModel' from 'mangaba_ai.core.models'`, isso pode ocorrer devido a diferenças na estrutura do projeto Mangaba.AI. A aplicação inclui um módulo de compatibilidade (`compat.py`) que tenta resolver esses problemas automaticamente.

Para resolver manualmente:

1. Verifique a estrutura do seu projeto Mangaba.AI
2. Certifique-se de que o diretório `src/mangaba_ai/core` existe e contém um arquivo `__init__.py`
3. Se necessário, crie os arquivos de compatibilidade conforme mostrado no diretório da aplicação

### Erro de Inicialização de Agentes

Se você encontrar um erro como `TypeError: __init__() missing required positional arguments: 'name', 'role', and 'goal'`, isso indica que a classe `Agent` requer esses parâmetros no construtor. Certifique-se de que as classes que herdam de `Agent` estão passando esses parâmetros corretamente.

## Limitações

- Esta implementação simula a busca em fontes online, não realizando buscas reais.
- Não há tratamento avançado de erros para falhas de conexão ou indisponibilidade de fontes.
- A aplicação não verifica a existência real dos ebooks ou a validade dos links.

## Próximos Passos

- Implementar busca real em fontes online
- Adicionar verificação de disponibilidade de links
- Implementar cache de resultados para melhorar o desempenho
- Adicionar suporte para mais formatos de ebook
- Implementar sistema de recomendação baseado em buscas anteriores