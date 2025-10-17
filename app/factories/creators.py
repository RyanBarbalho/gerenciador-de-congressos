"""
Factories para criação de objetos do sistema de alocação de salas.
Implementa Factory Pattern para criação consistente de objetos.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from ..models.domain import Materia, Sala, TipoSala, LocalSala


class MateriaFactory(ABC):
    """Factory abstrato para criação de matérias"""
    
    @abstractmethod
    def criar_materia(self, dados: Dict[str, Any]) -> Materia:
        """Cria uma matéria a partir de dados"""
        pass


class SalaFactory(ABC):
    """Factory abstrato para criação de salas"""
    
    @abstractmethod
    def criar_sala(self, dados: Dict[str, Any]) -> Sala:
        """Cria uma sala a partir de dados"""
        pass


class MateriaFactoryPadrao(MateriaFactory):
    """Factory padrão para criação de matérias"""
    
    def criar_materia(self, dados: Dict[str, Any]) -> Materia:
        """Cria uma matéria com validação básica"""
        # Campos obrigatórios
        campos_obrigatorios = ['id', 'nome', 'inscritos', 'horario']
        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValueError(f"Campo obrigatório '{campo}' não encontrado")
        
        # Campos opcionais com valores padrão
        precisa_lab = dados.get('precisa_lab', False)
        materiais_necessarios = dados.get('materiais_necessarios', [])
        
        return Materia(
            id=str(dados['id']),
            nome=str(dados['nome']),
            inscritos=int(dados['inscritos']),
            horario=str(dados['horario']),
            precisa_lab=bool(precisa_lab),
            materiais_necessarios=list(materiais_necessarios)
        )


class SalaFactoryPadrao(SalaFactory):
    """Factory padrão para criação de salas"""
    
    def criar_sala(self, dados: Dict[str, Any]) -> Sala:
        """Cria uma sala com validação básica"""
        # Campos obrigatórios
        campos_obrigatorios = ['id', 'nome', 'capacidade', 'tipo', 'local']
        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValueError(f"Campo obrigatório '{campo}' não encontrado")
        
        # Converter tipo e local para enums
        tipo = self._converter_tipo_sala(dados['tipo'])
        local = self._converter_local_sala(dados['local'])
        
        # Campos opcionais com valores padrão
        materiais_disponiveis = dados.get('materiais_disponiveis', [])
        custo_adicional = dados.get('custo_adicional', 0.0)
        
        return Sala(
            id=str(dados['id']),
            nome=str(dados['nome']),
            capacidade=int(dados['capacidade']),
            tipo=tipo,
            local=local,
            materiais_disponiveis=list(materiais_disponiveis),
            custo_adicional=float(custo_adicional)
        )
    
    def _converter_tipo_sala(self, tipo_str: str) -> TipoSala:
        """Converte string para TipoSala"""
        tipo_map = {
            'aula': TipoSala.AULA,
            'laboratorio': TipoSala.LABORATORIO,
            'laboratório': TipoSala.LABORATORIO,
            'auditorio': TipoSala.AUDITORIO,
            'auditório': TipoSala.AUDITORIO
        }
        
        tipo_lower = str(tipo_str).lower()
        if tipo_lower not in tipo_map:
            raise ValueError(f"Tipo de sala inválido: {tipo_str}")
        
        return tipo_map[tipo_lower]
    
    def _converter_local_sala(self, local_str: str) -> LocalSala:
        """Converte string para LocalSala"""
        local_map = {
            'ic': LocalSala.IC,
            'im': LocalSala.IM,
            'instituto de computação': LocalSala.IC,
            'instituto de matemática': LocalSala.IM
        }
        
        local_lower = str(local_str).lower()
        if local_lower not in local_map:
            raise ValueError(f"Local de sala inválido: {local_str}")
        
        return local_map[local_lower]


class MateriaFactoryCSV(MateriaFactory):
    """Factory especializado para criação de matérias a partir de CSV"""
    
    def __init__(self, materia_factory: MateriaFactory = None):
        self.materia_factory = materia_factory or MateriaFactoryPadrao()
    
    def criar_materia(self, dados: Dict[str, Any]) -> Materia:
        """Cria matéria a partir de dados CSV"""
        # Mapear campos do CSV para campos da matéria
        dados_normalizados = self._normalizar_dados_csv(dados)
        return self.materia_factory.criar_materia(dados_normalizados)
    
    def _normalizar_dados_csv(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza dados do CSV para formato padrão"""
        # Mapeamento de campos CSV para campos da matéria
        mapeamento = {
            'codigo': 'id',
            'nome': 'nome',
            'matriculados': 'inscritos',
            'horario': 'horario'
        }
        
        dados_normalizados = {}
        for campo_csv, campo_materia in mapeamento.items():
            if campo_csv in dados:
                dados_normalizados[campo_materia] = dados[campo_csv]
        
        # Determinar se precisa de laboratório baseado no nome
        nome_lower = str(dados.get('nome', '')).lower()
        lab_keywords = ['programação', 'banco de dados', 'redes', 'sistemas operacionais', 
                       'inteligência artificial', 'computação gráfica', 'compiladores']
        precisa_lab = any(keyword in nome_lower for keyword in lab_keywords)
        
        dados_normalizados['precisa_lab'] = precisa_lab
        
        # Determinar materiais necessários
        materiais = ["projetor", "quadro"]
        if precisa_lab:
            materiais.append("computadores")
        
        dados_normalizados['materiais_necessarios'] = materiais
        
        return dados_normalizados


class SalaFactoryCSV(SalaFactory):
    """Factory especializado para criação de salas a partir de CSV"""
    
    def __init__(self, sala_factory: SalaFactory = None):
        self.sala_factory = sala_factory or SalaFactoryPadrao()
    
    def criar_sala(self, dados: Dict[str, Any]) -> Sala:
        """Cria sala a partir de dados CSV"""
        # Mapear campos do CSV para campos da sala
        dados_normalizados = self._normalizar_dados_csv(dados)
        return self.sala_factory.criar_sala(dados_normalizados)
    
    def _normalizar_dados_csv(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza dados do CSV para formato padrão"""
        # Mapeamento de campos CSV para campos da sala
        dados_normalizados = {
            'id': dados.get('id', f"SALA_{dados.get('nome', 'UNKNOWN')}"),
            'nome': dados.get('nome', 'Sala Desconhecida'),
            'capacidade': dados.get('capacidade', 30),
            'tipo': self._determinar_tipo_sala(dados),
            'local': self._determinar_localizacao(dados),
            'materiais_disponiveis': self._determinar_materiais(dados),
            'custo_adicional': self._calcular_custo_adicional(dados)
        }
        
        return dados_normalizados
    
    def _determinar_tipo_sala(self, dados: Dict[str, Any]) -> str:
        """Determina o tipo de sala baseado nos dados"""
        local_str = str(dados.get('local', '')).lower()
        nome_str = str(dados.get('nome', '')).lower()
        
        # Palavras-chave que indicam laboratório
        lab_keywords = ['lab', 'laboratório', 'computação', 'programação']
        
        # Palavras-chave que indicam auditório
        aud_keywords = ['auditório', 'auditorio']
        
        if any(keyword in local_str or keyword in nome_str for keyword in aud_keywords):
            return 'auditorio'
        elif any(keyword in local_str or keyword in nome_str for keyword in lab_keywords):
            return 'laboratorio'
        else:
            return 'aula'
    
    def _determinar_localizacao(self, dados: Dict[str, Any]) -> str:
        """Determina a localização da sala"""
        local_str = str(dados.get('local', '')).lower()
        
        if 'im' in local_str or 'matemática' in local_str:
            return 'im'
        else:
            return 'ic'
    
    def _determinar_materiais(self, dados: Dict[str, Any]) -> List[str]:
        """Determina os materiais disponíveis"""
        materiais = ["projetor", "quadro"]
        
        tipo_str = self._determinar_tipo_sala(dados)
        if tipo_str == 'laboratorio':
            materiais.append("computadores")
        
        return materiais
    
    def _calcular_custo_adicional(self, dados: Dict[str, Any]) -> float:
        """Calcula custo adicional baseado na localização"""
        local_str = str(dados.get('local', '')).lower()
        
        if 'im' in local_str or 'matemática' in local_str:
            return 15.0
        else:
            return 0.0


class FactoryManager:
    """Gerenciador de factories para criação centralizada de objetos"""
    
    def __init__(self):
        self.materia_factory = MateriaFactoryPadrao()
        self.sala_factory = SalaFactoryPadrao()
        self.materia_csv_factory = MateriaFactoryCSV()
        self.sala_csv_factory = SalaFactoryCSV()
    
    def criar_materia(self, dados: Dict[str, Any], fonte: str = 'padrao') -> Materia:
        """Cria matéria usando factory apropriado"""
        if fonte == 'csv':
            return self.materia_csv_factory.criar_materia(dados)
        else:
            return self.materia_factory.criar_materia(dados)
    
    def criar_sala(self, dados: Dict[str, Any], fonte: str = 'padrao') -> Sala:
        """Cria sala usando factory apropriado"""
        if fonte == 'csv':
            return self.sala_csv_factory.criar_sala(dados)
        else:
            return self.sala_factory.criar_sala(dados)
    
    def criar_multiplas_materias(self, lista_dados: List[Dict[str, Any]], 
                                fonte: str = 'padrao') -> List[Materia]:
        """Cria múltiplas matérias"""
        return [self.criar_materia(dados, fonte) for dados in lista_dados]
    
    def criar_multiplas_salas(self, lista_dados: List[Dict[str, Any]], 
                             fonte: str = 'padrao') -> List[Sala]:
        """Cria múltiplas salas"""
        return [self.criar_sala(dados, fonte) for dados in lista_dados]
