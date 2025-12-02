import pytest
from unittest.mock import Mock, patch
from truco.baralho import Baralho
from truco.carta import Carta

class TestBaralho:
    def test_criar_baralho_deve_ter_40_cartas(self):
        # Setup & Execute
        baralho = Baralho()

        # Assert
        assert len(baralho.cartas) == 40
        assert len([c for c in baralho.cartas if c.numero == 8]) == 0
        assert len([c for c in baralho.cartas if c.numero == 9]) == 0

    def test_criar_baralho_naipes_corretos(self):
        # Setup & Execute
        baralho = Baralho()
        naipes = [carta.naipe for carta in baralho.cartas]

        # Assert
        assert "ESPADAS" in naipes
        assert "OUROS" in naipes
        assert "COPAS" in naipes
        assert "BASTOS" in naipes

    def test_embaralhar_altera_ordem(self):
        # Setup
        baralho = Baralho()
        cartas_originais = baralho.cartas.copy()

        # Execute
        baralho.embaralhar()

        # Assert
        baralho.cartas != cartas_originais

    def test_retirar_carta_remove_uma_carta(self):
        # Setup
        baralho = Baralho()
        tamanho_inicial = len(baralho.cartas)

        # Execute
        carta = baralho.retirar_carta()

        # Assert
        assert len(baralho.cartas) == tamanho_inicial - 1
        assert isinstance(carta, Carta)

    def test_resetar_limpa_baralho(self):
        # Setup
        baralho = Baralho()
        baralho.vira = [Mock()]
        baralho.manilhas = [Mock()]

        # Execute
        baralho.resetar()

        # Assert
        assert baralho.vira == []
        assert baralho.manilhas == []
        assert baralho.cartas == []

    def test_printar_baralho_nao_levanta_excecao(self):
        # Setup
        baralho = Baralho()

        # Execute & Assert
        try:
            baralho.printar_baralho()
        except Exception as e:
            pytest.fail(f"printar_baralho levantou exceção: {e}")

    def resetar(self):
        """Resetar variáveis ligadas ao baralho."""
        self.vira = []  # Adicione esta linha se não existir
        self.manilhas = []
        self.cartas = []  # Esta linha deve existir