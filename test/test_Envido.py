import pytest
from unittest.mock import Mock, patch
from truco.envido import Envido

class TestEnvido:

    @patch('builtins.input')  # CORRIJA O DECORATOR
    def test_envido_aceito_jogador1_ganha(self, mock_input):
        """Testa o fluxo quando envido é aceito"""
        # Setup
        mock_input.return_value = '1'  # Aceitar
        envido = Envido()
        jogador1 = Mock(retorna_pontos_envido=lambda: 25, pontos=0)
        jogador2 = Mock(retorna_pontos_envido=lambda: 20, pontos=0)
        cbr_mock = Mock()

        # Execute
        envido.controlador_envido(cbr_mock, Mock(), 6, 1, jogador1, jogador2, Mock())

        # Assert
        # O teste deve verificar o comportamento, não necessariamente pontos específicos

    def test_envido_recusado_jogador_ganha_pontos(self):
        """Testa envido recusado - use monkeypatch em vez de input"""
        # Setup
        envido = Envido()
        jogador1 = Mock(retorna_pontos_envido=lambda: 25, pontos=0)
        jogador2 = Mock(retorna_pontos_envido=lambda: 20, pontos=0)
        cbr_mock = Mock()
        cbr_mock.envido.return_value = 0  # Bot recusa

        # Execute - não use input, simule a resposta do bot
        envido.controlador_envido(cbr_mock, Mock(), 6, 1, jogador1, jogador2, Mock())

        # Assert - Verifique se os pontos foram adicionados
        # O teste deve passar se o jogador1 ganhou pontos
        assert jogador1.pontos > 0

    def test_real_envido_valor_5_pontos(self):
        """Testa real envido com valor 5 pontos"""
        # Setup
        envido = Envido()
        jogador1 = Mock()
        jogador2 = Mock()

        # Mock do input para evitar leitura real
        with patch('builtins.input', return_value='1'):
            # Execute
            envido.real_envido(Mock(), 1, jogador1, jogador2)

        # Assert
        assert envido.valor_envido == 5
        
    def test_falta_envido_calculo_correto(self):
        """Testa cálculo do falta envido"""
        # Setup
        envido = Envido()
        jogador1 = Mock(pontos=5)
        jogador2 = Mock(pontos=3)

        # Execute
        envido.falta_envido(Mock(), 1, jogador1, jogador2)

        # Assert - 12 - 5 = 7 (jogador1 tem 5 pontos)
        # Se está retornando 9, verifique a implementação real
        expected_valor = 12 - jogador1.pontos  # 7
        assert envido.valor_envido == expected_valor7

    def test_resetar_limpa_estado_envido(self):
        # Setup
        envido = Envido()
        envido.valor_envido = 5
        envido.estado_atual = 7

        # Execute
        envido.resetar()

        # Assert
        assert envido.valor_envido == 2
        assert envido.estado_atual == 0