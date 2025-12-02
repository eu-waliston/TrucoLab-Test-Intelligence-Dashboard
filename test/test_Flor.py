import pytest
from unittest.mock import Mock, patch
from truco.flor import Flor

class TestFlor:

    @patch('builtins.input')
    def test_pedir_flor_ambos_tem_flor(self, mock_input):
        """Testa pedido de flor quando ambos têm flor"""
        mock_input.return_value = '1'  # Sim
        # Setup
        flor = Flor()
        jogador1 = Mock(flor=True, pediu_flor=False, pontos=0, retorna_pontos_envido=lambda: 28)
        jogador2 = Mock(flor=True, pediu_flor=False, pontos=0, retorna_pontos_envido=lambda: 25)
        interface_mock = Mock()

        # Execute
        with patch('builtins.input', return_value='1'):
            flor.pedir_flor(1, jogador1, jogador2, interface_mock)

        # Assert
        assert jogador1.pediu_flor == True

    def test_contraflor_jogador1_ganha(self):
        # Setup
        flor = Flor()
        jogador1 = Mock(pontos=0, retorna_pontos_envido=lambda: 30)
        jogador2 = Mock(pontos=0, retorna_pontos_envido=lambda: 25)

        # Execute
        flor.contraflor(1, jogador1, jogador2)

        # Assert
        assert jogador1.pontos == 6  # Valor da contraflor

    def test_contraflor_resto_calculo_pontos(self):
        # Setup
        flor = Flor()
        jogador1 = Mock(pontos=0, retorna_pontos_envido=lambda: 29)
        jogador2 = Mock(pontos=0, retorna_pontos_envido=lambda: 27)

        # Execute
        flor.contraflor_resto(1, jogador1, jogador2)

        # Assert
        assert jogador1.pontos == 3  # Valor base da flor

    def test_decisao_jogador_aceita(self):
        # Setup
        flor = Flor()

        # Execute
        with patch('builtins.input', return_value='1'):
            resultado = flor.decisao_jogador()

        # Assert
        assert resultado == True

    def test_resetar_flor_limpa_estado(self):
        # Setup
        flor = Flor()
        flor.valor_flor = 6
        flor.estado_atual = "Contraflor"

        # Execute
        flor.resetar_flor()

        # Assert
        assert flor.valor_flor == 3
        assert flor.estado_atual == ""