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
    print("Carregando ofertas de CC e Engenharia com todas as salas do IC...\n")

    try:
        from app.services.data_loader import SistemaCompletoRefatorado
        from app.core.facade import SistemaAlocacaoFacade

        # Carregar dados de ambas as ofertas
        sistema = SistemaCompletoRefatorado()

        print("="*60)
        print("CARREGANDO OFERTA DE CIÊNCIA DA COMPUTAÇÃO")
        print("="*60)
        repository_cc = sistema.carregar_dados_csv('oferta_cc_2025_1.csv')
        materias_cc = list(repository_cc.buscar_materias())
        print(f"OK - {len(materias_cc)} matérias de CC carregadas")

        print("\n" + "="*60)
        print("CARREGANDO OFERTA DE ENGENHARIA DE COMPUTAÇÃO")
        print("="*60)
        repository_ec = sistema.carregar_dados_csv('oferta_ec_2025_1.csv')
        materias_ec = list(repository_ec.buscar_materias())
        print(f"OK - {len(materias_ec)} matérias de Engenharia carregadas")

        # Detectar e tratar matérias compartilhadas entre as ofertas
        print(f"\n" + "="*60)
        print("ANALISANDO MATÉRIAS COMPARTILHADAS")
        print("="*60)

        # Criar dicionário para detectar duplicatas reais (mesmo código, horário E professor)
        materias_por_codigo = {}
        materias_compartilhadas = []

        # Processar matérias de CC
        for materia in materias_cc:
            # Chave única: código + horário (professor não está armazenado na classe Materia)
            chave = f"{materia.id}_{materia.horario}"
            if chave in materias_por_codigo:
                # Matéria compartilhada - mesmo código e horário
                materia_existente = materias_por_codigo[chave]
                if materia.inscritos != materia_existente.inscritos:
                    print(f"  ATENÇÃO: Matéria compartilhada com inscritos diferentes!")
                    print(f"    {materia.id} - {materia.nome}")
                    print(f"    CC: {materia.inscritos} vs EC: {materia_existente.inscritos}")
                # Manter apenas uma cópia (não somar inscritos)
                materias_compartilhadas.append(f"{materia.id} - {materia.nome} ({materia.horario})")
                print(f"  MATÉRIA COMPARTILHADA: {materia.id} - {materia.nome}")
                print(f"    Mesmo código e horário - {materia_existente.inscritos} inscritos (mantendo valor original)")
            else:
                materia.id = f"CC_{materia.id}"
                materias_por_codigo[chave] = materia

        # Processar matérias de Engenharia
        for materia in materias_ec:
            # Chave única: código + horário (professor não está armazenado na classe Materia)
            chave = f"{materia.id}_{materia.horario}"
            if chave in materias_por_codigo:
                # Matéria compartilhada - mesmo código e horário
                materia_existente = materias_por_codigo[chave]
                if materia.inscritos != materia_existente.inscritos:
                    print(f"  ATENÇÃO: Matéria compartilhada com inscritos diferentes!")
                    print(f"    {materia.id} - {materia.nome}")
                    print(f"    CC: {materia_existente.inscritos} vs EC: {materia.inscritos}")
                # Manter apenas uma cópia (não somar inscritos)
                print(f"  MATÉRIA COMPARTILHADA: {materia.id} - {materia.nome}")
                print(f"    Mesmo código e horário - {materia_existente.inscritos} inscritos (mantendo valor original)")
            else:
                materia.id = f"EC_{materia.id}"
                materias_por_codigo[chave] = materia

        todas_materias = list(materias_por_codigo.values())
        print(f"\nOK - Total: {len(todas_materias)} matérias únicas")
        print(f"OK - {len(materias_compartilhadas)} matérias compartilhadas detectadas")

        if materias_compartilhadas:
            print(f"\nResumo das matérias compartilhadas:")
            for i, materia in enumerate(materias_compartilhadas, 1):
                print(f"  {i:2d}. {materia}")

        # Usar todas as salas (combinar salas de ambos os repositórios)
        salas_cc = list(repository_cc.buscar_salas())
        salas_ec = list(repository_ec.buscar_salas())

        # Combinar salas únicas (evitar duplicatas)
        todas_salas_dict = {}
        for sala in salas_cc + salas_ec:
            todas_salas_dict[sala.nome] = sala

        todas_salas = list(todas_salas_dict.values())
        print(f"OK - {len(todas_salas)} salas disponíveis")

        # Debug: mostrar distribuição de salas
        salas_if = [s for s in todas_salas if s.local.value == "if"]
        salas_ic = [s for s in todas_salas if s.local.value == "ic"]
        salas_im = [s for s in todas_salas if s.local.value == "im"]
        print(f"  - Salas do IF: {len(salas_if)}")
        print(f"  - Salas do IC: {len(salas_ic)}")
        print(f"  - Salas do IM: {len(salas_im)}")

        # Mostrar salas do IF se existirem
        if salas_if:
            print(f"\nSalas do IF disponíveis:")
            for sala in salas_if:
                print(f"  - {sala.nome} (capacidade: {sala.capacidade}, tipo: {sala.tipo_equipamento})")

        # Estatísticas combinadas
        total_inscritos = sum(m.inscritos for m in todas_materias)
        capacidade_total = sum(s.capacidade for s in todas_salas)
        utilizacao = (total_inscritos / capacidade_total) * 100 if capacidade_total > 0 else 0

        print(f"\n" + "="*60)
        print("ESTATÍSTICAS COMBINADAS")
        print("="*60)
        print(f"Total de matérias: {len(todas_materias)}")
        print(f"Total de salas: {len(todas_salas)}")
        print(f"Total de inscritos: {total_inscritos}")
        print(f"Capacidade total: {capacidade_total}")
        print(f"Utilização: {utilizacao:.1f}%")

        # Distribuição por material
        tipos_material = {0: 0, 1: 0, 2: 0, 3: 0}
        for materia in todas_materias:
            tipos_material[materia.material] += 1

        print(f"\nDistribuição por material:")
        for tipo, count in tipos_material.items():
            tipo_nome = {0: "Nenhum", 1: "Computadores", 2: "Robótica", 3: "Eletrônica"}.get(tipo, f"Tipo {tipo}")
            print(f"  {tipo_nome}: {count} matérias")

        # Executar alocação combinada
        print(f"\n" + "="*60)
        print("EXECUTANDO ALOCAÇÃO COMBINADA")
        print("="*60)

        facade = SistemaAlocacaoFacade()

        # Criar sistema combinado manualmente
        from app.repositories.alocacao_repo import AlocacaoLinearStrategy
        from app.strategies.interfaces import Compatibilidade
        from app.factories.creators import FactoryManager

        factory_manager = FactoryManager()
        compatibilidade = Compatibilidade()
        alocador = AlocacaoLinearStrategy(compatibilidade)

        resultado = alocador.alocar(todas_materias, todas_salas)

        if resultado.sucesso:
            print("OK - Alocação executada com sucesso!")
            print(f"OK - {len(resultado.alocacoes)} matérias alocadas")

            # Mostrar todas as alocações organizadas por tipo de material
            print(f"\n" + "="*80)
            print("TODAS AS ALOCAÇÕES REALIZADAS")
            print("="*80)

            # Agrupar alocações por tipo de material
            alocacoes_por_material = {
                'Nenhum': [],
                'Computadores': [],
                'Robótica': [],
                'Eletrônica': []
            }

            for alocacao in resultado.alocacoes:
                materia = alocacao.materia
                if materia.material == 0:
                    alocacoes_por_material['Nenhum'].append(alocacao)
                elif materia.material == 1:
                    alocacoes_por_material['Computadores'].append(alocacao)
                elif materia.material == 2:
                    alocacoes_por_material['Robótica'].append(alocacao)
                elif materia.material == 3:
                    alocacoes_por_material['Eletrônica'].append(alocacao)

            # Mostrar alocações por categoria
            for categoria, alocacoes in alocacoes_por_material.items():
                if alocacoes:
                    print(f"\n--- {categoria.upper()} ({len(alocacoes)} matérias) ---")
                    for i, alocacao in enumerate(alocacoes, 1):
                        materia = alocacao.materia
                        sala = alocacao.sala
                        lab_info = " [LAB]" if materia.material > 0 else ""
                        utilizacao = f"{materia.inscritos}/{sala.capacidade}"
                        percentual = (materia.inscritos / sala.capacidade) * 100 if sala.capacidade > 0 else 0
                        print(f"  {i:2d}. {materia.nome[:50]:<50} -> {sala.nome:<30} ({utilizacao:>8}) {percentual:5.1f}%{lab_info}")

            # Verificar matérias não alocadas
            materias_alocadas_ids = set(a.materia.id for a in resultado.alocacoes)
            todas_materias_ids = set(m.id for m in todas_materias)
            materias_nao_alocadas = [m for m in todas_materias if m.id not in materias_alocadas_ids]

            # Resumo final
            print(f"\n" + "="*80)
            print("RESUMO FINAL DA ALOCAÇÃO")
            print("="*80)
            print(f"Total de matérias: {len(todas_materias)}")
            print(f"Total de matérias alocadas: {len(resultado.alocacoes)}")
            
            if materias_nao_alocadas:
                print(f"⚠️  ATENÇÃO: {len(materias_nao_alocadas)} matéria(s) NÃO alocada(s)!")
                for materia in materias_nao_alocadas:
                    print(f"   - {materia.id} - {materia.nome} ({materia.inscritos} inscritos)")
            else:
                print(f"✓ Todas as matérias foram alocadas com sucesso!")
            
            # Contar salas únicas utilizadas por local
            salas_por_local = {'IC': set(), 'IM': set(), 'IF': set()}
            for alocacao in resultado.alocacoes:
                local = alocacao.sala.local.value.upper()
                salas_por_local[local].add(alocacao.sala.id)
            
            total_salas_utilizadas = len(set(a.sala.id for a in resultado.alocacoes))
            salas_unicas = {a.sala.id: a.sala for a in resultado.alocacoes}
            capacidade_total_utilizada = sum(s.capacidade for s in salas_unicas.values())
            
            print(f"\nTotal de salas utilizadas: {total_salas_utilizadas}")
            print(f"  - Salas do IC utilizadas: {len(salas_por_local['IC'])}")
            print(f"  - Salas do IM utilizadas: {len(salas_por_local['IM'])}")
            print(f"  - Salas do IF utilizadas: {len(salas_por_local['IF'])}")
            
            print(f"\nTotal de inscritos alocados: {sum(a.materia.inscritos for a in resultado.alocacoes)}")
            print(f"Capacidade total das salas utilizadas: {capacidade_total_utilizada}")

            # Estatísticas por local (com detalhamento de salas)
            locais_utilizados = {}
            salas_detalhadas_por_local = {}
            
            for alocacao in resultado.alocacoes:
                local = alocacao.sala.local.value.upper()
                
                if local not in locais_utilizados:
                    locais_utilizados[local] = {'materias': 0, 'inscritos': 0, 'capacidade': 0}
                    salas_detalhadas_por_local[local] = {}
                
                locais_utilizados[local]['materias'] += 1
                locais_utilizados[local]['inscritos'] += alocacao.materia.inscritos
                
                # Para capacidade, somar apenas uma vez por sala (não contar múltiplas vezes)
                if alocacao.sala.id not in salas_detalhadas_por_local[local]:
                    salas_detalhadas_por_local[local][alocacao.sala.id] = alocacao.sala
                    locais_utilizados[local]['capacidade'] += alocacao.sala.capacidade

            print(f"\nDistribuição por local:")
            for local in ['IC', 'IM', 'IF']:
                if local in locais_utilizados:
                    stats = locais_utilizados[local]
                    num_salas = len(salas_detalhadas_por_local[local])
                    utilizacao_local = (stats['inscritos'] / stats['capacidade']) * 100 if stats['capacidade'] > 0 else 0
                    print(f"  {local}: {stats['materias']} matérias em {num_salas} sala(s), "
                          f"{stats['inscritos']}/{stats['capacidade']} ({utilizacao_local:.1f}%)")
                    
                    # Listar salas utilizadas neste local
                    salas_nomes = [s.nome for s in salas_detalhadas_por_local[local].values()]
                    print(f"    Salas: {', '.join(salas_nomes)}")

            # Exibir métricas completas
            if resultado.metricas:
                print(f"\n" + "="*80)
                print("MÉTRICAS DE AVALIAÇÃO DA SOLUÇÃO")
                print("="*80)
                
                # 3.3.1 Métricas de Utilização
                print(f"\n--- 3.3.1 MÉTRICAS DE UTILIZAÇÃO ---")
                print(f"Utilização média: {resultado.metricas.get('utilizacao_media', 0):.2f}%")
                print(f"Espaço ocioso total: {resultado.metricas.get('espaco_ocioso_total', 0)}")
                print(f"Distribuição de utilização (variância): {resultado.metricas.get('distribuicao_utilizacao', 0):.2f}")
                
                # 3.3.2 Métricas de Eficiência
                print(f"\n--- 3.3.2 MÉTRICAS DE EFICIÊNCIA ---")
                print(f"Taxa de alocação: {resultado.metricas.get('taxa_alocacao', 0):.2f}% ({len(resultado.alocacoes)}/{len(todas_materias)} matérias)")
                print(f"Custo total: {resultado.metricas.get('custo_total', 0):.2f}")
                print(f"Número de salas utilizadas: {resultado.metricas.get('numero_salas_utilizadas', 0)}")
                
                # 3.3.3 Validação de Restrições
                print(f"\n--- 3.3.3 VALIDAÇÃO DE RESTRIÇÕES ---")
                restricoes_ok = resultado.metricas.get('todas_restricoes_satisfeitas', False)
                status_icon = "✓" if restricoes_ok else "✗"
                print(f"Todas as restrições satisfeitas: {status_icon} {restricoes_ok}")
                
                validacoes = resultado.metricas.get('validacoes', {})
                for nome, (satisfeita, mensagem) in validacoes.items():
                    icon = "✓" if satisfeita else "✗"
                    print(f"  {icon} {nome.replace('_', ' ').title()}: {mensagem}")

        else:
            print(f"ERRO na alocação: {resultado.erro}")
            print("Isso é esperado devido à capacidade insuficiente")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return False
    except ImportError as e:
        print(f"Erro de importação: {e}")
        print("Certifique-se de que todos os módulos estão disponíveis")
        return False
    except Exception as e:
        print(f"Erro durante execução: {e}")
        return False

    return True


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
