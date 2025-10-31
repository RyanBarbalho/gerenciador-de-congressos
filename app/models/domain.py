"""
Modelos de domínio para o sistema de alocação de salas.
Implementa entidades principais com validação e comportamento encapsulado.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set, Optional
from abc import ABC, abstractmethod


class TipoSala(Enum):
    """Tipos de salas disponíveis"""
    AULA = "aula"
    LABORATORIO = "laboratorio"
    AUDITORIO = "auditorio"


class LocalSala(Enum):
    """Localização das salas"""
    IC = "ic"  # Instituto de Computação
    IM = "im"  # Instituto de Matemática
    IF = "if"  # Instituto de Física


@dataclass
class Materia:
    """Representa uma matéria a ser alocada"""
    id: str
    nome: str
    inscritos: int
    horario: str  # Formato: "Segunda 14:00-16:00"
    material: int  # 0 = nenhum, 1 = computadores, 2 = robótica, 3 = eletrônica

    def __post_init__(self):
        """Validação pós-inicialização"""
        if self.inscritos <= 0:
            raise ValueError("Número de inscritos deve ser positivo")
        if not self.nome.strip():
            raise ValueError("Nome da matéria não pode ser vazio")
        if not self.horario.strip():
            raise ValueError("Horário não pode ser vazio")

    def get_capacidade_minima(self) -> int:
        """Retorna a capacidade mínima necessária"""
        return self.inscritos


@dataclass
class Sala:
    """Representa uma sala disponível"""
    id: str
    nome: str
    capacidade: int
    tipo: TipoSala
    local: LocalSala
    tipo_equipamento: int  # 1 = computadores, 2 = robótica, 3 = eletrônica, 0 = nenhum
    materiais_disponiveis: List[str] = field(default_factory=list)
    custo_adicional: float = 0.0

    def __post_init__(self):
        """Validação pós-inicialização"""
        if self.capacidade <= 0:
            raise ValueError("Capacidade deve ser positiva")
        if not self.nome.strip():
            raise ValueError("Nome da sala não pode ser vazio")
        if self.custo_adicional < 0:
            raise ValueError("Custo adicional não pode ser negativo")

    def get_materiais_disponiveis(self) -> Set[str]:
        """Retorna materiais disponíveis como conjunto"""
        return set(self.materiais_disponiveis)

    def calcular_espaco_ocioso(self, inscritos: int) -> int:
        """Calcula espaço ocioso para um número de inscritos"""
        return max(0, self.capacidade - inscritos)

    def calcular_utilizacao(self, inscritos: int) -> float:
        """Calcula percentual de utilização"""
        if self.capacidade == 0:
            return 0.0
        return (inscritos / self.capacidade) * 100


@dataclass
class Alocacao:
    """Representa uma alocação de matéria em sala"""
    materia: Materia
    sala: Sala
    espaco_ocioso: int
    utilizacao_percentual: float

    def __post_init__(self):
        """Calcula métricas automaticamente"""
        self.espaco_ocioso = self.sala.calcular_espaco_ocioso(self.materia.inscritos)
        self.utilizacao_percentual = self.sala.calcular_utilizacao(self.materia.inscritos)


class AlocacaoResultado:
    """Resultado de uma operação de alocação"""

    def __init__(self, sucesso: bool, alocacoes: List[Alocacao] = None,
                 erro: Optional[str] = None, todas_materias: List[Materia] = None,
                 todas_salas: List[Sala] = None):
        self.sucesso = sucesso
        self.alocacoes = alocacoes or []
        self.erro = erro
        self.todas_materias = todas_materias or []
        self.todas_salas = todas_salas or []
        self.metricas = self._calcular_metricas() if sucesso else None

    def _calcular_metricas(self) -> dict:
        """Calcula métricas do resultado usando o módulo de métricas completo"""
        if not self.alocacoes:
            return {}

        try:
            from ..services.metricas import CalculadorMetricas, MetricasCompletas
            
            metricas_completas = CalculadorMetricas.calcular_metricas_completas(
                self.alocacoes,
                self.todas_materias,
                self.todas_salas
            )
            
            # Retornar dicionário compatível com código existente
            return {
                'total_alocacoes': len(self.alocacoes),
                
                # Métricas de Utilização (3.3.1)
                'utilizacao_media': metricas_completas.utilizacao.utilizacao_media,
                'espaco_ocioso_total': metricas_completas.utilizacao.espaco_ocioso_total,
                'distribuicao_utilizacao': metricas_completas.utilizacao.distribuicao_utilizacao,
                
                # Métricas de Eficiência (3.3.2)
                'taxa_alocacao': metricas_completas.eficiencia.taxa_alocacao,
                'custo_total': metricas_completas.eficiencia.custo_total,
                'numero_salas_utilizadas': metricas_completas.eficiencia.numero_salas_utilizadas,
                
                # Validação de Restrições (3.3.3)
                'todas_restricoes_satisfeitas': metricas_completas.validacao.todas_restricoes_satisfeitas,
                'validacoes': metricas_completas.validacao.validacoes,
                
                # Objeto completo para acesso programático
                'metricas_completas': metricas_completas,
                
                # Compatibilidade com código antigo
                'salas_im_usadas': len(set(a.sala.id for a in self.alocacoes if a.sala.local == LocalSala.IM))
            }
        except ImportError:
            # Fallback para cálculo básico se módulo não estiver disponível
            total_ocioso = sum(a.espaco_ocioso for a in self.alocacoes)
            utilizacao_media = sum(a.utilizacao_percentual for a in self.alocacoes) / len(self.alocacoes)
            
            salas_im_unicas = set()
            for a in self.alocacoes:
                if a.sala.local == LocalSala.IM:
                    salas_im_unicas.add(a.sala.id)
            
            salas_im_unicas_objetos = {}
            for a in self.alocacoes:
                if a.sala.local == LocalSala.IM:
                    salas_im_unicas_objetos[a.sala.id] = a.sala
            
            custo_total = sum(sala.custo_adicional for sala in salas_im_unicas_objetos.values())

            return {
                'total_alocacoes': len(self.alocacoes),
                'espaco_ocioso_total': total_ocioso,
                'utilizacao_media': utilizacao_media,
                'salas_im_usadas': len(salas_im_unicas),
                'custo_total': custo_total
            }


class Observer(ABC):
    """Interface para observadores do processo de alocação"""

    @abstractmethod
    def on_progress(self, etapa: str, progresso: float):
        """Notifica progresso da alocação"""
        pass

    @abstractmethod
    def on_sucesso(self, resultado: AlocacaoResultado):
        """Notifica sucesso da alocação"""
        pass

    @abstractmethod
    def on_erro(self, erro: str):
        """Notifica erro na alocação"""
        pass


class Subject:
    """Sujeito para padrão Observer"""

    def __init__(self):
        self._observers: List[Observer] = []

    def adicionar_observer(self, observer: Observer):
        """Adiciona um observador"""
        self._observers.append(observer)

    def remover_observer(self, observer: Observer):
        """Remove um observador"""
        self._observers.remove(observer)

    def notificar_progresso(self, etapa: str, progresso: float):
        """Notifica progresso para todos os observadores"""
        for observer in self._observers:
            observer.on_progress(etapa, progresso)

    def notificar_sucesso(self, resultado: AlocacaoResultado):
        """Notifica sucesso para todos os observadores"""
        for observer in self._observers:
            observer.on_sucesso(resultado)

    def notificar_erro(self, erro: str):
        """Notifica erro para todos os observadores"""
        for observer in self._observers:
            observer.on_erro(erro)
