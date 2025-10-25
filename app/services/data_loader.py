"""
Carregador de dados refatorado usando padrões de projeto.
Implementa Repository Pattern, Factory Pattern e Strategy Pattern.
"""

import pandas as pd
import re
from typing import List, Dict, Optional, Any
from ..models.domain import Materia, Sala, Subject
from ..strategies.interfaces import Repository, Validator, ValidatorPadrao
from ..factories.creators import FactoryManager, MateriaFactoryCSV, SalaFactoryCSV
from ..repositories.alocacao_repo import AlocacaoRepository


class CSVRepository(Repository):
    """Repositório para dados CSV"""

    def __init__(self, arquivo_csv: str, factory_manager: FactoryManager):
        self.arquivo_csv = arquivo_csv
        self.factory_manager = factory_manager
        self.df: Optional[pd.DataFrame] = None
        self.materias: Dict[str, Materia] = {}
        self.salas: Dict[str, Sala] = {}
        self._carregar_dados()

    def _carregar_dados(self):
        """Carrega dados do arquivo CSV"""
        try:
            self.df = pd.read_csv(self.arquivo_csv)
            self._processar_dados()
        except Exception as e:
            raise ValueError(f"Erro ao carregar arquivo CSV: {e}")

    def _processar_dados(self):
        """Processa dados do CSV"""
        if self.df is None:
            return

        # Processar matérias
        for _, row in self.df.iterrows():
            if pd.isna(row.get('codigo')) or pd.isna(row.get('nome')):
                continue

            dados_materia = self._extrair_dados_materia(row)
            try:
                materia = self.factory_manager.criar_materia(dados_materia, fonte='csv')
                self.materias[materia.id] = materia
            except Exception as e:
                print(f"Erro ao criar matéria {row.get('nome', 'Unknown')}: {e}")

        # Processar salas
        salas_dict = self._extrair_salas_unicas()
        for nome_sala, dados_sala in salas_dict.items():
            try:
                sala = self.factory_manager.criar_sala(dados_sala, fonte='csv')
                self.salas[sala.id] = sala
            except Exception as e:
                print(f"Erro ao criar sala {nome_sala}: {e}")

    def _extrair_dados_materia(self, row: pd.Series) -> Dict[str, Any]:
        """Extrai dados de matéria de uma linha do CSV"""
        material_value = int(row.get('material', 0))

        return {
            'codigo': str(row['codigo']),
            'nome': str(row['nome']),
            'matriculados': int(row['matriculados']),
            'horario': self._mapear_horario(row['horario']),
            'capacidade': int(row['capacidade']),
            'material': material_value  # 1 = precisa de computadores, 0 = não precisa
        }

    def _mapear_horario(self, horario_str: str) -> str:
        """Converte formato de horário do CSV para formato legível"""
        if pd.isna(horario_str) or horario_str == '':
            return "Indefinido"

        # Mapear códigos de horário
        dias_map = {
            '1': 'Domingo', '2': 'Segunda', '3': 'Terça', '4': 'Quarta',
            '5': 'Quinta', '6': 'Sexta', '7': 'Sábado'
        }

        # Horários por turno e período
        horarios_map = {
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

        # Tratar múltiplos horários (separados por espaço)
        if ' ' in horario_str:
            horarios = horario_str.split()
            horarios_mapeados = []
            for h in horarios:
                horarios_mapeados.append(self._mapear_horario_simples(h, dias_map, horarios_map))
            return ' | '.join(horarios_mapeados)

        return self._mapear_horario_simples(horario_str, dias_map, horarios_map)

    def _mapear_horario_simples(self, horario_str: str, dias_map: dict, horarios_map: dict) -> str:
        """Mapeia um horário simples baseado no formato: dias + turno + horários"""
        # Padrão: dias + turno + horários (ex: 24T34, 6M12, 2M1234)
        match = re.match(r'^([1-7]+)([MTN])([1-6]+)$', horario_str)
        if match:
            dias_codigo = match.group(1)
            turno = match.group(2)
            horarios_codigo = match.group(3)

            # Mapear dias
            dias_nomes = []
            for dia_num in dias_codigo:
                if dia_num in dias_map:
                    dias_nomes.append(dias_map[dia_num])

            # Mapear horários
            horarios_lista = []
            for horario_num in horarios_codigo:
                if turno in horarios_map and horario_num in horarios_map[turno]:
                    horarios_lista.append(horarios_map[turno][horario_num])

            if dias_nomes and horarios_lista:
                dias_str = '/'.join(dias_nomes)
                horarios_str = '/'.join(horarios_lista)
                return f"{dias_str} {horarios_str}"

        return horario_str

    def _extrair_salas_unicas(self) -> Dict[str, Dict[str, Any]]:
        """Extrai salas do CSV de salas"""
        try:
            # Carregar CSV de salas
            df_salas = pd.read_csv('relacao_salas.csv')
            salas = {}

            for _, row in df_salas.iterrows():
                nome_sala = str(row['sala']).strip()
                bloco = str(row['bloco']).strip()
                capacidade = int(row['capacidade'])
                # Tratar valores NaN na coluna tipo
                tipo_raw = row.get('tipo', 0)
                if pd.isna(tipo_raw) or tipo_raw == '':
                    tipo_equipamento = 0
                else:
                    tipo_equipamento = int(tipo_raw)  # 1 = computadores, 2 = robótica, 3 = eletrônica, 0 = nenhum


                # Determinar tipo de sala baseado no nome
                tipo = self._determinar_tipo_sala_por_nome(nome_sala)

                # Determinar localização baseada no bloco
                localizacao = "im" if bloco == "IM" else "ic"

                # Determinar materiais disponíveis baseado no tipo de equipamento
                materiais = ["projetor", "quadro"]
                if tipo_equipamento == 1:  # Computadores
                    materiais.append("computadores")
                elif tipo_equipamento == 2:  # Robótica
                    materiais.extend(["robôs", "sensores"])
                elif tipo_equipamento == 3:  # Eletrônica
                    materiais.extend(["multímetros", "osciloscópios"])

                # Calcular custo adicional
                custo = 15.0 if localizacao == "im" else 0.0

                dados_sala = {
                    'id': f"SALA_{len(salas)+1:03d}",
                    'nome': nome_sala,
                    'capacidade': capacidade,
                    'tipo': tipo,
                    'local': localizacao,
                    'tipo_equipamento': tipo_equipamento,
                    'materiais_disponiveis': materiais,
                    'custo_adicional': custo
                }

                salas[nome_sala] = dados_sala

            return salas

        except FileNotFoundError:
            print("Arquivo relacao_salas.csv não encontrado. Usando salas do CSV de matérias.")
            return self._extrair_salas_original()
        except Exception as e:
            print(f"Erro ao carregar salas: {e}. Usando salas do CSV de matérias.")
            return self._extrair_salas_original()

    def _extrair_salas_original(self) -> Dict[str, Dict[str, Any]]:
        """Extrai salas únicas dos dados originais (fallback)"""
        salas = {}

        for _, row in self.df.iterrows():
            local = str(row['local']).strip()
            if local == 'nan' or local == '':
                continue

            # Processar locais com múltiplas salas
            locais = [l.strip() for l in local.split(';')]

            for local_item in locais:
                # Extrair nome da sala
                nome_sala = re.sub(r'\([^)]*\)', '', local_item).strip()
                nome_sala = self._corrigir_nome_sala(nome_sala)

                if nome_sala and nome_sala not in salas:
                    salas[nome_sala] = {
                        'id': f"SALA_{len(salas)+1:03d}",
                        'nome': nome_sala,
                        'capacidade': int(row['capacidade']),
                        'local': local_item
                    }

        return salas

    def _determinar_tipo_sala_por_nome(self, nome_sala: str) -> str:
        """Determina tipo de sala baseado no nome"""
        nome_lower = nome_sala.lower()

        if any(keyword in nome_lower for keyword in ['auditório', 'auditorio']):
            return "auditorio"
        elif any(keyword in nome_lower for keyword in ['lab', 'laboratório', 'robótica', 'circ']):
            return "laboratorio"
        else:
            return "aula"

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

    # Implementação da interface Repository
    def salvar_materia(self, materia: Materia) -> bool:
        """Salva uma matéria"""
        try:
            self.materias[materia.id] = materia
            return True
        except Exception:
            return False

    def salvar_sala(self, sala: Sala) -> bool:
        """Salva uma sala"""
        try:
            self.salas[sala.id] = sala
            return True
        except Exception:
            return False

    def buscar_materias(self) -> List[Materia]:
        """Busca todas as matérias"""
        return list(self.materias.values())

    def buscar_salas(self) -> List[Sala]:
        """Busca todas as salas"""
        return list(self.salas.values())

    def buscar_materia_por_id(self, materia_id: str) -> Optional[Materia]:
        """Busca matéria por ID"""
        return self.materias.get(materia_id)

    def buscar_sala_por_id(self, sala_id: str) -> Optional[Sala]:
        """Busca sala por ID"""
        return self.salas.get(sala_id)


class CarregadorDadosRefatorado:
    """Carregador de dados refatorado usando padrões de projeto"""

    def __init__(self, factory_manager: FactoryManager = None, validator: Validator = None):
        self.factory_manager = factory_manager or FactoryManager()
        self.validator = validator or ValidatorPadrao()
        self.repository: Optional[Repository] = None
        self.observers: List[Subject] = []

    def adicionar_observer(self, observer: Subject):
        """Adiciona observador"""
        self.observers.append(observer)

    def carregar_dados_csv(self, arquivo_csv: str) -> Repository:
        """Carrega dados de arquivo CSV"""
        try:
            # Notificar início
            for observer in self.observers:
                observer.on_progress("Carregando dados CSV", 0.0)

            # Criar repositório CSV
            self.repository = CSVRepository(arquivo_csv, self.factory_manager)

            # Validar dados carregados
            erros = self._validar_dados_carregados()
            if erros:
                print("Avisos de validação:")
                for erro in erros:
                    print(f"  - {erro}")

            # Notificar sucesso
            for observer in self.observers:
                observer.on_progress("Dados carregados com sucesso", 100.0)

            return self.repository

        except Exception as e:
            # Notificar erro
            for observer in self.observers:
                observer.on_erro(f"Erro ao carregar dados: {e}")
            raise

    def _validar_dados_carregados(self) -> List[str]:
        """Valida dados carregados"""
        erros = []

        if not self.repository:
            return ["Repositório não inicializado"]

        materias = self.repository.buscar_materias()
        salas = self.repository.buscar_salas()

        # Validar matérias
        for materia in materias:
            erros.extend(self.validator.validar_materia(materia))

        # Validar salas
        for sala in salas:
            erros.extend(self.validator.validar_sala(sala))

        # Validações específicas
        if not materias:
            erros.append("Nenhuma matéria válida encontrada")

        if not salas:
            erros.append("Nenhuma sala válida encontrada")

        return erros

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas dos dados carregados"""
        if not self.repository:
            return {}

        materias = self.repository.buscar_materias()
        salas = self.repository.buscar_salas()

        # Estatísticas básicas
        total_materias = len(materias)
        total_salas = len(salas)
        total_inscritos = sum(m.inscritos for m in materias)
        capacidade_total = sum(s.capacidade for s in salas)

        # Estatísticas por horário
        horarios = {}
        for materia in materias:
            horario = materia.horario
            horarios[horario] = horarios.get(horario, 0) + 1

        # Estatísticas por tipo de sala
        tipos_sala = {}
        for sala in salas:
            tipo = sala.tipo.value
            tipos_sala[tipo] = tipos_sala.get(tipo, 0) + 1

        # Estatísticas por localização
        locais = {}
        for sala in salas:
            local = sala.local.value
            locais[local] = locais.get(local, 0) + 1

        # Matérias que precisam de laboratório (material > 0)
        lab_count = sum(1 for m in materias if m.material > 0)

        return {
            'total_materias': total_materias,
            'total_salas': total_salas,
            'total_inscritos': total_inscritos,
            'capacidade_total': capacidade_total,
            'utilizacao_potencial': (total_inscritos / capacidade_total * 100) if capacidade_total > 0 else 0,
            'horarios': horarios,
            'tipos_sala': tipos_sala,
            'locais': locais,
            'materias_lab': lab_count,
            'distribuicao_inscritos': {
                'media': sum(m.inscritos for m in materias) / len(materias) if materias else 0,
                'maior_turma': max(m.inscritos for m in materias) if materias else 0,
                'menor_turma': min(m.inscritos for m in materias) if materias else 0
            }
        }

    def imprimir_estatisticas(self):
        """Imprime estatísticas dos dados carregados"""
        stats = self.obter_estatisticas()

        if not stats:
            print("Nenhuma estatística disponível")
            return

        print("\n=== ESTATÍSTICAS DOS DADOS CARREGADOS ===")
        print(f"Total de matérias: {stats['total_materias']}")
        print(f"Total de salas: {stats['total_salas']}")
        print(f"Total de inscritos: {stats['total_inscritos']}")
        print(f"Capacidade total: {stats['capacidade_total']}")
        print(f"Utilização potencial: {stats['utilizacao_potencial']:.2f}%")

        print(f"\nMatérias que precisam de laboratório: {stats['materias_lab']}")

        print("\nDistribuição de inscritos:")
        dist = stats['distribuicao_inscritos']
        print(f"  Média: {dist['media']:.1f} alunos")
        print(f"  Maior turma: {dist['maior_turma']} alunos")
        print(f"  Menor turma: {dist['menor_turma']} alunos")

        print("\nMatérias por horário:")
        for horario, count in sorted(stats['horarios'].items()):
            print(f"  {horario}: {count} matérias")

        print(f"\nTipos de salas: {stats['tipos_sala']}")
        print(f"Localizações: {stats['locais']}")


class SistemaCompletoRefatorado:
    """Sistema completo refatorado usando todos os padrões"""

    def __init__(self):
        self.factory_manager = FactoryManager()
        self.validator = ValidatorPadrao()
        self.carregador = CarregadorDadosRefatorado(self.factory_manager, self.validator)
        self.repository: Optional[Repository] = None
        self.observers: List[Subject] = []

    def adicionar_observer(self, observer: Subject):
        """Adiciona observador"""
        self.observers.append(observer)
        self.carregador.adicionar_observer(observer)

    def carregar_dados_csv(self, arquivo_csv: str):
        """Carrega dados de arquivo CSV"""
        self.repository = self.carregador.carregar_dados_csv(arquivo_csv)
        return self.repository

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do sistema"""
        return self.carregador.obter_estatisticas()

    def imprimir_estatisticas(self):
        """Imprime estatísticas"""
        self.carregador.imprimir_estatisticas()


def main():
    """Função principal para demonstrar o uso do sistema refatorado"""
    print("=== SISTEMA DE ALOCAÇÃO REFATORADO ===\n")

    # Criar sistema
    sistema = SistemaCompletoRefatorado()

    try:
        # Carregar dados reais
        print("Carregando dados reais...")
        repository = sistema.carregar_dados_csv('oferta_cc_2025_1.csv')

        # Imprimir estatísticas
        sistema.imprimir_estatisticas()

        print("\n=== DADOS CARREGADOS COM SUCESSO ===")
        print(f"Matérias: {len(repository.buscar_materias())}")
        print(f"Salas: {len(repository.buscar_salas())}")

    except FileNotFoundError:
        print("Arquivo CSV não encontrado. Criando dados de exemplo...")

        # Criar dados de exemplo usando o sistema refatorado
        from ..builders.constructors import AlocadorBuilder

        builder = AlocadorBuilder()

        # Criar dados de exemplo
        materias_dados = [
            {'id': 'MAT001', 'nome': 'Cálculo I', 'inscritos': 45, 'horario': 'Segunda 08:00-10:00'},
            {'id': 'MAT002', 'nome': 'Cálculo II', 'inscritos': 38, 'horario': 'Segunda 08:00-10:00'},
            {'id': 'COMP001', 'nome': 'Programação I', 'inscritos': 30, 'horario': 'Segunda 14:00-16:00', 'precisa_lab': True},
            {'id': 'COMP002', 'nome': 'Estruturas de Dados', 'inscritos': 25, 'horario': 'Segunda 16:00-18:00', 'precisa_lab': True},
        ]

        salas_dados = [
            {'id': 'IC101', 'nome': 'Sala IC-101', 'capacidade': 50, 'tipo': 'aula', 'local': 'ic'},
            {'id': 'IC102', 'nome': 'Sala IC-102', 'capacidade': 40, 'tipo': 'aula', 'local': 'ic'},
            {'id': 'IC301', 'nome': 'Lab IC-301', 'capacidade': 35, 'tipo': 'laboratorio', 'local': 'ic'},
            {'id': 'IC302', 'nome': 'Lab IC-302', 'capacidade': 30, 'tipo': 'laboratorio', 'local': 'ic'},
        ]

        factory_manager = FactoryManager()
        materias = factory_manager.criar_multiplas_materias(materias_dados)
        salas = factory_manager.criar_multiplas_salas(salas_dados)

        alocador = builder.com_materias(materias).com_salas(salas).construir()

        print(f"Dados de exemplo criados:")
        print(f"Matérias: {len(alocador.materias)}")
        print(f"Salas: {len(alocador.salas)}")

        # Obter estatísticas
        stats = alocador.obter_estatisticas()
        print(f"\nEstatísticas:")
        print(f"Total de inscritos: {stats['total_inscritos']}")
        print(f"Capacidade total: {stats['capacidade_total']}")
        print(f"Utilização potencial: {stats['utilizacao_potencial']:.2f}%")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
