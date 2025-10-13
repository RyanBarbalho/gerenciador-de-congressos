"""
Exemplo de uso do alocador de salas com dados reais da oferta de disciplinas.
"""

from carregador_dados_reais import CarregadorDadosReais
from alocador_salas import AlocadorSalas
import pandas as pd


def analisar_conflitos_horarios(alocador: AlocadorSalas):
    """Analisa conflitos de horários nas matérias"""
    print("\n=== ANÁLISE DE CONFLITOS DE HORÁRIOS ===")
    
    # Agrupar por horário
    horarios = {}
    for materia in alocador.materias:
        if materia.horario not in horarios:
            horarios[materia.horario] = []
        horarios[materia.horario].append(materia)
    
    # Encontrar horários com múltiplas matérias
    conflitos = {h: m for h, m in horarios.items() if len(m) > 1}
    
    if conflitos:
        print(f"⚠️  {len(conflitos)} horários com conflitos encontrados:")
        for horario, materias in conflitos.items():
            print(f"\n  {horario}:")
            for materia in materias:
                print(f"    - {materia.nome} ({materia.inscritos} alunos)")
    else:
        print("✓ Nenhum conflito de horário encontrado")


def analisar_capacidade_salas(alocador: AlocadorSalas):
    """Analisa se as salas têm capacidade suficiente"""
    print("\n=== ANÁLISE DE CAPACIDADE DAS SALAS ===")
    
    # Calcular total de alunos por tipo de sala
    total_alunos_lab = sum(m.inscritos for m in alocador.materias if m.precisa_lab)
    total_alunos_aula = sum(m.inscritos for m in alocador.materias if not m.precisa_lab)
    
    # Calcular capacidade total por tipo
    capacidade_lab = sum(s.capacidade for s in alocador.salas if s.tipo.value == 'laboratorio')
    capacidade_aula = sum(s.capacidade for s in alocador.salas if s.tipo.value == 'aula')
    capacidade_auditorio = sum(s.capacidade for s in alocador.salas if s.tipo.value == 'auditorio')
    
    print(f"Matérias de laboratório: {total_alunos_lab} alunos")
    print(f"Capacidade total de laboratórios: {capacidade_lab}")
    print(f"Disponibilidade: {capacidade_lab - total_alunos_lab} lugares")
    
    print(f"\nMatérias de aula: {total_alunos_aula} alunos")
    print(f"Capacidade total de salas de aula: {capacidade_aula}")
    print(f"Capacidade total de auditórios: {capacidade_auditorio}")
    print(f"Capacidade total (aula + auditório): {capacidade_aula + capacidade_auditorio}")
    print(f"Disponibilidade: {capacidade_aula + capacidade_auditorio - total_alunos_aula} lugares")


def sugerir_ajustes(alocador: AlocadorSalas):
    """Sugere ajustes para tornar o problema viável"""
    print("\n=== SUGESTÕES DE AJUSTES ===")
    
    # Analisar conflitos
    horarios = {}
    for materia in alocador.materias:
        if materia.horario not in horarios:
            horarios[materia.horario] = []
        horarios[materia.horario].append(materia)
    
    conflitos = {h: m for h, m in horarios.items() if len(m) > 1}
    
    if conflitos:
        print("1. CONFLITOS DE HORÁRIO:")
        print("   - Ajustar horários das matérias conflitantes")
        print("   - Considerar múltiplas turmas para matérias grandes")
        
        # Sugerir horários alternativos
        print("\n   Sugestões de horários alternativos:")
        horarios_disponiveis = [
            "Segunda 14:00-16:00", "Segunda 16:00-18:00",
            "Terça 14:00-16:00", "Terça 16:00-18:00",
            "Quarta 14:00-16:00", "Quarta 16:00-18:00",
            "Quinta 14:00-16:00", "Quinta 16:00-18:00",
            "Sexta 14:00-16:00", "Sexta 16:00-18:00"
        ]
        
        for i, horario in enumerate(horarios_disponiveis[:5]):
            if horario not in horarios:
                print(f"     - {horario}")
    
    # Analisar capacidade
    total_alunos_lab = sum(m.inscritos for m in alocador.materias if m.precisa_lab)
    capacidade_lab = sum(s.capacidade for s in alocador.salas if s.tipo.value == 'laboratorio')
    
    if total_alunos_lab > capacidade_lab:
        print(f"\n2. CAPACIDADE INSUFICIENTE:")
        print(f"   - Faltam {total_alunos_lab - capacidade_lab} lugares em laboratórios")
        print("   - Considerar:")
        print("     * Adicionar mais laboratórios")
        print("     * Aumentar capacidade dos laboratórios existentes")
        print("     * Mover algumas matérias para salas de aula com computadores")


def criar_versao_ajustada(alocador_original: AlocadorSalas) -> AlocadorSalas:
    """Cria uma versão ajustada do alocador para resolver conflitos"""
    print("\n=== CRIANDO VERSÃO AJUSTADA ===")
    
    # Criar novo alocador
    alocador_ajustado = AlocadorSalas()
    
    # Copiar salas
    for sala in alocador_original.salas:
        alocador_ajustado.adicionar_sala(sala)
    
    # Ajustar horários das matérias para evitar conflitos
    horarios_usados = set()
    materias_ajustadas = []
    
    for materia in alocador_original.materias:
        # Se o horário já está em uso, tentar encontrar um alternativo
        if materia.horario in horarios_usados:
            # Tentar horários alternativos
            horarios_alternativos = [
                f"{materia.horario.split()[0]} 14:00-16:00",
                f"{materia.horario.split()[0]} 16:00-18:00",
                "Quinta 14:00-16:00",
                "Quinta 16:00-18:00",
                "Sexta 14:00-16:00"
            ]
            
            novo_horario = materia.horario
            for alt_horario in horarios_alternativos:
                if alt_horario not in horarios_usados:
                    novo_horario = alt_horario
                    break
            
            # Criar nova matéria com horário ajustado
            materia_ajustada = type(materia)(
                id=materia.id,
                nome=materia.nome,
                inscritos=materia.inscritos,
                horario=novo_horario,
                precisa_lab=materia.precisa_lab,
                materiais_necessarios=materia.materiais_necessarios
            )
            materias_ajustadas.append(materia_ajustada)
            horarios_usados.add(novo_horario)
        else:
            materias_ajustadas.append(materia)
            horarios_usados.add(materia.horario)
    
    # Adicionar matérias ajustadas
    for materia in materias_ajustadas:
        alocador_ajustado.adicionar_materia(materia)
    
    print(f"✓ {len(materias_ajustadas)} matérias processadas")
    print(f"✓ {len(horarios_usados)} horários únicos")
    
    return alocador_ajustado


def main():
    """Função principal"""
    print("=== ALOCADOR DE SALAS - DADOS REAIS ===\n")
    
    # Carregar dados reais
    carregador = CarregadorDadosReais()
    alocador = carregador.carregar_dados_completos('oferta_cc_2025_1.csv')
    
    # Imprimir estatísticas
    carregador.imprimir_estatisticas_materias()
    
    # Analisar problemas potenciais
    analisar_conflitos_horarios(alocador)
    analisar_capacidade_salas(alocador)
    
    # Tentar resolver problema original
    print("\n=== TENTATIVA 1: DADOS ORIGINAIS ===")
    sucesso = alocador.resolver()
    
    if sucesso:
        print("✓ Solução encontrada com dados originais!")
        alocador.imprimir_resumo()
        
        # Salvar resultados
        df = alocador.obter_resultados()
        df.to_csv('resultados_alocacao_real_original.csv', index=False)
        print(f"\nResultados salvos em 'resultados_alocacao_real_original.csv'")
    else:
        print("✗ Problema infeasível com dados originais")
        
        # Sugerir ajustes
        sugerir_ajustes(alocador)
        
        # Criar versão ajustada
        print("\n=== TENTATIVA 2: DADOS AJUSTADOS ===")
        alocador_ajustado = criar_versao_ajustada(alocador)
        
        # Tentar resolver versão ajustada
        sucesso_ajustado = alocador_ajustado.resolver()
        
        if sucesso_ajustado:
            print("✓ Solução encontrada com dados ajustados!")
            alocador_ajustado.imprimir_resumo()
            
            # Salvar resultados ajustados
            df_ajustado = alocador_ajustado.obter_resultados()
            df_ajustado.to_csv('resultados_alocacao_real_ajustado.csv', index=False)
            print(f"\nResultados ajustados salvos em 'resultados_alocacao_real_ajustado.csv'")
        else:
            print("✗ Ainda não foi possível encontrar solução viável")
            print("Considere:")
            print("- Ajustar manualmente os horários")
            print("- Adicionar mais salas")
            print("- Aumentar capacidades das salas existentes")


if __name__ == "__main__":
    main()