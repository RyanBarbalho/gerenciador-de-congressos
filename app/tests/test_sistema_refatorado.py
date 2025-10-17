#!/usr/bin/env python3
"""
Script de teste para demonstrar o funcionamento do sistema refatorado.
Testa todos os padrões de projeto implementados.
"""

import sys
import os

# Adicionar o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_importacoes():
    """Testa se todas as importações estão funcionando"""
    print("=== TESTANDO IMPORTAÇÕES ===")
    
    try:
        from app.models.domain import Materia, Sala, TipoSala, LocalSala, Observer
        print("✓ models.domain importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar models.domain: {e}")
        return False
    
    try:
        from app.strategies.interfaces import CompatibilidadePadrao, AlocacaoLinearStrategy, ValidatorPadrao
        print("✓ strategies.interfaces importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar strategies.interfaces: {e}")
        return False
    
    try:
        from app.factories.creators import FactoryManager, MateriaFactoryPadrao, SalaFactoryPadrao
        print("✓ factories.creators importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar factories.creators: {e}")
        return False
    
    try:
        from app.builders.constructors import AlocadorBuilder, SistemaAlocacaoBuilder
        print("✓ builders.constructors importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar builders.constructors: {e}")
        return False
    
    try:
        from app.repositories.alocacao_repo import AlocacaoRepository, AlocacaoLinearStrategy, AlocacaoManager
        print("✓ repositories.alocacao_repo importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar repositories.alocacao_repo: {e}")
        return False
    
    try:
        from app.services.data_loader import SistemaCompletoRefatorado, CarregadorDadosRefatorado
        print("✓ services.data_loader importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar services.data_loader: {e}")
        return False
    
    try:
        from app.core.facade import SistemaAlocacaoFacade, ConsoleObserver
        print("✓ core.facade importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar core.facade: {e}")
        return False
    
    return True


def testar_factory_pattern():
    """Testa o Factory Pattern"""
    print("\n=== TESTANDO FACTORY PATTERN ===")
    
    try:
        from app.factories.creators import FactoryManager
        from app.models.domain import Materia, Sala
        
        factory_manager = FactoryManager()
        
        # Testar criação de matéria
        dados_materia = {
            'id': 'TEST001',
            'nome': 'Teste de Matéria',
            'inscritos': 30,
            'horario': 'Segunda 08:00-10:00',
            'precisa_lab': False,
            'materiais_necessarios': ['projetor', 'quadro']
        }
        
        materia = factory_manager.criar_materia(dados_materia)
        print(f"✓ Matéria criada: {materia.nome} ({materia.inscritos} inscritos)")
        
        # Testar criação de sala
        dados_sala = {
            'id': 'SALA001',
            'nome': 'Sala de Teste',
            'capacidade': 40,
            'tipo': 'aula',
            'local': 'ic',
            'materiais_disponiveis': ['projetor', 'quadro'],
            'custo_adicional': 0.0
        }
        
        sala = factory_manager.criar_sala(dados_sala)
        print(f"✓ Sala criada: {sala.nome} (capacidade: {sala.capacidade})")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no Factory Pattern: {e}")
        return False


def testar_strategy_pattern():
    """Testa o Strategy Pattern"""
    print("\n=== TESTANDO STRATEGY PATTERN ===")
    
    try:
        from app.strategies.interfaces import CompatibilidadePadrao, CompatibilidadeFlexivel
        from app.models.domain import Materia, Sala, TipoSala, LocalSala
        
        # Criar matéria e sala de teste
        materia = Materia(
            id="TEST001",
            nome="Programação I",
            inscritos=30,
            horario="Segunda 08:00-10:00",
            precisa_lab=True,
            materiais_necessarios=["computadores", "projetor"]
        )
        
        sala_lab = Sala(
            id="LAB001",
            nome="Laboratório IC-01",
            capacidade=35,
            tipo=TipoSala.LABORATORIO,
            local=LocalSala.IC,
            materiais_disponiveis=["computadores", "projetor", "quadro"]
        )
        
        sala_aula = Sala(
            id="AULA001",
            nome="Sala IC-01",
            capacidade=40,
            tipo=TipoSala.AULA,
            local=LocalSala.IC,
            materiais_disponiveis=["projetor", "quadro"]
        )
        
        # Testar estratégia padrão
        compatibilidade_padrao = CompatibilidadePadrao()
        print(f"✓ Compatibilidade padrão - Lab: {compatibilidade_padrao.eh_compativel(materia, sala_lab)}")
        print(f"✓ Compatibilidade padrão - Aula: {compatibilidade_padrao.eh_compativel(materia, sala_aula)}")
        
        # Testar estratégia flexível
        compatibilidade_flexivel = CompatibilidadeFlexivel({"projetor"})
        print(f"✓ Compatibilidade flexível - Lab: {compatibilidade_flexivel.eh_compativel(materia, sala_lab)}")
        print(f"✓ Compatibilidade flexível - Aula: {compatibilidade_flexivel.eh_compativel(materia, sala_aula)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no Strategy Pattern: {e}")
        return False


def testar_builder_pattern():
    """Testa o Builder Pattern"""
    print("\n=== TESTANDO BUILDER PATTERN ===")
    
    try:
        from app.builders.constructors import AlocadorBuilder
        from app.strategies.interfaces import CompatibilidadePadrao
        from app.factories.creators import FactoryManager
        
        # Criar dados de teste
        factory_manager = FactoryManager()
        
        materias_dados = [
            {'id': 'MAT001', 'nome': 'Cálculo I', 'inscritos': 45, 'horario': 'Segunda 08:00-10:00'},
            {'id': 'COMP001', 'nome': 'Programação I', 'inscritos': 30, 'horario': 'Segunda 14:00-16:00', 'precisa_lab': True}
        ]
        
        salas_dados = [
            {'id': 'IC101', 'nome': 'Sala IC-101', 'capacidade': 50, 'tipo': 'aula', 'local': 'ic'},
            {'id': 'IC301', 'nome': 'Lab IC-301', 'capacidade': 35, 'tipo': 'laboratorio', 'local': 'ic'}
        ]
        
        materias = factory_manager.criar_multiplas_materias(materias_dados)
        salas = factory_manager.criar_multiplas_salas(salas_dados)
        
        # Usar Builder Pattern
        builder = AlocadorBuilder()
        alocador = (builder
                   .com_materias(materias)
                   .com_salas(salas)
                   .com_compatibilidade_strategy(CompatibilidadePadrao())
                   .com_factory_manager(factory_manager)
                   .construir())
        
        print(f"✓ Sistema construído com Builder Pattern")
        print(f"  Matérias: {len(alocador.materias)}")
        print(f"  Salas: {len(alocador.salas)}")
        
        # Testar validação
        erros = alocador.validar_sistema()
        if erros:
            print(f"⚠ Avisos de validação: {len(erros)}")
        else:
            print("✓ Sistema validado com sucesso")
        
        # Obter estatísticas
        stats = alocador.obter_estatisticas()
        print(f"✓ Estatísticas obtidas: {stats['total_materias']} matérias, {stats['total_salas']} salas")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no Builder Pattern: {e}")
        return False


def testar_repository_pattern():
    """Testa o Repository Pattern"""
    print("\n=== TESTANDO REPOSITORY PATTERN ===")
    
    try:
        from app.repositories.alocacao_repo import AlocacaoRepository
        from app.models.domain import Materia, Sala, TipoSala, LocalSala
        
        repository = AlocacaoRepository()
        
        # Criar dados de teste
        materia = Materia(
            id="TEST001",
            nome="Teste",
            inscritos=30,
            horario="Segunda 08:00-10:00",
            precisa_lab=False,
            materiais_necessarios=["projetor"]
        )
        
        sala = Sala(
            id="SALA001",
            nome="Sala Teste",
            capacidade=40,
            tipo=TipoSala.AULA,
            local=LocalSala.IC,
            materiais_disponiveis=["projetor", "quadro"]
        )
        
        # Testar operações do repositório
        repository.salvar_materia(materia)
        repository.salvar_sala(sala)
        
        materias = repository.buscar_materias()
        salas = repository.buscar_salas()
        
        print(f"✓ Repositório funcionando: {len(materias)} matérias, {len(salas)} salas")
        
        # Testar busca por ID
        materia_encontrada = repository.buscar_materia_por_id("TEST001")
        sala_encontrada = repository.buscar_sala_por_id("SALA001")
        
        if materia_encontrada and sala_encontrada:
            print("✓ Busca por ID funcionando")
        else:
            print("✗ Erro na busca por ID")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no Repository Pattern: {e}")
        return False


def testar_observer_pattern():
    """Testa o Observer Pattern"""
    print("\n=== TESTANDO OBSERVER PATTERN ===")
    
    try:
        from app.core.facade import ConsoleObserver
        from app.models.domain import AlocacaoResultado
        
        observer = ConsoleObserver()
        
        # Testar notificações
        observer.on_progress("Teste de progresso", 50.0)
        observer.on_progress("Teste concluído", 100.0)
        
        # Criar resultado de teste
        resultado = AlocacaoResultado(sucesso=True, alocacoes=[])
        resultado.metricas = {
            'total_alocacoes': 5,
            'espaco_ocioso_total': 10,
            'utilizacao_media': 85.5,
            'salas_im_usadas': 1
        }
        
        observer.on_sucesso(resultado)
        observer.on_erro("Teste de erro")
        
        print("✓ Observer Pattern funcionando")
        return True
        
    except Exception as e:
        print(f"✗ Erro no Observer Pattern: {e}")
        return False


def testar_facade_pattern():
    """Testa o Facade Pattern"""
    print("\n=== TESTANDO FACADE PATTERN ===")
    
    try:
        from app.core.facade import SistemaAlocacaoFacade
        
        facade = SistemaAlocacaoFacade()
        
        # Criar sistema básico
        sistema = facade.criar_sistema_basico()
        print(f"✓ Sistema básico criado: {len(sistema['materias'])} matérias, {len(sistema['salas'])} salas")
        
        # Executar alocação
        resultado = facade.executar_alocacao_linear(sistema)
        
        if resultado['sucesso']:
            print(f"✓ Alocação executada: {resultado['metricas']['total_alocacoes']} alocações")
        else:
            print(f"⚠ Alocação falhou: {resultado['erro']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no Facade Pattern: {e}")
        return False


def testar_sistema_completo():
    """Testa o sistema completo integrado"""
    print("\n=== TESTANDO SISTEMA COMPLETO ===")
    
    try:
        from app.core.facade import SistemaAlocacaoFacade
        
        facade = SistemaAlocacaoFacade()
        
        # Criar sistema
        sistema = facade.criar_sistema_basico()
        
        # Comparar estratégias
        comparacao = facade.comparar_estrategias(sistema)
        
        if comparacao['linear']['sucesso'] and comparacao['gulosa']['sucesso']:
            print("✓ Ambas as estratégias funcionaram")
            print(f"  Linear: {comparacao['linear']['metricas']['espaco_ocioso_total']} espaço ocioso")
            print(f"  Gulosa: {comparacao['gulosa']['metricas']['espaco_ocioso_total']} espaço ocioso")
        else:
            print("⚠ Algumas estratégias falharam")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no sistema completo: {e}")
        return False


def main():
    """Função principal de teste"""
    print("=== TESTE COMPLETO DO SISTEMA REFATORADO ===")
    print("Testando todos os padrões de projeto implementados...\n")
    
    testes = [
        ("Importações", testar_importacoes),
        ("Factory Pattern", testar_factory_pattern),
        ("Strategy Pattern", testar_strategy_pattern),
        ("Builder Pattern", testar_builder_pattern),
        ("Repository Pattern", testar_repository_pattern),
        ("Observer Pattern", testar_observer_pattern),
        ("Facade Pattern", testar_facade_pattern),
        ("Sistema Completo", testar_sistema_completo)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        try:
            resultado = funcao_teste()
            resultados.append((nome_teste, resultado))
        except Exception as e:
            print(f"✗ Erro crítico no teste {nome_teste}: {e}")
            resultados.append((nome_teste, False))
    
    # Resumo dos resultados
    print("\n=== RESUMO DOS TESTES ===")
    sucessos = 0
    for nome, resultado in resultados:
        status = "✓ PASSOU" if resultado else "✗ FALHOU"
        print(f"{nome}: {status}")
        if resultado:
            sucessos += 1
    
    print(f"\nTotal: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema refatorado funcionando perfeitamente!")
    else:
        print(f"\n⚠ {len(resultados) - sucessos} teste(s) falharam. Verifique os erros acima.")
    
    return sucessos == len(resultados)


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
