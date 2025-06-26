#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo de Integração da Aplicação de Busca de Ebooks com Discord

Este script demonstra como integrar a aplicação de busca de ebooks
com um bot do Discord, permitindo que usuários busquem ebooks
através de comandos no Discord.

Nota: Este é um exemplo simulado para fins de demonstração.
Para uso real, você precisaria configurar um bot no Discord Developer Portal
e adicionar as credenciais apropriadas.
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao path para importar o módulo mangaba_ai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


# Importações simuladas do Discord.py
class MockDiscord:
    class Client:
        def __init__(self):
            self.event_handlers = {}
            self.commands = {}
            self.user = MockUser("EbookSearchBot", "1234567890")

        def event(self, func):
            self.event_handlers[func.__name__] = func
            return func

        def command(self):
            def decorator(func):
                self.commands[func.__name__] = func
                return func

            return decorator

        async def start(self, token):
            print(f"Bot iniciado com token: {token[:5]}...")
            if "on_ready" in self.event_handlers:
                await self.event_handlers["on_ready"]()
            return self

        async def process_command(self, command_name, ctx, *args):
            if command_name in self.commands:
                await self.commands[command_name](ctx, *args)


class MockUser:
    def __init__(self, name, id):
        self.name = name
        self.id = id


class MockMessage:
    def __init__(self, content, author):
        self.content = content
        self.author = author


class MockContext:
    def __init__(self, message, channel):
        self.message = message
        self.channel = channel
        self.author = message.author

    async def send(self, content):
        print(
            f"[{self.channel.name}] Bot: {content[:100]}{'...' if len(content) > 100 else ''}"
        )


class MockChannel:
    def __init__(self, name, id):
        self.name = name
        self.id = id


# Simula o módulo discord
sys.modules["discord"] = MockDiscord()
import discord as mock_discord
# Importa os componentes da aplicação
from ebook_search import EbookSearchApp

# Inicializa o cliente do Discord
client = mock_discord.Client()

# Inicializa a aplicação de busca de ebooks
ebook_app = EbookSearchApp()


@client.event
async def on_ready():
    """
    Evento disparado quando o bot está pronto.
    """
    print(f"Bot conectado como {client.user.name}")
    print("------")


@client.command()
async def buscar(ctx, *, query):
    """
    Comando para buscar ebooks.
    Uso: !buscar <nome do ebook>
    """
    # Verifica se a query é válida
    if not query or len(query.strip()) == 0:
        await ctx.send("Por favor, forneça um nome de ebook para buscar.")
        return

    # Informa que a busca está em andamento
    await ctx.send(f"🔍 Buscando '{query}'... Isso pode levar alguns segundos.")

    try:
        # Realiza a busca
        start_time = datetime.now()
        results = await ebook_app.search(query)
        end_time = datetime.now()

        # Calcula o tempo de busca
        search_time = (end_time - start_time).total_seconds()

        # Verifica se encontrou resultados
        if results["count"] == 0:
            await ctx.send(f"❌ Nenhum resultado encontrado para '{query}'.")
            return

        # Formata os resultados para o Discord (versão resumida)
        discord_results = f"📚 **Resultados para '{query}'** (Encontrados {results['count']} ebooks em {search_time:.2f}s)\n\n"

        # Adiciona os primeiros 5 resultados (para não exceder o limite de mensagem do Discord)
        for i, result in enumerate(results["results"][:5], 1):
            discord_results += f"**{i}. {result['title']}**\n"
            discord_results += f"📝 **Autor:** {result['author']}\n"
            discord_results += f"📁 **Formato:** {result['format']} | 📏 **Tamanho:** {result['size']}\n"
            discord_results += f"🔗 **Link:** {result['download_link']}\n\n"

        # Adiciona nota se houver mais resultados
        if results["count"] > 5:
            discord_results += f"*...e mais {results['count'] - 5} resultados. Use !detalhes <número> para ver mais.*\n"

        # Envia os resultados
        await ctx.send(discord_results)

    except Exception as e:
        await ctx.send(f"❌ Erro ao buscar ebooks: {str(e)}")


@client.command()
async def detalhes(ctx, *, numero):
    """
    Comando para mostrar detalhes de um resultado específico.
    Uso: !detalhes <número>
    """
    try:
        # Converte o número para inteiro
        num = int(numero)

        # Verifica se há uma busca recente
        if not hasattr(ebook_app, "last_results") or ebook_app.last_results is None:
            await ctx.send(
                "❌ Nenhuma busca recente encontrada. Use !buscar <nome> primeiro."
            )
            return

        # Verifica se o número é válido
        if num < 1 or num > len(ebook_app.last_results["results"]):
            await ctx.send(
                f"❌ Número inválido. Escolha entre 1 e {len(ebook_app.last_results['results'])}."
            )
            return

        # Obtém o resultado específico
        result = ebook_app.last_results["results"][num - 1]

        # Formata os detalhes
        details = f"📚 **Detalhes do Ebook #{num}**\n\n"
        details += f"**Título:** {result['title']}\n"
        details += f"**Autor:** {result['author']}\n"
        details += f"**Formato:** {result['format']}\n"
        details += f"**Tamanho:** {result['size']}\n"
        details += f"**Idioma:** {result['language']}\n"
        details += f"**Ano:** {result['year']}\n"
        details += f"**Fonte:** {result['source']}\n"
        details += f"**ISBN:** {result.get('isbn', 'N/A')}\n"
        details += f"**Descrição:** {result.get('description', 'Não disponível')}\n\n"
        details += f"**Link de Download:** {result['download_link']}\n"

        # Envia os detalhes
        await ctx.send(details)

    except ValueError:
        await ctx.send("❌ Por favor, forneça um número válido.")
    except Exception as e:
        await ctx.send(f"❌ Erro ao obter detalhes: {str(e)}")


@client.command()
async def ajuda(ctx):
    """
    Comando para mostrar ajuda sobre os comandos disponíveis.
    Uso: !ajuda
    """
    help_text = """📚 **Bot de Busca de Ebooks - Comandos**\n\n
    **!buscar <nome>** - Busca ebooks pelo nome fornecido\n
    **!detalhes <número>** - Mostra detalhes de um resultado específico\n
    **!ajuda** - Mostra esta mensagem de ajuda\n\n
    **Exemplo:** !buscar Dom Casmurro
    """
    await ctx.send(help_text)


async def main():
    """
    Função principal para demonstração do bot.
    """
    # Simula o token do bot (em um caso real, seria obtido de variáveis de ambiente)
    token = "SEU_TOKEN_AQUI"

    # Inicia o bot
    bot = await client.start(token)

    print("===== Bot de Busca de Ebooks - Demo de Integração =====\n")
    print("Este é um exemplo simulado de integração com Discord.")
    print("Digite comandos no formato '!comando argumentos' ou 'sair' para encerrar.\n")

    # Simula um canal e um usuário
    channel = MockChannel("busca-de-ebooks", "123456789")
    user = MockUser("Usuario", "987654321")

    while True:
        # Solicita entrada do usuário
        user_input = input(f"[{channel.name}] {user.name}: ")

        # Verifica se o usuário deseja sair
        if user_input.lower() == "sair":
            print("\nEncerrando a demo...")
            break

        # Cria uma mensagem simulada
        message = MockMessage(user_input, user)
        ctx = MockContext(message, channel)

        # Processa o comando
        if user_input.startswith("!"):
            parts = user_input[1:].split(" ", 1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""

            await client.process_command(command, ctx, args)
        else:
            print(
                f"[{channel.name}] Bot: Use comandos com prefixo '!'. Digite !ajuda para ver os comandos disponíveis."
            )

    print("\nDemo encerrada. Obrigado por testar a integração!")


if __name__ == "__main__":
    # Executa a função principal
    asyncio.run(main())
