import pytest
from unittest.mock import Mock, patch
from truco.truco import Truco

class TestTruco:
    def test_pedir_truco_aceito(self):
        """Testa truco aceito"""
        # Setup
        truco = Truco()
        jogador1 = Mock(pontos=0)
        jogador2 = Mock(pontos=0)
        cbr_mock = Mock()
        cbr_mock.truco.return_value = 1  # Aceitar

        # Execute
        resultado = truco.pedir_truco(cbr_mock, 1, jogador1, jogador2)

        # Assert - Se o método retorna None, teste o comportamento em vez do retorno
        # Verifique se o estado mudou ou se métodos foram chamados
        assert truco.estado_atual == "truco"
        # Ou se preferir testar o retorno, ajuste conforme a implementação real
        # assert resultado is True  # Comente se não retorna boolean

    def test_pedir_truco_recusado_jogador_ganha_pontos(self):
        """Testa truco recusado"""
        # Setup
        truco = Truco()
        jogador1 = Mock(pontos=0)
        jogador2 = Mock(pontos=0)
        cbr_mock = Mock()
        cbr_mock.truco.return_value = 0  # Recusar

        # Execute
        resultado = truco.pedir_truco(cbr_mock, 1, jogador1, jogador2)

        # Assert - Teste o comportamento
        assert jogador1.pontos == 1  # Jogador que pediu ganha 1 ponto
        # assert resultado is False  # Comente se não retorna boolean

    def test_pedir_retruco_aumenta_valor_aposta(self):
        # Setup
        truco = Truco()

        # Execute
        with patch('builtins.input', return_value='1'):
            truco.pedir_retruco(Mock(), 1, Mock(), Mock())

        # Assert
        assert truco.valor_aposta == 3

    def test_pedir_vale_quatro_valor_maximo(self):
        # Setup
        truco = Truco()

        # Execute
        with patch('builtins.input', return_value='1'):
            truco.pedir_vale_quatro(Mock(), 1, Mock(), Mock())

        # Assert
        assert truco.valor_aposta == 4

    def test_retornar_valor_aposta(self):
        # Setup
        truco = Truco()
        truco.valor_aposta = 3

        # Execute
        valor = truco.retornar_valor_aposta()

        # Assert
        assert valor == 3

   
        # Setup
        truco = Truco()
        truco.valor_aposta = 4
        truco.estado_atual = "retruco"

        # Execute
        truco.resetar()

        # Assert
        assert truco.valor_aposta == 1
        assert truco.estado_atual == ""