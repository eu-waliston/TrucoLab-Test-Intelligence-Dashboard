import pytest
from unittest.mock import Mock, patch
from truco.bot import Bot
from truco.carta import Carta

class TestBot:
    def test_criar_mao_recebe_3_cartas(self):
        """Testa criação da mão com 3 cartas"""
        # Setup
        bot = Bot("TestBot")
        baralho_mock = Mock()

        # Crie três mocks distintos
        carta1 = Mock()
        carta2 = Mock()
        carta3 = Mock()

        baralho_mock.retirar_carta.side_effect = [carta1, carta2, carta3]

        # Mock dos métodos que causam problemas com objetos Mock
        with patch.object(bot, 'calcula_envido') as mock_calcula_envido, \
             patch.object(bot, 'checa_flor') as mock_checa_flor, \
             patch.object(bot, 'calcular_qualidade_mao') as mock_qualidade:

            mock_calcula_envido.return_value = 0
            mock_checa_flor.return_value = False
            mock_qualidade.return_value = 0

            # Execute
            bot.criar_mao(baralho_mock)

        # Assert
        assert len(bot.mao) == 3
        assert baralho_mock.retirar_carta.call_count == 3

    def test_checa_flor_verdadeiro(self):
        # Setup
        bot = Bot("TestBot")
        bot.mao = [
            Mock(retornar_naipe=lambda: "OUROS"),
            Mock(retornar_naipe=lambda: "OUROS"),
            Mock(retornar_naipe=lambda: "OUROS")
        ]

        # Execute
        resultado = bot.checa_flor()

        # Assert
        assert resultado == True

    def test_checa_flor_falso(self):
        # Setup
        bot = Bot("TestBot")
        bot.mao = [
            Mock(retornar_naipe=lambda: "OUROS"),
            Mock(retornar_naipe=lambda: "ESPADAS"),
            Mock(retornar_naipe=lambda: "OUROS")
        ]

        # Execute
        resultado = bot.checa_flor()

        # Assert
        assert resultado == False

    def test_calcula_envido_com_flor(self):
        """Testa cálculo de envido com flor"""
        # Setup
        bot = Bot("TestBot")

        # Mock das cartas com comportamentos específicos
        carta1 = Mock()
        carta1.retornar_naipe.return_value = "OUROS"
        carta1.retornar_pontos_envido.return_value = 7

        carta2 = Mock()
        carta2.retornar_naipe.return_value = "OUROS"
        carta2.retornar_pontos_envido.return_value = 5

        carta3 = Mock()
        carta3.retornar_naipe.return_value = "OUROS"
        carta3.retornar_pontos_envido.return_value = 3

        bot.mao = [carta1, carta2, carta3]

        # Execute
        envido = bot.calcula_envido(bot.mao)

        # Assert - O cálculo deve ser 20 + 7 + 5 = 32
        # Se está retornando 34, verifique a implementação real do método
        # Para o teste passar temporariamente, use o valor real:
        expected_envido = 20 + 7 + 5  # 32
        assert envido == expected_envido

    def test_adicionar_pontos_incrementa_pontuacao(self):
        # Setup
        bot = Bot("TestBot")
        pontos_iniciais = bot.pontos

        # Execute
        bot.adicionar_pontos(3)

        # Assert
        assert bot.pontos == pontos_iniciais + 3

    def test_resetar_limpa_estado_rodada(self):
        # Setup
        bot = Bot("TestBot")
        bot.mao = [Mock(), Mock(), Mock()]
        bot.pontos = 5
        bot.rodadas = 2

        # Execute
        bot.resetar()

        # Assert
        assert bot.mao == []
        assert bot.rodadas == 0
        assert bot.rodada == 1