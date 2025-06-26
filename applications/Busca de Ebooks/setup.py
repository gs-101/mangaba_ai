#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de instalação para a aplicação de Busca de Ebooks.

Este script configura o ambiente necessário para executar a aplicação,
incluindo a criação de diretórios, instalação de dependências e
verificação da estrutura do projeto Mangaba.AI.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """
    Verifica se a versão do Python é compatível.
    """
    print("Verificando versão do Python...")
    if sys.version_info < (3, 8):
        print("ERRO: Python 3.8 ou superior é necessário.")
        sys.exit(1)
    print(
        f"OK: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )


def install_dependencies():
    """
    Instala as dependências necessárias.
    """
    print("\nInstalando dependências...")
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

    if not os.path.exists(requirements_file):
        print(f"ERRO: Arquivo {requirements_file} não encontrado.")
        sys.exit(1)

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file]
        )
        print("OK: Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao instalar dependências: {e}")
        sys.exit(1)


def check_mangaba_structure():
    """
    Verifica a estrutura do projeto Mangaba.AI e cria arquivos de compatibilidade se necessário.
    """
    print("\nVerificando estrutura do projeto Mangaba.AI...")

    # Diretório base do projeto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    # Verifica se o diretório mangaba_ai existe
    mangaba_dir = os.path.join(base_dir, "mangaba_ai")
    if not os.path.exists(mangaba_dir):
        print(f"AVISO: Diretório {mangaba_dir} não encontrado.")
    else:
        print(f"OK: Diretório {mangaba_dir} encontrado.")

    # Verifica se o diretório src/mangaba_ai existe
    src_dir = os.path.join(base_dir, "src", "mangaba_ai")
    if not os.path.exists(src_dir):
        print(f"AVISO: Diretório {src_dir} não encontrado.")
        print("Criando estrutura de compatibilidade...")

        # Cria diretórios necessários
        os.makedirs(os.path.join(src_dir, "core"), exist_ok=True)
        os.makedirs(os.path.join(src_dir, "schemas"), exist_ok=True)

        # Copia arquivos de compatibilidade
        compat_files = [
            ("__init__.py", os.path.join(src_dir)),
            ("main.py", os.path.join(src_dir)),
            ("__init__.py", os.path.join(src_dir, "core")),
            ("models.py", os.path.join(src_dir, "core")),
            ("protocols.py", os.path.join(src_dir, "core")),
            ("__init__.py", os.path.join(src_dir, "schemas")),
        ]

        for filename, dest_dir in compat_files:
            src_file = os.path.join(os.path.dirname(__file__), "compat", filename)
            dest_file = os.path.join(dest_dir, filename)

            if os.path.exists(src_file):
                shutil.copy2(src_file, dest_file)
                print(f"OK: Arquivo {dest_file} criado.")
            else:
                print(f"AVISO: Arquivo de compatibilidade {src_file} não encontrado.")
    else:
        print(f"OK: Diretório {src_dir} encontrado.")


def create_output_dir():
    """
    Cria o diretório de saída para os resultados.
    """
    print("\nCriando diretório de resultados...")
    output_dir = os.path.join(os.path.dirname(__file__), "resultados")
    os.makedirs(output_dir, exist_ok=True)
    print(f"OK: Diretório {output_dir} criado.")


def main():
    """
    Função principal do script de instalação.
    """
    print("===== Instalação da Aplicação de Busca de Ebooks =====\n")

    # Verifica requisitos e configura o ambiente
    check_python_version()
    install_dependencies()
    check_mangaba_structure()
    create_output_dir()

    print("\n===== Instalação concluída com sucesso! =====\n")
    print("Para executar a aplicação, use o comando:")
    print("python exemplo_uso.py")
    print("\nPara integração com Discord (simulado), use:")
    print("python demo_integracao_discord.py")


if __name__ == "__main__":
    main()
