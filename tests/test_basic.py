"""
Testes básicos para o Mangaba.AI
"""

import mangaba_ai
import pytest


def test_import():
    """Testa se o pacote pode ser importado"""
    assert mangaba_ai is not None


def test_version():
    """Testa se a versão está definida"""
    assert hasattr(mangaba_ai, "__version__")
    assert isinstance(mangaba_ai.__version__, str)
    assert len(mangaba_ai.__version__) > 0
