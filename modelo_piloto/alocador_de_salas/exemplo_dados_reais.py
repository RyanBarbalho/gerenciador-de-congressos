"""
Exemplo de uso do alocador com dados reais da oferta de Ciência da Computação.
"""

from carregador_dados_reais import criar_alocador_com_dados_reais, analisar_dados_reais
from alocacao_salas import AlocadorSalas
import pandas as pd
from datetime import datetime


def salvar_relatorio_detalhado(df, alocador):
    """
    Salva um relatório detalhado da alocação em arquivo de texto.
    
    Args:
        df: DataFrame com os resultados da alocação
        alocador: Instância do AlocadorSalas
    """
    with open('relatorio_alocacao.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RELATÓRIO DETALHADO DE ALOCAÇÃO DE SALAS\n")
        f.write("Ciência da Computação - 2025.1\n")
        f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # Estatísticas gerais
        f.write("1. ESTATÍSTICAS GERAIS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total de matérias alocadas: {len(df)}\n")
        f.write(f"Total de alunos: {df['Inscritos'].sum()}\n")
        f.write(f"Espaço ocioso total: {df['Espaco_Ocioso'].sum()}\n")
        f.write(f"Utilização média: {df['Utilizacao_%'].mean():.2f}%\n")
        f.write(f"Utilização mediana: {df['Utilizacao_%'].median():.2f}%\n\n")
        
        # Análise por tipo de sala
        f.write("2. ANÁLISE POR TIPO DE SALA\n")
        f.write("-" * 40 + "\n")
        for tipo in df['Tipo_Sala'].unique():
            tipo_df = df[df['Tipo_Sala'] == tipo]
            f.write(f"{tipo.upper()}:\n")
            f.write(f"  - Matérias: {len(tipo_df)}\n")
            f.write(f"  - Alunos: {tipo_df['Inscritos'].sum()}\n")
            f.write(f"  - Utilização média: {tipo_df['Utilizacao_%'].mean():.2f}%\n")
            f.write(f"  - Espaço ocioso: {tipo_df['Espaco_Ocioso'].sum()}\n\n")
        
        # Salas mais utilizadas
        f.write("3. SALAS COM MAIOR UTILIZAÇÃO\n")
        f.write("-" * 40 + "\n")
        salas_utilizacao = df.groupby('Sala')['Utilizacao_%'].mean().sort_values(ascending=False)
        for i, (sala, util) in enumerate(salas_utilizacao.head(10).items(), 1):
            f.write(f"{i:2d}. {sala}: {util:.2f}%\n")
        f.write("\n")
        
        # Salas menos utilizadas
        f.write("4. SALAS COM MENOR UTILIZAÇÃO\n")
        f.write("-" * 40 + "\n")
        for i, (sala, util) in enumerate(salas_utilizacao.tail(10).items(), 1):
            f.write(f"{i:2d}. {sala}: {util:.2f}%\n")
        f.write("\n")
        
        # Alocações por horário
        f.write("5. ALOCAÇÕES POR HORÁRIO\n")
        f.write("-" * 40 + "\n")
        horarios = df.groupby('Horario').size().sort_values(ascending=False)
        for horario, count in horarios.items():
            f.write(f"{horario}: {count} matérias\n")
        f.write("\n")
        
        # Lista completa de alocações
        f.write("6. LISTA COMPLETA DE ALOCAÇÕES\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Matéria':<50} {'Sala':<20} {'Alunos':<8} {'Capac.':<8} {'Util.':<8}\n")
        f.write("-" * 100 + "\n")
        
        for _, row in df.sort_values('Materia').iterrows():
            f.write(f"{row['Materia'][:49]:<50} {row['Sala']:<20} "
                   f"{row['Inscritos']:<8} {row['Capacidade']:<8} "
                   f"{row['Utilizacao_%']:.1f}%{'':<3}\n")
        
        f.write("\n")
        
        # Verificação de conflitos
        f.write("7. VERIFICAÇÃO DE CONFLITOS\n")
        f.write("-" * 40 + "\n")
        conflitos = df.groupby(['Sala', 'Horario']).size()
        conflitos = conflitos[conflitos > 1]
        if len(conflitos) == 0:
            f.write("✓ Nenhum conflito de horário detectado\n")
        else:
            f.write(f"✗ {len(conflitos)} conflitos de horário detectados:\n")
            for (sala, horario), count in conflitos.items():
                f.write(f"  - {sala} no horário {horario}: {count} matérias\n")
        
        f.write("\n")
        
        # Resumo das salas utilizadas
        f.write("8. RESUMO DAS SALAS UTILIZADAS\n")
        f.write("-" * 40 + "\n")
        salas_utilizadas = df['Sala'].unique()
        f.write(f"Total de salas utilizadas: {len(salas_utilizadas)}\n")
        f.write(f"Total de salas disponíveis: {len(alocador.salas)}\n")
        f.write(f"Taxa de utilização de salas: {len(salas_utilizadas)/len(alocador.salas)*100:.1f}%\n\n")
        
        # Salas não utilizadas
        salas_nao_utilizadas = [sala for sala in alocador.salas 
                               if sala.nome not in salas_utilizadas]
        if salas_nao_utilizadas:
            f.write("Salas não utilizadas:\n")
            for sala in salas_nao_utilizadas:
                f.write(f"  - {sala.nome} ({sala.capacidade} lugares, {sala.tipo.value})\n")
        else:
            f.write("Todas as salas foram utilizadas.\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("FIM DO RELATÓRIO\n")
        f.write("="*80 + "\n")


def executar_alocacao_real():
    """Executa a alocação com os dados reais"""
    print("=== ALOCAÇÃO COM DADOS REAIS - CIÊNCIA DA COMPUTAÇÃO 2025.1 ===\n")
    
    # Analisar dados primeiro
    print("1. ANALISANDO DADOS REAIS...")
    analisar_dados_reais('oferta_cc_2025_1.csv')
    
    print("\n" + "="*60)
    print("2. CRIANDO ALOCADOR COM DADOS REAIS...")
    print("="*60)
    
    # Criar alocador com dados reais
    alocador = criar_alocador_com_dados_reais('oferta_cc_2025_1.csv')
    
    print(f"Dados carregados:")
    print(f"- {len(alocador.materias)} matérias")
    print(f"- {len(alocador.salas)} salas")
    print()
    
    # Mostrar distribuição por tipo de sala necessária
    print("Distribuição das matérias por tipo de sala necessário:")
    tipos = {}
    for materia in alocador.materias:
        tipo = "LABORATORIO" if materia.precisa_lab else "AULA/AUDITORIO"
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    for tipo, count in tipos.items():
        print(f"  {tipo}: {count} matérias")
    print()
    
    # Resolver o problema
    print("3. RESOLVENDO PROBLEMA DE ALOCAÇÃO...")
    print("Isso pode levar alguns minutos...")
    
    sucesso = alocador.resolver()
    
    if sucesso:
        print("OK - Solução encontrada!\n")
        
        # Mostrar resumo
        alocador.imprimir_resumo()
        
        # Análise detalhada
        print("\n" + "="*60)
        print("4. ANÁLISE DETALHADA DOS RESULTADOS")
        print("="*60)
        
        df = alocador.obter_resultados()
        
        # Estatísticas gerais
        print(f"Total de matérias alocadas: {len(df)}")
        print(f"Total de alunos: {df['Inscritos'].sum()}")
        print(f"Espaço ocioso total: {df['Espaco_Ocioso'].sum()}")
        print(f"Utilização média: {df['Utilizacao_%'].mean():.2f}%")
        print()
        
        # Análise por tipo de sala
        print("Utilização por tipo de sala:")
        for tipo in df['Tipo_Sala'].unique():
            tipo_df = df[df['Tipo_Sala'] == tipo]
            print(f"  {tipo.upper()}: {len(tipo_df)} matérias, "
                  f"utilização média: {tipo_df['Utilizacao_%'].mean():.2f}%")
        print()
        
        # Salas mais utilizadas
        print("Salas com maior utilização:")
        salas_utilizacao = df.groupby('Sala')['Utilizacao_%'].mean().sort_values(ascending=False)
        for sala, util in salas_utilizacao.head(5).items():
            print(f"  {sala}: {util:.2f}%")
        print()
        
        # Salas menos utilizadas
        print("Salas com menor utilização:")
        for sala, util in salas_utilizacao.tail(5).items():
            print(f"  {sala}: {util:.2f}%")
        print()
        
        # Verificar conflitos
        print("Verificação de conflitos de horário:")
        conflitos = df.groupby(['Sala', 'Horario']).size()
        conflitos = conflitos[conflitos > 1]
        if len(conflitos) == 0:
            print("  OK - Nenhum conflito de horário detectado")
        else:
            print(f"  ERRO - {len(conflitos)} conflitos de horário detectados:")
            for (sala, horario), count in conflitos.items():
                print(f"    - {sala} no horário {horario}: {count} matérias")
        print()
        
        # Salvar resultados
        print("5. SALVANDO RESULTADOS...")
        df.to_csv('resultados_alocacao_real.csv', index=False)
        print("Resultados salvos em 'resultados_alocacao_real.csv'")
        
        # Salvar relatório detalhado em texto
        salvar_relatorio_detalhado(df, alocador)
        print("Relatório detalhado salvo em 'relatorio_alocacao.txt'")
        
        # Mostrar algumas alocações específicas
        print("\n6. EXEMPLOS DE ALOCAÇÕES:")
        print("Algumas matérias e suas alocações:")
        for _, row in df.head(10).iterrows():
            print(f"  {row['Materia']} -> {row['Sala']} "
                  f"({row['Inscritos']}/{row['Capacidade']}, "
                  f"{row['Utilizacao_%']:.1f}% utilizado)")
        
        if len(df) > 10:
            print(f"  ... e mais {len(df) - 10} alocações")
        
    else:
        print("ERRO - Não foi possível encontrar uma solução viável")
        print("Possíveis causas:")
        print("- Capacidade insuficiente das salas")
        print("- Conflitos de horário não resolvíveis")
        print("- Incompatibilidade entre matérias e salas")
        
        # Tentar identificar o problema
        print("\nTentando identificar o problema...")
        
        # Verificar se há matérias que precisam de laboratório
        lab_materias = [m for m in alocador.materias if m.precisa_lab]
        lab_salas = [s for s in alocador.salas if s.tipo.value == 'laboratorio']
        
        print(f"Matérias que precisam de laboratório: {len(lab_materias)}")
        print(f"Laboratórios disponíveis: {len(lab_salas)}")
        
        if len(lab_materias) > len(lab_salas):
            print("⚠️  Possível problema: Mais matérias precisam de laboratório do que laboratórios disponíveis")
        
        # Verificar capacidade total
        capacidade_total = sum(s.capacidade for s in alocador.salas)
        alunos_total = sum(m.inscritos for m in alocador.materias)
        
        print(f"Capacidade total das salas: {capacidade_total}")
        print(f"Total de alunos: {alunos_total}")
        
        if alunos_total > capacidade_total:
            print("⚠️  Possível problema: Mais alunos do que capacidade total das salas")


def comparar_cenarios():
    """Compara diferentes cenários de alocação"""
    print("\n" + "="*60)
    print("7. COMPARAÇÃO DE CENÁRIOS")
    print("="*60)
    
    # Cenário 1: Salas do IC apenas
    print("CENÁRIO 1: Apenas salas do IC")
    alocador1 = criar_alocador_com_dados_reais('oferta_cc_2025_1.csv')
    sucesso1 = alocador1.resolver()
    
    if sucesso1:
        df1 = alocador1.obter_resultados()
        print(f"  OK - Solução encontrada")
        print(f"  - Matérias alocadas: {len(df1)}")
        print(f"  - Utilização média: {df1['Utilizacao_%'].mean():.2f}%")
        print(f"  - Espaço ocioso: {df1['Espaco_Ocioso'].sum()}")
    else:
        print("  ERRO - Solução não encontrada")
    
    print()
    
    # Cenário 2: Adicionar salas do IM como backup
    print("CENÁRIO 2: Adicionando salas do IM como backup")
    alocador2 = criar_alocador_com_dados_reais('oferta_cc_2025_1.csv')
    
    # Adicionar algumas salas do IM
    from alocacao_salas import Sala, TipoSala, LocalSala
    salas_im = [
        Sala("IM_AUD_01", "Auditório IM-101", 100, TipoSala.AUDITORIO, LocalSala.IM, 
             ["projetor", "quadro", "som"], 5.0),
        Sala("IM_AULA_01", "Sala IM-201", 60, TipoSala.AULA, LocalSala.IM, 
             ["projetor", "quadro"], 3.0),
        Sala("IM_LAB_01", "Lab IM-301", 40, TipoSala.LABORATORIO, LocalSala.IM, 
             ["computadores", "projetor"], 8.0),
    ]
    
    for sala in salas_im:
        alocador2.adicionar_sala(sala)
    
    sucesso2 = alocador2.resolver()
    
    if sucesso2:
        df2 = alocador2.obter_resultados()
        im_count = len(df2[df2['Local'] == 'im'])
        print(f"  OK - Solução encontrada")
        print(f"  - Matérias alocadas: {len(df2)}")
        print(f"  - Matérias em salas do IM: {im_count}")
        print(f"  - Utilização média: {df2['Utilizacao_%'].mean():.2f}%")
        print(f"  - Espaço ocioso: {df2['Espaco_Ocioso'].sum()}")
    else:
        print("  ERRO - Solução não encontrada")


def main():
    """Função principal"""
    try:
        # Executar alocação principal
        executar_alocacao_real()
        
        # Comparar cenários
        comparar_cenarios()
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
