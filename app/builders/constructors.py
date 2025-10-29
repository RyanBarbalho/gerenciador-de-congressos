"""
Builder Pattern para construção complexa do sistema de alocação de salas.
Permite construção flexível e configurável do sistema.
"""

from typing import List, Optional, Dict, Any
from ..models.domain import Materia, Sala, Subject
from ..strategies.interfaces import CompatibilidadeStrategy, Compatibilidade, Validator, ValidatorPadrao
from ..factories.creators import FactoryManager


class AlocadorBuilder:
    """Builder para construção do sistema de alocação"""

    def __init__(self):
        self.reset()

    def reset(self) -> 'AlocadorBuilder':
        """Reseta o builder para uma nova construção"""
        self._materias: List[Materia] = []
        self._salas: List[Sala] = []
        self._compatibilidade_strategy: Optional[CompatibilidadeStrategy] = None
        self._validator: Optional[Validator] = None
        self._factory_manager: Optional[FactoryManager] = None
        self._observers: List[Subject] = []
        return self

    def com_materias(self, materias: List[Materia]) -> 'AlocadorBuilder':
        """Adiciona matérias ao sistema"""
        self._materias.extend(materias)
        return self

    def com_salas(self, salas: List[Sala]) -> 'AlocadorBuilder':
        """Adiciona salas ao sistema"""
        self._salas.extend(salas)
        return self

    def com_compatibilidade_strategy(self, strategy: CompatibilidadeStrategy) -> 'AlocadorBuilder':
        """Define estratégia de compatibilidade"""
        self._compatibilidade_strategy = strategy
        return self

    def com_validator(self, validator: Validator) -> 'AlocadorBuilder':
        """Define validador"""
        self._validator = validator
        return self

    def com_factory_manager(self, factory_manager: FactoryManager) -> 'AlocadorBuilder':
        """Define gerenciador de factories"""
        self._factory_manager = factory_manager
        return self

    def com_observer(self, observer: Subject) -> 'AlocadorBuilder':
        """Adiciona observador"""
        self._observers.append(observer)
        return self

    def construir(self) -> 'AlocadorSalasRefatorado':
        """Constrói o sistema de alocação"""
        # Validações básicas
        if not self._materias:
            raise ValueError("Pelo menos uma matéria deve ser fornecida")

        if not self._salas:
            raise ValueError("Pelo menos uma sala deve ser fornecida")

        # Configurações padrão se não fornecidas
        if self._compatibilidade_strategy is None:
            self._compatibilidade_strategy = Compatibilidade()

        if self._validator is None:
            self._validator = ValidatorPadrao()

        if self._factory_manager is None:
            self._factory_manager = FactoryManager()

        # Criar o sistema
        alocador = AlocadorSalasRefatorado(
            materias=self._materias,
            salas=self._salas,
            compatibilidade_strategy=self._compatibilidade_strategy,
            validator=self._validator,
            factory_manager=self._factory_manager
        )

        # Adicionar observadores
        for observer in self._observers:
            alocador.adicionar_observer(observer)

        return alocador


class SistemaAlocacaoBuilder:
    """Builder para construção de um sistema completo de alocação"""

    def __init__(self):
        self.reset()

    def reset(self) -> 'SistemaAlocacaoBuilder':
        """Reseta o builder"""
        self._configuracao: Dict[str, Any] = {}
        self._dados_csv: Optional[str] = None
        self._configuracao_personalizada: Dict[str, Any] = {}
        return self

    def com_configuracao_padrao(self) -> 'SistemaAlocacaoBuilder':
        """Usa configuração padrão"""
        self._configuracao = {
            'compatibilidade': 'padrao',
            'validator': 'padrao',
            'factory': 'padrao',
            'notificacoes': True
        }
        return self

    def com_dados_csv(self, arquivo_csv: str) -> 'SistemaAlocacaoBuilder':
        """Define arquivo CSV para carregar dados"""
        self._dados_csv = arquivo_csv
        return self

    def com_configuracao_personalizada(self, config: Dict[str, Any]) -> 'SistemaAlocacaoBuilder':
        """Define configuração personalizada"""
        self._configuracao_personalizada = config
        return self

    def construir(self) -> 'SistemaAlocacaoCompleto':
        """Constrói o sistema completo"""
        # Aplicar configuração personalizada sobre a padrão
        config_final = self._configuracao.copy()
        config_final.update(self._configuracao_personalizada)

        # Criar componentes
        factory_manager = FactoryManager()

        # Criar sistema
        sistema = SistemaAlocacaoCompleto(
            configuracao=config_final,
            factory_manager=factory_manager
        )

        # Carregar dados se especificado
        if self._dados_csv:
            sistema.carregar_dados_csv(self._dados_csv)

        return sistema


class AlocadorSalasRefatorado:
    """Sistema de alocação refatorado usando padrões de projeto"""

    def __init__(self, materias: List[Materia], salas: List[Sala],
                 compatibilidade_strategy: CompatibilidadeStrategy,
                 validator: Validator, factory_manager: FactoryManager):
        self.materias = materias
        self.salas = salas
        self.compatibilidade_strategy = compatibilidade_strategy
        self.validator = validator
        self.factory_manager = factory_manager
        self._observers: List[Subject] = []

    def adicionar_observer(self, observer: Subject):
        """Adiciona observador"""
        self._observers.append(observer)

    def validar_sistema(self) -> List[str]:
        """Valida todo o sistema"""
        erros = []

        # Validar matérias
        for materia in self.materias:
            erros.extend(self.validator.validar_materia(materia))

        # Validar salas
        for sala in self.salas:
            erros.extend(self.validator.validar_sala(sala))

        # Validar compatibilidades
        for materia in self.materias:
            salas_compatíveis = self._filtrar_salas_compatíveis(materia)
            if not salas_compatíveis:
                erros.append(f"Nenhuma sala compatível encontrada para matéria {materia.nome}")

        return erros

    def _filtrar_salas_compatíveis(self, materia: Materia) -> List[Sala]:
        """Filtra salas compatíveis com a matéria"""
        return [sala for sala in self.salas
                if self.compatibilidade_strategy.eh_compativel(materia, sala)]

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do sistema"""
        total_materias = len(self.materias)
        total_salas = len(self.salas)
        total_inscritos = sum(m.inscritos for m in self.materias)
        capacidade_total = sum(s.capacidade for s in self.salas)

        # Estatísticas por tipo de sala
        tipos_sala = {}
        for sala in self.salas:
            tipo = sala.tipo.value
            tipos_sala[tipo] = tipos_sala.get(tipo, 0) + 1

        # Estatísticas por localização
        locais = {}
        for sala in self.salas:
            local = sala.local.value
            locais[local] = locais.get(local, 0) + 1

        return {
            'total_materias': total_materias,
            'total_salas': total_salas,
            'total_inscritos': total_inscritos,
            'capacidade_total': capacidade_total,
            'tipos_sala': tipos_sala,
            'locais': locais,
            'utilizacao_potencial': (total_inscritos / capacidade_total * 100) if capacidade_total > 0 else 0
        }


class SistemaAlocacaoCompleto:
    """Sistema completo de alocação com todas as funcionalidades"""

    def __init__(self, configuracao: Dict[str, Any], factory_manager: FactoryManager):
        self.configuracao = configuracao
        self.factory_manager = factory_manager
        self.alocador: Optional[AlocadorSalasRefatorado] = None

    def carregar_dados_csv(self, arquivo_csv: str):
        """Carrega dados de um arquivo CSV"""
        # Esta implementação seria expandida para carregar dados reais
        # Por enquanto, cria dados de exemplo
        pass

    def criar_sistema_basico(self) -> AlocadorSalasRefatorado:
        """Cria um sistema básico para testes"""
        builder = AlocadorBuilder()

        # Criar dados de exemplo
        materias_dados = [
            {'id': 'MAT001', 'nome': 'Cálculo I', 'inscritos': 45, 'horario': 'Segunda 08:00-10:00'},
            {'id': 'COMP001', 'nome': 'Programação I', 'inscritos': 30, 'horario': 'Segunda 14:00-16:00', 'precisa_lab': True}
        ]

        salas_dados = [
            {'id': 'IC101', 'nome': 'Sala IC-101', 'capacidade': 50, 'tipo': 'aula', 'local': 'ic'},
            {'id': 'IC301', 'nome': 'Lab IC-301', 'capacidade': 35, 'tipo': 'laboratorio', 'local': 'ic'}
        ]

        materias = self.factory_manager.criar_multiplas_materias(materias_dados)
        salas = self.factory_manager.criar_multiplas_salas(salas_dados)

        self.alocador = builder.com_materias(materias).com_salas(salas).construir()
        return self.alocador
