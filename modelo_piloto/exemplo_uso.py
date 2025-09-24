"""
Exemplo de uso avançado do sistema de alocação de salas.
Este arquivo demonstra como usar o sistema com dados reais.
"""

from alocacao_salas import AlocadorSalas, Materia, Sala, TipoSala, LocalSala
import pandas as pd


def criar_cenario_realista():
    """Cria um cenário mais realista com mais matérias e salas"""
    alocador = AlocadorSalas()
    
    # Matérias do semestre
    materias = [
        # Cálculo e Matemática
        Materia("CALC1", "Cálculo Diferencial e Integral I", 60, "Segunda 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("CALC2", "Cálculo Diferencial e Integral II", 55, "Segunda 10:00-12:00", False, ["projetor", "quadro"]),
        Materia("CALC3", "Cálculo Diferencial e Integral III", 45, "Segunda 14:00-16:00", False, ["projetor", "quadro"]),
        Materia("ALG", "Álgebra Linear", 50, "Segunda 16:00-18:00", False, ["projetor", "quadro"]),
        
        # Programação e Computação
        Materia("PROG1", "Programação I", 40, "Terça 08:00-10:00", True, ["computadores"]),
        Materia("PROG2", "Programação II", 35, "Terça 10:00-12:00", True, ["computadores"]),
        Materia("ED", "Estruturas de Dados", 30, "Terça 14:00-16:00", True, ["computadores"]),
        Materia("ALGOR", "Algoritmos e Complexidade", 25, "Terça 16:00-18:00", False, ["projetor", "quadro"]),
        
        # Banco de Dados e Sistemas
        Materia("BD1", "Banco de Dados I", 35, "Quarta 08:00-10:00", True, ["computadores"]),
        Materia("BD2", "Banco de Dados II", 30, "Quarta 10:00-12:00", True, ["computadores"]),
        Materia("SO", "Sistemas Operacionais", 40, "Quarta 14:00-16:00", True, ["computadores"]),
        Materia("REDES", "Redes de Computadores", 28, "Quarta 16:00-18:00", True, ["computadores"]),
        
        # Inteligência Artificial e Machine Learning
        Materia("IA", "Inteligência Artificial", 25, "Quinta 08:00-10:00", True, ["computadores"]),
        Materia("ML", "Machine Learning", 20, "Quinta 10:00-12:00", True, ["computadores"]),
        Materia("ESTAT", "Estatística", 45, "Quinta 14:00-16:00", False, ["projetor", "quadro"]),
        Materia("PROB", "Probabilidade", 40, "Quinta 16:00-18:00", False, ["projetor", "quadro"]),
        
        # Engenharia de Software
        Materia("ES1", "Engenharia de Software I", 30, "Sexta 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("ES2", "Engenharia de Software II", 25, "Sexta 10:00-12:00", True, ["computadores"]),
        Materia("TESTES", "Testes de Software", 20, "Sexta 14:00-16:00", True, ["computadores"]),
        
        # Matérias adicionais para distribuir melhor os horários
        Materia("CALC4", "Cálculo Numérico", 30, "Segunda 18:00-20:00", False, ["projetor", "quadro"]),
        Materia("COMP7", "Compiladores", 25, "Terça 18:00-20:00", True, ["computadores"]),
    ]
    
    for materia in materias:
        alocador.adicionar_materia(materia)
    
    # Salas disponíveis
    salas = [
        # Salas do IC (preferidas - custo 0)
        Sala("IC101", "Auditório IC-101", 80, TipoSala.AUDITORIO, LocalSala.IC, 
             ["projetor", "quadro", "som"], 0.0),
        Sala("IC102", "Sala IC-102", 60, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC103", "Sala IC-103", 50, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC104", "Sala IC-104", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC201", "Sala IC-201", 35, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC202", "Sala IC-202", 30, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        
        # Laboratórios do IC
        Sala("IC301", "Lab IC-301", 35, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC302", "Lab IC-302", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC303", "Lab IC-303", 25, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC304", "Lab IC-304", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC305", "Lab IC-305", 25, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        
        # Salas do IM (penalizadas - custo alto)
        Sala("IM101", "Auditório IM-101", 100, TipoSala.AUDITORIO, LocalSala.IM, 
             ["projetor", "quadro", "som"], 20.0),
        Sala("IM102", "Sala IM-102", 70, TipoSala.AULA, LocalSala.IM, 
             ["projetor", "quadro"], 15.0),
        Sala("IM103", "Sala IM-103", 55, TipoSala.AULA, LocalSala.IM, 
             ["projetor", "quadro"], 15.0),
        Sala("IM201", "Sala IM-201", 45, TipoSala.AULA, LocalSala.IM, 
             ["projetor", "quadro"], 15.0),
        Sala("IM202", "Sala IM-202", 35, TipoSala.AULA, LocalSala.IM, 
             ["projetor", "quadro"], 15.0),
        
        # Laboratório do IM
        Sala("IM301", "Lab IM-301", 25, TipoSala.LABORATORIO, LocalSala.IM, 
             ["computadores", "projetor"], 25.0),
    ]
    
    for sala in salas:
        alocador.adicionar_sala(sala)
    
    return alocador


def analisar_resultados(alocador):
    """Analisa os resultados da alocação"""
    if not alocador.solucao:
        print("Nenhuma solução encontrada para análise")
        return
    
    df = alocador.obter_resultados()
    
    print("=== ANÁLISE DETALHADA DOS RESULTADOS ===\n")
    
    # Estatísticas gerais
    print("1. ESTATÍSTICAS GERAIS:")
    print(f"   - Total de matérias alocadas: {len(df)}")
    print(f"   - Espaço ocioso total: {df['Espaco_Ocioso'].sum()}")
    print(f"   - Utilização média: {df['Utilizacao_%'].mean():.2f}%")
    print(f"   - Utilização mediana: {df['Utilizacao_%'].median():.2f}%")
    print()
    
    # Análise por local
    print("2. ANÁLISE POR LOCAL:")
    ic_utilizacao = df[df['Local'] == 'ic']['Utilizacao_%'].mean()
    im_utilizacao = df[df['Local'] == 'im']['Utilizacao_%'].mean()
    
    print(f"   - Salas do IC: {len(df[df['Local'] == 'ic'])} matérias, "
          f"utilização média: {ic_utilizacao:.2f}%")
    print(f"   - Salas do IM: {len(df[df['Local'] == 'im'])} matérias, "
          f"utilização média: {im_utilizacao:.2f}%")
    print()
    
    # Análise por tipo de sala
    print("3. ANÁLISE POR TIPO DE SALA:")
    for tipo in df['Tipo_Sala'].unique():
        tipo_df = df[df['Tipo_Sala'] == tipo]
        print(f"   - {tipo.upper()}: {len(tipo_df)} matérias, "
              f"utilização média: {tipo_df['Utilizacao_%'].mean():.2f}%")
    print()
    
    # Salas mais e menos utilizadas
    print("4. SALAS COM MAIOR E MENOR UTILIZAÇÃO:")
    salas_utilizacao = df.groupby('Sala')['Utilizacao_%'].mean().sort_values(ascending=False)
    print("   Top 3 mais utilizadas:")
    for sala, util in salas_utilizacao.head(3).items():
        print(f"     - {sala}: {util:.2f}%")
    print("   Top 3 menos utilizadas:")
    for sala, util in salas_utilizacao.tail(3).items():
        print(f"     - {sala}: {util:.2f}%")
    print()
    
    # Conflitos de horário (deveria ser zero)
    print("5. VERIFICAÇÃO DE CONFLITOS:")
    conflitos = df.groupby(['Sala', 'Horario']).size()
    conflitos = conflitos[conflitos > 1]
    if len(conflitos) == 0:
        print("   ✓ Nenhum conflito de horário detectado")
    else:
        print(f"   ✗ {len(conflitos)} conflitos de horário detectados:")
        for (sala, horario), count in conflitos.items():
            print(f"     - {sala} no horário {horario}: {count} matérias")
    print()


def comparar_cenarios():
    """Compara diferentes cenários de alocação"""
    print("=== COMPARAÇÃO DE CENÁRIOS ===\n")
    
    # Cenário 1: Com penalização para IM
    print("CENÁRIO 1: Com penalização para salas do IM")
    alocador1 = criar_cenario_realista()
    sucesso1 = alocador1.resolver()
    
    if sucesso1:
        df1 = alocador1.obter_resultados()
        im_count1 = len(df1[df1['Local'] == 'im'])
        print(f"   - Matérias em salas do IM: {im_count1}")
        print(f"   - Utilização média: {df1['Utilizacao_%'].mean():.2f}%")
        print(f"   - Espaço ocioso total: {df1['Espaco_Ocioso'].sum()}")
    
    print()
    
    # Cenário 2: Sem penalização (todos os custos iguais)
    print("CENÁRIO 2: Sem penalização (custos iguais)")
    alocador2 = criar_cenario_realista()
    
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
    
    print()


def main():
    """Função principal"""
    print("=== EXEMPLO AVANÇADO DE ALOCAÇÃO DE SALAS ===\n")
    
    # Criar e resolver cenário realista
    alocador = criar_cenario_realista()
    
    print(f"Dados carregados:")
    print(f"- {len(alocador.materias)} matérias")
    print(f"- {len(alocador.salas)} salas")
    print()
    
    print("Resolvendo problema...")
    sucesso = alocador.resolver()
    
    if sucesso:
        print("✓ Solução encontrada!\n")
        alocador.imprimir_resumo()
        print()
        analisar_resultados(alocador)
        
        # Salvar resultados
        df = alocador.obter_resultados()
        df.to_csv('resultados_detalhados.csv', index=False)
        print("Resultados salvos em 'resultados_detalhados.csv'")
        
        # Comparar cenários
        print()
        comparar_cenarios()
        
    else:
        print("✗ Não foi possível encontrar uma solução viável")


if __name__ == "__main__":
    main()
