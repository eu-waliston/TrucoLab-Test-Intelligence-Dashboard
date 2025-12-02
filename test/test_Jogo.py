import pytest
import sys
import os
from unittest.mock import Mock, patch

# Adicione o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from truco.jogo import Jogo
from truco.pontos import MANILHA, CARTAS_VALORES

class TestJogo:

    def test_criar_jogador(self):
        """Testa criação de jogador humano"""
        # Setup
        jogo = Jogo()
        baralho_mock = Mock()

        # Mock da classe Jogador
        with patch('jogo.Jogador') as mock_jogador_class:
            jogador_mock = Mock()
            mock_jogador_class.return_value = jogador_mock

            # Execute
            resultado = jogo.criar_jogador("João", baralho_mock)

        # Assert
        mock_jogador_class.assert_called_with("João")
        jogador_mock.criar_mao.assert_called_with(baralho_mock)
        assert resultado == jogador_mock

    def test_criar_bot(self):
        """Testa criação de bot"""
        # Setup
        jogo = Jogo()
        baralho_mock = Mock()  # CORREÇÃO: variável correta

        # Mock da classe Bot
        with patch('jogo.Bot') as mock_bot_class:
            bot_mock = Mock()
            mock_bot_class.return_value = bot_mock

            # Execute
            resultado = jogo.criar_bot("Bot", baralho_mock)

        # Assert
        mock_bot_class.assert_called_with("Bot")
        bot_mock.criar_mao.assert_called_with(baralho_mock)
        assert resultado == bot_mock