"""
Carregador de dados reais para o sistema de alocação de salas.
Converte dados do CSV da oferta de disciplinas para o formato do alocador.
"""

import pandas as pd
import re
from typing import List, Dict, Tuple
from alocador_salas import AlocadorSalas, Materia, Sala, TipoSala, LocalSala


class CarregadorDadosReais:
    """Carrega e converte dados reais para o formato do alocador"""
    
    def __init__(self):
        self.alocador = AlocadorSalas()
        self.salas_disponiveis = {}
        
    def carregar_dados_csv(self, arquivo_csv: str):
        """Carrega dados do arquivo CSV da oferta"""
        df = pd.read_csv(arquivo_csv)
        print(f"Carregados {len(df)} registros do arquivo {arquivo_csv}")
        return df

    def mapear_horario(self, horario_str: str) -> str:
        """Converte formato de horário do CSV para formato do alocador"""
        if pd.isna(horario_str) or horario_str == '':
            return "Indefinido"
        
        # Mapear códigos de horário para formato legível
        # Ex: "6T12" -> "Sexta 10:00-12:00"
        # Ex: "24T34" -> "Segunda 10:00-12:00"
        # Ex: "35M34" -> "Terça 10:00-12:00"
        
        # Dicionário de mapeamento de dias
        dias_map = {
            '2': 'Segunda', '3': 'Terça', '4': 'Quarta', 
            '5': 'Quinta', '6': 'Sexta', '7': 'Sábado'
        }
        
        # Dicionário de mapeamento de turnos
        turnos_map = {
            'M': '08:00-10:00',  # Manhã
            'T': '10:00-12:00',  # Tarde
            'N': '19:00-21:00'   # Noite
        }
        
        # Extrair dia, turno e período
        match = re.match(r'(\d+)([MTN])(\d+)', horario_str)
        if match:
            dia_num = match.group(1)
            turno = match.group(2)
            periodo = match.group(3)
            
            # Converter dia
            dia = dias_map.get(dia_num, f"Dia{dia_num}")
            
            # Converter turno
            horario = turnos_map.get(turno, "Indefinido")
            
            return f"{dia} {horario}"
        
        return horario_str
    
    def determinar_tipo_sala(self, local_str: str, nome_materia: str) -> TipoSala:
        """Determina o tipo de sala baseado no local e nome da matéria"""
        local_lower = local_str.lower()
        nome_lower = nome_materia.lower()
        
        # Palavras-chave que indicam laboratório
        lab_keywords = ['lab', 'laboratório', 'computação', 'programação', 'banco de dados', 
                       'redes', 'sistemas operacionais', 'inteligência artificial']
        
        # Palavras-chave que indicam auditório
        aud_keywords = ['auditório', 'auditorio']
        
        if any(keyword in local_lower for keyword in aud_keywords):
            return TipoSala.AUDITORIO
        elif any(keyword in nome_lower for keyword in lab_keywords):
            return TipoSala.LABORATORIO
        else:
            return TipoSala.AULA
    
    def determinar_localizacao(self, local_str: str) -> LocalSala:
        """Determina a localização da sala (IC ou IM)"""
        local_lower = local_str.lower()
        
        if 'im' in local_lower or 'matemática' in local_lower:
            return LocalSala.IM
        else:
            return LocalSala.IC
    
    def determinar_materiais_necessarios(self, tipo_sala: TipoSala, nome_materia: str) -> List[str]:
        """Determina os materiais necessários baseado no tipo de sala e matéria"""
        materiais = ["projetor", "quadro"]
        
        if tipo_sala == TipoSala.LABORATORIO:
            materiais.append("computadores")
        
        # Adicionar materiais específicos baseado no nome da matéria
        nome_lower = nome_materia.lower()
        if 'redes' in nome_lower or 'sistemas operacionais' in nome_lower:
            materiais.append("equipamentos_redes")
        
        return materiais
    
    def _corrigir_nome_sala(self, nome_sala: str) -> str:
        """Corrige nomes de salas com grafia incorreta"""
        correcoes = {
            'Istituto de Computaçãp': 'Instituto de Computação',
            'Instituição de Computação': 'Instituto de Computação',
            'Instituto de Computaçãp': 'Instituto de Computação',
            'Laboratório-01': 'Lab IC-01',
            'Sala-02-IC': 'Sala IC-02',
            'Sala-03-IC': 'Sala IC-03',
            'sala-25': 'Sala IC-25',
            'Auditório-IC': 'Auditório IC',
            'Bloco-12-IM-Sala-204': 'Sala IM-204',
            'Terça': 'Sala IC-Terça',
            'Quarta': 'Sala IC-Quarta',
            'Lab01': 'Lab IC-01'
        }
        
        return correcoes.get(nome_sala, nome_sala)
    
    def extrair_salas_unicas(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """Extrai salas únicas dos dados"""
        salas = {}
        
        for _, row in df.iterrows():
            local = str(row['local']).strip()
            if local == 'nan' or local == '':
                continue
                
            # Processar locais com múltiplas salas (ex: "Lab01(Segunda); Auditório-IC(Quarta)")
            locais = [l.strip() for l in local.split(';')]
            
            for local_item in locais:
                # Extrair nome da sala (remover horários entre parênteses)
                nome_sala = re.sub(r'\([^)]*\)', '', local_item).strip()
                
                # Corrigir nomes de salas com grafia incorreta
                nome_sala = self._corrigir_nome_sala(nome_sala)
                
                if nome_sala and nome_sala not in salas:
                    # Determinar tipo e localização
                    tipo = self.determinar_tipo_sala(local_item, row['nome'])
                    localizacao = self.determinar_localizacao(local_item)
                    
                    # Estimar capacidade baseada na matéria com maior número de matriculados
                    capacidade = int(row['capacidade'])
                    
                    # Determinar materiais
                    materiais = self.determinar_materiais_necessarios(tipo, row['nome'])
                    
                    # Custo adicional (penalizar IM)
                    custo = 15.0 if localizacao == LocalSala.IM else 0.0
                    
                    salas[nome_sala] = {
                        'nome': nome_sala,
                        'capacidade': capacidade,
                        'tipo': tipo,
                        'local': localizacao,
                        'materiais': materiais,
                        'custo': custo
                    }
        
        return salas
    
    def processar_materias(self, df: pd.DataFrame) -> List[Materia]:
        """Processa as matérias do DataFrame"""
        materias = []
        
        for i, row in df.iterrows():
            # Pular linhas vazias
            if pd.isna(row['codigo']) or pd.isna(row['nome']):
                continue
            
            # Converter horário
            horario = self.mapear_horario(row['horario'])
            
            # Determinar se precisa de laboratório
            nome_lower = str(row['nome']).lower()
            lab_keywords = ['programação', 'banco de dados', 'redes', 'sistemas operacionais', 
                           'inteligência artificial', 'computação gráfica', 'compiladores']
            precisa_lab = any(keyword in nome_lower for keyword in lab_keywords)
            
            # Determinar materiais necessários
            tipo_sala = TipoSala.LABORATORIO if precisa_lab else TipoSala.AULA
            materiais = self.determinar_materiais_necessarios(tipo_sala, row['nome'])
            
            materia = Materia(
                id=str(row['codigo']),
                nome=str(row['nome']),
                inscritos=int(row['matriculados']),
                horario=horario,
                precisa_lab=precisa_lab,
                materiais_necessarios=materiais
            )
            
            materias.append(materia)
        
        return materias
    
    def criar_salas_do_sistema(self, salas_dict: Dict[str, Dict]) -> List[Sala]:
        """Cria objetos Sala a partir do dicionário de salas"""
        salas = []
        
        for i, (nome, info) in enumerate(salas_dict.items()):
            sala = Sala(
                id=f"SALA_{i+1:03d}",
                nome=info['nome'],
                capacidade=info['capacidade'],
                tipo=info['tipo'],
                local=info['local'],
                materiais_disponiveis=info['materiais'],
                custo_adicional=info['custo']
            )
            salas.append(sala)
        
        return salas
    
    def carregar_dados_completos(self, arquivo_csv: str) -> AlocadorSalas:
        """Carrega todos os dados e configura o alocador"""
        print("=== CARREGANDO DADOS REAIS ===")
        
        # Carregar CSV
        df = self.carregar_dados_csv(arquivo_csv)
        
        # Processar matérias
        print("Processando matérias...")
        materias = self.processar_materias(df)
        print(f"✓ {len(materias)} matérias processadas")
        
        # Extrair salas únicas
        print("Extraindo salas únicas...")
        salas_dict = self.extrair_salas_unicas(df)
        print(f"✓ {len(salas_dict)} salas únicas encontradas")
        
        # Criar objetos Sala
        print("Criando objetos de salas...")
        salas = self.criar_salas_do_sistema(salas_dict)
        print(f"✓ {len(salas)} salas criadas")
        
        # Adicionar ao alocador
        for materia in materias:
            self.alocador.adicionar_materia(materia)
        
        for sala in salas:
            self.alocador.adicionar_sala(sala)
        
        print(f"\n=== RESUMO DOS DADOS CARREGADOS ===")
        print(f"Matérias: {len(materias)}")
        print(f"Salas: {len(salas)}")
        
        # Estatísticas por tipo de sala
        tipos = {}
        for sala in salas:
            tipo = sala.tipo.value
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        print(f"Tipos de salas: {tipos}")
        
        # Estatísticas por localização
        locais = {}
        for sala in salas:
            local = sala.local.value
            locais[local] = locais.get(local, 0) + 1
        
        print(f"Localizações: {locais}")
        
        return self.alocador
    
    def imprimir_estatisticas_materias(self):
        """Imprime estatísticas das matérias carregadas"""
        if not self.alocador.materias:
            print("Nenhuma matéria carregada")
            return
        
        print("\n=== ESTATÍSTICAS DAS MATÉRIAS ===")
        
        # Matérias por horário
        horarios = {}
        for materia in self.alocador.materias:
            horario = materia.horario
            horarios[horario] = horarios.get(horario, 0) + 1
        
        print("Matérias por horário:")
        for horario, count in sorted(horarios.items()):
            print(f"  {horario}: {count} matérias")
        
        # Matérias que precisam de laboratório
        lab_count = sum(1 for m in self.alocador.materias if m.precisa_lab)
        print(f"\nMatérias que precisam de laboratório: {lab_count}")
        
        # Distribuição de inscritos
        inscritos = [m.inscritos for m in self.alocador.materias]
        print(f"Total de inscritos: {sum(inscritos)}")
        print(f"Média de inscritos por matéria: {sum(inscritos)/len(inscritos):.1f}")
        print(f"Maior turma: {max(inscritos)} alunos")
        print(f"Menor turma: {min(inscritos)} alunos")


def main():
    """Função principal para testar o carregador"""
    carregador = CarregadorDadosReais()
    
    # Carregar dados reais
    alocador = carregador.carregar_dados_completos('oferta_cc_2025_1.csv')
    
    # Imprimir estatísticas
    carregador.imprimir_estatisticas_materias()
    
    # Tentar resolver o problema
    print("\n=== RESOLVENDO PROBLEMA DE ALOCAÇÃO ===")
    sucesso = alocador.resolver()
    
    if sucesso:
        print("✓ Solução encontrada!")
        alocador.imprimir_resumo()
        
        # Salvar resultados
        df = alocador.obter_resultados()
        df.to_csv('resultados_alocacao_real.csv', index=False)
        print(f"\nResultados salvos em 'resultados_alocacao_real.csv'")
    else:
        print("✗ Não foi possível encontrar uma solução viável")
        print("Isso pode acontecer devido a:")
        print("- Conflitos de horário")
        print("- Capacidade insuficiente")
        print("- Incompatibilidades entre matérias e salas")


if __name__ == "__main__":
    main()
