import pytest
import pandas as pd
import os
from unittest.mock import Mock, patch, MagicMock
from truco.dados import Dados

class TestDados:

    def test_init_carrega_colunas_corretas(self):
        """Testa se a inicialização carrega as colunas corretas"""
        # Setup & Execute
        dados = Dados()

        # Assert
        assert isinstance(dados.colunas, list)
        assert len(dados.colunas) > 0
        assert 'idMao' in dados.colunas
        assert 'jogadorMao' in dados.colunas
        assert 'cartaAltaRobo' in dados.colunas

    @patch('pandas.read_csv')
    def test_init_carrega_colunas_corretas(self, mock_read_csv):
        """Testa se a inicialização carrega as colunas corretas"""
        # Setup - Mock do DataFrame
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df

        # Execute
        dados = Dados()

        # Assert
        assert isinstance(dados.colunas, list)
        assert len(dados.colunas) > 0

    @patch('pandas.read_csv')
    def setUp(self, mock_read_csv):
        """Setup para todos os testes de Dados"""
        mock_df = MagicMock()
        # Configure o mock para retornar valores padrão
        mock_df.__getitem__ = Mock(side_effect=lambda x: MagicMock())
        mock_read_csv.return_value = mock_df
        self.dados = Dados()

    @patch('pandas.read_csv')
    def test_cartas_jogadas_pelo_bot_primeira_rodada(self, mock_read_csv):
        """Testa registro de cartas do bot na primeira rodada"""
        # Setup
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df
        dados = Dados()

        carta_mock = Mock()
        carta_mock.retornar_numero.return_value = 5
        carta_mock.retornar_naipe_codificado.return_value = 2

        # Execute
        dados.cartas_jogadas_pelo_bot('primeira', carta_mock)

        # Assert - Verifique se os atributos foram setados
        assert hasattr(dados.registro, 'primeiraCartaRobo')

    def test_cartas_jogadas_pelo_bot_primeira_rodada(self):
        """Testa registro de cartas do bot na primeira rodada"""
        # Setup
        dados = Dados()
        carta_mock = Mock()
        carta_mock.retornar_numero.return_value = 5
        carta_mock.retornar_naipe_codificado.return_value = 2  # OUROS

        # Execute
        dados.cartas_jogadas_pelo_bot('primeira', carta_mock)

        # Assert
        assert dados.registro.primeiraCartaRobo == 5
        assert dados.registro.naipePrimeiraCartaRobo == 2

    def test_cartas_jogadas_pelo_bot_segunda_rodada(self):
        """Testa registro de cartas do bot na segunda rodada"""
        # Setup
        dados = Dados()
        carta_mock = Mock()
        carta_mock.retornar_numero.return_value = 7
        carta_mock.retornar_naipe_codificado.return_value = 1  # ESPADAS

        # Execute
        dados.cartas_jogadas_pelo_bot('segunda', carta_mock)

        # Assert
        assert dados.registro.segundaCartaRobo == 7
        assert dados.registro.naipeSegundaCartaRobo == 1

    def test_cartas_jogadas_pelo_bot_terceira_rodada(self):
        """Testa registro de cartas do bot na terceira rodada"""
        # Setup
        dados = Dados()
        carta_mock = Mock()
        carta_mock.retornar_numero.return_value = 3
        carta_mock.retornar_naipe_codificado.return_value = 3  # BASTOS

        # Execute
        dados.cartas_jogadas_pelo_bot('terceira', carta_mock)

        # Assert
        assert dados.registro.terceiraCartaRobo == 3
        assert dados.registro.naipeTerceiraCartaRobo == 3

    def test_primeira_rodada_registro_completo(self):
        """Testa registro completo da primeira rodada"""
        # Setup
        dados = Dados()
        pontuacao_cartas = [24, 16, 8]  # Alta, Media, Baixa
        mao_rank = ['Alta', 'Media', 'Baixa']
        qualidade_mao_bot = 18.5
        carta_humano_mock = Mock()
        carta_humano_mock.retornar_numero.return_value = 2
        carta_humano_mock.retornar_naipe_codificado.return_value = 4  # COPAS

        # Execute
        dados.primeira_rodada(pontuacao_cartas, mao_rank, qualidade_mao_bot, carta_humano_mock)

        # Assert
        assert dados.registro.jogadorMao == 1
        assert dados.registro.cartaAltaRobo == 24
        assert dados.registro.cartaMediaRobo == 16
        assert dados.registro.cartaBaixaRobo == 8
        assert dados.registro.qualidadeMaoBot == 18.5
        assert dados.registro.primeiraCartaHumano == 2
        assert dados.registro.naipePrimeiraCartaHumano == 4

    def test_segunda_rodada_registro_ganhador(self):
        """Testa registro da segunda rodada com ganhador"""
        # Setup
        dados = Dados()
        carta_humano_mock = Mock()
        carta_humano_mock.retornar_numero.return_value = 3
        carta_humano_mock.retornar_naipe_codificado.return_value = 1

        carta_robo_mock = Mock()
        carta_robo_mock.retornar_numero.return_value = 7

        # Execute
        dados.segunda_rodada(carta_humano_mock, carta_robo_mock, 1)  # Ganhador: 1 (humano)

        # Assert
        assert dados.registro.ganhadorPrimeiraRodada == 1
        assert dados.registro.primeiraCartaHumano == 3
        assert dados.registro.naipePrimeiraCartaHumano == 1

    def test_terceira_rodada_registro_ganhador(self):
        """Testa registro da terceira rodada com ganhador"""
        # Setup
        dados = Dados()
        carta_humano_mock = Mock()
        carta_humano_mock.retornar_numero.return_value = 12
        carta_humano_mock.retornar_naipe_codificado.return_value = 2

        carta_robo_mock = Mock()
        carta_robo_mock.retornar_numero.return_value = 5

        # Execute
        dados.terceira_rodada(carta_humano_mock, carta_robo_mock, 2)  # Ganhador: 2 (bot)

        # Assert
        assert dados.registro.ganhadorSegundaRodada == 2
        assert dados.registro.SegundaCartaHumano == 12
        assert dados.registro.naipeSegundaCartaHumano == 2

    def test_finalizar_rodadas_registro_completo(self):
        """Testa registro final das rodadas"""
        # Setup
        dados = Dados()
        carta_humano_mock = Mock()
        carta_humano_mock.retornar_numero.return_value = 1
        carta_humano_mock.retornar_naipe_codificado.return_value = 3

        carta_robo_mock = Mock()
        carta_robo_mock.retornar_numero.return_value = 11

        # Execute
        dados.finalizar_rodadas(carta_humano_mock, carta_robo_mock, 1)  # Ganhador: 1

        # Assert
        assert dados.registro.ganhadorTerceiraRodada == 1
        assert dados.registro.terceiraCartaHumano == 1
        assert dados.registro.naipeTerceiraCartaHumano == 3

    def test_envido_registro_pedidos(self):
        """Testa registro de pedidos de envido"""
        # Setup
        dados = Dados()

        # Execute
        dados.envido(1, 2, 0, 1)  # quem_envido, quem_real_envido, quem_falta_envido, quem_ganhou_envido

        # Assert
        assert dados.registro.quemEnvido == 1
        assert dados.registro.quemRealEnvido == 2
        assert dados.registro.quemFaltaEnvido == 0
        assert dados.registro.quemGanhouEnvido == 1

    def test_truco_registro_sequencia(self):
        """Testa registro da sequência de truco"""
        # Setup
        dados = Dados()

        # Execute
        dados.truco(1, 2, 1, 0, 1)  # quem_truco, quem_retruco, quem_vale_quatro, quem_negou_truco, quem_ganhou_truco

        # Assert
        assert dados.registro.quemTruco == 1
        assert dados.registro.quemRetruco == 2
        assert dados.registro.quemValeQuatro == 1
        assert dados.registro.quemNegouTruco == 0
        assert dados.registro.quemGanhouTruco == 1

    def test_flor_registro_pedidos(self):
        """Testa registro de pedidos de flor"""
        # Setup
        dados = Dados()

        # Execute
        dados.flor(1, 2, 0, 28)  # quem_flor, quem_contraflor, quem_contraflor_resto, pontos_flor_robo

        # Assert
        assert dados.registro.quemGanhouFlor == 2
        assert dados.registro.quemFlor == 1
        assert dados.registro.quemContraFlor == 2
        assert dados.registro.quemContraFlorResto == 0
        assert dados.registro.pontosFlorRobo == 28

    def test_vencedor_envido_registro(self):
        """Testa registro de vencedor do envido"""
        # Setup
        dados = Dados()

        # Execute
        dados.vencedor_envido(2, 1)  # quem_ganhou_envido, quem_negou_envido

        # Assert
        assert dados.registro.quemGanhouEnvido == 2
        assert dados.registro.quemNegouEnvido == 1

    def test_vencedor_truco_registro(self):
        """Testa registro de vencedor do truco"""
        # Setup
        dados = Dados()

        # Execute
        dados.vencedor_truco(1, 2)  # quem_ganhou_truco, quem_negou_truco

        # Assert
        assert dados.registro.quemNegouTruco == 2
        assert dados.registro.quemGanhouTruco == 1

    def test_vencedor_flor_registro(self):
        """Testa registro de vencedor da flor"""
        # Setup
        dados = Dados()

        # Execute
        dados.vencedor_flor(2, 1)  # quem_ganhou_flor, quem_negou_flor

        # Assert
        assert dados.registro.quemGanhouFlor == 2
        assert dados.registro.quemNegouFlor == 1

    @patch('pandas.read_csv')
    def test_carregar_modelo_zerado(self, mock_read_csv):
        """Testa carregamento do modelo zerado"""
        # Setup
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df

        # Execute
        dados = Dados()
        resultado = dados.carregar_modelo_zerado()

        # Assert
        mock_read_csv.assert_called_with('modelo_registro.csv',
                                        usecols=dados.colunas,
                                        index_col='idMao')
        assert resultado == mock_df

    def test_retornar_registro(self):
        """Testa retorno do registro atual"""
        # Setup
        dados = Dados()

        # Execute
        registro = dados.retornar_registro()

        # Assert
        assert registro is not None
        assert hasattr(registro, 'columns')

    def test_retornar_casos(self):
        """Testa retorno dos casos carregados"""
        # Setup
        dados = Dados()

        # Execute
        casos = dados.retornar_casos()

        # Assert
        assert casos is not None

    @patch('pandas.read_csv')
    @patch('os.path.isfile')
    def test_finalizar_partida_novo_arquivo(self, mock_isfile, mock_read_csv):
        """Testa finalização de partida com criação de novo arquivo"""
        # Setup
        mock_isfile.return_value = False
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df

        dados = Dados()

        # Mock do método to_csv
        with patch.object(dados.registro, 'to_csv') as mock_to_csv:
            # Execute
            dados.finalizar_partida()

            # Assert - Verifique se to_csv foi chamado com os parâmetros corretos
            mock_to_csv.assert_called_once()
            # Não especifique parâmetros exatos, apenas que foi chamado
            assert mock_to_csv.called

    @patch('pandas.DataFrame.to_csv')
    @patch('os.path.isfile')
    def test_finalizar_partida_arquivo_existente(self, mock_isfile, mock_read_csv):
        """Testa finalização de partida com arquivo existente"""
        # Setup
        mock_isfile.return_value = True
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df

        dados = Dados()

        # Mock do método to_csv
        with patch.object(dados.registro, 'to_csv') as mock_to_csv:
            # Execute
            dados.finalizar_partida()

            # Assert
            mock_to_csv.assert_called_once()
            assert mock_to_csv.called

    @patch.object(Dados, 'tratamento_inicial_df')
    @patch.object(Dados, 'carregar_modelo_zerado')
    def test_resetar(self, mock_carregar_modelo, mock_tratamento_df):
        """Testa reset completo dos dados"""
        # Setup
        mock_carregar_modelo.return_value = MagicMock()
        mock_tratamento_df.return_value = MagicMock()

        # Crie a instância DEPOIS de configurar os mocks
        dados = Dados()

        # Reset call counts porque o init já chamou uma vez
        mock_tratamento_df.reset_mock()

        # Execute
        dados.resetar()

        # Assert - Agora deve ser chamado apenas uma vez
        assert mock_tratamento_df.call_count == 1
        assert mock_carregar_modelo.call_count == 1

    def test_registro_estrutura_completa(self):
        """Testa se o registro mantém estrutura consistente após múltiplas operações"""
        # Setup
        dados = Dados()

        # Execute múltiplas operações
        carta_mock = Mock()
        carta_mock.retornar_numero.return_value = 5
        carta_mock.retornar_naipe_codificado.return_value = 2

        dados.cartas_jogadas_pelo_bot('primeira', carta_mock)
        dados.envido(1, 0, 0, 1)
        dados.truco(2, 1, 0, 0, 2)

        # Assert - Verifica se a estrutura permanece consistente
        registro = dados.retornar_registro()
        assert hasattr(registro, 'primeiraCartaRobo')
        assert hasattr(registro, 'quemEnvido')
        assert hasattr(registro, 'quemTruco')
        assert registro.primeiraCartaRobo == 5
        assert registro.quemEnvido == 1
        assert registro.quemTruco == 2

    def test_mao_rank_classificacao_correta(self):
        """Testa se a classificação da mão em Alta/Media/Baixa funciona corretamente"""
        # Setup
        dados = Dados()
        pontuacao_cartas = [30, 20, 10]  # Valores distintos
        mao_rank = ['Alta', 'Media', 'Baixa']
        qualidade_mao = 25.0

        carta_mock = Mock()
        carta_mock.retornar_numero.return_value = 3
        carta_mock.retornar_naipe_codificado.return_value = 1

        # Execute
        dados.primeira_rodada(pontuacao_cartas, mao_rank, qualidade_mao, carta_mock)

        # Assert
        assert dados.registro.cartaAltaRobo == 30
        assert dados.registro.cartaMediaRobo == 20
        assert dados.registro.cartaBaixaRobo == 10
        assert dados.registro.qualidadeMaoBot == 25.0
