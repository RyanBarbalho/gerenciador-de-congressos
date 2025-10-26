# 🏫 Sistema de Alocação de Salas - Frontend Streamlit

Interface web moderna e interativa para o sistema de alocação de salas.

## 🚀 Início Rápido

### Instalação

```bash
pip install -r requirements_streamlit.txt
```

### Executar o App

```bash
streamlit run streamlit_app.py
```

O app será aberto automaticamente no seu navegador em `http://localhost:8501`

## ✨ Recursos

### 🏠 Home
- Dashboard inicial com métricas principais
- Botões de ação rápida
- Guia de uso do sistema
- Informações sobre padrões de projeto

### 📊 Dashboard
- Visualização de estatísticas gerais
- Gráficos interativos de distribuição
- Análise de materiais e salas
- Comparação entre cursos (CC e EC)

### 📁 Dados
- **Carregar**: Upload de arquivos CSV ou carregamento de dados padrão
- **Visualizar**: Exploração interativa de matérias e salas com busca
- **Exportar**: Download dos dados em formato CSV

### ⚙️ Alocação
- Seleção de estratégia (Linear ou Gulosa)
- Configuração de ofertas a incluir
- Execução da otimização com barra de progresso
- Visualização de métricas em tempo real

### 📈 Resultados
- **Por Sala**: Visualização detalhada de alocações em cada sala
- **Por Horário**: Organização por horários com conflitos resolvidos
- **Por Matéria**: Lista completa com busca e filtros
- **Por Local**: Distribuição geográfica (IC, IM, IF)
- Download de resultados em CSV

### 📉 Análises
- **Gráficos**: Visualizações avançadas de utilização e eficiência
- **Otimização**: Análise de qualidade da alocação
- **Comparações**: Métricas comparativas por local, tipo e categoria

## 🎨 Design

- Interface moderna com gradientes coloridos
- Cards de métricas com visual atraente
- Gráficos interativos com Plotly
- Responsivo e otimizado
- Tema claro e profissional

## 📊 Visualizações

- Gráficos de pizza para distribuições
- Gráficos de barras para comparações
- Histogramas para análises estatísticas
- Box plots para distribuições
- Mapas de calor para utilização

## 🔧 Tecnologias

- **Streamlit**: Framework web Python
- **Plotly**: Gráficos interativos
- **Pandas**: Manipulação de dados
- **PuLP**: Otimização linear

## 📝 Uso

1. **Carregue os dados**: Clique em "Carregar Dados Padrão" na Home ou faça upload na página Dados
2. **Configure a alocação**: Vá para "Alocação" e escolha suas preferências
3. **Execute**: Clique em "Executar Alocação" e aguarde
4. **Analise**: Explore os resultados em múltiplas visualizações
5. **Exporte**: Faça download dos resultados para uso posterior

## 🎯 Recursos Avançados

### Filtros e Busca
- Busca por nome de matéria
- Filtros por curso (CC/EC)
- Filtros por local e tipo de sala

### Métricas em Tempo Real
- Utilização de salas
- Espaço ocioso
- Custos adicionais
- Eficiência global

### Análises Comparativas
- Por local (IC, IM, IF)
- Por tipo de sala (Aula, Lab, Auditório)
- Por categoria (Lab vs Não-Lab)

### Exportação
- CSV com todos os dados
- Formatação pronta para relatórios
- Compatível com Excel

## 🐛 Solução de Problemas

### Erro ao carregar dados
- Verifique se os arquivos CSV estão no diretório correto
- Confirme o formato dos arquivos (colunas obrigatórias)

### App não inicia
- Verifique se todas as dependências estão instaladas
- Execute `pip install -r requirements_streamlit.txt`

### Gráficos não aparecem
- Atualize o navegador (Ctrl+F5)
- Verifique a conexão com a internet

## 📱 Responsividade

O app é totalmente responsivo e funciona em:
- Desktop (recomendado)
- Tablets
- Smartphones (visualização limitada)

## 🔄 Atualizações Futuras

- [ ] Exportação para PDF
- [ ] Modo escuro
- [ ] Múltiplos idiomas
- [ ] Salvamento de configurações
- [ ] Histórico de alocações
- [ ] Comparação entre execuções
- [ ] API REST
- [ ] Autenticação de usuários

## 📞 Suporte

Para problemas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Streamlit**

