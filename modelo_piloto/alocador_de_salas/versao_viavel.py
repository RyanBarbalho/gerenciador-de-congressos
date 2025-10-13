"""
Versão viável do alocador de salas com dados reais.
Adiciona salas extras e ajusta capacidades para tornar o problema solucionável.
"""

from carregador_dados_reais_fixed import CarregadorDadosReais
from alocador_salas import AlocadorSalas, Sala, TipoSala, LocalSala
import pandas as pd


def criar_salas_extras(alocador: AlocadorSalas):
    """Adiciona salas extras para tornar o problema viável"""
    print("=== ADICIONANDO SALAS EXTRAS ===")
    
    # Calcular necessidades
    total_alunos_lab = sum(m.inscritos for m in alocador.materias if m.precisa_lab)
    total_alunos_aula = sum(m.inscritos for m in alocador.materias if not m.precisa_lab)
    
    capacidade_lab_atual = sum(s.capacidade for s in alocador.salas if s.tipo == TipoSala.LABORATORIO)
    capacidade_aula_atual = sum(s.capacidade for s in alocador.salas if s.tipo in [TipoSala.AULA, TipoSala.AUDITORIO])
    
    print(f"Necessidade de laboratórios: {total_alunos_lab} alunos")
    print(f"Capacidade atual de laboratórios: {capacidade_lab_atual}")
    print(f"Deficit: {total_alunos_lab - capacidade_lab_atual}")
    
    print(f"Necessidade de salas de aula: {total_alunos_aula} alunos")
    print(f"Capacidade atual de salas de aula: {capacidade_aula_atual}")
    print(f"Deficit: {total_alunos_aula - capacidade_aula_atual}")
    
    # Adicionar laboratórios extras
    laboratorios_extras = [
        Sala("LAB_EXTRA_1", "Lab IC-401", 40, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("LAB_EXTRA_2", "Lab IC-402", 35, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("LAB_EXTRA_3", "Lab IC-403", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("LAB_EXTRA_4", "Lab IC-404", 25, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
        Sala("LAB_EXTRA_5", "Lab IC-405", 30, TipoSala.LABORATORIO, LocalSala.IC, 
             ["computadores", "projetor"], 0.0),
    ]
    
    # Adicionar salas de aula extras
    salas_aula_extras = [
        Sala("AULA_EXTRA_1", "Sala IC-501", 60, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("AULA_EXTRA_2", "Sala IC-502", 50, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("AULA_EXTRA_3", "Sala IC-503", 45, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("AULA_EXTRA_4", "Sala IC-504", 40, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("AULA_EXTRA_5", "Sala IC-505", 35, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
        Sala("AULA_EXTRA_6", "Sala IC-506", 30, TipoSala.AULA, LocalSala.IC, 
             ["projetor", "quadro"], 0.0),
    ]
    
    # Adicionar auditórios extras
    auditorios_extras = [
        Sala("AUD_EXTRA_1", "Auditório IC-201", 100, TipoSala.AUDITORIO, LocalSala.IC, 
             ["projetor", "quadro", "som"], 0.0),
        Sala("AUD_EXTRA_2", "Auditório IC-202", 80, TipoSala.AUDITORIO, LocalSala.IC, 
             ["projetor", "quadro", "som"], 0.0),
    ]
    
    # Adicionar todas as salas extras
    for sala in laboratorios_extras + salas_aula_extras + auditorios_extras:
        alocador.adicionar_sala(sala)
    
    print(f"✓ Adicionadas {len(laboratorios_extras)} laboratórios extras")
    print(f"✓ Adicionadas {len(salas_aula_extras)} salas de aula extras")
    print(f"✓ Adicionados {len(auditorios_extras)} auditórios extras")
    
    # Recalcular capacidades
    nova_capacidade_lab = sum(s.capacidade for s in alocador.salas if s.tipo == TipoSala.LABORATORIO)
    nova_capacidade_aula = sum(s.capacidade for s in alocador.salas if s.tipo in [TipoSala.AULA, TipoSala.AUDITORIO])
    
    print(f"\nNova capacidade de laboratórios: {nova_capacidade_lab}")
    print(f"Nova capacidade de salas de aula: {nova_capacidade_aula}")
    print(f"Excesso de laboratórios: {nova_capacidade_lab - total_alunos_lab}")
    print(f"Excesso de salas de aula: {nova_capacidade_aula - total_alunos_aula}")


def ajustar_horarios_conflitantes(alocador: AlocadorSalas):
    """Ajusta horários para reduzir conflitos"""
    print("\n=== AJUSTANDO HORÁRIOS CONFLITANTES ===")
    
    # Horários alternativos disponíveis
    horarios_alternativos = [
        "Segunda 14:00-16:00", "Segunda 16:00-18:00", "Segunda 18:00-20:00",
        "Terça 14:00-16:00", "Terça 16:00-18:00", "Terça 18:00-20:00",
        "Quarta 14:00-16:00", "Quarta 16:00-18:00", "Quarta 18:00-20:00",
        "Quinta 14:00-16:00", "Quinta 16:00-18:00", "Quinta 18:00-20:00",
        "Sexta 14:00-16:00", "Sexta 16:00-18:00", "Sexta 18:00-20:00",
        "Sábado 08:00-10:00", "Sábado 10:00-12:00", "Sábado 14:00-16:00"
    ]
    
    # Agrupar por horário
    horarios = {}
    for materia in alocador.materias:
        if materia.horario not in horarios:
            horarios[materia.horario] = []
        horarios[materia.horario].append(materia)
    
    # Encontrar conflitos
    conflitos = {h: m for h, m in horarios.items() if len(m) > 1}
    
    print(f"Encontrados {len(conflitos)} horários com conflitos")
    
    # Ajustar conflitos
    horarios_usados = set(horarios.keys())
    ajustes_feitos = 0
    
    for horario, materias in conflitos.items():
        if len(materias) <= 1:
            continue
            
        print(f"\nAjustando conflito em {horario} ({len(materias)} matérias):")
        
        # Manter a primeira matéria no horário original
        primeira_materia = materias[0]
        print(f"  - {primeira_materia.nome} mantém {horario}")
        
        # Ajustar as demais matérias
        for i, materia in enumerate(materias[1:], 1):
            # Encontrar horário alternativo
            novo_horario = None
            for alt_horario in horarios_alternativos:
                if alt_horario not in horarios_usados:
                    novo_horario = alt_horario
                    break
            
            if novo_horario:
                # Atualizar horário da matéria
                materia.horario = novo_horario
                horarios_usados.add(novo_horario)
                print(f"  - {materia.nome} movida para {novo_horario}")
                ajustes_feitos += 1
            else:
                print(f"  - {materia.nome} não pôde ser ajustada (sem horários disponíveis)")
    
    print(f"\n✓ {ajustes_feitos} matérias tiveram horários ajustados")


def criar_versao_viavel(arquivo_csv: str) -> AlocadorSalas:
    """Cria uma versão viável do alocador com dados reais"""
    print("=== CRIANDO VERSÃO VIÁVEL ===")
    
    # Carregar dados originais
    carregador = CarregadorDadosReais()
    alocador = carregador.carregar_dados_completos(arquivo_csv)
    
    # Adicionar salas extras
    criar_salas_extras(alocador)
    
    # Ajustar horários conflitantes
    ajustar_horarios_conflitantes(alocador)
    
    return alocador


def analisar_solucao(alocador: AlocadorSalas):
    """Analisa a solução encontrada"""
    if not alocador.solucao:
        print("Nenhuma solução para analisar")
        return
    
    df = alocador.obter_resultados()
    
    print("\n=== ANÁLISE DA SOLUÇÃO ===")
    print(f"Total de matérias alocadas: {len(df)}")
    print(f"Utilização média: {df['Utilizacao_%'].mean():.2f}%")
    print(f"Espaço ocioso total: {df['Espaco_Ocioso'].sum()}")
    
    # Análise por tipo de sala
    print("\nUtilização por tipo de sala:")
    for tipo in df['Tipo_Sala'].unique():
        tipo_df = df[df['Tipo_Sala'] == tipo]
        print(f"  {tipo.upper()}: {len(tipo_df)} matérias, "
              f"utilização média: {tipo_df['Utilizacao_%'].mean():.2f}%")
    
    # Análise por localização
    print("\nUtilização por localização:")
    for local in df['Local'].unique():
        local_df = df[df['Local'] == local]
        print(f"  {local.upper()}: {len(local_df)} matérias, "
              f"utilização média: {local_df['Utilizacao_%'].mean():.2f}%")
    
    # Salas mais utilizadas
    print("\nSalas mais utilizadas:")
    top_salas = df.groupby('Sala')['Utilizacao_%'].mean().sort_values(ascending=False).head(5)
    for sala, util in top_salas.items():
        print(f"  {sala}: {util:.1f}%")
    
    # Salas menos utilizadas
    print("\nSalas menos utilizadas:")
    bottom_salas = df.groupby('Sala')['Utilizacao_%'].mean().sort_values(ascending=True).head(5)
    for sala, util in bottom_salas.items():
        print(f"  {sala}: {util:.1f}%")


def main():
    """Função principal"""
    print("=== ALOCADOR DE SALAS - VERSÃO VIÁVEL ===\n")
    
    # Criar versão viável
    alocador = criar_versao_viavel('oferta_cc_2025_1.csv')
    
    print(f"\n=== DADOS FINAIS ===")
    print(f"Matérias: {len(alocador.materias)}")
    print(f"Salas: {len(alocador.salas)}")
    
    # Estatísticas por tipo de sala
    tipos = {}
    for sala in alocador.salas:
        tipo = sala.tipo.value
        tipos[tipo] = tipos.get(tipo, 0) + 1
    print(f"Tipos de salas: {tipos}")
    
    # Tentar resolver
    print("\n=== RESOLVENDO PROBLEMA ===")
    sucesso = alocador.resolver()
    
    if sucesso:
        print("✓ Solução encontrada!")
        alocador.imprimir_resumo()
        analisar_solucao(alocador)
        
        # Salvar resultados
        df = alocador.obter_resultados()
        df.to_csv('resultados_alocacao_viavel.csv', index=False)
        print(f"\nResultados salvos em 'resultados_alocacao_viavel.csv'")
        
        # Salvar resumo das salas utilizadas
        salas_utilizadas = df['Sala'].unique()
        print(f"\nSalas utilizadas: {len(salas_utilizadas)} de {len(alocador.salas)}")
        
        # Salas não utilizadas
        todas_salas = {sala.nome for sala in alocador.salas}
        salas_nao_utilizadas = todas_salas - set(salas_utilizadas)
        if salas_nao_utilizadas:
            print(f"Salas não utilizadas: {sorted(salas_nao_utilizadas)}")
        
    else:
        print("✗ Ainda não foi possível encontrar solução viável")
        print("Considere adicionar mais salas ou ajustar os dados")


if __name__ == "__main__":
    main()
