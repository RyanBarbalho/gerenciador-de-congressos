"""
Exemplo simples e funcional do sistema de alocação de salas.
Este exemplo demonstra o uso básico com dados que garantem uma solução viável.
"""

from alocacao_salas import AlocadorSalas, Materia, Sala, TipoSala, LocalSala


def criar_exemplo_simples():
    """Cria um exemplo simples e viável"""
    alocador = AlocadorSalas()
    
    # Matérias com horários distribuídos
    materias = [
        # Segunda-feira
        Materia("MAT1", "Cálculo I", 30, "Segunda 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("COMP1", "Programação I", 25, "Segunda 10:00-12:00", True, ["computadores"]),
        Materia("MAT2", "Álgebra Linear", 35, "Segunda 14:00-16:00", False, ["projetor", "quadro"]),
        
        # Terça-feira
        Materia("COMP2", "Estruturas de Dados", 20, "Terça 08:00-10:00", True, ["computadores"]),
        Materia("MAT3", "Estatística", 40, "Terça 10:00-12:00", False, ["projetor", "quadro"]),
        Materia("COMP3", "Banco de Dados", 30, "Terça 14:00-16:00", True, ["computadores"]),
        
        # Quarta-feira
        Materia("COMP4", "Algoritmos", 25, "Quarta 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("COMP5", "Redes", 20, "Quarta 10:00-12:00", True, ["computadores"]),
        Materia("MAT4", "Probabilidade", 35, "Quarta 14:00-16:00", False, ["projetor", "quadro"]),
    ]
    
    for materia in materias:
        alocador.adicionar_materia(materia)
    
    # Salas com capacidade adequada
    salas = [
        # Salas do IC (preferidas)
        Sala("IC101", "Sala IC-101", 50, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC102", "Sala IC-102", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC103", "Sala IC-103", 35, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC201", "Lab IC-201", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC202", "Lab IC-202", 25, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC203", "Lab IC-203", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        
        # Salas do IM (penalizadas)
        Sala("IM101", "Sala IM-101", 60, TipoSala.AULA, LocalSala.IM, 
             ["projetor", "quadro"], 15.0),
        Sala("IM102", "Sala IM-102", 45, TipoSala.AULA, LocalSala.IM, 
             ["projetor", "quadro"], 15.0),
        Sala("IM201", "Lab IM-201", 35, TipoSala.LABORATORIO, LocalSala.IM, 
             ["computadores", "projetor"], 20.0),
    ]
    
    for sala in salas:
        alocador.adicionar_sala(sala)
    
    return alocador


def demonstrar_funcionalidades():
    """Demonstra as principais funcionalidades do sistema"""
    print("=== DEMONSTRAÇÃO DO SISTEMA DE ALOCAÇÃO DE SALAS ===\n")
    
    # Criar exemplo
    alocador = criar_exemplo_simples()
    
    print("1. DADOS CARREGADOS:")
    print(f"   - {len(alocador.materias)} matérias")
    print(f"   - {len(alocador.salas)} salas")
    print()
    
    # Mostrar matérias
    print("2. MATÉRIAS:")
    for materia in alocador.materias:
        lab_str = " (Lab)" if materia.precisa_lab else ""
        print(f"   - {materia.nome}: {materia.inscritos} alunos{lab_str} - {materia.horario}")
    print()
    
    # Mostrar salas
    print("3. SALAS:")
    for sala in alocador.salas:
        custo_str = f" (custo: {sala.custo_adicional})" if sala.custo_adicional > 0 else ""
        print(f"   - {sala.nome}: {sala.capacidade} lugares - {sala.tipo.value} - {sala.local.value}{custo_str}")
    print()
    
    # Resolver problema
    print("4. RESOLVENDO PROBLEMA...")
    sucesso = alocador.resolver()
    
    if sucesso:
        print("   ✓ Solução encontrada!\n")
        
        # Mostrar resultados
        print("5. RESULTADOS DA ALOCAÇÃO:")
        alocador.imprimir_resumo()
        
        # Análise detalhada
        print("\n6. ANÁLISE DETALHADA:")
        df = alocador.obter_resultados()
        
        # Estatísticas
        print(f"   - Utilização média: {df['Utilizacao_%'].mean():.2f}%")
        print(f"   - Espaço ocioso total: {df['Espaco_Ocioso'].sum()}")
        
        # Distribuição por local
        ic_count = len(df[df['Local'] == 'ic'])
        im_count = len(df[df['Local'] == 'im'])
        print(f"   - Matérias no IC: {ic_count}")
        print(f"   - Matérias no IM: {im_count}")
        
        # Salas mais utilizadas
        print("\n   Salas mais utilizadas:")
        top_salas = df.groupby('Sala')['Utilizacao_%'].mean().sort_values(ascending=False).head(3)
        for sala, util in top_salas.items():
            print(f"     - {sala}: {util:.1f}%")
        
        # Salvar resultados
        df.to_csv('exemplo_simples_resultados.csv', index=False)
        print(f"\n7. Resultados salvos em 'exemplo_simples_resultados.csv'")
        
    else:
        print("   ✗ Não foi possível encontrar uma solução viável")
        print("   Isso pode acontecer quando há conflitos de horário ou")
        print("   incompatibilidades entre matérias e salas disponíveis.")


def demonstrar_penalizacao():
    """Demonstra o efeito da penalização para salas do IM"""
    print("\n" + "="*60)
    print("=== DEMONSTRAÇÃO DO EFEITO DA PENALIZAÇÃO ===\n")
    
    # Cenário 1: Com penalização
    print("CENÁRIO 1: Com penalização para salas do IM")
    alocador1 = criar_exemplo_simples()
    sucesso1 = alocador1.resolver()
    
    if sucesso1:
        df1 = alocador1.obter_resultados()
        im_count1 = len(df1[df1['Local'] == 'im'])
        print(f"   - Matérias em salas do IM: {im_count1}")
        print(f"   - Utilização média: {df1['Utilizacao_%'].mean():.2f}%")
        print(f"   - Espaço ocioso total: {df1['Espaco_Ocioso'].sum()}")
    
    # Cenário 2: Sem penalização
    print("\nCENÁRIO 2: Sem penalização (custos iguais)")
    alocador2 = criar_exemplo_simples()
    
    # Remove penalizações
    for sala in alocador2.salas:
        sala.custo_adicional = 0.0
    
    sucesso2 = alocador2.resolver()
    
    if sucesso2:
        df2 = alocador2.obter_resultados()
        im_count2 = len(df2[df2['Local'] == 'im'])
        print(f"   - Matérias em salas do IM: {im_count2}")
        print(f"   - Utilização média: {df2['Utilizacao_%'].mean():.2f}%")
        print(f"   - Espaço ocioso total: {df2['Espaco_Ocioso'].sum()}")
        
        print(f"\nDiferença: {im_count2 - im_count1} matérias a mais no IM sem penalização")


def main():
    """Função principal"""
    demonstrar_funcionalidades()
    demonstrar_penalizacao()
    
    print("\n" + "="*60)
    print("=== CONCLUSÃO ===")
    print("O sistema de alocação de salas implementa com sucesso:")
    print("✓ Minimização de espaços ociosos")
    print("✓ Preferência por salas do IC sobre IM")
    print("✓ Respeito às capacidades das salas")
    print("✓ Compatibilidade de materiais")
    print("✓ Evitação de conflitos de horário")
    print("✓ Análise detalhada dos resultados")


if __name__ == "__main__":
    main()
