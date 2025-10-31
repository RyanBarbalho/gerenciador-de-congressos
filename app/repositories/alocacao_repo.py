"""
Repositório e algoritmo de alocação refatorado.
Implementa Repository Pattern e Strategy Pattern para algoritmos de alocação.
"""

import pulp
import pandas as pd
from typing import List, Dict, Optional, Any
from ..models.domain import Materia, Sala, Alocacao, AlocacaoResultado, Subject
from ..strategies.interfaces import AlocacaoStrategy, CompatibilidadeStrategy, Compatibilidade, SolverStrategy
from ..factories.creators import FactoryManager


class AlocacaoRepository:
    """Repositório para gerenciamento de dados de alocação"""

    def __init__(self):
        self.materias: Dict[str, Materia] = {}
        self.salas: Dict[str, Sala] = {}
        self.alocacoes: List[Alocacao] = []

    def salvar_materia(self, materia: Materia) -> bool:
        """Salva uma matéria"""
        try:
            self.materias[materia.id] = materia
            return True
        except Exception:
            return False

    def salvar_sala(self, sala: Sala) -> bool:
        """Salva uma sala"""
        try:
            self.salas[sala.id] = sala
            return True
        except Exception:
            return False

    def buscar_materias(self) -> List[Materia]:
        """Busca todas as matérias"""
        return list(self.materias.values())

    def buscar_salas(self) -> List[Sala]:
        """Busca todas as salas"""
        return list(self.salas.values())

    def buscar_materia_por_id(self, materia_id: str) -> Optional[Materia]:
        """Busca matéria por ID"""
        return self.materias.get(materia_id)

    def buscar_sala_por_id(self, sala_id: str) -> Optional[Sala]:
        """Busca sala por ID"""
        return self.salas.get(sala_id)

    def salvar_alocacao(self, alocacao: Alocacao) -> bool:
        """Salva uma alocação"""
        try:
            self.alocacoes.append(alocacao)
            return True
        except Exception:
            return False

    def buscar_alocacoes(self) -> List[Alocacao]:
        """Busca todas as alocações"""
        return self.alocacoes.copy()

    def limpar_alocacoes(self):
        """Limpa todas as alocações"""
        self.alocacoes.clear()


class PulpSolverStrategy(SolverStrategy):
    """Estratégia de solver usando PuLP"""

    def resolver(self, problema) -> bool:
        """Resolve o problema usando PuLP"""
        try:
            problema.solve(pulp.PULP_CBC_CMD(msg=0))
            return pulp.LpStatus[problema.status] == "Optimal"
        except Exception:
            return False

    def extrair_solucao(self, problema) -> Dict[str, str]:
        """Extrai a solução do problema"""
        solucao = {}

        for var in problema.variables():
            if var.varValue == 1:
                # Extrair IDs da variável (formato: x_CC_COMP377_SALA_001)
                parts = var.name.split('_')
                if len(parts) >= 4:
                    # Formato: x_CC_COMP377_SALA_001
                    # parts[0] = "x", parts[1] = "CC", parts[2] = "COMP377", parts[3] = "SALA", parts[4] = "001"
                    materia_id = f"{parts[1]}_{parts[2]}"  # CC_COMP377
                    sala_id = f"{parts[3]}_{parts[4]}"     # SALA_001
                    solucao[materia_id] = sala_id

        return solucao


class AlocacaoLinearStrategy(AlocacaoStrategy):
    """Estratégia de alocação usando programação linear inteira"""

    def __init__(self, compatibilidade: CompatibilidadeStrategy = None,
                 solver_strategy: SolverStrategy = None):
        super().__init__(compatibilidade)
        self.solver_strategy = solver_strategy or PulpSolverStrategy()
        self.problema = None
        self.variaveis = {}

    def alocar(self, materias: List[Materia], salas: List[Sala]) -> AlocacaoResultado:
        """Executa alocação usando programação linear"""
        try:
            # Criar problema
            self.problema = pulp.LpProblem("AlocacaoSalas", pulp.LpMinimize)

            # Criar variáveis e restrições
            self._criar_variaveis_decisao(materias, salas)
            self._criar_funcao_objetivo(materias, salas)
            self._criar_restricoes_hard(materias, salas)

            # Resolver
            sucesso = self.solver_strategy.resolver(self.problema)

            if sucesso:
                solucao = self.solver_strategy.extrair_solucao(self.problema)
                alocacoes = self._criar_alocacoes(materias, salas, solucao)
                return AlocacaoResultado(
                    sucesso=True, 
                    alocacoes=alocacoes,
                    todas_materias=materias,
                    todas_salas=salas
                )
            else:
                return AlocacaoResultado(
                    sucesso=False, 
                    erro="Não foi possível encontrar solução ótima",
                    todas_materias=materias,
                    todas_salas=salas
                )

        except Exception as e:
            return AlocacaoResultado(
                sucesso=False, 
                erro=str(e),
                todas_materias=materias,
                todas_salas=salas
            )

    def _criar_variaveis_decisao(self, materias: List[Materia], salas: List[Sala]):
        """Cria variáveis de decisão"""
        self.variaveis = {}

        for materia in materias:
            for sala in salas:
                if self.compatibilidade.eh_compativel(materia, sala):
                    var_name = f"x_{materia.id}_{sala.id}"
                    self.variaveis[(materia.id, sala.id)] = pulp.LpVariable(
                        var_name, cat='Binary'
                    )

    def _criar_funcao_objetivo(self, materias: List[Materia], salas: List[Sala]):
        """Cria função objetivo"""
        objetivo = 0

        for materia in materias:
            for sala in salas:
                if (materia.id, sala.id) in self.variaveis:
                    # Espaço ocioso + custo adicional
                    espaco_ocioso = sala.capacidade - materia.inscritos
                    custo_total = espaco_ocioso + sala.custo_adicional

                    objetivo += self.variaveis[(materia.id, sala.id)] * custo_total

        self.problema += objetivo

    def _criar_restricoes_hard(self, materias: List[Materia], salas: List[Sala]):
        """Cria restrições hard"""
        # 1. Cada matéria deve ser alocada em exatamente uma sala
        for materia in materias:
            restricao = 0
            for sala in salas:
                if (materia.id, sala.id) in self.variaveis:
                    restricao += self.variaveis[(materia.id, sala.id)]

            self.problema += restricao == 1, f"alocacao_unica_{materia.id}"

        # 2. Capacidade da sala deve ser suficiente
        for materia in materias:
            for sala in salas:
                if (materia.id, sala.id) in self.variaveis:
                    self.problema += (
                        self.variaveis[(materia.id, sala.id)] * materia.inscritos <= sala.capacidade,
                        f"capacidade_{materia.id}_{sala.id}"
                    )

        # 3. Sem conflito de horários na mesma sala
        horarios = self._agrupar_por_horario(materias)
        for horario, materias_horario in horarios.items():
            for sala in salas:
                restricao = 0
                for materia in materias_horario:
                    if (materia.id, sala.id) in self.variaveis:
                        restricao += self.variaveis[(materia.id, sala.id)]

                if restricao != 0:
                    self.problema += restricao <= 1, f"sem_conflito_{horario}_{sala.id}"

    def _agrupar_por_horario(self, materias: List[Materia]) -> Dict[str, List[Materia]]:
        """Agrupa matérias por horário, considerando sobreposições temporais"""
        horarios = {}

        for materia in materias:
            # Extrair slots de tempo da matéria
            slots_materia = self._extrair_slots_tempo(materia.horario)

            # Para cada slot de tempo, adicionar a matéria ao grupo correspondente
            for slot in slots_materia:
                if slot not in horarios:
                    horarios[slot] = []
                horarios[slot].append(materia)

        return horarios

    def _extrair_slots_tempo(self, horario_str: str) -> List[str]:
        """Extrai slots de tempo individuais de um horário complexo"""
        import re

        # Padrão para extrair dias e horários
        # Ex: "Segunda/Quinta 09:00-09:50/10:00-10:50" -> ["Segunda 09:00-09:50", "Segunda 10:00-10:50", "Quinta 09:00-09:50", "Quinta 10:00-10:50"]

        # Dividir por " | " se houver múltiplos horários
        horarios_parts = horario_str.split(' | ')
        slots = []

        for part in horarios_parts:
            # Extrair dias e horários
            match = re.match(r'([^0-9]+)\s+(.+)', part.strip())
            if not match:
                continue

            dias_str, horarios_str = match.groups()
            dias = [d.strip() for d in dias_str.split('/')]
            horarios = [h.strip() for h in horarios_str.split('/')]

            # Combinar cada dia com cada horário
            for dia in dias:
                for horario in horarios:
                    slots.append(f"{dia} {horario}")

        return slots if slots else [horario_str]

    def _criar_alocacoes(self, materias: List[Materia], salas: List[Sala],
                        solucao: Dict[str, str]) -> List[Alocacao]:
        """Cria objetos Alocacao a partir da solução"""
        alocacoes = []

        for materia in materias:
            if materia.id in solucao:
                sala_id = solucao[materia.id]
                sala = next(s for s in salas if s.id == sala_id)

                alocacao = Alocacao(
                    materia=materia,
                    sala=sala,
                    espaco_ocioso=sala.calcular_espaco_ocioso(materia.inscritos),
                    utilizacao_percentual=sala.calcular_utilizacao(materia.inscritos)
                )
                alocacoes.append(alocacao)

        return alocacoes


class AlocacaoManager:
    """Gerenciador principal de alocação"""

    def __init__(self, repository: AlocacaoRepository = None):
        self.repository = repository or AlocacaoRepository()
        self.alocacao_strategy: Optional[AlocacaoStrategy] = None
        self.observers: List[Subject] = []

    def definir_estrategia(self, strategy: AlocacaoStrategy):
        """Define estratégia de alocação"""
        self.alocacao_strategy = strategy

    def adicionar_observer(self, observer: Subject):
        """Adiciona observador"""
        self.observers.append(observer)

    def executar_alocacao(self) -> AlocacaoResultado:
        """Executa processo de alocação"""
        if not self.alocacao_strategy:
            return AlocacaoResultado(sucesso=False, erro="Estratégia de alocação não definida")

        materias = self.repository.buscar_materias()
        salas = self.repository.buscar_salas()

        if not materias or not salas:
            return AlocacaoResultado(sucesso=False, erro="Dados insuficientes para alocação")

        # Notificar início
        for observer in self.observers:
            observer.on_progress("Iniciando alocação", 0.0)

        # Executar alocação
        resultado = self.alocacao_strategy.alocar(materias, salas)

        # Salvar alocações se bem-sucedida
        if resultado.sucesso:
            self.repository.limpar_alocacoes()
            for alocacao in resultado.alocacoes:
                self.repository.salvar_alocacao(alocacao)

            # Notificar sucesso
            for observer in self.observers:
                observer.on_sucesso(resultado)
        else:
            # Notificar erro
            for observer in self.observers:
                observer.on_erro(resultado.erro or "Erro desconhecido")

        return resultado

    def obter_resultados_dataframe(self) -> pd.DataFrame:
        """Obtém resultados em formato DataFrame"""
        alocacoes = self.repository.buscar_alocacoes()

        if not alocacoes:
            return pd.DataFrame()

        dados = []
        for alocacao in alocacoes:
            dados.append({
                'Materia': alocacao.materia.nome,
                'Inscritos': alocacao.materia.inscritos,
                'Sala': alocacao.sala.nome,
                'Capacidade': alocacao.sala.capacidade,
                'Espaco_Ocioso': alocacao.espaco_ocioso,
                'Utilizacao_%': round(alocacao.utilizacao_percentual, 2),
                'Tipo_Sala': alocacao.sala.tipo.value,
                'Local': alocacao.sala.local.value,
                'Horario': alocacao.materia.horario
            })

        return pd.DataFrame(dados)
