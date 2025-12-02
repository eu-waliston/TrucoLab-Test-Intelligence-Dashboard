import pytest
from unittest.mock import Mock, patch, MagicMock

@pytest.fixture(autouse=True)
def mock_csv_files():
    """Mock para arquivos CSV usados nos testes"""
    with patch('pandas.read_csv') as mock_read_csv:
        # Crie um DataFrame mock mais realista
        mock_df = MagicMock()
        # Configure alguns comportamentos básicos do DataFrame
        mock_df.__getitem__ = Mock(side_effect=lambda x: MagicMock())
        mock_df.fillna.return_value = mock_df
        mock_df.replace.return_value = mock_df
        mock_df.astype.return_value = mock_df
        mock_read_csv.return_value = mock_df
        yield mock_read_csv

@pytest.fixture
def mock_carta():
    """Fixture para criar cartas mock"""
    def _carta(numero=3, naipe="OUROS", pontos_envido=3):
        carta = Mock()
        carta.numero = numero
        carta.naipe = naipe
        carta.retornar_numero.return_value = numero
        carta.retornar_naipe.return_value = naipe
        carta.retornar_naipe_codificado.return_value = {
            "ESPADAS": 1,
            "OUROS": 2,
            "BASTOS": 3,
            "COPAS": 4
        }.get(naipe, 2)
        carta.retornar_pontos_envido.return_value = pontos_envido
        carta.retornar_carta.return_value = f"{numero} de {naipe}"
        carta.retornar_pontos_carta.return_value = {
            1: 12, 2: 16, 3: 24, 4: 1, 5: 2, 6: 3, 7: 4, 10: 6, 11: 7, 12: 8
        }.get(numero, 1)
        carta.exibir_carta.return_value = None
        return carta
    return _carta

@pytest.fixture
def mock_baralho():
    """Fixture para criar baralho mock"""
    baralho = Mock()
    # Crie cartas mock para retornar
    cartas_mock = [Mock() for _ in range(10)]
    baralho.retirar_carta.side_effect = cartas_mock
    baralho.cartas = []
    baralho.vira = []
    baralho.manilhas = []
    return baralho

@pytest.fixture
def mock_jogador():
    """Fixture para criar jogador mock"""
    def _jogador(nome="Jogador Teste", pontos=0, rodadas=0):
        jogador = Mock()
        jogador.nome = nome
        jogador.pontos = pontos
        jogador.rodadas = rodadas
        jogador.mao = []
        jogador.flor = False
        jogador.pediu_flor = False
        jogador.pediu_truco = False
        jogador.primeiro = False
        jogador.ultimo = False
        jogador.envido = 0

        # Configure os métodos
        jogador.adicionar_pontos = Mock(side_effect=lambda x: setattr(jogador, 'pontos', jogador.pontos + x))
        jogador.adicionar_rodada = Mock(side_effect=lambda: setattr(jogador, 'rodadas', jogador.rodadas + 1))
        jogador.retorna_pontos_envido = Mock(return_value=jogador.envido)
        jogador.retorna_pontos_totais = Mock(return_value=jogador.pontos)
        jogador.checa_mao = Mock(return_value=jogador.mao)
        jogador.checa_flor = Mock(return_value=jogador.flor)

        return jogador
    return _jogador

@pytest.fixture
def mock_interface():
    """Fixture para criar interface mock"""
    interface = Mock()
    interface.mostrar_carta_jogada = Mock()
    interface.mostrar_carta_ganhadora = Mock()
    interface.mostrar_ganhador_rodada = Mock()
    interface.mostrar_placar_total = Mock()
    interface.mostrar_placar_rodadas = Mock()
    interface.mostrar_vencedor_flor = Mock()
    interface.mostrar_vencedor_envido = Mock()
    interface.mostrar_ganhador_jogo = Mock()
    interface.border_msg = Mock()
    return interface

@pytest.fixture
def mock_cbr():
    """Fixture para criar CBR mock"""
    cbr = Mock()
    cbr.truco = Mock(return_value=1)  # Por padrão aceita truco
    cbr.envido = Mock(return_value=1)  # Por padrão aceita envido
    cbr.flor = Mock(return_value=True)  # Por padrão tem flor
    cbr.jogar_carta = Mock(return_value=0)  # Por padrão joga primeira carta
    return cbr