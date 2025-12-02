import pytest
from truco.pontos import MANILHA, CARTAS_VALORES, ENVIDO

class TestPontos:

    def test_manilha_hierarquia_correta(self):
        """Testa se a hierarquia das manilhas está correta conforme regras gaúchas"""
        # Assert - Hierarquia gaúcha das manilhas (Zap > 7 Ouros > Espadilha > 1 Bastos)
        assert MANILHA["1 de ESPADAS"] == 52  # Espadilha
        assert MANILHA["1 de BASTOS"] == 50   # 1 de Bastos
        assert MANILHA["7 de ESPADAS"] == 42  # 7 de Espadas
        assert MANILHA["7 de OUROS"] == 40    # 7 de Ouros (mais alta)

        # Verifica ordem decrescente correta
        assert MANILHA["1 de ESPADAS"] > MANILHA["1 de BASTOS"]
        assert MANILHA["1 de BASTOS"] > MANILHA["7 de ESPADAS"]
        assert MANILHA["7 de ESPADAS"] > MANILHA["7 de OUROS"]

    def test_cartas_valores_hierarquia_correta(self):
        """Testa se a hierarquia das cartas normais está correta"""
        # Assert - Hierarquia das cartas normais do truco gaúcho
        assert CARTAS_VALORES["3"] == 24  # Carta mais alta
        assert CARTAS_VALORES["2"] == 16
        assert CARTAS_VALORES["1"] == 12
        assert CARTAS_VALORES["12"] == 8   # Rei
        assert CARTAS_VALORES["11"] == 7   # Cavalo
        assert CARTAS_VALORES["10"] == 6   # Dama
        assert CARTAS_VALORES["7"] == 4
        assert CARTAS_VALORES["6"] == 3
        assert CARTAS_VALORES["5"] == 2
        assert CARTAS_VALORES["4"] == 1    # Carta mais baixa

        # Verifica ordem decrescente completa
        assert CARTAS_VALORES["3"] > CARTAS_VALORES["2"]
        assert CARTAS_VALORES["2"] > CARTAS_VALORES["1"]
        assert CARTAS_VALORES["1"] > CARTAS_VALORES["12"]
        assert CARTAS_VALORES["12"] > CARTAS_VALORES["11"]
        assert CARTAS_VALORES["11"] > CARTAS_VALORES["10"]
        assert CARTAS_VALORES["10"] > CARTAS_VALORES["7"]
        assert CARTAS_VALORES["7"] > CARTAS_VALORES["6"]
        assert CARTAS_VALORES["6"] > CARTAS_VALORES["5"]
        assert CARTAS_VALORES["5"] > CARTAS_VALORES["4"]

    def test_envido_pontos_corretos(self):
        """Testa se os pontos de envido estão corretos conforme regras"""
        # Assert - Pontos de envido por carta (figuras valem 0)
        assert ENVIDO["1"] == 1
        assert ENVIDO["2"] == 2
        assert ENVIDO["3"] == 3
        assert ENVIDO["4"] == 4
        assert ENVIDO["5"] == 5
        assert ENVIDO["6"] == 6
        assert ENVIDO["7"] == 7
        assert ENVIDO["10"] == 0  # Figuras valem 0 no envido
        assert ENVIDO["11"] == 0  # Figuras valem 0 no envido
        assert ENVIDO["12"] == 0  # Figuras valem 0 no envido

    def test_estrutura_completa_pontos(self):
        """Testa se todas as estruturas têm entradas completas para todas as cartas"""
        # Assert - Verifica se todas as cartas do baralho estão presentes
        cartas_necessarias = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]

        for carta in cartas_necessarias:
            assert carta in CARTAS_VALORES, f"Carta {carta} faltando em CARTAS_VALORES"
            assert carta in ENVIDO, f"Carta {carta} faltando em ENVIDO"

    def test_manilhas_completas(self):
        """Testa se todas as manilhas estão definidas"""
        # Assert - Verifica as 4 manilhas do truco gaúcho
        manilhas_necessarias = [
            "1 de ESPADAS",
            "1 de BASTOS",
            "7 de ESPADAS",
            "7 de OUROS"
        ]

        for manilha in manilhas_necessarias:
            assert manilha in MANILHA, f"Manilha {manilha} faltando"

    def test_valores_consistentes(self):
        """Testa a consistência dos valores entre as diferentes estruturas"""
        # Cartas que são manilhas também devem ter valores normais para envido
        assert ENVIDO["1"] == 1  # 1 vale 1 no envido, mesmo sendo manilha
        assert ENVIDO["7"] == 7  # 7 vale 7 no envido, mesmo sendo manilha

        # Verifica que não há sobreposição indevida
        assert "1 de ESPADAS" not in CARTAS_VALORES  # Manilhas não estão em CARTAS_VALORES
        assert "1 de ESPADAS" not in ENVIDO  # Manilhas não estão em ENVIDO

    def test_hierarquia_envido_consistente(self):
        """Testa se a hierarquia do envido é consistente"""
        # No envido, as cartas numéricas mantém sua ordem natural
        assert ENVIDO["7"] > ENVIDO["6"]
        assert ENVIDO["6"] > ENVIDO["5"]
        assert ENVIDO["5"] > ENVIDO["4"]
        assert ENVIDO["4"] > ENVIDO["3"]
        assert ENVIDO["3"] > ENVIDO["2"]
        assert ENVIDO["2"] > ENVIDO["1"]

    def test_pontuacao_nao_negativa(self):
        """Testa que todos os valores são não-negativos"""
        for valor in CARTAS_VALORES.values():
            assert valor >= 0

        for valor in MANILHA.values():
            assert valor >= 0

        for valor in ENVIDO.values():
            assert valor >= 0

    def test_estruturas_imutaveis(self):
        """Testa que as estruturas de pontos não foram modificadas acidentalmente"""
        # Verifica que os dicionários mantém seus tamanhos originais
        assert len(MANILHA) == 4
        assert len(CARTAS_VALORES) == 10
        assert len(ENVIDO) == 10