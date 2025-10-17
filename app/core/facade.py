"""
Sistema principal refatorado integrando todos os padrões de projeto.
Demonstra o uso de Factory, Builder, Strategy, Repository e Observer patterns.
"""

from typing import Dict, Any, List
from ..models.domain import Subject, Observer
from ..strategies.interfaces import CompatibilidadePadrao, CompatibilidadeFlexivel, ValidatorPadrao
from ..factories.creators import FactoryManager
from ..builders.constructors import AlocadorBuilder, SistemaAlocacaoBuilder
from ..repositories.alocacao_repo import AlocacaoLinearStrategy, AlocacaoGulosaStrategy, AlocacaoManager, AlocacaoRepository
from ..services.data_loader import CarregadorDadosRefatorado, SistemaCompletoRefatorado


class ConsoleObserver(Observer):
    """Observador para exibir progresso no console"""
    
    def on_progress(self, etapa: str, progresso: float):
        """Exibe progresso no console"""
        print(f"[{progresso:5.1f}%] {etapa}")
    
    def on_sucesso(self, resultado):
        """Exibe resultado de sucesso"""
        print(f"✓ Sucesso! {resultado.metricas['total_alocacoes']} alocações realizadas")
        print(f"  Espaço ocioso total: {resultado.metricas['espaco_ocioso_total']}")
        print(f"  Utilização média: {resultado.metricas['utilizacao_media']:.2f}%")
        print(f"  Salas do IM utilizadas: {resultado.metricas['salas_im_usadas']}")
    
    def on_erro(self, erro: str):
        """Exibe erro"""
        print(f"✗ Erro: {erro}")


class SistemaAlocacaoFacade:
    """Facade para simplificar o uso do sistema de alocação"""
    
    def __init__(self):
        self.factory_manager = FactoryManager()
        self.validator = ValidatorPadrao()
        self.observers: List[Observer] = []
        self._adicionar_observador_padrao()
    
    def _adicionar_observador_padrao(self):
        """Adiciona observador padrão"""
        observer = ConsoleObserver()
        self.observers.append(observer)
    
    def adicionar_observador(self, observer: Observer):
        """Adiciona observador personalizado"""
        self.observers.append(observer)
    
    def criar_sistema_basico(self) -> Dict[str, Any]:
        """Cria um sistema básico para demonstração"""
        print("=== CRIANDO SISTEMA BÁSICO ===")
        
        # Usar Builder Pattern
        builder = AlocadorBuilder()
        
        # Criar dados de exemplo usando Factory Pattern
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
        
        # Usar Factory Pattern para criar objetos
        materias = self.factory_manager.criar_multiplas_materias(materias_dados)
        salas = self.factory_manager.criar_multiplas_salas(salas_dados)
        
        # Usar Builder Pattern para construir sistema
        alocador = (builder
                   .com_materias(materias)
                   .com_salas(salas)
                   .com_compatibilidade_strategy(CompatibilidadePadrao())
                   .com_validator(self.validator)
                   .com_factory_manager(self.factory_manager)
                   .construir())
        
        return {
            'alocador': alocador,
            'materias': materias,
            'salas': salas
        }
    
    def executar_alocacao_linear(self, sistema: Dict[str, Any]) -> Dict[str, Any]:
        """Executa alocação usando programação linear"""
        print("\n=== EXECUTANDO ALOCAÇÃO LINEAR ===")
        
        alocador = sistema['alocador']
        materias = sistema['materias']
        salas = sistema['salas']
        
        # Usar Repository Pattern
        repository = AlocacaoRepository()
        for materia in materias:
            repository.salvar_materia(materia)
        for sala in salas:
            repository.salvar_sala(sala)
        
        # Usar Strategy Pattern para algoritmo de alocação
        strategy = AlocacaoLinearStrategy(CompatibilidadePadrao())
        
        # Usar Manager Pattern
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
            return {
                'sucesso': False,
                'erro': resultado.erro
            }
    
    def executar_alocacao_gulosa(self, sistema: Dict[str, Any]) -> Dict[str, Any]:
        """Executa alocação usando algoritmo guloso"""
        print("\n=== EXECUTANDO ALOCAÇÃO GULOSA ===")
        
        alocador = sistema['alocador']
        materias = sistema['materias']
        salas = sistema['salas']
        
        # Usar Repository Pattern
        repository = AlocacaoRepository()
        for materia in materias:
            repository.salvar_materia(materia)
        for sala in salas:
            repository.salvar_sala(sala)
        
        # Usar Strategy Pattern para algoritmo guloso
        strategy = AlocacaoGulosaStrategy(CompatibilidadeFlexivel())
        
        # Usar Manager Pattern
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
            return {
                'sucesso': False,
                'erro': resultado.erro
            }
    
    def carregar_dados_csv(self, arquivo_csv: str) -> Dict[str, Any]:
        """Carrega dados de arquivo CSV"""
        print(f"\n=== CARREGANDO DADOS DE {arquivo_csv} ===")
        
        try:
            # Usar sistema completo refatorado
            sistema_completo = SistemaCompletoRefatorado()
            
            # Adicionar observadores
            for observer in self.observers:
                sistema_completo.adicionar_observer(observer)
            
            # Carregar dados
            repository = sistema_completo.carregar_dados_csv(arquivo_csv)
            
            # Obter estatísticas
            stats = sistema_completo.obter_estatisticas()
            sistema_completo.imprimir_estatisticas()
            
            return {
                'sucesso': True,
                'repository': repository,
                'estatisticas': stats,
                'materias': repository.buscar_materias(),
                'salas': repository.buscar_salas()
            }
        
        except FileNotFoundError:
            print(f"Arquivo {arquivo_csv} não encontrado")
            return {'sucesso': False, 'erro': 'Arquivo não encontrado'}
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return {'sucesso': False, 'erro': str(e)}
    
    def comparar_estrategias(self, sistema: Dict[str, Any]) -> Dict[str, Any]:
        """Compara diferentes estratégias de alocação"""
        print("\n=== COMPARANDO ESTRATÉGIAS ===")
        
        # Executar ambas as estratégias
        resultado_linear = self.executar_alocacao_linear(sistema)
        resultado_gulosa = self.executar_alocacao_gulosa(sistema)
        
        comparacao = {
            'linear': resultado_linear,
            'gulosa': resultado_gulosa
        }
        
        # Comparar métricas se ambas foram bem-sucedidas
        if resultado_linear['sucesso'] and resultado_gulosa['sucesso']:
            print("\n=== COMPARAÇÃO DE RESULTADOS ===")
            
            metricas_linear = resultado_linear['metricas']
            metricas_gulosa = resultado_gulosa['metricas']
            
            print(f"Alocação Linear:")
            print(f"  Espaço ocioso: {metricas_linear['espaco_ocioso_total']}")
            print(f"  Utilização média: {metricas_linear['utilizacao_media']:.2f}%")
            print(f"  Salas IM: {metricas_linear['salas_im_usadas']}")
            
            print(f"Alocação Gulosa:")
            print(f"  Espaço ocioso: {metricas_gulosa['espaco_ocioso_total']}")
            print(f"  Utilização média: {metricas_gulosa['utilizacao_media']:.2f}%")
            print(f"  Salas IM: {metricas_gulosa['salas_im_usadas']}")
            
            # Determinar melhor estratégia
            if metricas_linear['espaco_ocioso_total'] < metricas_gulosa['espaco_ocioso_total']:
                melhor = "Linear"
            elif metricas_gulosa['espaco_ocioso_total'] < metricas_linear['espaco_ocioso_total']:
                melhor = "Gulosa"
            else:
                melhor = "Empate"
            
            print(f"\nMelhor estratégia: {melhor}")
            comparacao['melhor_estrategia'] = melhor
        
        return comparacao


def demonstrar_padroes():
    """Demonstra o uso de todos os padrões de projeto"""
    print("=== DEMONSTRAÇÃO DOS PADRÕES DE PROJETO ===\n")
    
    # Criar facade
    facade = SistemaAlocacaoFacade()
    
    # 1. Factory Pattern - Criação de objetos
    print("1. FACTORY PATTERN - Criação consistente de objetos")
    sistema = facade.criar_sistema_basico()
    print(f"   ✓ {len(sistema['materias'])} matérias criadas")
    print(f"   ✓ {len(sistema['salas'])} salas criadas")
    
    # 2. Builder Pattern - Construção complexa
    print("\n2. BUILDER PATTERN - Construção flexível do sistema")
    print("   ✓ Sistema construído com configurações personalizadas")
    
    # 3. Strategy Pattern - Algoritmos intercambiáveis
    print("\n3. STRATEGY PATTERN - Algoritmos de alocação")
    comparacao = facade.comparar_estrategias(sistema)
    
    # 4. Repository Pattern - Gerenciamento de dados
    print("\n4. REPOSITORY PATTERN - Gerenciamento de dados")
    print("   ✓ Dados organizados em repositórios")
    
    # 5. Observer Pattern - Notificações
    print("\n5. OBSERVER PATTERN - Sistema de notificações")
    print("   ✓ Observadores notificados sobre progresso")
    
    # 6. Facade Pattern - Interface simplificada
    print("\n6. FACADE PATTERN - Interface simplificada")
    print("   ✓ Sistema complexo acessível através de interface simples")
    
    return comparacao


def main():
    """Função principal"""
    print("=== SISTEMA DE ALOCAÇÃO DE SALAS REFATORADO ===")
    print("Implementando padrões de projeto: Factory, Builder, Strategy, Repository, Observer, Facade\n")
    
    try:
        # Demonstrar padrões
        comparacao = demonstrar_padroes()
        
        # Tentar carregar dados reais
        print("\n=== TENTATIVA DE CARREGAR DADOS REAIS ===")
        dados_reais = SistemaAlocacaoFacade().carregar_dados_csv('oferta_cc_2025_1.csv')
        
        if dados_reais['sucesso']:
            print("✓ Dados reais carregados com sucesso!")
            
            # Executar alocação com dados reais
            facade_real = SistemaAlocacaoFacade()
            sistema_real = {
                'alocador': None,  # Seria criado a partir dos dados reais
                'materias': dados_reais['materias'],
                'salas': dados_reais['salas']
            }
            
            # Aqui seria executada a alocação com dados reais
            print("Sistema pronto para alocação com dados reais!")
        
    except Exception as e:
        print(f"Erro na demonstração: {e}")
        print("Continuando com dados de exemplo...")
        
        # Fallback para dados de exemplo
        facade = SistemaAlocacaoFacade()
        sistema = facade.criar_sistema_basico()
        comparacao = facade.comparar_estrategias(sistema)
    
    print("\n=== DEMONSTRAÇÃO CONCLUÍDA ===")
    print("Todos os padrões de projeto foram demonstrados com sucesso!")


if __name__ == "__main__":
    main()
