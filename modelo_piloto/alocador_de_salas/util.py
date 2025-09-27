"""
Utilitários para decodificação de horários do sistema da universidade.
"""

import re
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class HorarioDecodificado:
    """Representa um horário decodificado"""
    dia_semana: int  # 2=segunda, 3=terça, ..., 7=sábado
    turno: str  # 'M'=manhã, 'T'=tarde
    periodos: List[int]  # Lista de períodos (ex: [1, 2] para 7:30-8:20)
    horario_legivel: str  # Formato legível (ex: "Segunda 07:30-08:20")
    codigo_original: str  # Código original (ex: "2M12")


def decodificar_horario(codigo_horario: str) -> List[HorarioDecodificado]:
    """
    Decodifica um código de horário do sistema da universidade.
    
    Formato: [dias][turno][períodos]
    - dias: números que representam os dias da semana (2=segunda, 3=terça, etc.)
    - turno: M (manhã) ou T (tarde)
    - períodos: números que representam os períodos
    
    Exemplos:
    - "2M12" -> Segunda manhã, períodos 1 e 2
    - "6T23" -> Sexta tarde, períodos 2 e 3
    - "24T34" -> Segunda e quarta tarde, períodos 3 e 4
    - "35M12" -> Terça e quinta manhã, períodos 1 e 2
    - "5M456" -> Quinta manhã, períodos 4, 5 e 6
    
    Args:
        codigo_horario: Código do horário (ex: "2M12", "6T23", "24T34")
        
    Returns:
        Lista de HorarioDecodificado
    """
    # Mapeamento de dias da semana
    dias_semana = {
        2: "Segunda",
        3: "Terça", 
        4: "Quarta",
        5: "Quinta",
        6: "Sexta",
        7: "Sábado"
    }
    
    # Mapeamento de turnos
    turnos = {
        'M': "manhã",
        'T': "tarde"
    }
    
    # Se o horário contém múltiplos códigos separados por espaço
    if ' ' in codigo_horario:
        codigos = codigo_horario.split()
        resultados = []
        for codigo in codigos:
            resultados.extend(decodificar_horario(codigo))
        return resultados
    
    # Regex para extrair dias, turno e períodos
    pattern = r'^(\d+)([MT])(\d+)$'
    match = re.match(pattern, codigo_horario)
    
    if not match:
        raise ValueError(f"Formato de horário inválido: {codigo_horario}")
    
    dias_str = match.group(1)
    turno = match.group(2)
    periodos_str = match.group(3)
    
    # Extrair dias individuais
    dias = [int(d) for d in dias_str]
    
    # Validar dias da semana
    for dia in dias:
        if dia < 2 or dia > 7:
            raise ValueError(f"Dia da semana inválido: {dia}")
    
    # Extrair períodos individuais
    periodos = [int(p) for p in periodos_str]
    
    # Validar períodos
    for periodo in periodos:
        if periodo < 1 or periodo > 6:
            raise ValueError(f"Período inválido: {periodo}")
    
    # Mapeamento de períodos para horários (diferente para manhã e tarde)
    periodos_horarios_manha = {
        1: "07:30-08:20",
        2: "08:20-09:10", 
        3: "09:10-10:00",
        4: "10:20-11:10",
        5: "11:10-12:00",
        6: "12:00-12:50"
    }
    
    periodos_horarios_tarde = {
        1: "13:30-14:20",
        2: "14:20-15:10",
        3: "15:10-16:00",
        4: "16:20-17:10",
        5: "17:10-18:00",
        6: "18:00-18:50"
    }
    
    # Escolher o mapeamento correto baseado no turno
    periodos_horarios = periodos_horarios_manha if turno == 'M' else periodos_horarios_tarde
    
    # Criar horários para cada dia
    resultados = []
    for dia in dias:
        dia_nome = dias_semana[dia]
        turno_nome = turnos[turno]
        
        # Se há múltiplos períodos, mostrar o primeiro e último
        if len(periodos) == 1:
            horario_legivel = f"{dia_nome} {periodos_horarios[periodos[0]]}"
        else:
            primeiro_horario = periodos_horarios[min(periodos)]
            ultimo_horario = periodos_horarios[max(periodos)]
            # Extrair apenas o horário final do último período
            ultimo_fim = ultimo_horario.split('-')[1]
            primeiro_inicio = primeiro_horario.split('-')[0]
            horario_legivel = f"{dia_nome} {primeiro_inicio}-{ultimo_fim}"
        
        resultados.append(HorarioDecodificado(
            dia_semana=dia,
            turno=turno,
            periodos=periodos,
            horario_legivel=horario_legivel,
            codigo_original=codigo_horario
        ))
    
    return resultados


def converter_para_formato_alocador(codigo_horario: str) -> str:
    """
    Converte um código de horário para o formato usado pelo alocador.
    
    Args:
        codigo_horario: Código do horário (ex: "2M12", "24T34")
        
    Returns:
        String no formato "Dia HH:MM-HH:MM" ou "Dia1/Dia2 HH:MM-HH:MM" para múltiplos dias
    """
    horarios = decodificar_horario(codigo_horario)
    if not horarios:
        return ""
    
    # Se há apenas um horário, retornar diretamente
    if len(horarios) == 1:
        return horarios[0].horario_legivel
    
    # Se há múltiplos horários (múltiplos dias), combinar
    dias = [h.dia_semana for h in horarios]
    turno = horarios[0].turno
    periodos = horarios[0].periodos
    
    # Mapeamento de dias da semana
    dias_semana = {
        2: "Segunda",
        3: "Terça", 
        4: "Quarta",
        5: "Quinta",
        6: "Sexta",
        7: "Sábado"
    }
    
    # Mapeamento de períodos para horários (diferente para manhã e tarde)
    periodos_horarios_manha = {
        1: "07:30-08:20",
        2: "08:20-09:10", 
        3: "09:10-10:00",
        4: "10:20-11:10",
        5: "11:10-12:00",
        6: "12:00-12:50"
    }
    
    periodos_horarios_tarde = {
        1: "13:30-14:20",
        2: "14:20-15:10",
        3: "15:10-16:00",
        4: "16:20-17:10",
        5: "17:10-18:00",
        6: "18:00-18:50"
    }
    
    # Escolher o mapeamento correto baseado no turno
    periodos_horarios = periodos_horarios_manha if turno == 'M' else periodos_horarios_tarde
    
    # Criar string de dias
    dias_nomes = [dias_semana[d] for d in sorted(dias)]
    dias_str = "/".join(dias_nomes)
    
    # Criar string de horário
    if len(periodos) == 1:
        horario_str = periodos_horarios[periodos[0]]
    else:
        primeiro_horario = periodos_horarios[min(periodos)]
        ultimo_horario = periodos_horarios[max(periodos)]
        ultimo_fim = ultimo_horario.split('-')[1]
        primeiro_inicio = primeiro_horario.split('-')[0]
        horario_str = f"{primeiro_inicio}-{ultimo_fim}"
    
    return f"{dias_str} {horario_str}"


def extrair_requisitos_sala(nome_materia: str, codigo: str) -> List[str]:
    """
    Extrai requisitos de sala baseado no nome e código da matéria.
    
    Args:
        nome_materia: Nome da matéria
        codigo: Código da matéria
        
    Returns:
        Lista de requisitos de equipamentos
    """
    requisitos = []
    
    # Palavras-chave que indicam necessidade de laboratório
    lab_keywords = [
        'programação', 'compiladores', 'banco de dados', 'sistemas operacionais',
        'redes', 'inteligência artificial', 'aprendizagem', 'computação gráfica',
        'processamento', 'interação homem-máquina', 'navegação de robôs',
        'redes neurais', 'sistemas digitais', 'projeto e desenvolvimento'
    ]
    
    # Palavras-chave que indicam necessidade de auditório
    auditorio_keywords = [
        'álgebra linear', 'cálculo', 'geometria analítica', 'matemática discreta',
        'probabilidade e estatística', 'teoria da computação', 'lógica'
    ]
    
    nome_lower = nome_materia.lower()
    codigo_lower = codigo.lower()
    
    # Verificar se precisa de laboratório
    if any(keyword in nome_lower for keyword in lab_keywords):
        requisitos.extend(['computadores', 'projetor'])
    elif any(keyword in nome_lower for keyword in auditorio_keywords):
        requisitos.extend(['projetor', 'quadro', 'som'])
    else:
        # Requisitos padrão para outras matérias
        requisitos.extend(['projetor', 'quadro'])
    
    return requisitos


def determinar_tipo_sala(nome_materia: str, codigo: str, capacidade: int) -> str:
    """
    Determina o tipo de sala baseado na matéria e capacidade.
    
    Args:
        nome_materia: Nome da matéria
        codigo: Código da matéria
        capacidade: Capacidade necessária
        
    Returns:
        Tipo de sala ('AUDITORIO', 'AULA', 'LABORATORIO')
    """
    nome_lower = nome_materia.lower()
    
    # Palavras-chave que indicam laboratório
    lab_keywords = [
        'programação', 'compiladores', 'banco de dados', 'sistemas operacionais',
        'redes', 'inteligência artificial', 'aprendizagem', 'computação gráfica',
        'processamento', 'interação homem-máquina', 'navegação de robôs',
        'redes neurais', 'sistemas digitais', 'projeto e desenvolvimento'
    ]
    
    if any(keyword in nome_lower for keyword in lab_keywords):
        return 'LABORATORIO'
    elif capacidade >= 60:
        return 'AUDITORIO'
    else:
        return 'AULA'


def testar_decodificador():
    """Função para testar o decodificador de horários"""
    exemplos = [
        "2M12",    # Segunda manhã, períodos 1 e 2
        "6T23",    # Sexta tarde, períodos 2 e 3  
        "5M456",   # Quinta manhã, períodos 4, 5 e 6
        "24T34",   # Segunda e quarta tarde, períodos 3 e 4
        "35M12",   # Terça e quinta manhã, períodos 1 e 2
        "236T1234 4T56 5T12"  # Múltiplos horários
    ]
    
    print("=== TESTE DO DECODIFICADOR DE HORÁRIOS ===\n")
    
    for exemplo in exemplos:
        try:
            horarios = decodificar_horario(exemplo)
            print(f"Código: {exemplo}")
            for horario in horarios:
                print(f"  -> {horario.horario_legivel}")
            print()
        except Exception as e:
            print(f"Erro ao decodificar {exemplo}: {e}")
            print()


if __name__ == "__main__":
    testar_decodificador()