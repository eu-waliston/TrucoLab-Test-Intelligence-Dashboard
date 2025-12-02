import pytest
from truco.carta import Carta
from truco.pontos import MANILHA, CARTAS_VALORES

class TestCarta:
    def test_verificar_carta_alta_manilha(self):
        # Setup
        carta1 = Carta(1, "ESPADAS")  # Manilha mais alta
        carta2 = Carta(7, "OUROS")    # Manilha

        # Execute
        resultado = carta1.verificar_carta_alta(carta1, carta2)

        # Assert
        assert resultado == carta1

    def test_verificar_carta_alta_carta_normal(self):
        # Setup
        carta1 = Carta(3, "ESPADAS")  # Carta alta normal
        carta2 = Carta(2, "OUROS")    # Carta média

        # Execute
        resultado = carta1.verificar_carta_alta(carta1, carta2)

        # Assert
        assert resultado == carta1

    def test_verificar_carta_baixa(self):
        # Setup
        carta1 = Carta(3, "ESPADAS")  # Carta alta
        carta2 = Carta(5, "OUROS")    # Carta baixa

        # Execute
        resultado = carta1.verificar_carta_baixa(carta1, carta2)

        # Assert
        assert resultado == carta2

    def test_retornar_pontos_carta_manilha(self):
        # Setup
        carta = Carta(1, "ESPADAS")  # Manilha

        # Execute
        pontos = carta.retornar_pontos_carta(carta)

        # Assert
        assert pontos == MANILHA["1 de ESPADAS"]

    def test_retornar_pontos_carta_normal(self):
        # Setup
        carta = Carta(3, "ESPADAS")  # Carta normal

        # Execute
        pontos = carta.retornar_pontos_carta(carta)

        # Assert
        assert pontos == CARTAS_VALORES["3"]

    def test_classificar_carta_ranks_corretos(self):
        # Setup
        carta1 = Carta(3, "ESPADAS")  # Alta
        carta2 = Carta(2, "ESPADAS")  # Média
        carta3 = Carta(5, "ESPADAS")  # Baixa
        cartas = [carta1, carta2, carta3]

        # Execute
        pontos, classificacao = carta1.classificar_carta(cartas)

        # Assert
        assert "Alta" in classificacao
        assert "Media" in classificacao
        assert "Baixa" in classificacao

    def test_retornar_naipe_codificado(self):
        # Setup
        carta = Carta(3, "ESPADAS")

        # Execute & Assert
        assert carta.retornar_naipe_codificado() == 1

        carta2 = Carta(3, "OUROS")
        assert carta2.retornar_naipe_codificado() == 2