"""Módulo de schemas do Mangaba.AI."""

# Importações simuladas para schemas que podem não existir no caminho alternativo
from dataclasses import dataclass


@dataclass
class Message:
    content: str
    role: str = "user"


@dataclass
class AnalysisResult:
    content: str
    score: float = 0.0
