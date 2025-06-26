#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de uso da aplicação de Busca de Ebooks

Este script demonstra como utilizar a aplicação de busca de ebooks
em um caso real, com entrada do usuário e exibição dos resultados.
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao path para importar o módulo mangaba_ai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importa os componentes da aplicação
from ebook_search import EbookSearchApp


async def main():
    """
    Função principal para demonstração da aplicação.
    """
    # Inicializa a aplicação
    app = EbookSearchApp()

    print("===== Aplicação de Busca de Ebooks - Mangaba.AI =====\n")
    print("Esta aplicação permite buscar ebooks em diversas fontes online.")
    print("Digite o nome do ebook que deseja buscar ou 'sair' para encerrar.\n")

    while True:
        # Solicita entrada do usuário
        ebook_name = input("Nome do ebook: ")

        # Verifica se o usuário deseja sair
        if ebook_name.lower() == "sair":
            print("\nEncerrando a aplicação...")
            break

        # Verifica se a entrada é válida
        if not ebook_name.strip():
            print("\nPor favor, digite um nome válido.\n")
            continue

        print(f"\nBuscando '{ebook_name}'...\n")

        try:
            # Realiza a busca
            start_time = datetime.now()
            results = await app.search(ebook_name)
            end_time = datetime.now()

            # Calcula o tempo de busca
            search_time = (end_time - start_time).total_seconds()

            # Formata e exibe os resultados
            formatted_results = app.format_results(results)
            print(formatted_results)
            print(f"Busca concluída em {search_time:.2f} segundos.\n")

            # Pergunta se deseja salvar os resultados
            save_option = input("Deseja salvar os resultados? (s/n): ")
            if save_option.lower() == "s":
                # Cria o diretório de resultados se não existir
                results_dir = "resultados"
                os.makedirs(results_dir, exist_ok=True)

                # Define o nome do arquivo
                filename = os.path.join(
                    results_dir,
                    f"busca_{ebook_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                )

                # Salva os resultados
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(formatted_results)

                print(f"Resultados salvos em: {filename}\n")

            # Pergunta se deseja exportar em JSON
            json_option = input("Deseja exportar os resultados em JSON? (s/n): ")
            if json_option.lower() == "s":
                # Cria o diretório de resultados se não existir
                results_dir = "resultados"
                os.makedirs(results_dir, exist_ok=True)

                # Define o nome do arquivo JSON
                json_filename = os.path.join(
                    results_dir,
                    f"busca_{ebook_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                )

                # Prepara os dados para exportação
                export_data = {
                    "query": results["query"],
                    "timestamp": datetime.now().isoformat(),
                    "count": results["count"],
                    "results": results["results"],
                }

                # Salva os resultados em JSON
                with open(json_filename, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)

                print(f"Resultados exportados em JSON: {json_filename}\n")

        except Exception as e:
            print(f"\nErro ao buscar ebooks: {str(e)}\n")

    print("\nObrigado por utilizar a aplicação de Busca de Ebooks!")


if __name__ == "__main__":
    # Executa a função principal
    asyncio.run(main())
