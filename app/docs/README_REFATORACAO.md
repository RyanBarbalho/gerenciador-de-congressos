# Sistema de Alocação de Salas - Refatorado com Padrões de Projeto

Este projeto foi refatorado para implementar diversos padrões de projeto, melhorando a estrutura, manutenibilidade e extensibilidade do código.

## Padrões de Projeto Implementados

### 1. Factory Pattern (`factories/creators.py`)
- **MateriaFactory**: Criação consistente de matérias
- **SalaFactory**: Criação consistente de salas
- **FactoryManager**: Gerenciamento centralizado
- **Especializações**: MateriaFactoryCSV, SalaFactoryCSV para dados CSV

### 2. Builder Pattern (`builders/constructors.py`)
- **AlocadorBuilder**: Construção flexível do sistema
- **SistemaAlocacaoBuilder**: Construção de sistema completo
- **Interface fluente** para configuração

### 3. Strategy Pattern (`strategies/interfaces.py`)
- **CompatibilidadeStrategy**: Diferentes estratégias de compatibilidade
- **AlocacaoStrategy**: Diferentes algoritmos de alocação
- **SolverStrategy**: Diferentes tipos de solvers
- **Validator**: Diferentes tipos de validação

### 4. Repository Pattern (`repositories/alocacao_repo.py`)
- **AlocacaoRepository**: Gerenciamento de dados
- **CSVRepository**: Repositório especializado para CSV
- **Interface abstrata** para diferentes fontes de dados

### 5. Observer Pattern (`models/domain.py`)
- **Observer**: Interface para observadores
- **Subject**: Sujeito observável
- **ConsoleObserver**: Implementação para console

### 6. Facade Pattern (`core/facade.py`)
- **SistemaAlocacaoFacade**: Interface simplificada
- **SistemaCompletoRefatorado**: Sistema integrado

## Estrutura dos Arquivos

```
app/
├── models/
│   ├── __init__.py
│   └── domain.py                 # Modelos de domínio e Observer Pattern
├── strategies/
│   ├── __init__.py
│   └── interfaces.py            # Strategy Pattern e interfaces
├── factories/
│   ├── __init__.py
│   └── creators.py              # Factory Pattern
├── builders/
│   ├── __init__.py
│   └── constructors.py          # Builder Pattern
├── repositories/
│   ├── __init__.py
│   └── alocacao_repo.py         # Repository Pattern e algoritmos
├── services/
│   ├── __init__.py
│   └── data_loader.py           # Carregador refatorado
├── core/
│   ├── __init__.py
│   └── facade.py                # Facade Pattern e integração
├── tests/
│   ├── __init__.py
│   └── test_sistema_refatorado.py # Testes abrangentes
├── docs/
│   ├── __init__.py
│   ├── README_REFATORACAO.md    # Documentação completa
│   └── RESUMO_REFATORACAO.md   # Resumo executivo
└── carregador_dados_reais_fixed copy.py # Arquivo original refatorado
```

## Benefícios da Refatoração

### 1. **Flexibilidade**
- Fácil troca de algoritmos de alocação (Strategy Pattern)
- Diferentes tipos de validação e compatibilidade
- Múltiplas fontes de dados (CSV, banco de dados, etc.)

### 2. **Manutenibilidade**
- Código organizado em módulos específicos
- Responsabilidades bem definidas
- Fácil adição de novas funcionalidades

### 3. **Testabilidade**
- Interfaces bem definidas facilitam testes unitários
- Dependências injetadas permitem mocks
- Separação clara entre lógica de negócio e infraestrutura

### 4. **Extensibilidade**
- Novos tipos de salas e matérias facilmente adicionados
- Novos algoritmos de alocação podem ser implementados
- Diferentes tipos de observadores podem ser adicionados

## Como Usar

### Uso Básico
```python
from app.core.facade import SistemaAlocacaoFacade

# Criar facade
facade = SistemaAlocacaoFacade()

# Criar sistema básico
sistema = facade.criar_sistema_basico()

# Executar alocação
resultado = facade.executar_alocacao_linear(sistema)
```

### Carregamento de Dados CSV
```python
from app.services.data_loader import SistemaCompletoRefatorado

# Criar sistema
sistema = SistemaCompletoRefatorado()

# Carregar dados
repository = sistema.carregar_dados_csv('dados.csv')

# Obter estatísticas
stats = sistema.obter_estatisticas()
```

### Uso Avançado com Builder
```python
from app.builders.constructors import AlocadorBuilder
from app.strategies.interfaces import CompatibilidadeFlexivel

# Construir sistema personalizado
builder = AlocadorBuilder()
alocador = (builder
           .com_materias(materias)
           .com_salas(salas)
           .com_compatibilidade_strategy(CompatibilidadeFlexivel())
           .construir())
```

## Algoritmos de Alocação Disponíveis

### 1. **Alocação Linear** (`AlocacaoLinearStrategy`)
- Usa programação linear inteira (PuLP)
- Encontra solução ótima
- Mais lento para problemas grandes

### 2. **Alocação Gulosa** (`AlocacaoGulosaStrategy`)
- Algoritmo heurístico rápido
- Solução aproximada
- Boa para problemas grandes

## Estratégias de Compatibilidade

### 1. **Compatibilidade Padrão** (`CompatibilidadePadrao`)
- Regras rígidas de compatibilidade
- Materiais obrigatórios devem estar disponíveis

### 2. **Compatibilidade Flexível** (`CompatibilidadeFlexivel`)
- Permite alguns materiais opcionais
- Mais flexível para alocação

## Validação

O sistema inclui validação robusta:
- Validação de matérias (inscritos, nome, horário)
- Validação de salas (capacidade, nome, custo)
- Validação de alocações (capacidade, compatibilidade)

## Observadores

Sistema de notificações para acompanhar progresso:
- `ConsoleObserver`: Exibe progresso no console
- Fácil adição de novos observadores (logs, interface gráfica, etc.)

## Exemplo de Execução

```bash
# Executar sistema refatorado
python -m app.core.facade

# Executar carregador refatorado
python -m app.services.data_loader

# Executar testes
python -m app.tests.test_sistema_refatorado
```

## Migração do Sistema Original

O arquivo `carregador_dados_reais_fixed copy.py` foi refatorado para usar o novo sistema, mantendo compatibilidade com a interface original mas utilizando os padrões de projeto internamente.

### Principais Mudanças:
1. **Factory Pattern** para criação de objetos
2. **Repository Pattern** para gerenciamento de dados
3. **Strategy Pattern** para algoritmos de alocação
4. **Observer Pattern** para notificações
5. **Facade Pattern** para interface simplificada

## Próximos Passos

1. **Adicionar novos algoritmos** de alocação
2. **Implementar persistência** em banco de dados
3. **Criar interface gráfica** usando Observer Pattern
4. **Adicionar testes unitários** para cada padrão
5. **Implementar cache** para melhorar performance
6. **Adicionar logging** estruturado

## Dependências

- `pandas`: Manipulação de dados CSV
- `pulp`: Programação linear inteira
- `numpy`: Operações numéricas
- `typing`: Type hints para melhor documentação

## Conclusão

A refatoração com padrões de projeto resultou em um sistema mais robusto, flexível e manutenível. Cada padrão contribui para uma arquitetura limpa e extensível, facilitando futuras modificações e melhorias.
