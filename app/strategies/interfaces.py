"""
Interfaces e estratégias para o sistema de alocação de salas.
Implementa Strategy Pattern para diferentes algoritmos de alocação.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..models.domain import Materia, Sala, AlocacaoResultado


class CompatibilidadeStrategy(ABC):
    """Estratégia para verificar compatibilidade entre matéria e sala"""

    @abstractmethod
    def eh_compativel(self, materia: Materia, sala: Sala) -> bool:
        """Verifica se uma matéria é compatível com uma sala"""
        pass


class Compatibilidade(CompatibilidadeStrategy):
    """Estratégia padrão de compatibilidade"""

    def eh_compativel(self, materia: Materia, sala: Sala) -> bool:
        """Verifica compatibilidade baseada em tipo de sala, material e localização"""

        # Restrição de localização: matérias de Física (IF) só podem ir para salas do IF
        if materia.id.startswith('IF') and sala.local.value != "if":
            return False

        # Matérias não-Física não podem ir para salas do IF
        if not materia.id.startswith('IF') and sala.local.value == "if":
            return False

        # Se a matéria precisa de material especial, só pode ir para laboratório
        if materia.material > 0 and sala.tipo.value != "laboratorio":
            return False

        # Verificar compatibilidade de material/equipamento
        if materia.material == 1 and sala.tipo_equipamento != 1:
            # Matéria precisa de computadores, sala deve ter computadores
            return False
        elif materia.material == 2 and sala.tipo_equipamento != 2:
            # Matéria de robótica, sala deve ter equipamentos de robótica
            return False
        elif materia.material == 3 and sala.tipo_equipamento != 3:
            # Matéria de eletrônica, sala deve ter equipamentos de eletrônica
            return False
        elif materia.material == 0:
            # Matéria sem material especial, pode ir para qualquer sala
            pass

        return True


class AlocacaoStrategy(ABC):
    """Estratégia para algoritmos de alocação"""

    def __init__(self, compatibilidade: CompatibilidadeStrategy = None):
        self.compatibilidade = compatibilidade or Compatibilidade()

    @abstractmethod
    def alocar(self, materias: List[Materia], salas: List[Sala]) -> AlocacaoResultado:
        """Executa o algoritmo de alocação"""
        pass

    def _filtrar_salas_compatíveis(self, materia: Materia, salas: List[Sala]) -> List[Sala]:
        """Filtra salas compatíveis com a matéria"""
        return [sala for sala in salas if self.compatibilidade.eh_compativel(materia, sala)]


class SolverStrategy(ABC):
    """Estratégia para diferentes tipos de solvers"""

    @abstractmethod
    def resolver(self, problema) -> bool:
        """Resolve o problema de otimização"""
        pass

    @abstractmethod
    def extrair_solucao(self, problema) -> Dict[str, str]:
        """Extrai a solução do problema resolvido"""
        pass


class Repository(ABC):
    """Interface para repositórios de dados"""

    @abstractmethod
    def salvar_materia(self, materia: Materia) -> bool:
        """Salva uma matéria"""
        pass

    @abstractmethod
    def salvar_sala(self, sala: Sala) -> bool:
        """Salva uma sala"""
        pass

    @abstractmethod
    def buscar_materias(self) -> List[Materia]:
        """Busca todas as matérias"""
        pass

    @abstractmethod
    def buscar_salas(self) -> List[Sala]:
        """Busca todas as salas"""
        pass

    @abstractmethod
    def buscar_materia_por_id(self, materia_id: str) -> Optional[Materia]:
        """Busca matéria por ID"""
        pass

    @abstractmethod
    def buscar_sala_por_id(self, sala_id: str) -> Optional[Sala]:
        """Busca sala por ID"""
        pass


class Validator(ABC):
    """Interface para validadores"""

    @abstractmethod
    def validar_materia(self, materia: Materia) -> List[str]:
        """Valida uma matéria e retorna lista de erros"""
        pass

    @abstractmethod
    def validar_sala(self, sala: Sala) -> List[str]:
        """Valida uma sala e retorna lista de erros"""
        pass

    @abstractmethod
    def validar_alocacao(self, materia: Materia, sala: Sala) -> List[str]:
        """Valida uma alocação específica"""
        pass


class ValidatorPadrao(Validator):
    """Validador padrão com regras básicas"""

    def validar_materia(self, materia: Materia) -> List[str]:
        """Valida uma matéria"""
        erros = []

        if not materia.nome.strip():
            erros.append("Nome da matéria não pode ser vazio")

        if materia.inscritos <= 0:
            erros.append("Número de inscritos deve ser positivo")

        if not materia.horario.strip():
            erros.append("Horário não pode ser vazio")

        return erros

    def validar_sala(self, sala: Sala) -> List[str]:
        """Valida uma sala"""
        erros = []

        if not sala.nome.strip():
            erros.append("Nome da sala não pode ser vazio")

        if sala.capacidade <= 0:
            erros.append("Capacidade deve ser positiva")

        if sala.custo_adicional < 0:
            erros.append("Custo adicional não pode ser negativo")

        return erros

    def validar_alocacao(self, materia: Materia, sala: Sala) -> List[str]:
        """Valida uma alocação específica"""
        erros = []

        # Validações básicas
        erros.extend(self.validar_materia(materia))
        erros.extend(self.validar_sala(sala))

        # Validação de capacidade
        if materia.inscritos > sala.capacidade:
            erros.append(f"Capacidade da sala ({sala.capacidade}) insuficiente para {materia.inscritos} inscritos")

        return erros
