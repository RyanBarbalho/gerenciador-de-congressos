# 🏫 Sistema de Alocação de Salas - Guia Completo de Recursos

## 📋 Visão Geral

Frontend web completo e moderno construído com Streamlit, oferecendo uma interface intuitiva e rica em recursos para o sistema de alocação de salas.

---

## 🚀 Execução Rápida

### Windows
```bash
run_streamlit.bat
```

### Linux/Mac
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

### Manual
```bash
streamlit run streamlit_app.py
```

---

## ✨ Recursos Principais

### 1. 🏠 **Página Home**

#### Cards de Métricas com Gradientes Coloridos
- **Otimização Inteligente** (Roxo): Destaque para programação linear
- **Rápido** (Verde): Tempo médio de execução < 5s
- **Múltiplas Análises** (Rosa): Visualizações diversas
- **6 Padrões de Projeto** (Azul): Design patterns implementados

#### Botões de Ação Rápida
- **Carregar Dados Padrão**: Carrega ofertas de CC e EC automaticamente
- **Executar Alocação**: Redireciona para página de alocação
- **Ver Resultados**: Acessa visualização de resultados

#### Guia de Uso
- Tutorial passo a passo em 4 etapas
- Explicação dos padrões de projeto
- Informações sobre o sistema

---

### 2. 📊 **Dashboard Interativo**

#### Métricas Principais (5 cards)
- Total de Matérias
- Total de Salas
- Total de Inscritos
- Capacidade Total
- Utilização Potencial (%)

#### Gráficos Interativos

**Distribuição de Matérias (Gráfico de Pizza)**
- Sem Laboratório
- Computadores
- Robótica
- Eletrônica
- Cores diferenciadas por categoria

**Distribuição de Salas por Local (Gráfico de Barras)**
- IC (Instituto de Computação)
- IM (Instituto de Matemática)
- IF (Instituto de Física)
- Cores vibrantes por local

**Distribuição de Inscritos (Histograma)**
- Visualização da frequência de turmas por tamanho
- Métricas: Média, Máximo, Mínimo

**Distribuição de Capacidade (Histograma)**
- Análise de capacidades das salas
- Métricas: Média, Máximo, Mínimo

**Matérias por Curso**
- Comparação entre CC e EC
- Total de inscritos por curso

---

### 3. 📁 **Gerenciamento de Dados**

#### Tab: Carregar

**Upload de Arquivos**
- Suporte para CSV
- Processamento em tempo real
- Feedback visual de sucesso/erro

**Carregamento Padrão**
- Botões para ofertas de CC e EC
- Carregamento automático dos arquivos padrão

**Informações sobre Formato**
- Documentação das colunas obrigatórias
- Exemplos de formato

#### Tab: Visualizar

**Seleção de Fonte de Dados**
- Ciência da Computação
- Engenharia de Computação
- Todas as Matérias (combinadas)

**Tabela de Matérias**
- Busca em tempo real
- Colunas: Código, Nome, Inscritos, Horário, Material
- Scroll vertical para grandes volumes

**Tabela de Salas**
- Informações completas de cada sala
- Colunas: Nome, Capacidade, Tipo, Local, Equipamento, Custo

#### Tab: Exportar

**Download de Dados**
- Exportação para CSV
- Botões separados para CC e EC
- Formatação pronta para uso

---

### 4. ⚙️ **Execução de Alocação**

#### Configurações

**Seleção de Estratégia**
- **Programação Linear (Ótimo)**: Solução ótima garantida
- **Guloso (Rápido)**: Execução mais rápida, solução aproximada

**Seleção de Ofertas**
- Checkbox para incluir CC
- Checkbox para incluir EC
- Possibilidade de combinar ambas

#### Status em Tempo Real
- Indicadores visuais de dados carregados
- Contagem de matérias por curso

#### Execução

**Barra de Progresso Animada**
- Indicação visual do progresso
- Mensagens de status

**Tratamento de Matérias Compartilhadas**
- Detecção automática de duplicatas
- Deduplicação inteligente
- Notificação de matérias compartilhadas

**Resultados Imediatos**
- 4 métricas principais em cards
- Animação de balões em caso de sucesso
- Mensagens de erro claras

---

### 5. 📈 **Visualização de Resultados**

#### Métricas Gerais (5 cards)
- Matérias Alocadas
- Salas Utilizadas
- Utilização Média (%)
- Espaço Ocioso
- Custo Total (R$)

#### Tab: Por Sala

**Expansores Interativos**
- Um expander por sala
- Informações da sala (Local, Tipo, Capacidade)
- Tabela de todas as matérias alocadas na sala
- Colunas: Matéria, Horário, Inscritos, Utilização, Ocioso, Lab

#### Tab: Por Horário

**Organização Temporal**
- Agrupamento por horário
- Total de matérias e alunos por horário
- Tabela detalhada de alocações
- Identificação de uso simultâneo de salas

#### Tab: Por Matéria

**Lista Completa**
- Todas as matérias alocadas
- Busca em tempo real
- Colunas completas de informação
- **Botão de Download CSV**

#### Tab: Por Local

**Análise Geográfica**
- Cards por local (IC, IM, IF)
- 4 métricas por local:
  - Número de matérias
  - Número de salas
  - Total de inscritos
  - Utilização (%)

---

### 6. 📉 **Análises Avançadas**

#### Tab: Gráficos

**Utilização por Sala (Gráfico de Barras)**
- Top 15 salas
- Escala de cores (RdYlGn)
- Ordenação por utilização

**Espaço Ocioso (Gráfico de Barras)**
- Top 15 salas com mais ociosidade
- Escala de cores vermelha
- Identificação de desperdício

**Alocações por Local (Gráfico de Pizza)**
- Distribuição geográfica
- Porcentagens e valores absolutos

**Distribuição de Turmas (Box Plot)**
- Análise estatística de tamanhos de turma
- Identificação de outliers

#### Tab: Otimização

**Cards de Métricas Coloridos**
- **Eficiência Global**: Utilização total do sistema
- **Uso de Salas IM**: Percentual de uso de salas com custo
- **Matérias em Labs**: Percentual de aulas práticas

**Faixas de Utilização**
- Gráfico de barras com distribuição:
  - 0-50%: Subutilização
  - 50-70%: Baixa utilização
  - 70-85%: Ótima utilização
  - 85-100%: Alta utilização
  - >100%: Sobre capacidade

**Melhores Alocações**
- Top 10 alocações mais eficientes
- Próximas de 85% de utilização

**Alocações Problemáticas**
- Top 10 com maior espaço ocioso
- Oportunidades de otimização

#### Tab: Comparações

**Gráficos Comparativos**

1. **Por Local**: Utilização média por local
2. **Por Tipo de Sala**: Aula vs Lab vs Auditório
3. **Lab vs Não-Lab**: Comparação de eficiência

**Resumo Executivo**
- Consolidação de todas as métricas
- Recomendações automáticas
- Insights de otimização

---

## 🎨 Design e UX

### Elementos Visuais

**Gradientes Coloridos**
- Roxo/Roxo-escuro
- Verde/Verde-claro
- Rosa/Vermelho
- Azul/Azul-claro

**Cards de Métricas**
- Sombras suaves
- Bordas arredondadas
- Tipografia hierárquica

**Tabelas**
- Bordas arredondadas
- Hover effects
- Ordenação interativa
- Busca em tempo real

### Navegação

**Sidebar Persistente**
- Menu de navegação por radio buttons
- Ícones emoji para cada página
- Seção "Sobre" informativa

**Feedback Visual**
- Spinners durante carregamento
- Mensagens de sucesso (verde)
- Mensagens de erro (vermelho)
- Mensagens informativas (azul)
- Avisos (amarelo)

### Responsividade

**Layouts Adaptativos**
- Colunas responsivas (2, 3, 4, 5 colunas)
- Gráficos com `use_container_width=True`
- Tabelas com altura fixa e scroll

---

## 📊 Tecnologias de Visualização

### Plotly Express

**Tipos de Gráficos Utilizados**
- `px.pie`: Gráficos de pizza
- `px.bar`: Gráficos de barras
- `go.Histogram`: Histogramas customizados
- `go.Box`: Box plots

**Recursos Plotly**
- Hover interativo
- Zoom e pan
- Exportação de imagens
- Temas customizados
- Escalas de cores profissionais

### Pandas DataFrames

**Funcionalidades**
- Agrupamento (`groupby`)
- Ordenação (`sort_values`)
- Filtragem com máscaras
- Agregações (`sum`, `mean`)
- Exportação para CSV

---

## 🔧 Funcionalidades Técnicas

### State Management

**Session State**
- `sistema`: Instância do sistema
- `resultado`: Resultado da alocação
- `materias`: Lista de matérias
- `salas`: Lista de salas
- `repository_cc`: Repositório CC
- `repository_ec`: Repositório EC

### Observer Pattern

**StreamlitObserver**
- Captura de progresso
- Mensagens de sucesso
- Tratamento de erros
- Integração com UI

### Processamento de Dados

**Detecção de Duplicatas**
- Chave única: código + horário
- Deduplicação automática
- Registro de compartilhamentos

**Agregações**
- Por sala
- Por horário
- Por local
- Por tipo

---

## 🎯 Casos de Uso

### 1. Planejamento Semestral

**Fluxo:**
1. Carregar ofertas de CC e EC
2. Visualizar estatísticas no Dashboard
3. Executar alocação linear
4. Analisar resultados por sala
5. Exportar para planejamento

### 2. Otimização de Recursos

**Fluxo:**
1. Executar alocação
2. Ir para Análises → Otimização
3. Identificar alocações problemáticas
4. Ajustar configurações
5. Re-executar alocação

### 3. Análise Comparativa

**Fluxo:**
1. Executar alocação com CC
2. Exportar resultados
3. Executar alocação com EC
4. Comparar métricas
5. Análise por local e tipo

### 4. Relatório Executivo

**Fluxo:**
1. Executar alocação completa
2. Ir para Análises → Comparações
3. Visualizar Resumo Executivo
4. Exportar resultados
5. Gerar relatório

---

## 💡 Dicas de Uso

### Performance

- **Dados grandes**: Use filtros para reduzir volume visualizado
- **Gráficos lentos**: Limite o número de elementos (top 15)
- **Export rápido**: Use a funcionalidade CSV nativa

### Análise

- **Compare estratégias**: Execute Linear e Gulosa e compare
- **Identifique padrões**: Use gráficos de distribuição
- **Otimize gradualmente**: Comece com dados pequenos

### Troubleshooting

- **Dados não aparecem**: Verifique se carregou corretamente
- **Erro na alocação**: Verifique capacidade total vs inscritos
- **Gráficos vazios**: Certifique-se que a alocação foi executada

---

## 📦 Estrutura de Arquivos Criados

```
gerenciador-de-congressos/
├── streamlit_app.py              # Aplicação principal
├── requirements_streamlit.txt    # Dependências
├── README_STREAMLIT.md          # Documentação
├── STREAMLIT_FEATURES.md        # Este arquivo
├── run_streamlit.bat            # Executável Windows
└── run_streamlit.sh             # Executável Linux/Mac
```

---

## 🚀 Próximos Passos Sugeridos

### Curto Prazo
- [ ] Adicionar modo escuro
- [ ] Implementar cache de dados
- [ ] Adicionar mais filtros
- [ ] Melhorar exportação (PDF)

### Médio Prazo
- [ ] Histórico de alocações
- [ ] Comparação entre execuções
- [ ] Personalização de cores
- [ ] Templates de configuração

### Longo Prazo
- [ ] API REST
- [ ] Autenticação de usuários
- [ ] Banco de dados persistente
- [ ] Deploy em nuvem

---

## 📞 Suporte

Para dúvidas ou sugestões sobre o frontend:
- Consulte `README_STREAMLIT.md`
- Verifique a documentação do projeto
- Abra uma issue no repositório

---

## 🎉 Conclusão

Este frontend Streamlit oferece uma experiência completa e profissional para o sistema de alocação de salas, com:

✅ **6 páginas principais**
✅ **15+ tipos de visualizações**
✅ **30+ gráficos e tabelas**
✅ **Design moderno e responsivo**
✅ **Funcionalidades avançadas**
✅ **Documentação completa**

**Aproveite! 🚀**

