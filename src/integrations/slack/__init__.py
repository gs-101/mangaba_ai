"""
Slack integration package for Mangaba.AI
"""

from .mangaba_channel_analyzer import MangabaChannelAnalyzer
from .slack_agent_handler import SlackAgentHandler

__all__ = ["SlackAgentHandler", "MangabaChannelAnalyzer"]
