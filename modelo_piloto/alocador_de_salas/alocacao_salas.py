"""
Solução de Programação Linear Inteira para Alocação de Salas
Baseado no modelo matemático fornecido no prompt.

Este módulo implementa um solver para alocar matérias em salas considerando:
- Capacidade das salas
- Compatibilidade de materiais
- Conflitos de horário
- Preferência por salas do IC sobre IM
- Minimização de espaços ociosos
"""

import pulp
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class TipoSala(Enum):
    """Tipos de salas disponíveis"""
    AULA = "aula"
    LABORATORIO = "laboratorio"
    AUDITORIO = "auditorio"


class LocalSala(Enum):
    """Localização das salas"""
    IC = "ic"  # Instituto de Computação
    IM = "im"  # Instituto de Matemática


@dataclass
class Materia:
    """Representa uma matéria a ser alocada"""
    id: str
    nome: str
    inscritos: int
    horario: str  # Formato: "Segunda 14:00-16:00"
    material: int  # 0 = nenhum, 1 = computadores, 2 = robótica, 3 = eletrônica


@dataclass
class Sala:
    """Representa uma sala disponível"""
    id: str
    nome: str
    capacidade: int
    tipo: TipoSala
    local: LocalSala
    tipo_equipamento: int  # 1 = computadores, 2 = robótica, 3 = eletrônica, 0 = nenhum
    materiais_disponiveis: List[str]
    custo_adicional: float = 0.0  # Para penalizar salas do IM


class AlocadorSalas:
    """Solver principal para alocação de salas"""

    def __init__(self):
        self.materias: List[Materia] = []
        self.salas: List[Sala] = []
        self.problema = None
        self.variaveis = {}
        self.solucao = None

    def adicionar_materia(self, materia: Materia):
        """Adiciona uma matéria ao problema"""
        self.materias.append(materia)

    def adicionar_sala(self, sala: Sala):
        """Adiciona uma sala ao problema"""
        self.salas.append(sala)

    def _criar_variaveis_decisao(self):
        """Cria as variáveis de decisão x[m,s]"""
        self.variaveis = {}

        for materia in self.materias:
            for sala in self.salas:
                # Verifica se a matéria é compatível com a sala
                if self._eh_compativel(materia, sala):
                    var_name = f"x_{materia.id}_{sala.id}"
                    self.variaveis[(materia.id, sala.id)] = pulp.LpVariable(
                        var_name, cat='Binary'
                    )

    def _eh_compativel(self, materia: Materia, sala: Sala) -> bool:
        """Verifica se uma matéria é compatível com uma sala"""
        # Se a matéria precisa de material especial, só pode ir para laboratório
        if materia.material > 0 and sala.tipo != TipoSala.LABORATORIO:
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

    def _criar_funcao_objetivo(self):
        """Cria a função objetivo: minimizar espaços ociosos + custos adicionais"""
        objetivo = 0

        for materia in self.materias:
            for sala in self.salas:
                if (materia.id, sala.id) in self.variaveis:
                    # Espaço ocioso: capacidade - inscritos
                    espaco_ocioso = sala.capacidade - materia.inscritos
                    # Custo adicional (penalização para salas do IM)
                    custo_total = espaco_ocioso + sala.custo_adicional

                    objetivo += self.variaveis[(materia.id, sala.id)] * custo_total

        self.problema += objetivo

    def _criar_restricoes_hard(self):
        """Cria as restrições hard do problema"""

        # 1. Cada matéria deve ser alocada em exatamente uma sala
        for materia in self.materias:
            restricao = 0
            for sala in self.salas:
                if (materia.id, sala.id) in self.variaveis:
                    restricao += self.variaveis[(materia.id, sala.id)]

            self.problema += restricao == 1, f"alocacao_unica_{materia.id}"

        # 2. Capacidade da sala deve ser suficiente
        for materia in self.materias:
            for sala in self.salas:
                if (materia.id, sala.id) in self.variaveis:
                    self.problema += (
                        self.variaveis[(materia.id, sala.id)] * materia.inscritos <= sala.capacidade,
                        f"capacidade_{materia.id}_{sala.id}"
                    )

        # 3. Sem conflito de horários na mesma sala
        #TODO: verificar funcionamento dessa hrad constraint com os dados do IC
        horarios = self._agrupar_por_horario()
        for horario, materias_horario in horarios.items():
            for sala in self.salas:
                restricao = 0
                for materia in materias_horario:
                    if (materia.id, sala.id) in self.variaveis:
                        restricao += self.variaveis[(materia.id, sala.id)]

                if restricao != 0:  # Só cria restrição se houver variáveis
                    self.problema += restricao <= 1, f"sem_conflito_{horario}_{sala.id}"

    def _agrupar_por_horario(self) -> Dict[str, List[Materia]]:
        """Agrupa matérias por horário para detectar conflitos"""
        horarios = {}
        for materia in self.materias:
            if materia.horario not in horarios:
                horarios[materia.horario] = []
            horarios[materia.horario].append(materia)
        return horarios

    def resolver(self) -> bool:
        """Resolve o problema de alocação"""
        if not self.materias or not self.salas:
            raise ValueError("É necessário adicionar matérias e salas antes de resolver")

        # Cria o problema
        self.problema = pulp.LpProblem("AlocacaoSalas", pulp.LpMinimize)

        # Cria variáveis e restrições
        self._criar_variaveis_decisao()
        self._criar_funcao_objetivo()
        self._criar_restricoes_hard()

        # Resolve o problema
        self.problema.solve(pulp.PULP_CBC_CMD(msg=0))

        # Verifica se encontrou solução
        if pulp.LpStatus[self.problema.status] == "Optimal":
            self.solucao = self._extrair_solucao()
            return True
        else:
            print(f"Status da solução: {pulp.LpStatus[self.problema.status]}")
            return False

    def _extrair_solucao(self) -> Dict[str, str]:
        """Extrai a solução encontrada"""
        solucao = {}

        for (materia_id, sala_id), var in self.variaveis.items():
            if var.varValue == 1:
                solucao[materia_id] = sala_id

        return solucao

    def obter_resultados(self) -> pd.DataFrame:
        """Retorna os resultados em formato DataFrame"""
        if not self.solucao:
            raise ValueError("Problema não foi resolvido ainda")

        resultados = []

        for materia in self.materias:
            if materia.id in self.solucao:
                sala_id = self.solucao[materia.id]
                sala = next(s for s in self.salas if s.id == sala_id)

                espaco_ocioso = sala.capacidade - materia.inscritos
                utilizacao = (materia.inscritos / sala.capacidade) * 100

                resultados.append({
                    'Materia': materia.nome,
                    'Inscritos': materia.inscritos,
                    'Sala': sala.nome,
                    'Capacidade': sala.capacidade,
                    'Espaco_Ocioso': espaco_ocioso,
                    'Utilizacao_%': round(utilizacao, 2),
                    'Tipo_Sala': sala.tipo.value,
                    'Local': sala.local.value,
                    'Horario': materia.horario
                })

        return pd.DataFrame(resultados)

    def imprimir_resumo(self):
        """Imprime um resumo da solução"""
        if not self.solucao:
            print("Nenhuma solução encontrada")
            return

        df = self.obter_resultados()

        print("=== RESUMO DA ALOCAÇÃO ===")
        print(f"Total de matérias alocadas: {len(df)}")
        print(f"Espaço ocioso total: {df['Espaco_Ocioso'].sum()}")
        print(f"Utilização média: {df['Utilizacao_%'].mean():.2f}%")
        print()

        print("=== ALOCAÇÕES POR SALA ===")
        for _, row in df.iterrows():
            print(f"{row['Materia']} -> {row['Sala']} "
                  f"({row['Inscritos']}/{row['Capacidade']}, "
                  f"{row['Utilizacao_%']:.1f}% utilizado)")

        print()
        print("=== SALAS DO IM UTILIZADAS ===")
        salas_im = df[df['Local'] == 'im']
        if len(salas_im) > 0:
            for _, row in salas_im.iterrows():
                print(f"{row['Materia']} -> {row['Sala']} (IM)")
        else:
            print("Nenhuma sala do IM foi utilizada")


def criar_dados_exemplo():
    """Cria dados de exemplo para testar o sistema"""
    alocador = AlocadorSalas()

    # Criar matérias
    materias = [
        Materia("MAT001", "Cálculo I", 45, "Segunda 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("MAT002", "Cálculo II", 38, "Segunda 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("COMP001", "Programação I", 30, "Segunda 14:00-16:00", True, ["computadores"]),
        Materia("COMP002", "Estruturas de Dados", 25, "Segunda 16:00-18:00", True, ["computadores"]),
        Materia("COMP003", "Algoritmos", 20, "Terça 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("COMP004", "Banco de Dados", 35, "Terça 10:00-12:00", True, ["computadores"]),
        Materia("MAT003", "Álgebra Linear", 40, "Terça 14:00-16:00", False, ["projetor", "quadro"]),
        Materia("COMP005", "Redes de Computadores", 28, "Terça 16:00-18:00", True, ["computadores"]),
        Materia("MAT004", "Estatística", 35, "Quarta 08:00-10:00", False, ["projetor", "quadro"]),
        Materia("COMP006", "Inteligência Artificial", 22, "Quarta 10:00-12:00", True, ["computadores"]),
    ]

    for materia in materias:
        alocador.adicionar_materia(materia)

    # Criar salas
    salas = [
        # Salas do IC (preferidas)
        Sala("IC101", "Sala IC-101", 50, TipoSala.AULA, LocalSala.IC,
             ["projetor", "quadro"], 0.0),
        Sala("IC102", "Sala IC-102", 40, TipoSala.AULA, LocalSala.IC,
             ["projetor", "quadro"], 0.0),
        Sala("IC201", "Sala IC-201", 30, TipoSala.AULA, LocalSala.IC,
             ["projetor", "quadro"], 0.0),
        Sala("IC202", "Sala IC-202", 25, TipoSala.AULA, LocalSala.IC,
             ["projetor", "quadro"], 0.0),
        Sala("IC301", "Lab IC-301", 35, TipoSala.LABORATORIO, LocalSala.IC,
             ["computadores", "projetor"], 0.0),
        Sala("IC302", "Lab IC-302", 30, TipoSala.LABORATORIO, LocalSala.IC,
             ["computadores", "projetor"], 0.0),
        Sala("IC303", "Lab IC-303", 25, TipoSala.LABORATORIO, LocalSala.IC,
             ["computadores", "projetor"], 0.0),

        # Salas do IM (penalizadas)
        Sala("IM101", "Sala IM-101", 60, TipoSala.AULA, LocalSala.IM,
             ["projetor", "quadro"], 10.0),
        Sala("IM102", "Sala IM-102", 35, TipoSala.AULA, LocalSala.IM,
             ["projetor", "quadro"], 10.0),
        Sala("IM201", "Lab IM-201", 30, TipoSala.LABORATORIO, LocalSala.IM,
             ["computadores", "projetor"], 15.0),
    ]

    for sala in salas:
        alocador.adicionar_sala(sala)

    return alocador


def main():
    """Função principal para demonstrar o uso"""
    print("=== SOLVER DE ALOCAÇÃO DE SALAS ===\n")

    # Criar dados de exemplo
    alocador = criar_dados_exemplo()

    print("Dados carregados:")
    print(f"- {len(alocador.materias)} matérias")
    print(f"- {len(alocador.salas)} salas")
    print()

    # Resolver o problema
    print("Resolvendo problema de alocação...")
    sucesso = alocador.resolver()

    if sucesso:
        print("✓ Solução encontrada!\n")
        alocador.imprimir_resumo()

        # Salvar resultados em CSV
        df = alocador.obter_resultados()
        df.to_csv('resultados_alocacao.csv', index=False)
        print(f"\nResultados salvos em 'resultados_alocacao.csv'")

    else:
        print("✗ Não foi possível encontrar uma solução viável")
        print("Tente ajustar os dados ou relaxar algumas restrições")


if __name__ == "__main__":
    main()
