import pytest
import os
from unittest.mock import Mock, patch, call
from truco.interface import Interface

class TestInterface:

    def test_border_msg_sem_titulo(self):
        """Testa criação de borda sem título"""
        # Setup
        interface = Interface()

        # Execute
        with patch('builtins.print') as mock_print:
            interface.border_msg("Teste mensagem")

        # Assert - Verifica se print foi chamado
        assert mock_print.called

    def test_border_msg_com_titulo(self):
        """Testa criação de borda com título"""
        # Setup
        interface = Interface()

        # Execute
        with patch('builtins.print') as mock_print:
            interface.border_msg("Teste mensagem", title="Título")

        # Assert
        assert mock_print.called

    def test_border_msg_multilinha(self):
        """Testa borda com mensagem multilinha"""
        # Setup
        interface = Interface()
        mensagem = "Linha 1\nLinha 2\nLinha 3"

        # Execute
        with patch('builtins.print') as mock_print:
            interface.border_msg(mensagem)

        # Assert
        assert mock_print.called

    @patch('os.system')
    def test_limpar_tela_linux(self, mock_system):
        """Testa limpeza de tela (Linux)"""
        # Setup
        interface = Interface()

        # Execute
        interface.limpar_tela()

        # Assert
        mock_system.assert_called_with("clear")

    def test_mostrar_carta_jogada(self):
        """Testa exibição de carta jogada"""
        # Setup
        interface = Interface()
        jogador_mock = "Jogador 1"
        carta_mock = Mock()
        carta_mock.retornar_carta.return_value = "3 de OUROS"

        # Execute
        with patch('builtins.print') as mock_print:
            interface.mostrar_carta_jogada(jogador_mock, carta_mock)

        # Assert
        mock_print.assert_called_with("Jogador 1 jogou a carta: 3 de OUROS")

    def test_mostrar_carta_ganhadora(self):
        """Testa exibição de carta ganhadora"""
        # Setup
        interface = Interface()
        carta_mock = Mock()
        carta_mock.retornar_carta.return_value = "7 de ESPADAS"

        # Execute
        with patch('builtins.print') as mock_print:
            interface.mostrar_carta_ganhadora(carta_mock)

        # Assert
        mock_print.assert_called_with("\nCarta ganhadora: 7 de ESPADAS\n")

    def test_mostrar_ganhador_rodada(self):
        """Testa exibição de ganhador da rodada"""
        # Setup
        interface = Interface()

        # Execute
        with patch('builtins.print') as mock_print:
            interface.mostrar_ganhador_rodada("Jogador 1")

        # Assert
        mock_print.assert_called_with("Jogador 1 ganhou a rodada\n")

    def test_mostrar_placar_total_jogador_fugiu(self):
        """Testa exibição de jogador que fugiu"""
        # Setup
        interface = Interface()
        jogador_fugiu_mock = Mock()
        jogador_fugiu_mock.nome = "Jogador 2"

        # Execute
        with patch('builtins.print') as mock_print:
            interface.mostrar_placar_total_jogador_fugiu(
                jogador_fugiu_mock, "J1", 5, "J2", 3
            )

        # Assert
        mock_print.assert_called_with("Jogador Jogador 2 fugiu!")

    def test_mostrar_placar_total(self):
        """Testa exibição de placar total"""
        # Setup
        interface = Interface()

        # Execute
        with patch.object(interface, 'border_msg') as mock_border:
            interface.mostrar_placar_total("Jogador 1", 8, "Jogador 2", 6)

        # Assert
        mock_border.assert_called_with(
            "Jogador 1 - Jogador 1: 8 Pontos Acumulados\nJogador 2 - Jogador 2: 6 Pontos Acumulados",
            title='Pontuação Total'
        )

    def test_mostrar_placar_rodadas(self):
        """Testa exibição de placar de rodadas"""
        # Setup
        interface = Interface()

        # Execute
        with patch.object(interface, 'border_msg') as mock_border:
            interface.mostrar_placar_rodadas("J1", 2, "J2", 1)

        # Assert
        mock_border.assert_called_with(
            "Jogador 1 - J1: Venceu 2 Rodada(s)\nJogador 2 - J2: Venceu 1 Rodada(s)",
            title='Rodadas da Partida Atual'
        )

    def test_mostrar_vencedor_flor_jogador1(self):
        """Testa exibição de vencedor da flor (jogador 1)"""
        # Setup
        interface = Interface()

        # Execute
        with patch.object(interface, 'border_msg') as mock_border:
            interface.mostrar_vencedor_flor(1, "J1", "J2", 3)

        # Assert
        mock_border.assert_called_with(
            "Jogador 1 - J1: Venceu a flor e ganhou 3 pontos",
            title='Vencedor Flor'
        )

    def test_mostrar_vencedor_flor_jogador2(self):
        """Testa exibição de vencedor da flor (jogador 2)"""
        # Setup
        interface = Interface()

        # Execute
        with patch.object(interface, 'border_msg') as mock_border:
            interface.mostrar_vencedor_flor(2, "J1", "J2", 6)

        # Assert
        mock_border.assert_called_with(
            "Jogador 2 - J2: Venceu a flor e ganhou 6 pontos",
            title='Vencedor Flor'
        )

    def test_mostrar_vencedor_envido_jogador1(self):
        """Testa exibição de vencedor do envido (jogador 1)"""
        # Setup
        interface = Interface()

        # Execute
        with patch.object(interface, 'border_msg') as mock_border:
            interface.mostrar_vencedor_envido(1, "J1", 25, "J2", 20)

        # Assert
        mock_border.assert_called_with(
            "Jogador 1 - J1: Venceu o envido com 25 pontos\nJogador 2 - J2: PERDEU o envido com 20 pontos",
            title='Jogador 1 Vencedor Envido'
        )

    def test_mostrar_vencedor_envido_jogador2(self):
        """Testa exibição de vencedor do envido (jogador 2)"""
        # Setup
        interface = Interface()

        # Execute
        with patch.object(interface, 'border_msg') as mock_border:
            interface.mostrar_vencedor_envido(2, "J1", 18, "J2", 28)

        # Assert
        mock_border.assert_called_with(
            "Jogador 2 - J2: Venceu o envido com 28 pontos\nJogador 1 - J1: PERDEU o envido com 18 pontos",
            title='Jogador 2 Vencedor Envido'
        )

    def test_mostrar_ganhador_jogo(self):
        """Testa exibição de ganhador do jogo"""
        # Setup
        interface = Interface()

        # Execute
        with patch('builtins.print') as mock_print:
            interface.mostrar_ganhador_jogo("Jogador 1")

        # Assert
        mock_print.assert_called_with("\nJogador 1 ganhou o jogo")

    def test_mostrar_pediu_truco(self):
        """Testa exibição de aviso de truco já pedido"""
        # Setup
        interface = Interface()

        # Execute
        with patch('builtins.print') as mock_print:
            interface.mostrar_pediu_truco("Jogador 1")

        # Assert
        mock_print.assert_called_with("Jogador 1 pediu truco e o pedido já foi aceito, escolha outra jogada!")

    def test_mostrar_jogador_opcoes(self):
        """Testa exibição de opções do jogador"""
        # Setup
        interface = Interface()

        # Execute
        with patch('builtins.print') as mock_print:
            interface.mostrar_jogador_opcoes("Jogador 1")

        # Assert
        mock_print.assert_called_with("Jogador 1 é mão")

    def test_desenhar_cartas_ouros(self):
        """Testa desenho de carta de ouros"""
        # Setup
        interface = Interface()

        # Execute
        resultado = interface.desenhar_cartas("3 de OUROS")

        # Assert
        assert "♦" in resultado[4]  # Símbolo de ouros na posição 4

    def test_desenhar_cartas_espadas(self):
        """Testa desenho de carta de espadas"""
        # Setup
        interface = Interface()

        # Execute
        resultado = interface.desenhar_cartas("7 de ESPADAS")

        # Assert
        assert "♠" in resultado[4]  # Símbolo de espadas na posição 4

    def test_desenhar_cartas_copas(self):
        """Testa desenho de carta de copas"""
        # Setup
        interface = Interface()

        # Execute
        resultado = interface.desenhar_cartas("1 de COPAS")

        # Assert
        assert "♥" in resultado[4]  # Símbolo de copas na posição 4

    def test_desenhar_cartas_bastos(self):
        """Testa desenho de carta de bastos"""
        # Setup
        interface = Interface()

        # Execute
        resultado = interface.desenhar_cartas("12 de BASTOS")

        # Assert
        assert "♣" in resultado[4]  # Símbolo de bastos na posição 4

    def test_exibir_cartas(self):
        """Testa exibição de múltiplas cartas"""
        # Setup
        interface = Interface()
        cartas = ["3 de OUROS", "7 de ESPADAS", "1 de COPAS"]

        # Execute
        with patch('builtins.print') as mock_print:
            interface.exibir_cartas(cartas)

        # Assert
        assert mock_print.called

    def test_exibir_unica_carta(self):
        """Testa exibição de carta única"""
        # Setup
        interface = Interface()
        carta = "3 de OUROS"

        # Execute
        with patch('builtins.print') as mock_print:
            interface.exibir_unica_carta(carta)

        # Assert
        assert mock_print.called