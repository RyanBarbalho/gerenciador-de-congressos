# Sistema de Alocação de Salas - Refatorado

Este diretório contém o sistema de alocação de salas refatorado usando padrões de projeto modernos.

## 🚀 Início Rápido

### Executar o Sistema
```bash
cd app/
python main.py
```

### Executar Testes
```bash
cd app/
python main.py test
```

### Executar Testes Diretamente
```bash
cd app/
python -m tests.test_sistema_refatorado
```

## 📁 Estrutura do Projeto

```
app/
├── main.py                           # Ponto de entrada principal
├── carregador_dados_reais_fixed copy.py  # Arquivo original refatorado
├── models/                           # Modelos de domínio
│   ├── __init__.py
│   └── domain.py                    # Entidades principais e Observer Pattern
├── strategies/                       # Strategy Pattern
│   ├── __init__.py
│   └── interfaces.py               # Interfaces e estratégias
├── factories/                        # Factory Pattern
│   ├── __init__.py
│   └── creators.py                  # Factories para criação de objetos
├── builders/                         # Builder Pattern
│   ├── __init__.py
│   └── constructors.py             # Builders para construção complexa
├── repositories/                     # Repository Pattern
│   ├── __init__.py
│   └── alocacao_repo.py            # Repositórios e algoritmos
├── services/                         # Services Layer
│   ├── __init__.py
│   └── data_loader.py               # Carregador de dados refatorado
├── core/                             # Core Business Logic
│   ├── __init__.py
│   └── facade.py                    # Facade Pattern e integração
├── tests/                            # Testes
│   ├── __init__.py
│   └── test_sistema_refatorado.py   # Testes abrangentes
└── docs/                             # Documentação
    ├── __init__.py
    ├── README_REFATORACAO.md        # Documentação completa
    └── RESUMO_REFATORACAO.md       # Resumo executivo
```

## 🎯 Padrões de Projeto Implementados

1. **Factory Pattern** - Criação consistente de objetos
2. **Builder Pattern** - Construção flexível do sistema
3. **Strategy Pattern** - Algoritmos intercambiáveis
4. **Repository Pattern** - Gerenciamento de dados
5. **Observer Pattern** - Sistema de notificações
6. **Facade Pattern** - Interface simplificada

## 📖 Como Usar

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

## 🧪 Testes

O sistema inclui testes abrangentes que verificam todos os padrões de projeto:

- ✅ Testes de importação
- ✅ Testes de Factory Pattern
- ✅ Testes de Strategy Pattern
- ✅ Testes de Builder Pattern
- ✅ Testes de Repository Pattern
- ✅ Testes de Observer Pattern
- ✅ Testes de Facade Pattern
- ✅ Testes do sistema completo

## 📚 Documentação

- **`docs/README_REFATORACAO.md`** - Documentação completa com exemplos
- **`docs/RESUMO_REFATORACAO.md`** - Resumo executivo da refatoração

## 🔧 Dependências

- `pandas` - Manipulação de dados CSV
- `pulp` - Programação linear inteira
- `numpy` - Operações numéricas
- `typing` - Type hints

## 🎉 Benefícios da Refatoração

- **Flexibilidade**: Troca fácil de algoritmos e estratégias
- **Manutenibilidade**: Código modular e bem organizado
- **Testabilidade**: Interfaces claras e dependências injetadas
- **Extensibilidade**: Fácil adição de novas funcionalidades
- **Compatibilidade**: Mantém interface original com melhorias internas

## 🚀 Próximos Passos

1. Adicionar novos algoritmos de alocação
2. Implementar persistência em banco de dados
3. Criar interface gráfica usando Observer Pattern
4. Adicionar testes unitários para cada padrão
5. Implementar cache para melhorar performance
6. Adicionar logging estruturado

---

**Sistema refatorado com sucesso usando padrões de projeto modernos!**
