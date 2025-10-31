"""
Módulo de métricas para avaliação de qualidade das soluções de alocação.
Implementa métricas de utilização, eficiência e validação de restrições.
"""

import statistics
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from ..models.domain import Alocacao, Materia, Sala, TipoSala, LocalSala


@dataclass
class MetricasUtilizacao:
    """Métricas de utilização de salas"""
    utilizacao_media: float  # Percentual médio de ocupação das salas utilizadas
    espaco_ocioso_total: int  # Soma dos espaços não utilizados em todas as alocações
    distribuicao_utilizacao: float  # Variância da utilização entre salas


@dataclass
class MetricasEficiencia:
    """Métricas de eficiência do processo de alocação"""
    taxa_alocacao: float  # Percentual de matérias que foram alocadas com sucesso
    custo_total: float  # Soma dos custos adicionais (ex: uso de salas em blocos distantes)
    numero_salas_utilizadas: int  # Indica a eficiência no uso do espaço físico


@dataclass
class ValidacaoRestricoes:
    """Resultado da validação de restrições hard"""
    todas_restricoes_satisfeitas: bool
    validacoes: Dict[str, Tuple[bool, str]]  # Nome da restrição -> (satisfeita, mensagem)


@dataclass
class MetricasCompletas:
    """Todas as métricas de avaliação da solução"""
    utilizacao: MetricasUtilizacao
    eficiencia: MetricasEficiencia
    validacao: ValidacaoRestricoes


class CalculadorMetricas:
    """Calcula métricas completas para uma solução de alocação"""

    @staticmethod
    def calcular_metricas_utilizacao(alocacoes: List[Alocacao]) -> MetricasUtilizacao:
        """
        Calcula métricas de utilização das salas.
        
        3.3.1 Métricas de Utilização:
        - Utilização média: Percentual médio de ocupação das salas utilizadas
        - Espaço ocioso total: Soma dos espaços não utilizados em todas as alocações
        - Distribuição de utilização: Análise da variância da utilização entre salas
        """
        if not alocacoes:
            return MetricasUtilizacao(0.0, 0, 0.0)

        # Calcular utilização média (percentual médio de ocupação)
        utilizacoes = [a.utilizacao_percentual for a in alocacoes]
        utilizacao_media = statistics.mean(utilizacoes) if utilizacoes else 0.0

        # Calcular espaço ocioso total
        espaco_ocioso_total = sum(a.espaco_ocioso for a in alocacoes)

        # Calcular distribuição de utilização (variância)
        distribuicao_utilizacao = statistics.variance(utilizacoes) if len(utilizacoes) > 1 else 0.0

        return MetricasUtilizacao(
            utilizacao_media=utilizacao_media,
            espaco_ocioso_total=espaco_ocioso_total,
            distribuicao_utilizacao=distribuicao_utilizacao
        )

    @staticmethod
    def calcular_metricas_eficiencia(
        alocacoes: List[Alocacao],
        total_materias: int
    ) -> MetricasEficiencia:
        """
        Calcula métricas de eficiência do processo de alocação.
        
        3.3.2 Métricas de Eficiência:
        - Taxa de alocação: Percentual de matérias que foram alocadas com sucesso
        - Custo total: Soma dos custos adicionais (ex: uso de salas em blocos distantes)
        - Número de salas utilizadas: Indica a eficiência no uso do espaço físico
        """
        # Taxa de alocação
        materias_alocadas = len(alocacoes)
        taxa_alocacao = (materias_alocadas / total_materias * 100) if total_materias > 0 else 0.0

        # Custo total: soma dos custos adicionais (salas do IM têm custo adicional)
        # Contar salas únicas utilizadas para calcular custo corretamente
        salas_utilizadas = {}
        for alocacao in alocacoes:
            sala_id = alocacao.sala.id
            if sala_id not in salas_utilizadas:
                salas_utilizadas[sala_id] = alocacao.sala

        custo_total = sum(sala.custo_adicional for sala in salas_utilizadas.values())

        # Número de salas utilizadas (salas únicas)
        numero_salas_utilizadas = len(salas_utilizadas)

        return MetricasEficiencia(
            taxa_alocacao=taxa_alocacao,
            custo_total=custo_total,
            numero_salas_utilizadas=numero_salas_utilizadas
        )

    @staticmethod
    def validar_restricoes(
        alocacoes: List[Alocacao],
        todas_materias: List[Materia],
        todas_salas: List[Sala]
    ) -> ValidacaoRestricoes:
        """
        Valida que todas as restrições hard foram satisfeitas.
        
        3.3.3 Validação de Restrições:
        - Cada matéria alocada em exatamente uma sala
        - Capacidade respeitada em todas as alocações
        - Compatibilidade de tipo mantida (lab vs. aula)
        - Sem conflitos de horário
        """
        validacoes = {}
        todas_satisfeitas = True

        # 1. Cada matéria alocada em exatamente uma sala
        materias_alocadas = set(a.materia.id for a in alocacoes)
        
        # Verificar se cada matéria alocada está em exatamente uma sala
        materias_por_id = {}
        alocacao_unica_ok = True
        materias_multiplas = []
        
        for alocacao in alocacoes:
            materia_id = alocacao.materia.id
            if materia_id in materias_por_id:
                # Matéria já está alocada em outra sala
                alocacao_unica_ok = False
                materias_multiplas.append(materia_id)
            else:
                materias_por_id[materia_id] = alocacao
        
        if alocacao_unica_ok:
            validacoes['alocacao_unica'] = (
                True,
                f"Todas as {len(materias_alocadas)} matérias alocadas estão em exatamente uma sala"
            )
        else:
            todas_satisfeitas = False
            validacoes['alocacao_unica'] = (
                False,
                f"Matérias alocadas em múltiplas salas: {', '.join(set(materias_multiplas))}"
            )

        # 2. Capacidade respeitada em todas as alocações
        capacidade_respeitada = True
        violacoes_capacidade = []
        for alocacao in alocacoes:
            if alocacao.materia.inscritos > alocacao.sala.capacidade:
                capacidade_respeitada = False
                violacoes_capacidade.append(
                    f"Matéria {alocacao.materia.id} ({alocacao.materia.inscritos} inscritos) "
                    f"excede capacidade da sala {alocacao.sala.id} ({alocacao.sala.capacidade})"
                )
        
        if capacidade_respeitada:
            validacoes['capacidade'] = (
                True,
                f"Capacidade respeitada em todas as {len(alocacoes)} alocações"
            )
        else:
            todas_satisfeitas = False
            validacoes['capacidade'] = (
                False,
                f"Violações de capacidade: {', '.join(violacoes_capacidade)}"
            )

        # 3. Compatibilidade de tipo mantida (lab vs. aula)
        compatibilidade_ok = True
        violacoes_compatibilidade = []
        for alocacao in alocacoes:
            materia = alocacao.materia
            sala = alocacao.sala
            
            # Se matéria precisa de material especial, deve estar em laboratório
            if materia.material > 0 and sala.tipo != TipoSala.LABORATORIO:
                compatibilidade_ok = False
                violacoes_compatibilidade.append(
                    f"Matéria {materia.id} precisa de material especial (tipo {materia.material}) "
                    f"mas está em sala tipo {sala.tipo.value}"
                )
            
            # Verificar compatibilidade de equipamento
            if materia.material > 0:
                if materia.material != sala.tipo_equipamento:
                    compatibilidade_ok = False
                    violacoes_compatibilidade.append(
                        f"Matéria {materia.id} precisa de equipamento tipo {materia.material} "
                        f"mas sala {sala.id} tem tipo {sala.tipo_equipamento}"
                    )
        
        if compatibilidade_ok:
            validacoes['compatibilidade_tipo'] = (
                True,
                f"Compatibilidade de tipo mantida em todas as {len(alocacoes)} alocações"
            )
        else:
            todas_satisfeitas = False
            validacoes['compatibilidade_tipo'] = (
                False,
                f"Violações de compatibilidade: {', '.join(violacoes_compatibilidade)}"
            )

        # 4. Sem conflitos de horário na mesma sala
        conflitos = []
        # Agrupar alocações por sala e horário
        alocacoes_por_sala_horario = {}
        for alocacao in alocacoes:
            sala_id = alocacao.sala.id
            horario = alocacao.materia.horario
            
            # Extrair slots de tempo do horário
            slots = CalculadorMetricas._extrair_slots_tempo(horario)
            
            for slot in slots:
                chave = (sala_id, slot)
                if chave not in alocacoes_por_sala_horario:
                    alocacoes_por_sala_horario[chave] = []
                alocacoes_por_sala_horario[chave].append(alocacao)
        
        # Verificar se há múltiplas matérias na mesma sala no mesmo horário
        for (sala_id, slot), alocacoes_slot in alocacoes_por_sala_horario.items():
            if len(alocacoes_slot) > 1:
                conflitos.append(
                    f"Sala {sala_id} tem {len(alocacoes_slot)} matérias no horário {slot}"
                )
        
        if not conflitos:
            validacoes['sem_conflitos_horario'] = (
                True,
                f"Sem conflitos de horário em todas as alocações"
            )
        else:
            todas_satisfeitas = False
            validacoes['sem_conflitos_horario'] = (
                False,
                f"Conflitos encontrados: {', '.join(conflitos)}"
            )

        return ValidacaoRestricoes(
            todas_restricoes_satisfeitas=todas_satisfeitas,
            validacoes=validacoes
        )

    @staticmethod
    def _extrair_slots_tempo(horario_str: str) -> List[str]:
        """Extrai slots de tempo individuais de um horário complexo"""
        import re

        # Dividir por " | " se houver múltiplos horários
        horarios_parts = horario_str.split(' | ')
        slots = []

        for part in horarios_parts:
            # Extrair dias e horários
            match = re.match(r'([^0-9]+)\s+(.+)', part.strip())
            if not match:
                # Se não conseguir fazer match, usar o horário completo como slot único
                slots.append(horario_str)
                continue

            dias_str, horarios_str = match.groups()
            dias = [d.strip() for d in dias_str.split('/')]
            horarios = [h.strip() for h in horarios_str.split('/')]

            # Combinar cada dia com cada horário
            for dia in dias:
                for horario in horarios:
                    slots.append(f"{dia} {horario}")

        return slots if slots else [horario_str]

    @staticmethod
    def calcular_metricas_completas(
        alocacoes: List[Alocacao],
        todas_materias: List[Materia],
        todas_salas: List[Sala]
    ) -> MetricasCompletas:
        """
        Calcula todas as métricas completas da solução.
        
        Returns:
            MetricasCompletas: Objeto contendo todas as métricas calculadas
        """
        metricas_utilizacao = CalculadorMetricas.calcular_metricas_utilizacao(alocacoes)
        metricas_eficiencia = CalculadorMetricas.calcular_metricas_eficiencia(
            alocacoes, len(todas_materias)
        )
        validacao = CalculadorMetricas.validar_restricoes(
            alocacoes, todas_materias, todas_salas
        )

        return MetricasCompletas(
            utilizacao=metricas_utilizacao,
            eficiencia=metricas_eficiencia,
            validacao=validacao
        )

