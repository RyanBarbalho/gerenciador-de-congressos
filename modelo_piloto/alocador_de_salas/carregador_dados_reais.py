"""
Carregador de dados reais da oferta de Ciência da Computação.
Converte os dados do CSV para o formato usado pelo alocador.
"""

import pandas as pd
from typing import List
from alocacao_salas import AlocadorSalas, Materia, Sala, TipoSala, LocalSala
from util import converter_para_formato_alocador, extrair_requisitos_sala, determinar_tipo_sala


def carregar_dados_csv(caminho_csv: str) -> pd.DataFrame:
    """
    Carrega os dados do CSV da oferta.
    
    Args:
        caminho_csv: Caminho para o arquivo CSV
        
    Returns:
        DataFrame com os dados carregados
    """
    df = pd.read_csv(caminho_csv)
    return df


def criar_alocador_com_dados_reais(caminho_csv: str) -> AlocadorSalas:
    """
    Cria um alocador com os dados reais da oferta de CC.
    
    Args:
        caminho_csv: Caminho para o arquivo CSV da oferta
        
    Returns:
        AlocadorSalas configurado com os dados reais
    """
    # Carregar dados do CSV
    df = carregar_dados_csv(caminho_csv)
    
    # Criar alocador
    alocador = AlocadorSalas()
    
    # Processar matérias
    contador_materias = {}  # Para controlar matérias duplicadas
    
    for _, row in df.iterrows():
        # Converter horário para formato do alocador
        horario_legivel = converter_para_formato_alocador(row['horario'])
        
        # Determinar se precisa de laboratório
        precisa_lab = determinar_tipo_sala(row['nome'], row['codigo'], row['capacidade']) == 'LABORATORIO'
        
        # Extrair requisitos de materiais
        materiais = extrair_requisitos_sala(row['nome'], row['codigo'])
        
        # Criar ID único para matérias duplicadas
        codigo_base = row['codigo']
        if codigo_base in contador_materias:
            contador_materias[codigo_base] += 1
            materia_id = f"{codigo_base}_T{contador_materias[codigo_base]}"
        else:
            contador_materias[codigo_base] = 1
            materia_id = codigo_base
        
        # Criar matéria
        materia = Materia(
            id=materia_id,
            nome=row['nome'],
            inscritos=row['matriculados'],
            horario=horario_legivel,
            precisa_lab=precisa_lab,
            materiais_necessarios=materiais
        )
        
        alocador.adicionar_materia(materia)
    
    # Criar salas baseadas nas necessidades reais
    salas = criar_salas_ic()
    for sala in salas:
        alocador.adicionar_sala(sala)
    
    return alocador


def criar_salas_ic() -> List[Sala]:
    """
    Cria as salas disponíveis no IC baseadas nas necessidades reais.
    
    Returns:
        Lista de salas do IC
    """
    salas = [
        # Auditórios
        Sala("IC_AUD_01", "Auditório IC-101", 80, TipoSala.AUDITORIO, LocalSala.IC, 
             ["projetor", "quadro", "som"], 0.0),
        Sala("IC_AUD_02", "Auditório IC-102", 100, TipoSala.AUDITORIO, LocalSala.IC, 
             ["projetor", "quadro", "som"], 0.0),
        
        # Salas de aula pequenas (até 40 alunos)
        Sala("IC_AULA_01", "Sala IC-201", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_02", "Sala IC-202", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_03", "Sala IC-203", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_04", "Sala IC-204", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_05", "Sala IC-205", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        
        # Salas de aula médias (40-60 alunos)
        Sala("IC_AULA_06", "Sala IC-301", 60, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_07", "Sala IC-302", 60, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_08", "Sala IC-303", 60, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_09", "Sala IC-304", 60, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        
        # Salas de aula grandes (60+ alunos)
        Sala("IC_AULA_10", "Sala IC-401", 80, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("IC_AULA_11", "Sala IC-402", 80, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        
        # Laboratórios pequenos (até 30 alunos)
        Sala("IC_LAB_01", "Lab IC-501", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC_LAB_02", "Lab IC-502", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC_LAB_03", "Lab IC-503", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC_LAB_04", "Lab IC-504", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC_LAB_05", "Lab IC-505", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        
        # Laboratórios médios (30-50 alunos)
        Sala("IC_LAB_06", "Lab IC-601", 50, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC_LAB_07", "Lab IC-602", 50, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC_LAB_08", "Lab IC-603", 50, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        
        # Laboratórios grandes (50+ alunos)
        Sala("IC_LAB_09", "Lab IC-701", 70, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("IC_LAB_10", "Lab IC-702", 70, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
    ]
    
    return salas


def analisar_dados_reais(caminho_csv: str):
    """
    Analisa os dados reais da oferta para entender as necessidades.
    
    Args:
        caminho_csv: Caminho para o arquivo CSV da oferta
    """
    df = carregar_dados_csv(caminho_csv)
    
    print("=== ANÁLISE DOS DADOS REAIS ===\n")
    
    # Estatísticas gerais
    print(f"Total de matérias: {len(df)}")
    print(f"Total de alunos matriculados: {df['matriculados'].sum()}")
    print(f"Capacidade total necessária: {df['capacidade'].sum()}")
    print()
    
    # Análise por tipo de matéria
    print("=== ANÁLISE POR TIPO DE MATÉRIA ===")
    df['tipo_sala'] = df.apply(lambda row: determinar_tipo_sala(row['nome'], row['codigo'], row['capacidade']), axis=1)
    
    for tipo in df['tipo_sala'].unique():
        tipo_df = df[df['tipo_sala'] == tipo]
        print(f"{tipo.upper()}: {len(tipo_df)} matérias, {tipo_df['matriculados'].sum()} alunos")
    
    print()
    
    # Análise de horários
    print("=== ANÁLISE DE HORÁRIOS ===")
    horarios_unicos = df['horario'].unique()
    print(f"Total de horários únicos: {len(horarios_unicos)}")
    
    # Mostrar alguns exemplos de horários decodificados
    print("\nExemplos de horários decodificados:")
    for i, horario in enumerate(horarios_unicos[:5]):
        try:
            horario_legivel = converter_para_formato_alocador(horario)
            print(f"  {horario} -> {horario_legivel}")
        except Exception as e:
            print(f"  {horario} -> ERRO: {e}")
    
    print()
    
    # Análise de capacidade
    print("=== ANÁLISE DE CAPACIDADE ===")
    print(f"Capacidade mínima necessária: {df['capacidade'].min()}")
    print(f"Capacidade máxima necessária: {df['capacidade'].max()}")
    print(f"Capacidade média necessária: {df['capacidade'].mean():.1f}")
    print(f"Capacidade mediana necessária: {df['capacidade'].median():.1f}")
    
    # Distribuição de capacidades
    print("\nDistribuição de capacidades:")
    distribuicao = df['capacidade'].value_counts().sort_index()
    for cap, count in distribuicao.items():
        print(f"  {cap} alunos: {count} matérias")


def main():
    """Função principal para testar o carregador"""
    print("=== CARREGADOR DE DADOS REAIS ===\n")
    
    # Analisar dados
    analisar_dados_reais('oferta_cc_2025_1.csv')
    
    print("\n" + "="*50)
    print("CRIANDO ALOCADOR COM DADOS REAIS...")
    print("="*50)
    
    # Criar alocador com dados reais
    alocador = criar_alocador_com_dados_reais('oferta_cc_2025_1.csv')
    
    print(f"Dados carregados:")
    print(f"- {len(alocador.materias)} matérias")
    print(f"- {len(alocador.salas)} salas")
    
    # Mostrar algumas matérias como exemplo
    print("\nExemplos de matérias carregadas:")
    for i, materia in enumerate(alocador.materias[:5]):
        print(f"  {materia.id}: {materia.nome} ({materia.inscritos} alunos) - {materia.horario}")
    
    print(f"\n... e mais {len(alocador.materias) - 5} matérias")


if __name__ == "__main__":
    main()
