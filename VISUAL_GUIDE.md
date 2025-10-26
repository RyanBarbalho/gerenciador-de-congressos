# 🖼️ Guia Visual do Frontend

## Layout Geral

```
┌─────────────────────────────────────────────────────────────┐
│  SIDEBAR                    │  MAIN CONTENT AREA             │
│                             │                                │
│  🏫 Sistema de Alocação     │  [Conteúdo da página atual]   │
│  ─────────────────────      │                                │
│                             │                                │
│  ○ 🏠 Home                  │                                │
│  ● 📊 Dashboard             │                                │
│  ○ 📁 Dados                 │                                │
│  ○ ⚙️ Alocação              │                                │
│  ○ 📈 Resultados            │                                │
│  ○ 📉 Análises              │                                │
│  ─────────────────────      │                                │
│                             │                                │
│  Sobre                      │                                │
│  Sistema inteligente...     │                                │
│                             │                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏠 Página Home

```
╔═══════════════════════════════════════════════════════════════╗
║  🏫 Sistema de Alocação de Salas                             ║
║  Otimização inteligente usando programação linear            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    ║
║  │   🎯     │  │    ⚡    │  │    📊    │  │    🎨    │    ║
║  │Otimização│  │  Rápido  │  │Múltiplas │  │ Padrões  │    ║
║  │Inteligente│  │   < 5s   │  │ Análises │  │ 6 tipos  │    ║
║  └──────────┘  └──────────┘  └──────────┘  └──────────┘    ║
║     [Roxo]      [Verde]       [Rosa]         [Azul]         ║
║                                                               ║
║  🚀 Começar                                                   ║
║                                                               ║
║  [📁 Carregar Dados]  [⚙️ Executar Alocação]  [📈 Ver...]   ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  📖 Como Usar                                                 ║
║                                                               ║
║  1️⃣ Carregar Dados        3️⃣ Analisar Resultados            ║
║  • Clique em "Carregar"    • Visualize alocações             ║
║  • Upload personalizado    • Veja distribuição               ║
║                                                               ║
║  2️⃣ Executar Alocação     4️⃣ Exportar                       ║
║  • Escolha estratégia      • Exporte para CSV                ║
║  • Configure parâmetros    • Gere relatórios                 ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  🎨 Padrões de Projeto Implementados                          ║
║                                                               ║
║  🏭 Factory    🎯 Strategy    👁️ Observer                    ║
║  🔨 Builder    📦 Repository  🎭 Facade                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📊 Página Dashboard

```
╔═══════════════════════════════════════════════════════════════╗
║  📊 Dashboard                                                 ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [150]        [45]         [3,420]      [4,500]     [76.0%]  ║
║  Matérias     Salas        Inscritos    Capacidade  Utilização║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  ┌─────────────────────────────┬─────────────────────────┐   ║
║  │                             │                         │   ║
║  │  📚 Distribuição Matérias   │  🏢 Salas por Local    │   ║
║  │                             │                         │   ║
║  │     ┌───────────┐           │     ███████             │   ║
║  │     │           │           │     ███████  IC         │   ║
║  │     │  Gráfico  │           │     ████     IM         │   ║
║  │     │  de Pizza │           │     ██       IF         │   ║
║  │     │           │           │                         │   ║
║  │     └───────────┘           │                         │   ║
║  │                             │                         │   ║
║  └─────────────────────────────┴─────────────────────────┘   ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  ┌─────────────────────────────┬─────────────────────────┐   ║
║  │                             │                         │   ║
║  │  👥 Distribuição Inscritos  │  🪑 Distribuição Cap.  │   ║
║  │                             │                         │   ║
║  │    ▁▃▅▇█▇▅▃▁               │    ▁▃▅▇█▇▅▃▁           │   ║
║  │    Histograma               │    Histograma           │   ║
║  │                             │                         │   ║
║  │  Média: 22.8  Max: 75       │  Média: 52.3  Max: 100 │   ║
║  │                             │                         │   ║
║  └─────────────────────────────┴─────────────────────────┘   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📁 Página Dados

```
╔═══════════════════════════════════════════════════════════════╗
║  📁 Gerenciamento de Dados                                    ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [📥 Carregar] [👁️ Visualizar] [💾 Exportar]                 ║
║                                                               ║
║  ═══════════════════════════════════════════════════════     ║
║  Tab: Visualizar                                              ║
║                                                               ║
║  ( ) CC  ( ) EC  (●) Todas as Matérias                       ║
║                                                               ║
║  📚 Matérias                                                  ║
║                                                               ║
║  🔍 Buscar: [________________]                                ║
║                                                               ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ Código │ Nome              │ Inscritos │ Horário     │    ║
║  ├──────────────────────────────────────────────────────┤    ║
║  │ COMP001│ Algoritmos        │    45     │ 2M34        │    ║
║  │ COMP002│ Estruturas Dados  │    38     │ 3T12        │    ║
║  │ MAT001 │ Cálculo I         │    62     │ 24M56       │    ║
║  │ ...    │ ...               │    ...    │ ...         │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  🏢 Salas                                                     ║
║                                                               ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ Nome       │ Capacidade │ Tipo  │ Local │ Equip.    │    ║
║  ├──────────────────────────────────────────────────────┤    ║
║  │ Sala IC-01 │    45      │ Aula  │ IC    │ Nenhum    │    ║
║  │ Lab IC-301 │    40      │ Lab   │ IC    │ Comput.   │    ║
║  │ Aud CEPETEC│   100      │ Audit.│ IC    │ Nenhum    │    ║
║  │ ...        │    ...     │ ...   │ ...   │ ...       │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## ⚙️ Página Alocação

```
╔═══════════════════════════════════════════════════════════════╗
║  ⚙️ Executar Alocação                                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌────────────────────────────────┬──────────────────────┐   ║
║  │  Configurações                 │  Status              │   ║
║  │                                │                      │   ║
║  │  Estratégia de Alocação:       │  ✅ CC: 85 matérias │   ║
║  │  [Programação Linear (Ótimo)▼] │  ✅ EC: 65 matérias │   ║
║  │                                │                      │   ║
║  │  ☑ Incluir CC                  │                      │   ║
║  │  ☑ Incluir EC                  │                      │   ║
║  │                                │                      │   ║
║  └────────────────────────────────┴──────────────────────┘   ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║                 [🚀 Executar Alocação]                        ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  Após execução:                                               ║
║                                                               ║
║  ✅ Alocação executada com sucesso!                           ║
║                                                               ║
║  [142]         [35]          [87.5%]        [520]            ║
║  Alocadas      Salas         Utilização     Ocioso           ║
║                                                               ║
║  🎈 🎈 🎈 (Animação de sucesso)                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📈 Página Resultados

```
╔═══════════════════════════════════════════════════════════════╗
║  📈 Resultados da Alocação                                    ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [142]    [35]      [87.5%]    [520]      [R$ 150.00]       ║
║  Alocadas  Salas    Utilização  Ocioso    Custo             ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  [📋 Por Sala] [🕐 Por Horário] [📚 Por Matéria] [📍 Local] ║
║                                                               ║
║  ═══════════════════════════════════════════════════════     ║
║  Tab: Por Sala                                                ║
║                                                               ║
║  ▶ 🏢 Sala IC-01 - 8 matérias                                ║
║  ▼ 🏢 Lab IC-301 - 12 matérias                               ║
║     IC | LABORATORIO | 40 lugares                            ║
║     12 matérias | 456 alunos | 95.0% utilização              ║
║     ──────────────────────────────────────────               ║
║     ┌──────────────────────────────────────────────────┐     ║
║     │ Matéria          │ Horário │ Inscritos │ Util.  │     ║
║     ├──────────────────────────────────────────────────┤     ║
║     │ Algoritmos       │ 2M34    │    38     │ 95.0%  │     ║
║     │ Estruturas Dados │ 3T12    │    40     │ 100%   │     ║
║     │ ...              │ ...     │    ...    │ ...    │     ║
║     └──────────────────────────────────────────────────┘     ║
║                                                               ║
║  ▶ 🏢 Sala IC-02 - 6 matérias                                ║
║  ▶ 🏢 Auditório IC - 4 matérias                              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📉 Página Análises

```
╔═══════════════════════════════════════════════════════════════╗
║  📉 Análises Avançadas                                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [📊 Gráficos] [🎯 Otimização] [📈 Comparações]              ║
║                                                               ║
║  ═══════════════════════════════════════════════════════     ║
║  Tab: Otimização                                              ║
║                                                               ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐                   ║
║  │Eficiência│  │ Uso IM   │  │ Labs     │                   ║
║  │  Global  │  │          │  │          │                   ║
║  │  87.5%   │  │  15.0%   │  │  42.3%   │                   ║
║  └──────────┘  └──────────┘  └──────────┘                   ║
║   [Roxo]        [Laranja]     [Verde]                        ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  📊 Faixas de Utilização                                      ║
║                                                               ║
║       ████                                                    ║
║       ████ 0-50%                                              ║
║       ████████████                                            ║
║       ████████████ 50-70%                                     ║
║       ████████████████████████                                ║
║       ████████████████████████ 70-85%                         ║
║       ████████████████                                        ║
║       ████████████████ 85-100%                                ║
║       ██                                                      ║
║       ██ >100%                                                ║
║                                                               ║
║  ───────────────────────────────────────────────────────     ║
║                                                               ║
║  ┌─────────────────────────────┬─────────────────────────┐   ║
║  │  ⭐ Melhores Alocações      │  ⚠️ Problemáticas       │   ║
║  │                             │                         │   ║
║  │  Algoritmos → Lab IC-301    │  Cálculo I → Aud IC     │   ║
║  │  (85.0%)                    │  (50 vagas ociosas)     │   ║
║  │  ...                        │  ...                    │   ║
║  └─────────────────────────────┴─────────────────────────┘   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 🎨 Elementos de Design

### Cards com Gradientes

```
┌──────────────────────────┐
│   [Ícone Grande]         │  ← Gradiente de fundo
│                          │    (Roxo, Verde, Rosa ou Azul)
│   Título                 │
│   ─────────              │
│   Valor Principal        │  ← Texto grande e bold
│   Descrição              │  ← Texto menor, opacidade 0.9
│                          │
└──────────────────────────┘
     Sombra suave
```

### Tabelas Interativas

```
┌─────────────────────────────────────────────┐
│ 🔍 [Campo de busca]                         │ ← Filtro em tempo real
├─────────────────────────────────────────────┤
│ Coluna 1 │ Coluna 2 │ Coluna 3 │ Ações    │
├─────────────────────────────────────────────┤
│  Valor A │  123     │  45.2%   │  [...]   │ ← Hover effect
│  Valor B │  456     │  87.5%   │  [...]   │
│  ...     │  ...     │  ...     │  ...     │
└─────────────────────────────────────────────┘
           ↕ Scroll vertical
```

### Gráficos Plotly

```
┌─────────────────────────────────────────────┐
│  Título do Gráfico                    [🔧] │ ← Controles
├─────────────────────────────────────────────┤
│                                             │
│    ▁▃▅▇█▇▅▃▁  ou  ●●●  ou  ████            │ ← Interativo
│                                             │
│    [Legenda] [Escala] [Hover Info]         │
│                                             │
└─────────────────────────────────────────────┘
   Zoom, Pan, Download, Reset View
```

### Expansores

```
▶ Título do Expander (clicável)
───────────────────────────────────
  (conteúdo escondido)

▼ Título do Expander (expandido)
───────────────────────────────────
  │ Conteúdo visível aqui
  │ Pode ter qualquer coisa
  │ - Tabelas
  │ - Gráficos
  │ - Texto
  └──────────────────────────────
```

---

## 🎭 Animações e Feedback

### Loading States

```
⏳ Carregando dados...
   [████████████        ] 60%
```

### Success Messages

```
✅ Alocação executada com sucesso!
🎈 🎈 🎈 (Balões animados)
```

### Error Messages

```
❌ Erro na alocação: Capacidade insuficiente
ℹ️ Sugestão: Adicione mais salas ou reduza matérias
```

### Info Messages

```
ℹ️ 15 matérias compartilhadas detectadas
⚠️ Execute a alocação primeiro!
```

---

## 📱 Responsividade

### Desktop (> 1200px)
```
┌────────┬──────────────────────────────────┐
│ Sidebar│  Main Content (5 colunas)       │
│ (Fixo) │  [●][●][●][●][●]                │
│        │                                  │
└────────┴──────────────────────────────────┘
```

### Tablet (768px - 1200px)
```
┌────────┬────────────────────┐
│ Sidebar│  Main (3 colunas)  │
│ (Fixo) │  [●][●][●]         │
│        │                    │
└────────┴────────────────────┘
```

### Mobile (< 768px)
```
┌─────────────────┐
│   ☰ Menu        │
├─────────────────┤
│  Main Content   │
│  (1 coluna)     │
│  [●]            │
│  [●]            │
│  [●]            │
└─────────────────┘
```

---

## 🎨 Paleta de Cores

### Gradientes Principais

**Roxo/Violeta** (Primary)
- Start: #667eea
- End: #764ba2
- Uso: Otimização, Headers

**Verde/Turquesa** (Success)
- Start: #11998e
- End: #38ef7d
- Uso: Sucesso, Performance

**Rosa/Vermelho** (Warning)
- Start: #f093fb
- End: #f5576c
- Uso: Alertas, Destaque

**Azul/Ciano** (Info)
- Start: #4facfe
- End: #00f2fe
- Uso: Informações, Links

### Cores de Status

- ✅ Success: #38ef7d
- ❌ Error: #f5576c
- ⚠️ Warning: #ffa726
- ℹ️ Info: #00f2fe

### Texto

- Primary: #1f77b4
- Secondary: #666
- Light: #999
- White: #fff (em cards)

---

## 🖱️ Interações

### Hover States
- Cards: Leve elevação
- Botões: Mudança de cor
- Tabelas: Highlight da linha
- Gráficos: Tooltip detalhado

### Click Actions
- Botões: Ripple effect
- Expansores: Animação smooth
- Tabs: Transição suave
- Links: Underline

### Loading
- Progress bar animada
- Spinner rotativo
- Skeleton screens
- Fade in/out

---

Este guia visual mostra como o frontend é organizado e apresentado ao usuário! 🎨

