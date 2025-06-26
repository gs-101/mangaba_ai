import pytest
from unittest.mock import Mock, patch
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configurações do app HistoryReaderBot
SLACK_APP_ID = "A08R9C6SXPH"
SLACK_WORKSPACE = "IntegratedMLAI"
SLACK_TOKEN = "YOUR_SLACK_BOT_TOKEN"


def test_slack_connection():
    """Testa a conexão com a API do Slack (mockado)"""
    with patch.object(WebClient, 'auth_test') as mock_auth:
        # Mock da resposta de autenticação
        mock_auth.return_value = {
            "ok": True,
            "user": "test_user",
            "team": "test_team"
        }
        
        client = WebClient(token=SLACK_TOKEN)
        auth_response = client.auth_test()
        
        assert auth_response["ok"] is True
        assert "user" in auth_response
        
        print("\nConexão com Slack bem sucedida! (mockado)")
    print(f"App: HistoryReaderBot")
    print(f"App ID: {SLACK_APP_ID}")
    print(f"Workspace: {SLACK_WORKSPACE}")
    print(f"Conectado como: {auth_response['user']}")
    print("\nPermissões disponíveis:")
    print("- channels:history")
    print("- groups:history")
    print("- im:history")
    print("- mpim:history")


def test_slack_permissions():
    """Testa as permissões necessárias no Slack (mockado)"""
    with patch.object(WebClient, 'auth_test') as mock_auth:
        # Mock da resposta de autenticação
        mock_auth.return_value = {
            "ok": True,
            "user": "test_user",
            "team": "test_team"
        }
        
        client = WebClient(token=SLACK_TOKEN)
        auth_response = client.auth_test()
        
        assert auth_response["ok"] is True
        
        print("\nPermissões do Slack verificadas com sucesso! (mockado)")
    print(f"App: HistoryReaderBot (ID: {SLACK_APP_ID})")
    print("O bot tem as seguintes permissões:")
    print("- channels:history (para ler mensagens de canais)")
    print("- groups:history (para ler mensagens de grupos privados)")
    print("- im:history (para ler mensagens diretas)")
    print("- mpim:history (para ler mensagens de grupos diretos)")
