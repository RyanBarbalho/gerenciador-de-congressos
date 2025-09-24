# Documentação Técnica - Sistema de Alocação de Salas

## 📋 Visão Geral

Este sistema implementa uma solução de **Programação Linear Inteira** para o problema de alocação de salas em universidades, baseado no modelo matemático fornecido no prompt.

## 🧮 Modelo Matemático

### Variáveis de Decisão
```
x[m,s] = {1 se a matéria m for alocada na sala s
         {0 caso contrário
```

### Função Objetivo
```
min Σ Σ x[m,s] * (capacidade_s - inscritos_m + custo_s)
    m s
```

Onde:
- `capacidade_s - inscritos_m`: espaço ocioso
- `custo_s`: penalização para salas do IM

### Restrições Hard

1. **Alocação única**: Cada matéria em exatamente uma sala
   ```
   Σ x[m,s] = 1  ∀m
     s
   ```

2. **Capacidade**: Sala deve ter capacidade suficiente
   ```
   x[m,s] * inscritos_m ≤ capacidade_s  ∀m,s
   ```

3. **Compatibilidade**: Matéria deve ser compatível com sala
   ```
   x[m,s] = 0  se matéria m não compatível com sala s
   ```

4. **Sem conflitos**: Máximo uma matéria por sala por horário
   ```
   Σ x[m,s] ≤ 1  ∀s,∀horário
   m∈horário
   ```

## 🏗️ Arquitetura do Sistema

### Classes Principais

#### `Materia`
```python
@dataclass
class Materia:
    id: str                    # Identificador único
    nome: str                  # Nome da matéria
    inscritos: int             # Número de alunos inscritos
    horario: str               # Horário da aula
    precisa_lab: bool          # Se precisa de laboratório
    materiais_necessarios: List[str]  # Materiais necessários
```

#### `Sala`
```python
@dataclass
class Sala:
    id: str                    # Identificador único
    nome: str                  # Nome da sala
    capacidade: int            # Capacidade máxima
    tipo: TipoSala             # Tipo (AULA, LABORATORIO, AUDITORIO)
    local: LocalSala           # Localização (IC, IM)
    materiais_disponiveis: List[str]  # Materiais disponíveis
    custo_adicional: float     # Custo de penalização
```

#### `AlocadorSalas`
Classe principal que implementa o solver de programação linear.

### Métodos Principais

#### `adicionar_materia(materia: Materia)`
Adiciona uma matéria ao problema de otimização.

#### `adicionar_sala(sala: Sala)`
Adiciona uma sala ao problema de otimização.

#### `resolver() -> bool`
Resolve o problema de programação linear inteira.
- Retorna `True` se encontrou solução ótima
- Retorna `False` se problema é infeasível

#### `obter_resultados() -> pd.DataFrame`
Retorna os resultados da alocação em formato DataFrame.

## 🔧 Implementação Técnica

### Solver Utilizado
- **PuLP** com solver **CBC** (Coin-or Branch and Cut)
- Adequado para problemas de programação linear inteira de tamanho médio

### Estrutura de Dados
- **Variáveis de decisão**: Dicionário `{(materia_id, sala_id): LpVariable}`
- **Restrições**: Adicionadas dinamicamente ao modelo PuLP
- **Resultados**: Extraídos da solução ótima

### Algoritmo de Resolução

1. **Criação de variáveis**: Apenas para combinações viáveis (matéria-sala compatíveis)
2. **Função objetivo**: Minimização de espaço ocioso + custos
3. **Restrições hard**: Capacidade, compatibilidade, conflitos
4. **Resolução**: PuLP com CBC
5. **Extração**: Solução convertida para formato legível

## 📊 Análise de Complexidade

### Complexidade Computacional
- **Variáveis**: O(M × S) onde M = matérias, S = salas
- **Restrições**: O(M + M×S + H×S) onde H = horários únicos
- **Tempo**: Exponencial no pior caso (problema NP-hard)

### Limitações Práticas
- **Tamanho máximo**: ~1000 variáveis (recomendado)
- **Solver**: CBC é gratuito mas pode ser lento para problemas grandes
- **Alternativas**: Gurobi, CPLEX para problemas maiores

## 🎯 Casos de Uso

### Uso Básico
```python
from alocacao_salas import AlocadorSalas, Materia, Sala, TipoSala, LocalSala

alocador = AlocadorSalas()

# Adicionar dados
alocador.adicionar_materia(materia)
alocador.adicionar_sala(sala)

# Resolver
if alocador.resolver():
    resultados = alocador.obter_resultados()
```

### Uso Avançado
```python
# Ajustar penalizações
for sala in alocador.salas:
    if sala.local == LocalSala.IM:
        sala.custo_adicional = 20.0

# Adicionar restrições customizadas
alocador.problema += (
    alocador.variaveis[("MAT001", "IC101")] == 1,
    "forcar_alocacao"
)
```

## 🔍 Validação e Testes

### Testes Implementados
- ✅ **Viabilidade**: Verificação de solução ótima
- ✅ **Restrições**: Validação de capacidades e conflitos
- ✅ **Compatibilidade**: Verificação de materiais necessários
- ✅ **Penalizações**: Efeito dos custos adicionais

### Métricas de Qualidade
- **Utilização média**: Percentual de ocupação das salas
- **Espaço ocioso**: Capacidade não utilizada
- **Distribuição**: IC vs IM, tipos de salas
- **Conflitos**: Verificação de sobreposições

## 🚀 Extensões Possíveis

### Funcionalidades Adicionais
1. **Restrições de distância**: Penalizar salas muito distantes
2. **Preferências de professores**: Custos baseados em preferências
3. **Horários flexíveis**: Múltiplos horários possíveis por matéria
4. **Sala compartilhada**: Múltiplas matérias na mesma sala
5. **Análise de sensibilidade**: Efeito de mudanças nos parâmetros

### Otimizações
1. **Solver híbrido**: Heurística + exato
2. **Decomposição**: Dividir problema em subproblemas
3. **Paralelização**: Resolver múltiplos cenários
4. **Cache**: Armazenar soluções parciais

## 📈 Performance

### Benchmarks
- **Problema pequeno** (10 matérias, 10 salas): < 1 segundo
- **Problema médio** (50 matérias, 30 salas): 1-10 segundos
- **Problema grande** (100+ matérias, 50+ salas): 10+ segundos

### Fatores que Afetam Performance
- **Número de variáveis**: Principal fator
- **Densidade de restrições**: Mais restrições = mais lento
- **Tipo de solver**: CBC vs Gurobi vs CPLEX
- **Qualidade da solução**: Ótima vs viável

## 🛠️ Manutenção

### Dependências
- `pulp>=2.7.0`: Solver de programação linear
- `pandas>=1.5.0`: Manipulação de dados
- `numpy>=1.21.0`: Operações numéricas

### Atualizações
- **Solver**: Atualizar PuLP para versões mais recentes
- **Dados**: Manter compatibilidade com formatos de entrada
- **Restrições**: Adicionar novas restrições conforme necessário

## 📚 Referências

1. **PuLP Documentation**: https://pypi.org/project/PuLP/
2. **CBC Solver**: https://github.com/coin-or/Cbc
3. **Programação Linear Inteira**: Hillier & Lieberman
4. **Otimização Combinatória**: Papadimitriou & Steiglitz

## 🤝 Contribuição

### Como Contribuir
1. Fork do repositório
2. Criar branch para feature
3. Implementar mudanças
4. Testes unitários
5. Pull request

### Áreas de Melhoria
- [ ] Interface gráfica
- [ ] API REST
- [ ] Integração com sistemas acadêmicos
- [ ] Análise de sensibilidade
- [ ] Relatórios avançados
- [ ] Otimizações de performance
