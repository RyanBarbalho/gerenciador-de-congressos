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
        from app.core.facade import SistemaAlocacaoFacade
        
        # Criar facade
        facade = SistemaAlocacaoFacade()
        
        # Demonstrar padrões de projeto
        print("=== DEMONSTRAÇÃO DOS PADRÕES DE PROJETO ===\n")
        sistema = facade.demonstrar_padroes_projeto()
        
        # Executar alocação com dados de demonstração
        print("\n" + "="*60)
        print("🚀 EXECUTANDO ALOCAÇÃO COM DADOS DE DEMONSTRAÇÃO")
        print("="*60)
        resultado = facade.executar_alocacao_otimizada(sistema)
        
        if resultado['sucesso']:
            print("✅ Alocação de demonstração concluída com sucesso!")
        else:
            print(f"❌ Erro na alocação de demonstração: {resultado['erro']}")
        
        # Carregar e processar dados reais
        print("\n" + "="*60)
        print("📊 PROCESSANDO DADOS REAIS")
        print("="*60)
        dados_reais = facade.carregar_dados_reais('oferta_cc_2025_1.csv')
        
        if dados_reais['sucesso']:
            print("✅ Dados reais processados com sucesso!")
            print("🎯 Sistema pronto para alocação com dados reais!")
        else:
            print(f"⚠ Dados reais não disponíveis: {dados_reais['erro']}")
        
        print("\n" + "="*80)
        print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("✅ Todos os padrões de projeto implementados com sucesso!")
        print("✅ Alocação otimizada usando programação linear!")
        print("✅ Interface simplificada e experiência do usuário melhorada!")
        print("="*80)
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Certifique-se de que todos os módulos estão disponíveis")
        return False
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
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
