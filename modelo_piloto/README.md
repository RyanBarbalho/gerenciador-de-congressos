# Sistema de Alocação de Salas - Programação Linear Inteira

Este projeto implementa uma solução de **Programação Linear Inteira** para o problema de alocação de salas em universidades, baseado no modelo matemático fornecido.

## 📋 Características

### Modelo Matemático Implementado

- **Variáveis de Decisão**: `x[m,s]` binárias (1 se matéria m alocada na sala s, 0 caso contrário)
- **Função Objetivo**: Minimizar espaços ociosos + custos adicionais
- **Restrições Hard**:
  - Cada matéria em exatamente uma sala
  - Capacidade da sala suficiente
  - Compatibilidade de materiais
  - Sem conflitos de horário
- **Soft Constraints**: Preferência por salas do IC sobre IM

### Funcionalidades

✅ **Alocação Otimizada**: Minimiza espaços ociosos e maximiza utilização  
✅ **Compatibilidade**: Verifica se matérias são compatíveis com salas  
✅ **Conflitos de Horário**: Evita sobreposição de matérias na mesma sala  
✅ **Preferências**: Prioriza salas do IC sobre IM  
✅ **Flexibilidade**: Suporte a diferentes tipos de salas (aula, laboratório, auditório)  
✅ **Análise Detalhada**: Relatórios de utilização e eficiência  

## 🚀 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

## 📖 Uso Básico

```python
from alocacao_salas import AlocadorSalas, Materia, Sala, TipoSala, LocalSala

# Criar alocador
alocador = AlocadorSalas()

# Adicionar matérias
materia = Materia(
    id="MAT001",
    nome="Cálculo I", 
    inscritos=45,
    horario="Segunda 08:00-10:00",
    precisa_lab=False,
    materiais_necessarios=["projetor", "quadro"]
)
alocador.adicionar_materia(materia)

# Adicionar salas
sala = Sala(
    id="IC101",
    nome="Sala IC-101",
    capacidade=50,
    tipo=TipoSala.AULA,
    local=LocalSala.IC,
    materiais_disponiveis=["projetor", "quadro"],
    custo_adicional=0.0
)
alocador.adicionar_sala(sala)

# Resolver problema
if alocador.resolver():
    alocador.imprimir_resumo()
    df = alocador.obter_resultados()
```

## 🎯 Exemplos de Uso

### Exemplo Simples
```bash
python alocacao_salas.py
```

### Exemplo Avançado
```bash
python exemplo_uso.py
```

## 📊 Estrutura dos Dados

### Matéria
- `id`: Identificador único
- `nome`: Nome da matéria
- `inscritos`: Número de alunos inscritos
- `horario`: Horário da aula (formato: "Dia HH:MM-HH:MM")
- `precisa_lab`: Se precisa de laboratório
- `materiais_necessarios`: Lista de materiais necessários

### Sala
- `id`: Identificador único
- `nome`: Nome da sala
- `capacidade`: Número máximo de alunos
- `tipo`: Tipo da sala (AULA, LABORATORIO, AUDITORIO)
- `local`: Localização (IC, IM)
- `materiais_disponiveis`: Lista de materiais disponíveis
- `custo_adicional`: Custo extra (para penalizar salas do IM)

## 🔧 Configuração Avançada

### Ajustando Penalizações
```python
# Penalizar salas do IM
for sala in alocador.salas:
    if sala.local == LocalSala.IM:
        sala.custo_adicional = 15.0  # Custo alto
    else:
        sala.custo_adicional = 0.0   # Sem custo
```

### Adicionando Restrições Customizadas
```python
# Exemplo: Forçar uma matéria específica em uma sala
materia_especifica = "MAT001"
sala_especifica = "IC101"

# Adicionar restrição: x[MAT001, IC101] = 1
if (materia_especifica, sala_especifica) in alocador.variaveis:
    alocador.problema += (
        alocador.variaveis[(materia_especifica, sala_especifica)] == 1,
        f"forcar_{materia_especifica}_{sala_especifica}"
    )
```

## 📈 Análise de Resultados

O sistema gera relatórios detalhados incluindo:

- **Utilização por sala**: Percentual de ocupação
- **Espaço ocioso**: Capacidade não utilizada
- **Distribuição por local**: IC vs IM
- **Análise por tipo**: Aula vs Laboratório vs Auditório
- **Detecção de conflitos**: Verificação de sobreposições

## 🧮 Modelo Matemático Detalhado

### Função Objetivo
```
min Σ Σ x[m,s] * (capacidade_s - inscritos_m + custo_s)
    m s
```

### Restrições

1. **Alocação única**:
   ```
   Σ x[m,s] = 1  ∀m
     s
   ```

2. **Capacidade**:
   ```
   x[m,s] * inscritos_m ≤ capacidade_s  ∀m,s
   ```

3. **Compatibilidade**:
   ```
   x[m,s] = 0  se matéria m não compatível com sala s
   ```

4. **Sem conflitos**:
   ```
   Σ x[m,s] ≤ 1  ∀s,∀horário
   m∈horário
   ```

## 📁 Arquivos

- `alocacao_salas.py`: Implementação principal
- `exemplo_uso.py`: Exemplos avançados
- `requirements.txt`: Dependências Python
- `README.md`: Documentação

## 🔍 Dependências

- `pulp`: Solver de programação linear
- `pandas`: Manipulação de dados
- `numpy`: Operações numéricas

## ⚡ Performance

O solver utiliza o **CBC** (Coin-or Branch and Cut) através da biblioteca PuLP, que é eficiente para problemas de programação linear inteira de tamanho médio.

Para problemas muito grandes (>1000 variáveis), considere:
- Usar solvers comerciais (Gurobi, CPLEX)
- Implementar heurísticas
- Dividir o problema em subproblemas

## 🤝 Contribuição

Contribuições são bem-vindas! Áreas de melhoria:

- Otimizações de performance
- Novos tipos de restrições
- Interface gráfica
- Integração com sistemas acadêmicos
- Análise de sensibilidade

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.