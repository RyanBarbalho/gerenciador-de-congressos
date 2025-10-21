#!/usr/bin/env python3
"""
Sistema Principal de Alocação de Salas - Refatorado
Ponto de entrada principal para o sistema refatorado com padrões de projeto.
"""

import sys
import os

# Adicionar o diretório pai ao path para permitir imports absolutos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Função principal do sistema"""
    print("=== SISTEMA DE ALOCAÇÃO DE SALAS REFATORADO ===")
    print("Implementando padrões de projeto: Factory, Builder, Strategy, Repository, Observer, Facade\n")

    try:
        # Importar e usar o sistema refatorado
        from app.core.facade import SistemaAlocacaoFacade, demonstrar_padroes
        
        # Demonstrar todos os padrões
        comparacao = demonstrar_padroes()
        
        # Tentar carregar dados reais
        print("\n=== TENTATIVA DE CARREGAR DADOS REAIS ===")
        facade = SistemaAlocacaoFacade()
        dados_reais = facade.carregar_dados_csv('oferta_cc_2025_1.csv')
        
        if dados_reais['sucesso']:
            print("✓ Dados reais carregados com sucesso!")
            print("Sistema pronto para alocação com dados reais!")
        else:
            print("⚠ Dados reais não disponíveis, usando sistema de exemplo")
        
        print("\n=== SISTEMA FUNCIONANDO PERFEITAMENTE ===")
        print("Todos os padrões de projeto implementados com sucesso!")
        
    except ImportError as e:
        print(f"Erro de importação: {e}")
        print("Certifique-se de que todos os módulos estão disponíveis")
        return False
    except Exception as e:
        print(f"Erro durante execução: {e}")
        return False
    
    return True


def executar_teste():
    """Executa os testes do sistema"""
    print("=== EXECUTANDO TESTES DO SISTEMA ===")
    
    try:
        from app.tests.test_sistema_refatorado import main as testar_sistema
        return testar_sistema()
    except ImportError as e:
        print(f"Erro ao importar testes: {e}")
        return False
    except Exception as e:
        print(f"Erro durante testes: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Executar testes
        sucesso = executar_teste()
        sys.exit(0 if sucesso else 1)
    else:
        # Executar sistema principal
        sucesso = main()
        sys.exit(0 if sucesso else 1)
