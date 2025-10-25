"""
Facade para alocação de salas usando programação linear
Implementa padrões de projeto: Factory, Builder, Strategy, Repository, Observer, Facade
"""

from typing import Dict, Any, List
from ..models.domain import Observer
from ..factories.creators import FactoryManager
from ..builders.constructors import AlocadorBuilder
from ..repositories.alocacao_repo import AlocacaoLinearStrategy, AlocacaoRepository, AlocacaoManager
from ..services.data_loader import CarregadorDadosRefatorado
from ..strategies.interfaces import CompatibilidadePadrao


class ConsoleObserver(Observer):
    """Observador para exibir progresso no console"""

    def on_progress(self, etapa: str, progresso: float):
        print(f"[{progresso:5.1f}%] {etapa}")

    def on_sucesso(self, resultado):
        print(f"Alocação concluída com sucesso!")
        print(f"  {resultado.metricas['total_alocacoes']} matérias alocadas")
        print(f"  Utilização média: {resultado.metricas['utilizacao_media']:.1f}%")
        print(f"  Salas utilizadas: {len(set(a.sala.id for a in resultado.alocacoes))}")
        print(f"  Custo total: R$ {resultado.metricas.get('custo_total', 0):.2f}")
        self._mostrar_resumo_por_sala(resultado.alocacoes)

    def on_erro(self, erro: str):
        print(f"Erro na alocação: {erro}")

    def _mostrar_resumo_por_sala(self, alocacoes):
        """Mostra resumo das alocações por sala"""
        if not alocacoes:
            return

        print("\n" + "="*80)
        print("RESUMO DAS ALOCAÇÕES POR SALA")
        print("="*80)

        # Agrupar alocações por sala
        salas_materias = {}
        for alocacao in alocacoes:
            sala_id = alocacao.sala.id
            if sala_id not in salas_materias:
                salas_materias[sala_id] = {'sala': alocacao.sala, 'materias': []}
            salas_materias[sala_id]['materias'].append(alocacao)

        # Mostrar resumo por sala
        for sala_id in sorted(salas_materias.keys()):
            info_sala = salas_materias[sala_id]
            sala = info_sala['sala']
            materias = info_sala['materias']

            total_alunos = sum(m.inscritos for m in [a.materia for a in materias])
            utilizacao_media = sum(a.utilizacao_percentual for a in materias) / len(materias)

            print(f"\n{sala.nome}")
            print(f"   {sala.local.value.upper()} | {sala.tipo.value.upper()} | {sala.capacidade} lugares")
            print(f"   {len(materias)} matérias | {total_alunos} alunos | {utilizacao_media:.1f}% utilização")
            print("   " + "-"*60)

            for alocacao in sorted(materias, key=lambda a: a.materia.nome):
                materia = alocacao.materia
                lab_info = " [LAB]" if materia.precisa_lab else ""
                print(f"   • {materia.nome}{lab_info}")
                print(f"     {materia.horario}")
                print(f"     {materia.inscritos} alunos | {alocacao.utilizacao_percentual:.1f}% | {alocacao.espaco_ocioso} vagas ociosas")

        self._mostrar_resumo_por_horario(alocacoes)

    def _mostrar_resumo_por_horario(self, alocacoes):
        """Mostra resumo das alocações por horário"""
        if not alocacoes:
            return

        print("\n" + "="*80)
        print("RESUMO DAS ALOCAÇÕES POR HORÁRIO")
        print("="*80)

        # Agrupar alocações por horário
        horarios_materias = {}
        for alocacao in alocacoes:
            horario = alocacao.materia.horario
            if horario not in horarios_materias:
                horarios_materias[horario] = []
            horarios_materias[horario].append(alocacao)

        # Mostrar resumo por horário
        for horario in sorted(horarios_materias.keys()):
            materias_horario = horarios_materias[horario]
            total_alunos = sum(m.inscritos for m in [a.materia for a in materias_horario])

            print(f"\n{horario}")
            print(f"   {len(materias_horario)} matérias | {total_alunos} alunos")
            print("   " + "-"*60)

            for alocacao in sorted(materias_horario, key=lambda a: a.materia.nome):
                materia = alocacao.materia
                sala = alocacao.sala
                lab_info = " [LAB]" if materia.precisa_lab else ""
                print(f"   • {materia.nome}{lab_info}")
                print(f"     {sala.nome} ({sala.tipo.value.upper()}) - {sala.local.value.upper()}")
                print(f"     {materia.inscritos}/{sala.capacidade} | {alocacao.utilizacao_percentual:.1f}% | {alocacao.espaco_ocioso} vagas")


class SistemaAlocacaoFacade:
    """Facade para alocação de salas usando programação linear"""

    def __init__(self):
        self.factory_manager = FactoryManager()
        self.observers: List[Observer] = []
        self._adicionar_observador_padrao()

    def _adicionar_observador_padrao(self):
        """Adiciona observador padrão"""
        self.observers.append(ConsoleObserver())

    def adicionar_observador(self, observer: Observer):
        """Adiciona observador personalizado"""
        self.observers.append(observer)

    def criar_sistema_basico(self) -> Dict[str, Any]:
        """Cria um sistema básico para demonstração"""
        print("\n" + "="*60)
        print("CRIANDO SISTEMA DE DEMONSTRAÇÃO")
        print("="*60)

        # Dados de exemplo
        materias_dados = [
            {'id': 'MAT001', 'nome': 'Cálculo I', 'inscritos': 45, 'horario': 'Segunda 08:00-10:00'},
            {'id': 'MAT002', 'nome': 'Cálculo II', 'inscritos': 38, 'horario': 'Segunda 08:00-10:00'},
            {'id': 'COMP001', 'nome': 'Programação I', 'inscritos': 30, 'horario': 'Segunda 14:00-16:00', 'precisa_lab': True},
            {'id': 'COMP002', 'nome': 'Estruturas de Dados', 'inscritos': 25, 'horario': 'Segunda 16:00-18:00', 'precisa_lab': True},
            {'id': 'COMP003', 'nome': 'Algoritmos', 'inscritos': 20, 'horario': 'Terça 08:00-10:00'},
            {'id': 'COMP004', 'nome': 'Banco de Dados', 'inscritos': 35, 'horario': 'Terça 10:00-12:00', 'precisa_lab': True},
        ]

        salas_dados = [
            {'id': 'IC101', 'nome': 'Sala IC-101', 'capacidade': 50, 'tipo': 'aula', 'local': 'ic'},
            {'id': 'IC102', 'nome': 'Sala IC-102', 'capacidade': 40, 'tipo': 'aula', 'local': 'ic'},
            {'id': 'IC201', 'nome': 'Sala IC-201', 'capacidade': 30, 'tipo': 'aula', 'local': 'ic'},
            {'id': 'IC301', 'nome': 'Lab IC-301', 'capacidade': 35, 'tipo': 'laboratorio', 'local': 'ic'},
            {'id': 'IC302', 'nome': 'Lab IC-302', 'capacidade': 30, 'tipo': 'laboratorio', 'local': 'ic'},
            {'id': 'IM101', 'nome': 'Sala IM-101', 'capacidade': 60, 'tipo': 'aula', 'local': 'im', 'custo_adicional': 10.0},
        ]

        # Criar objetos usando Factory Pattern
        materias = self.factory_manager.criar_multiplas_materias(materias_dados)
        salas = self.factory_manager.criar_multiplas_salas(salas_dados)

        print(f"{len(materias)} matérias criadas")
        print(f"{len(salas)} salas criadas")

        # Construir sistema usando Builder Pattern
        alocador = (AlocadorBuilder()
                   .com_materias(materias)
                   .com_salas(salas)
                   .com_compatibilidade_strategy(CompatibilidadePadrao())
                   .com_factory_manager(self.factory_manager)
                   .construir())

        return {'alocador': alocador, 'materias': materias, 'salas': salas}

    def executar_alocacao(self, sistema: Dict[str, Any]) -> Dict[str, Any]:
        """Executa alocação usando programação linear"""
        print("\n" + "="*60)
        print("EXECUTANDO ALOCAÇÃO (PROGRAMAÇÃO LINEAR)")
        print("="*60)

        alocador = sistema['alocador']
        materias = sistema['materias']
        salas = sistema['salas']

        # Configurar repositório
        repository = AlocacaoRepository()
        for materia in materias:
            repository.salvar_materia(materia)
        for sala in salas:
            repository.salvar_sala(sala)

        # Configurar estratégia e manager
        strategy = AlocacaoLinearStrategy(CompatibilidadePadrao())
        manager = AlocacaoManager(repository)
        manager.definir_estrategia(strategy)

        # Adicionar observadores
        for observer in self.observers:
            manager.adicionar_observer(observer)

        # Executar alocação
        resultado = manager.executar_alocacao()

        if resultado.sucesso:
            df_resultados = manager.obter_resultados_dataframe()
            return {
                'sucesso': True,
                'resultado': resultado,
                'dataframe': df_resultados,
                'metricas': resultado.metricas
            }
        else:
            return {'sucesso': False, 'erro': resultado.erro}

    def carregar_dados_reais(self, arquivo_csv: str = "oferta_cc_2025_1.csv") -> Dict[str, Any]:
        """Carrega dados reais de um arquivo CSV"""
        print("\n" + "="*60)
        print(f"CARREGANDO DADOS REAIS DE {arquivo_csv}")
        print("="*60)

        try:
            carregador = CarregadorDadosRefatorado()

            # Adicionar observadores
            for observer in self.observers:
                carregador.adicionar_observer(observer)

            # Carregar dados
            repository = carregador.carregar_dados_csv(arquivo_csv)
            materias = list(repository.buscar_materias())
            salas = list(repository.buscar_salas())

            # Mostrar estatísticas
            self._mostrar_estatisticas_dados(materias, salas)

            # Criar sistema com dados reais
            builder = AlocadorBuilder()
            alocador = (builder
                       .com_materias(materias)
                       .com_salas(salas)
                       .com_compatibilidade_strategy(CompatibilidadePadrao())
                       .com_factory_manager(self.factory_manager)
                       .construir())

            sistema_real = {'alocador': alocador, 'materias': materias, 'salas': salas}
            resultado_alocacao = self.executar_alocacao(sistema_real)

            return {
                'sucesso': True,
                'repository': repository,
                'materias': materias,
                'salas': salas,
                'alocacao': resultado_alocacao
            }

        except FileNotFoundError:
            print(f"Arquivo {arquivo_csv} não encontrado")
            return {'sucesso': False, 'erro': 'Arquivo não encontrado'}
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return {'sucesso': False, 'erro': str(e)}

    def _mostrar_estatisticas_dados(self, materias, salas):
        """Mostra estatísticas dos dados carregados"""
        print("\n" + "="*60)
        print("ESTATÍSTICAS DOS DADOS CARREGADOS")
        print("="*60)

        total_materias = len(materias)
        total_salas = len(salas)
        total_inscritos = sum(m.inscritos for m in materias)
        capacidade_total = sum(s.capacidade for s in salas)
        utilizacao_potencial = (total_inscritos / capacidade_total) * 100 if capacidade_total > 0 else 0
        materias_lab = sum(1 for m in materias if m.precisa_lab)

        print(f"Total de matérias: {total_materias}")
        print(f"Total de salas: {total_salas}")
        print(f"Total de inscritos: {total_inscritos}")
        print(f"🪑 Capacidade total: {capacidade_total}")
        print(f"Utilização potencial: {utilizacao_potencial:.2f}%")
        print(f"Matérias que precisam de laboratório: {materias_lab}")

        # Distribuição de inscritos
        inscritos = [m.inscritos for m in materias]
        print(f"\nDistribuição de inscritos:")
        print(f"   Média: {sum(inscritos)/len(inscritos):.1f} alunos")
        print(f"   Maior turma: {max(inscritos)} alunos")
        print(f"   Menor turma: {min(inscritos)} alunos")

        # Tipos de salas
        tipos_salas = {}
        for sala in salas:
            tipo = sala.tipo.value
            tipos_salas[tipo] = tipos_salas.get(tipo, 0) + 1
        print(f"\nTipos de salas: {tipos_salas}")

        # Localizações
        locais = {}
        for sala in salas:
            local = sala.local.value
            locais[local] = locais.get(local, 0) + 1
        print(f"Localizações: {locais}")

    def demonstrar_padroes_projeto(self):
        """Demonstra os padrões de projeto implementados"""
        print("\n" + "="*80)
        print("🎨 DEMONSTRAÇÃO DOS PADRÕES DE PROJETO")
        print("="*80)

        print("\n1. 🏭 FACTORY PATTERN - Criação consistente de objetos")
        sistema = self.criar_sistema_basico()

        print("\n2. BUILDER PATTERN - Construção flexível do sistema")
        print("   Sistema construído com configurações personalizadas")

        print("\n3. STRATEGY PATTERN - Algoritmos de alocação")
        print("   Estratégia de programação linear implementada")

        print("\n4. REPOSITORY PATTERN - Gerenciamento de dados")
        print("   Dados organizados em repositórios")

        print("\n5. OBSERVER PATTERN - Sistema de notificações")
        print("   Observadores notificados sobre progresso")

        print("\n6. 🎭 FACADE PATTERN - Interface simplificada")
        print("   Sistema complexo acessível através de interface simples")

        return sistema