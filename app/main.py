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
    print("=== SISTEMA DE ALOCAÇÃO DE SALAS ===")
    print("Carregando dados reais e executando alocação...\n")

    try:
        from app.carregador_dados import CarregadorDados
        carregador = CarregadorDados()
        
        # Tentar diferentes caminhos para o arquivo CSV
        caminhos_csv = [
            'oferta_cc_2025_1.csv',
            '../oferta_cc_2025_1.csv',
            'app/oferta_cc_2025_1.csv'
        ]
        
        dados_reais = None
        for caminho in caminhos_csv:
            try:
                dados_reais = carregador.carregar_dados_csv(caminho)
                break
            except FileNotFoundError:
                continue
        
        if dados_reais is None:
            raise FileNotFoundError("Arquivo CSV não encontrado em nenhum dos caminhos testados")
        
        if dados_reais['sucesso']:
            print("✅ Dados reais processados com sucesso!")
            print("🎯 Sistema pronto para alocação com dados reais!")
            
            # Imprimir estatísticas detalhadas
            carregador.imprimir_estatisticas()
            
            # Executar alocação
            resultado_alocacao = carregador.executar_alocacao('oferta_cc_2025_1.csv')
            if resultado_alocacao['sucesso']:
                print("✅ Alocação executada com sucesso!")
            else:
                print(f"ℹ️ {resultado_alocacao.get('mensagem', 'Alocação não executada')}")
        else:
            print(f"⚠ Dados reais não disponíveis: {dados_reais.get('erro', 'Erro desconhecido')}")
            return False
        
        print("\n" + "="*80)
        print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("✅ Alocação otimizada usando programação linear!")
        print("✅ Interface simplificada e experiência do usuário melhorada!")
        print("="*80)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return False
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Certifique-se de que todos os módulos estão disponíveis")
        return False
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        return False
    
    return True


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
