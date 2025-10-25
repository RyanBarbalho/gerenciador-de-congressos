"""
Carregador de Dados - Sistema de Alocação de Salas
Versão limpa e otimizada
"""

import pandas as pd
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

# Imports do sistema refatorado
try:
    from app.core.facade import SistemaAlocacaoFacade
    from app.services.data_loader import SistemaCompletoRefatorado
    from app.models.domain import Materia, Sala, TipoSala, LocalSala
    from app.factories.creators import FactoryManager
    from app.strategies.interfaces import ValidatorPadrao, Repository
    REFATORADO_DISPONIVEL = True
except ImportError:
    REFATORADO_DISPONIVEL = False


class CarregadorDados:
    """Carregador de dados unificado para o sistema de alocação"""

    def __init__(self):
        self.factory_manager = FactoryManager() if REFATORADO_DISPONIVEL else None
        self.validator = ValidatorPadrao() if REFATORADO_DISPONIVEL else None
        self.facade = SistemaAlocacaoFacade() if REFATORADO_DISPONIVEL else None
        self.sistema_completo = SistemaCompletoRefatorado() if REFATORADO_DISPONIVEL else None

        # Cache para dados carregados
        self._cache = {}

    def carregar_dados_csv(self, arquivo_csv: str) -> Dict[str, Any]:
        """Carrega dados de arquivo CSV"""
        print(f"\n{'='*50}")
        print(f"CARREGANDO DADOS: {arquivo_csv}")
        print(f"{'='*50}")

        # Verificar se arquivo existe
        if not Path(arquivo_csv).exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_csv}")

        # Verificar cache
        cache_key = str(Path(arquivo_csv).absolute())
        if cache_key in self._cache:
            print("Usando dados do cache")
            return self._cache[cache_key]

        try:
            if REFATORADO_DISPONIVEL:
                resultado = self._carregar_refatorado(arquivo_csv)
            else:
                resultado = self._carregar_original(arquivo_csv)

            # Cache do resultado
            self._cache[cache_key] = resultado
            return resultado

        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            raise

    def _carregar_refatorado(self, arquivo_csv: str) -> Dict[str, Any]:
        """Carrega dados usando sistema refatorado"""
        print("Usando sistema refatorado...")

        try:
            repository = self.sistema_completo.carregar_dados_csv(arquivo_csv)
            materias = list(repository.buscar_materias())
            salas = list(repository.buscar_salas())
            estatisticas = self.sistema_completo.obter_estatisticas()

            resultado = {
                'sucesso': True,
                'repository': repository,
                'materias': materias,
                'salas': salas,
                'estatisticas': estatisticas,
                'sistema': 'refatorado'
            }

            print(f"OK - {len(materias)} matérias, {len(salas)} salas carregadas")
            return resultado

        except Exception as e:
            print(f"Erro no sistema refatorado: {e}")
            print("Usando sistema original...")
            return self._carregar_original(arquivo_csv)

    def _carregar_original(self, arquivo_csv: str) -> Dict[str, Any]:
        """Carrega dados usando sistema original"""
        print("Usando sistema original...")

        df = pd.read_csv(arquivo_csv)
        materias = self._processar_materias(df)
        salas = self._processar_salas(df)
        estatisticas = self._calcular_estatisticas(materias, salas)

        resultado = {
            'sucesso': True,
            'dataframe': df,
            'materias': materias,
            'salas': salas,
            'estatisticas': estatisticas,
            'sistema': 'original'
        }

        print(f"OK - {len(materias)} matérias, {len(salas)} salas carregadas")
        return resultado

    def _processar_materias(self, df: pd.DataFrame) -> List[Dict]:
        """Processa matérias do DataFrame"""
        materias = []

        for _, row in df.iterrows():
            if pd.isna(row.get('codigo')) or pd.isna(row.get('nome')):
                continue

            horario = self._mapear_horario(row['horario'])
            precisa_lab = self._precisa_laboratorio(row['nome'])
            materiais = ["projetor", "quadro"] + (["computadores"] if precisa_lab else [])

            materia = {
                'id': str(row['codigo']),
                'nome': str(row['nome']),
                'inscritos': int(row['matriculados']),
                'horario': horario,
                'precisa_lab': precisa_lab,
                'materiais_necessarios': materiais,
                'capacidade': int(row['capacidade'])
            }

            materias.append(materia)

        return materias

    def _processar_salas(self, df: pd.DataFrame) -> List[Dict]:
        """Processa salas do CSV de salas"""
        try:
            # Carregar CSV de salas
            df_salas = pd.read_csv('relacao_salas.csv')
            salas = []

            for _, row in df_salas.iterrows():
                nome_sala = str(row['sala']).strip()
                bloco = str(row['bloco']).strip()
                capacidade = int(row['capacidade'])

                # Determinar tipo de sala baseado no nome
                tipo = self._determinar_tipo_sala_por_nome(nome_sala)

                # Determinar localização baseada no bloco
                localizacao = "im" if bloco == "IM" else "ic"

                # Determinar materiais disponíveis
                materiais = ["projetor", "quadro"]
                if tipo == "laboratorio":
                    materiais.append("computadores")

                # Calcular custo adicional
                custo = 15.0 if localizacao == "im" else 0.0

                sala = {
                    'id': f"SALA_{len(salas)+1:03d}",
                    'nome': nome_sala,
                    'capacidade': capacidade,
                    'tipo': tipo,
                    'local': localizacao,
                    'materiais_disponiveis': materiais,
                    'custo_adicional': custo
                }

                salas.append(sala)

            return salas

        except FileNotFoundError:
            print("Arquivo relacao_salas.csv não encontrado. Usando salas do CSV de matérias.")
            return self._processar_salas_original(df)
        except Exception as e:
            print(f"Erro ao carregar salas: {e}. Usando salas do CSV de matérias.")
            return self._processar_salas_original(df)

    def _processar_salas_original(self, df: pd.DataFrame) -> List[Dict]:
        """Processa salas do DataFrame original (fallback)"""
        salas_dict = {}

        for _, row in df.iterrows():
            local = str(row.get('local', '')).strip()
            if local == 'nan' or local == '':
                continue

            locais = [l.strip() for l in local.split(';')]

            for local_item in locais:
                nome_sala = re.sub(r'\([^)]*\)', '', local_item).strip()
                nome_sala = self._corrigir_nome_sala(nome_sala)

                if nome_sala and nome_sala not in salas_dict:
                    tipo = self._determinar_tipo_sala(local_item, row['nome'])
                    localizacao = self._determinar_localizacao(local_item)
                    capacidade = int(row['capacidade'])
                    materiais = ["projetor", "quadro"] + (["computadores"] if tipo == "laboratorio" else [])
                    custo = 15.0 if localizacao == "im" else 0.0

                    salas_dict[nome_sala] = {
                        'id': f"SALA_{len(salas_dict)+1:03d}",
                        'nome': nome_sala,
                        'capacidade': capacidade,
                        'tipo': tipo,
                        'local': localizacao,
                        'materiais_disponiveis': materiais,
                        'custo_adicional': custo
                    }

        return list(salas_dict.values())

    def _determinar_tipo_sala_por_nome(self, nome_sala: str) -> str:
        """Determina tipo de sala baseado no nome"""
        nome_lower = nome_sala.lower()

        if any(keyword in nome_lower for keyword in ['auditório', 'auditorio']):
            return "auditorio"
        elif any(keyword in nome_lower for keyword in ['lab', 'laboratório', 'robótica', 'circ']):
            return "laboratorio"
        else:
            return "aula"

    def _mapear_horario(self, horario_str: str) -> str:
        """Mapeia horário do CSV para formato legível"""
        if pd.isna(horario_str) or horario_str == '':
            return "Indefinido"

        # Mapear dias (2=Segunda, 3=Terça, 4=Quarta, 5=Quinta, 6=Sexta, 7=Sábado)
        dias_map = {'2': 'Segunda', '3': 'Terça', '4': 'Quarta', '5': 'Quinta', '6': 'Sexta', '7': 'Sábado'}

        # Mapear turnos e períodos
        turnos_map = {
            'M': {  # Manhã
                '1': '07:00-07:50', '2': '08:00-08:50', '3': '09:00-09:50',
                '4': '10:00-10:50', '5': '11:00-11:50', '6': '12:00-12:50'
            },
            'T': {  # Tarde
                '1': '13:00-13:50', '2': '13:50-14:40', '3': '14:40-15:30',
                '4': '15:30-16:20', '5': '16:20-17:10', '6': '17:10-18:00'
            },
            'N': {  # Noite
                '1': '18:00-18:50', '2': '18:50-19:40', '3': '19:40-20:30',
                '4': '20:30-21:20', '5': '21:20-22:10', '6': '22:10-23:00'
            }
        }

        # Padrão: dígitos (dias) + letra (turno) + dígitos (períodos)
        match = re.match(r'(\d+)([MTN])(\d+)', horario_str)
        if not match:
            return horario_str

        dias_str, turno, periodos_str = match.groups()

        # Processar múltiplos dias
        dias = []
        for dia_char in dias_str:
            if dia_char in dias_map:
                dias.append(dias_map[dia_char])

        if not dias:
            return horario_str

        # Processar múltiplos períodos
        periodos = []
        for periodo_char in periodos_str:
            if turno in turnos_map and periodo_char in turnos_map[turno]:
                periodos.append(turnos_map[turno][periodo_char])

        if not periodos:
            return horario_str

        # Combinar dias e períodos
        if len(dias) == 1 and len(periodos) == 1:
            return f"{dias[0]} {periodos[0]}"
        elif len(dias) == 1:
            # Múltiplos períodos no mesmo dia
            periodo_inicio = periodos[0].split('-')[0]
            periodo_fim = periodos[-1].split('-')[1]
            return f"{dias[0]} {periodo_inicio}-{periodo_fim}"
        elif len(periodos) == 1:
            # Múltiplos dias, mesmo período
            dias_str = '/'.join(dias)
            return f"{dias_str} {periodos[0]}"
        else:
            # Múltiplos dias e períodos
            dias_str = '/'.join(dias)
            periodo_inicio = periodos[0].split('-')[0]
            periodo_fim = periodos[-1].split('-')[1]
            return f"{dias_str} {periodo_inicio}-{periodo_fim}"

    def _precisa_laboratorio(self, nome_materia: str) -> bool:
        """Determina se matéria precisa de laboratório"""
        nome_lower = nome_materia.lower()
        lab_keywords = ['programação', 'banco de dados', 'redes', 'sistemas operacionais',
                       'inteligência artificial', 'computação gráfica', 'compiladores']
        return any(keyword in nome_lower for keyword in lab_keywords)

    def _determinar_tipo_sala(self, local_str: str, nome_materia: str) -> str:
        """Determina tipo de sala"""
        local_lower = local_str.lower()
        nome_lower = nome_materia.lower()

        if any(keyword in local_lower for keyword in ['auditório', 'auditorio']):
            return "auditorio"
        elif any(keyword in nome_lower for keyword in ['lab', 'laboratório', 'computação', 'programação']):
            return "laboratorio"
        else:
            return "aula"

    def _determinar_localizacao(self, local_str: str) -> str:
        """Determina localização da sala"""
        return "im" if 'im' in local_str.lower() or 'matemática' in local_str.lower() else "ic"

    def _corrigir_nome_sala(self, nome_sala: str) -> str:
        """Corrige nomes de salas com grafia incorreta"""
        correcoes = {
            'Istituto de Computaçãp': 'Instituto de Computação',
            'Instituição de Computação': 'Instituto de Computação',
            'Instituto de Computaçãp': 'Instituto de Computação',
            'Laboratório-01': 'Lab IC-01',
            'Sala-02-IC': 'Sala IC-02',
            'Sala-03-IC': 'Sala IC-03',
            'sala-25': 'Sala IC-25',
            'Auditório-IC': 'Auditório IC',
            'Bloco-12-IM-Sala-204': 'Sala IM-204',
            'Terça': 'Sala IC-Terça',
            'Quarta': 'Sala IC-Quarta',
            'Lab01': 'Lab IC-01'
        }
        return correcoes.get(nome_sala, nome_sala)

    def _calcular_estatisticas(self, materias: List[Dict], salas: List[Dict]) -> Dict[str, Any]:
        """Calcula estatísticas dos dados"""
        total_materias = len(materias)
        total_salas = len(salas)
        total_inscritos = sum(m.get('inscritos', 0) for m in materias)
        capacidade_total = sum(s.get('capacidade', 0) for s in salas)

        # Estatísticas por horário
        horarios = {}
        for materia in materias:
            horario = materia.get('horario', 'Indefinido')
            horarios[horario] = horarios.get(horario, 0) + 1

        # Estatísticas por tipo de sala
        tipos_sala = {}
        for sala in salas:
            tipo = sala.get('tipo', 'aula')
            tipos_sala[tipo] = tipos_sala.get(tipo, 0) + 1

        # Estatísticas por localização
        locais = {}
        for sala in salas:
            local = sala.get('local', 'ic')
            locais[local] = locais.get(local, 0) + 1

        return {
            'total_materias': total_materias,
            'total_salas': total_salas,
            'total_inscritos': total_inscritos,
            'capacidade_total': capacidade_total,
            'utilizacao_potencial': (total_inscritos / capacidade_total * 100) if capacidade_total > 0 else 0,
            'horarios': horarios,
            'tipos_sala': tipos_sala,
            'locais': locais
        }

    def imprimir_estatisticas(self, arquivo_csv: str = None):
        """Imprime estatísticas dos dados carregados"""
        if arquivo_csv:
            dados = self.carregar_dados_csv(arquivo_csv)
            estatisticas = dados.get('estatisticas', {})
        else:
            estatisticas = {}

        if not estatisticas:
            print("Nenhuma estatística disponível")
            return

        print(f"\n{'='*50}")
        print("ESTATÍSTICAS DOS DADOS")
        print(f"{'='*50}")

        print(f"Matérias: {estatisticas.get('total_materias', 0)}")
        print(f"Salas: {estatisticas.get('total_salas', 0)}")
        print(f"Inscritos: {estatisticas.get('total_inscritos', 0)}")
        print(f"Capacidade: {estatisticas.get('capacidade_total', 0)}")
        print(f"Utilização: {estatisticas.get('utilizacao_potencial', 0):.1f}%")

        # Matérias por horário
        horarios = estatisticas.get('horarios', {})
        if horarios:
            print(f"\n🕐 Matérias por horário:")
            for horario, count in sorted(horarios.items()):
                print(f"   {horario}: {count}")

        # Tipos de sala
        tipos_sala = estatisticas.get('tipos_sala', {})
        if tipos_sala:
            print(f"\nTipos de sala:")
            for tipo, count in sorted(tipos_sala.items()):
                print(f"   {tipo.upper()}: {count}")

    def executar_alocacao(self, arquivo_csv: str) -> Dict[str, Any]:
        """Executa alocação usando o sistema apropriado"""
        print(f"\n{'='*50}")
        print("EXECUTANDO ALOCAÇÃO")
        print(f"{'='*50}")

        dados = self.carregar_dados_csv(arquivo_csv)

        if not dados['sucesso']:
            return {'sucesso': False, 'erro': 'Falha ao carregar dados'}

        if REFATORADO_DISPONIVEL and dados['sistema'] == 'refatorado':
            try:
                # Criar alocador usando Builder Pattern
                from app.builders.constructors import AlocadorBuilder
                from app.strategies.interfaces import CompatibilidadePadrao

                builder = AlocadorBuilder()
                alocador = (builder
                           .com_materias(dados['materias'])
                           .com_salas(dados['salas'])
                           .com_compatibilidade_strategy(CompatibilidadePadrao())
                           .com_factory_manager(self.factory_manager)
                           .construir())

                print("Executando alocação com sistema refatorado...")
                resultado = self.facade.executar_alocacao({
                    'alocador': alocador,
                    'materias': dados['materias'],
                    'salas': dados['salas']
                })
                print(f"Resultado da alocação: {resultado}")
                return resultado
            except Exception as e:
                import traceback
                print(f"Erro detalhado na alocação: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                return {'sucesso': False, 'erro': f'Erro na alocação: {e}'}
        else:
            return {
                'sucesso': True,
                'mensagem': 'Dados carregados. Sistema original não possui alocação automática.',
                'dados': dados
            }


def main():
    """Função principal para testar o carregador"""
    print("=== TESTANDO CARREGADOR DE DADOS ===")

    carregador = CarregadorDados()

    try:
        resultado = carregador.carregar_dados_csv('oferta_cc_2025_1.csv')

        if resultado['sucesso']:
            print("\nDados carregados com sucesso!")
            carregador.imprimir_estatisticas()

            resultado_alocacao = carregador.executar_alocacao('oferta_cc_2025_1.csv')
            if resultado_alocacao['sucesso']:
                print("\nAlocação executada com sucesso!")
            else:
                print(f"\n{resultado_alocacao.get('erro', 'Erro desconhecido')}")
        else:
            print(f"\nErro: {resultado.get('erro', 'Erro desconhecido')}")

    except FileNotFoundError:
        print("Arquivo CSV não encontrado.")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()