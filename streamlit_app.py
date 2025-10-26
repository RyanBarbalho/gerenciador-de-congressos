import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from io import StringIO

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.data_loader import SistemaCompletoRefatorado
from app.repositories.alocacao_repo import AlocacaoLinearStrategy, AlocacaoGulosaStrategy, AlocacaoManager
from app.strategies.interfaces import CompatibilidadePadrao
from app.models.domain import Observer, AlocacaoResultado

try:
    from pdf_generator import create_timetable_pdf_from_alocacoes
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

st.set_page_config(
    page_title="Sistema de Alocação de Salas",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card-orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        font-size: 1.1rem;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

class StreamlitObserver(Observer):
    def __init__(self):
        self.messages = []
        
    def on_progress(self, etapa: str, progresso: float):
        self.messages.append(f"[{progresso:5.1f}%] {etapa}")
        
    def on_sucesso(self, resultado: AlocacaoResultado):
        self.messages.append("✅ Alocação concluída com sucesso!")
        
    def on_erro(self, erro: str):
        self.messages.append(f"❌ Erro: {erro}")

if 'sistema' not in st.session_state:
    st.session_state.sistema = None
if 'resultado' not in st.session_state:
    st.session_state.resultado = None
if 'materias' not in st.session_state:
    st.session_state.materias = None
if 'salas' not in st.session_state:
    st.session_state.salas = None
if 'repository_cc' not in st.session_state:
    st.session_state.repository_cc = None
if 'repository_ec' not in st.session_state:
    st.session_state.repository_ec = None

with st.sidebar:
    st.markdown("### 🏫 Sistema de Alocação")
    st.markdown("---")
    
    page = st.radio(
        "Navegação",
        ["🏠 Home", "📊 Dashboard", "📁 Dados", "⚙️ Alocação", "📈 Resultados", "📉 Análises"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Sobre")
    st.markdown("""
    Sistema inteligente de alocação de salas usando programação linear.
    
    **Recursos:**
    - Otimização automática
    - Múltiplas estratégias
    - Análises detalhadas
    - Exportação de dados
    """)

if page == "🏠 Home":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="main-header">🏫 Sistema de Alocação de Salas</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Otimização inteligente usando programação linear</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Otimização</h3>
            <p style="font-size: 1.5rem; margin: 0;">Inteligente</p>
            <p style="margin: 0; opacity: 0.9;">Programação Linear</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card-green">
            <h3>⚡ Rápido</h3>
            <p style="font-size: 1.5rem; margin: 0;">< 5s</p>
            <p style="margin: 0; opacity: 0.9;">Tempo médio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card-orange">
            <h3>📊 Múltiplas</h3>
            <p style="font-size: 1.5rem; margin: 0;">Análises</p>
            <p style="margin: 0; opacity: 0.9;">Visualizações</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card-blue">
            <h3>🎨 Padrões</h3>
            <p style="font-size: 1.5rem; margin: 0;">6 tipos</p>
            <p style="margin: 0; opacity: 0.9;">Design Patterns</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Começar")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Carregar Dados Padrão", use_container_width=True):
            with st.spinner("Carregando dados..."):
                try:
                    sistema = SistemaCompletoRefatorado()
                    
                    if os.path.exists('oferta_cc_2025_1.csv'):
                        st.session_state.repository_cc = sistema.carregar_dados_csv('oferta_cc_2025_1.csv')
                        st.success("✅ Dados de CC carregados!")
                    
                    if os.path.exists('oferta_ec_2025_1.csv'):
                        st.session_state.repository_ec = sistema.carregar_dados_csv('oferta_ec_2025_1.csv')
                        st.success("✅ Dados de EC carregados!")
                    
                    st.session_state.sistema = sistema
                    
                except Exception as e:
                    st.error(f"Erro ao carregar dados: {e}")
    
    with col2:
        if st.button("⚙️ Executar Alocação", use_container_width=True):
            if st.session_state.repository_cc or st.session_state.repository_ec:
                st.info("Vá para a página 'Alocação' para executar!")
            else:
                st.warning("Carregue os dados primeiro!")
    
    with col3:
        if st.button("📈 Ver Resultados", use_container_width=True):
            if st.session_state.resultado:
                st.info("Vá para a página 'Resultados'!")
            else:
                st.warning("Execute a alocação primeiro!")
    
    st.markdown("---")
    
    st.markdown("### 📖 Como Usar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Carregar Dados
        - Clique em "Carregar Dados Padrão"
        - Ou vá para "Dados" para upload personalizado
        - Suporta múltiplas ofertas (CC, EC)
        
        #### 2️⃣ Executar Alocação
        - Escolha a estratégia (Linear ou Gulosa)
        - Configure parâmetros opcionais
        - Execute a otimização
        """)
    
    with col2:
        st.markdown("""
        #### 3️⃣ Analisar Resultados
        - Visualize alocações por sala
        - Veja distribuição por horário
        - Analise métricas de utilização
        
        #### 4️⃣ Exportar
        - Exporte para CSV
        - Gere relatórios em PDF
        - Compartilhe os resultados
        """)
    
    st.markdown("---")
    
    st.markdown("### 🎨 Padrões de Projeto Implementados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        - 🏭 **Factory Pattern**: Criação de objetos
        - 🔨 **Builder Pattern**: Construção flexível
        """)
    
    with col2:
        st.markdown("""
        - 🎯 **Strategy Pattern**: Algoritmos intercambiáveis
        - 📦 **Repository Pattern**: Gerenciamento de dados
        """)
    
    with col3:
        st.markdown("""
        - 👁️ **Observer Pattern**: Sistema de notificações
        - 🎭 **Facade Pattern**: Interface simplificada
        """)

elif page == "📊 Dashboard":
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.repository_cc and not st.session_state.repository_ec:
        st.warning("⚠️ Nenhum dado carregado. Vá para 'Home' ou 'Dados' para carregar.")
    else:
        materias_cc = list(st.session_state.repository_cc.buscar_materias()) if st.session_state.repository_cc else []
        materias_ec = list(st.session_state.repository_ec.buscar_materias()) if st.session_state.repository_ec else []
        
        todas_materias = materias_cc + materias_ec
        
        if st.session_state.repository_cc:
            salas = list(st.session_state.repository_cc.buscar_salas())
        elif st.session_state.repository_ec:
            salas = list(st.session_state.repository_ec.buscar_salas())
        else:
            salas = []
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total de Matérias", len(todas_materias), delta=None)
        
        with col2:
            st.metric("Total de Salas", len(salas), delta=None)
        
        with col3:
            total_inscritos = sum(m.inscritos for m in todas_materias)
            st.metric("Total de Inscritos", total_inscritos, delta=None)
        
        with col4:
            capacidade_total = sum(s.capacidade for s in salas)
            st.metric("Capacidade Total", capacidade_total, delta=None)
        
        with col5:
            utilizacao = (total_inscritos / capacidade_total * 100) if capacidade_total > 0 else 0
            st.metric("Utilização Potencial", f"{utilizacao:.1f}%", delta=None)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📚 Distribuição de Matérias")
            
            material_counts = {0: 0, 1: 0, 2: 0, 3: 0}
            for materia in todas_materias:
                material_counts[materia.material] += 1
            
            material_names = {
                0: "Sem Laboratório",
                1: "Computadores",
                2: "Robótica",
                3: "Eletrônica"
            }
            
            df_material = pd.DataFrame([
                {"Tipo": material_names[k], "Quantidade": v}
                for k, v in material_counts.items()
            ])
            
            fig = px.pie(df_material, values='Quantidade', names='Tipo',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏢 Distribuição de Salas por Local")
            
            locais_count = {}
            for sala in salas:
                local = sala.local.value.upper()
                locais_count[local] = locais_count.get(local, 0) + 1
            
            df_locais = pd.DataFrame([
                {"Local": k, "Quantidade": v}
                for k, v in locais_count.items()
            ])
            
            fig = px.bar(df_locais, x='Local', y='Quantidade',
                        color='Local',
                        color_discrete_sequence=px.colors.qualitative.Bold)
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👥 Distribuição de Inscritos")
            
            inscritos = [m.inscritos for m in todas_materias]
            
            fig = go.Figure(data=[go.Histogram(x=inscritos, nbinsx=20,
                                              marker_color='#667eea')])
            fig.update_layout(
                xaxis_title="Número de Inscritos",
                yaxis_title="Frequência",
                showlegend=False,
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Média", f"{sum(inscritos)/len(inscritos):.1f}")
            with col_b:
                st.metric("Máximo", max(inscritos))
            with col_c:
                st.metric("Mínimo", min(inscritos))
        
        with col2:
            st.markdown("### 🪑 Distribuição de Capacidade")
            
            capacidades = [s.capacidade for s in salas]
            
            fig = go.Figure(data=[go.Histogram(x=capacidades, nbinsx=15,
                                              marker_color='#11998e')])
            fig.update_layout(
                xaxis_title="Capacidade da Sala",
                yaxis_title="Frequência",
                showlegend=False,
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Média", f"{sum(capacidades)/len(capacidades):.1f}")
            with col_b:
                st.metric("Máximo", max(capacidades))
            with col_c:
                st.metric("Mínimo", min(capacidades))
        
        st.markdown("---")
        
        st.markdown("### 🎓 Matérias por Curso")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if materias_cc:
                st.info(f"**Ciência da Computação**: {len(materias_cc)} matérias")
                st.caption(f"Total de inscritos: {sum(m.inscritos for m in materias_cc)}")
        
        with col2:
            if materias_ec:
                st.info(f"**Engenharia de Computação**: {len(materias_ec)} matérias")
                st.caption(f"Total de inscritos: {sum(m.inscritos for m in materias_ec)}")

elif page == "📁 Dados":
    st.markdown('<div class="main-header">📁 Gerenciamento de Dados</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📥 Carregar", "👁️ Visualizar", "💾 Exportar"])
    
    with tab1:
        st.markdown("### Carregar Dados de Ofertas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📚 Ciência da Computação")
            
            cc_file = st.file_uploader("Upload CSV de CC", type=['csv'], key="cc_upload")
            
            if st.button("Carregar CC Padrão"):
                try:
                    with st.spinner("Carregando..."):
                        sistema = SistemaCompletoRefatorado()
                        st.session_state.repository_cc = sistema.carregar_dados_csv('oferta_cc_2025_1.csv')
                        st.session_state.sistema = sistema
                        st.success("✅ Dados de CC carregados!")
                except Exception as e:
                    st.error(f"Erro: {e}")
            
            if cc_file:
                try:
                    with st.spinner("Processando arquivo..."):
                        stringio = StringIO(cc_file.getvalue().decode("utf-8"))
                        sistema = SistemaCompletoRefatorado()
                        
                        temp_file = "temp_cc.csv"
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            f.write(stringio.read())
                        
                        st.session_state.repository_cc = sistema.carregar_dados_csv(temp_file)
                        st.session_state.sistema = sistema
                        
                        os.remove(temp_file)
                        
                        st.success("✅ Arquivo de CC carregado!")
                except Exception as e:
                    st.error(f"Erro ao processar arquivo: {e}")
        
        with col2:
            st.markdown("#### 🔧 Engenharia de Computação")
            
            ec_file = st.file_uploader("Upload CSV de EC", type=['csv'], key="ec_upload")
            
            if st.button("Carregar EC Padrão"):
                try:
                    with st.spinner("Carregando..."):
                        sistema = SistemaCompletoRefatorado()
                        st.session_state.repository_ec = sistema.carregar_dados_csv('oferta_ec_2025_1.csv')
                        st.session_state.sistema = sistema
                        st.success("✅ Dados de EC carregados!")
                except Exception as e:
                    st.error(f"Erro: {e}")
            
            if ec_file:
                try:
                    with st.spinner("Processando arquivo..."):
                        stringio = StringIO(ec_file.getvalue().decode("utf-8"))
                        sistema = SistemaCompletoRefatorado()
                        
                        temp_file = "temp_ec.csv"
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            f.write(stringio.read())
                        
                        st.session_state.repository_ec = sistema.carregar_dados_csv(temp_file)
                        st.session_state.sistema = sistema
                        
                        os.remove(temp_file)
                        
                        st.success("✅ Arquivo de EC carregado!")
                except Exception as e:
                    st.error(f"Erro ao processar arquivo: {e}")
        
        st.markdown("---")
        st.markdown("### 📋 Formato do CSV")
        st.info("""
        O arquivo CSV deve conter as seguintes colunas:
        - **codigo**: Código da matéria
        - **nome**: Nome da matéria
        - **matriculados**: Número de alunos
        - **horario**: Horário (ex: 2M34, 35T12)
        - **capacidade**: Capacidade necessária
        - **material**: 0=Nenhum, 1=Computadores, 2=Robótica, 3=Eletrônica
        """)
    
    with tab2:
        if not st.session_state.repository_cc and not st.session_state.repository_ec:
            st.warning("⚠️ Nenhum dado carregado.")
        else:
            data_source = st.radio("Visualizar dados de:", 
                                  ["Ciência da Computação", "Engenharia de Computação", "Todas as Matérias"])
            
            if data_source == "Ciência da Computação" and st.session_state.repository_cc:
                materias = list(st.session_state.repository_cc.buscar_materias())
                salas = list(st.session_state.repository_cc.buscar_salas())
            elif data_source == "Engenharia de Computação" and st.session_state.repository_ec:
                materias = list(st.session_state.repository_ec.buscar_materias())
                salas = list(st.session_state.repository_ec.buscar_salas())
            else:
                materias_cc = list(st.session_state.repository_cc.buscar_materias()) if st.session_state.repository_cc else []
                materias_ec = list(st.session_state.repository_ec.buscar_materias()) if st.session_state.repository_ec else []
                materias = materias_cc + materias_ec
                
                if st.session_state.repository_cc:
                    salas = list(st.session_state.repository_cc.buscar_salas())
                else:
                    salas = list(st.session_state.repository_ec.buscar_salas())
            
            st.markdown("### 📚 Matérias")
            
            df_materias = pd.DataFrame([{
                "Código": m.id,
                "Nome": m.nome,
                "Inscritos": m.inscritos,
                "Horário": m.horario,
                "Material": {0: "Nenhum", 1: "Computadores", 2: "Robótica", 3: "Eletrônica"}.get(m.material, "N/A")
            } for m in materias])
            
            search = st.text_input("🔍 Buscar matéria", "")
            if search:
                df_materias = df_materias[df_materias['Nome'].str.contains(search, case=False, na=False)]
            
            st.dataframe(df_materias, use_container_width=True, height=400)
            
            st.markdown("---")
            st.markdown("### 🏢 Salas")
            
            df_salas = pd.DataFrame([{
                "Nome": s.nome,
                "Capacidade": s.capacidade,
                "Tipo": s.tipo.value,
                "Local": s.local.value.upper(),
                "Equipamento": {0: "Nenhum", 1: "Computadores", 2: "Robótica", 3: "Eletrônica"}.get(s.tipo_equipamento, "N/A"),
                "Custo Adicional": f"R$ {s.custo_adicional:.2f}"
            } for s in salas])
            
            st.dataframe(df_salas, use_container_width=True, height=400)
    
    with tab3:
        st.markdown("### 💾 Exportar Dados")
        
        if not st.session_state.repository_cc and not st.session_state.repository_ec:
            st.warning("⚠️ Nenhum dado para exportar.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.repository_cc:
                    materias_cc = list(st.session_state.repository_cc.buscar_materias())
                    df_export = pd.DataFrame([{
                        "Código": m.id,
                        "Nome": m.nome,
                        "Inscritos": m.inscritos,
                        "Horário": m.horario,
                        "Material": m.material
                    } for m in materias_cc])
                    
                    csv = df_export.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Matérias CC (CSV)",
                        data=csv,
                        file_name="materias_cc.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col2:
                if st.session_state.repository_ec:
                    materias_ec = list(st.session_state.repository_ec.buscar_materias())
                    df_export = pd.DataFrame([{
                        "Código": m.id,
                        "Nome": m.nome,
                        "Inscritos": m.inscritos,
                        "Horário": m.horario,
                        "Material": m.material
                    } for m in materias_ec])
                    
                    csv = df_export.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Matérias EC (CSV)",
                        data=csv,
                        file_name="materias_ec.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

elif page == "⚙️ Alocação":
    st.markdown('<div class="main-header">⚙️ Executar Alocação</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.repository_cc and not st.session_state.repository_ec:
        st.warning("⚠️ Carregue os dados primeiro!")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Configurações")
            
            strategy_type = st.selectbox(
                "Estratégia de Alocação",
                ["Programação Linear (Ótimo)", "Guloso (Rápido)"],
                help="Linear encontra a solução ótima, Guloso é mais rápido mas pode não ser ótimo"
            )
            
            include_cc = st.checkbox("Incluir Ciência da Computação", 
                                    value=bool(st.session_state.repository_cc),
                                    disabled=not st.session_state.repository_cc)
            include_ec = st.checkbox("Incluir Engenharia de Computação", 
                                    value=bool(st.session_state.repository_ec),
                                    disabled=not st.session_state.repository_ec)
        
        with col2:
            st.markdown("### Status")
            
            if st.session_state.repository_cc:
                materias_cc = list(st.session_state.repository_cc.buscar_materias())
                st.success(f"✅ CC: {len(materias_cc)} matérias")
            
            if st.session_state.repository_ec:
                materias_ec = list(st.session_state.repository_ec.buscar_materias())
                st.success(f"✅ EC: {len(materias_ec)} matérias")
        
        st.markdown("---")
        
        if st.button("🚀 Executar Alocação", type="primary", use_container_width=True):
            with st.spinner("Executando alocação..."):
                try:
                    todas_materias = []
                    materias_por_codigo = {}
                    materias_compartilhadas = []
                    
                    if include_cc and st.session_state.repository_cc:
                        materias_cc = list(st.session_state.repository_cc.buscar_materias())
                        for materia in materias_cc:
                            chave = f"{materia.id}_{materia.horario}"
                            if chave in materias_por_codigo:
                                materias_compartilhadas.append(materia.id)
                            else:
                                materias_por_codigo[chave] = materia
                    
                    if include_ec and st.session_state.repository_ec:
                        materias_ec = list(st.session_state.repository_ec.buscar_materias())
                        for materia in materias_ec:
                            chave = f"{materia.id}_{materia.horario}"
                            if chave in materias_por_codigo:
                                materias_compartilhadas.append(materia.id)
                            else:
                                materias_por_codigo[chave] = materia
                    
                    todas_materias = list(materias_por_codigo.values())
                    
                    if st.session_state.repository_cc:
                        salas = list(st.session_state.repository_cc.buscar_salas())
                    else:
                        salas = list(st.session_state.repository_ec.buscar_salas())
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    compatibilidade = CompatibilidadePadrao()
                    
                    if "Linear" in strategy_type:
                        status_text.text("Usando estratégia de Programação Linear...")
                        progress_bar.progress(30)
                        alocador = AlocacaoLinearStrategy(compatibilidade)
                    else:
                        status_text.text("Usando estratégia Gulosa...")
                        progress_bar.progress(30)
                        alocador = AlocacaoGulosaStrategy(compatibilidade)
                    
                    progress_bar.progress(50)
                    status_text.text("Executando alocação...")
                    
                    resultado = alocador.alocar(todas_materias, salas)
                    
                    progress_bar.progress(100)
                    
                    if resultado.sucesso:
                        st.session_state.resultado = resultado
                        st.session_state.materias = todas_materias
                        st.session_state.salas = salas
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.success("✅ Alocação executada com sucesso!")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Matérias Alocadas", len(resultado.alocacoes))
                        
                        with col2:
                            salas_usadas = len(set(a.sala.id for a in resultado.alocacoes))
                            st.metric("Salas Utilizadas", salas_usadas)
                        
                        with col3:
                            utilizacao = resultado.metricas['utilizacao_media']
                            st.metric("Utilização Média", f"{utilizacao:.1f}%")
                        
                        with col4:
                            ocioso = resultado.metricas['espaco_ocioso_total']
                            st.metric("Espaço Ocioso", ocioso)
                        
                        if materias_compartilhadas:
                            st.info(f"ℹ️ {len(materias_compartilhadas)} matérias compartilhadas detectadas")
                        
                        st.markdown("---")
                        
                        if PDF_AVAILABLE:
                            col_pdf1, col_pdf2 = st.columns(2)
                            
                            with col_pdf1:
                                if st.button("📄 Gerar PDF de Horários Agora", type="secondary", use_container_width=True):
                                    with st.spinner("Gerando PDF..."):
                                        try:
                                            pdf_filename = "horario_alocacao.pdf"
                                            sucesso_pdf = create_timetable_pdf_from_alocacoes(resultado, pdf_filename)
                                            
                                            if sucesso_pdf and os.path.exists(pdf_filename):
                                                st.success(f"✅ PDF gerado com sucesso!")
                                                
                                                with open(pdf_filename, "rb") as pdf_file:
                                                    pdf_bytes = pdf_file.read()
                                                    st.download_button(
                                                        label="⬇️ Download PDF",
                                                        data=pdf_bytes,
                                                        file_name=pdf_filename,
                                                        mime="application/pdf",
                                                        use_container_width=True
                                                    )
                                            else:
                                                st.error("❌ Erro ao gerar PDF")
                                        except Exception as e:
                                            st.error(f"❌ Erro ao gerar PDF: {e}")
                            
                            with col_pdf2:
                                st.info("💡 Você também pode gerar o PDF na página 'Resultados'")
                        
                        st.balloons()
                        
                    else:
                        status_text.empty()
                        progress_bar.empty()
                        st.error(f"❌ Erro na alocação: {resultado.erro}")
                
                except Exception as e:
                    status_text.empty()
                    progress_bar.empty()
                    st.error(f"❌ Erro durante a alocação: {e}")
                    
                    with st.expander("🔍 Detalhes do erro (para debug)"):
                        import traceback
                        st.code(traceback.format_exc())
                        
                        st.markdown("### Informações de Debug")
                        st.write(f"**Total de matérias**: {len(todas_materias)}")
                        st.write(f"**Total de salas**: {len(salas)}")
                        st.write(f"**Exemplos de IDs de matérias**: {[m.id for m in todas_materias[:5]]}")
                        st.write(f"**Exemplos de IDs de salas**: {[s.id for s in salas[:5]]}")

elif page == "📈 Resultados":
    st.markdown('<div class="main-header">📈 Resultados da Alocação</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.resultado:
        st.warning("⚠️ Execute a alocação primeiro!")
    else:
        resultado = st.session_state.resultado
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("✅ Alocadas", len(resultado.alocacoes))
        
        with col2:
            salas_usadas = len(set(a.sala.id for a in resultado.alocacoes))
            st.metric("🏢 Salas", salas_usadas)
        
        with col3:
            utilizacao = resultado.metricas['utilizacao_media']
            st.metric("📊 Utilização", f"{utilizacao:.1f}%")
        
        with col4:
            ocioso = resultado.metricas['espaco_ocioso_total']
            st.metric("🪑 Ocioso", ocioso)
        
        with col5:
            custo = resultado.metricas.get('custo_total', 0)
            st.metric("💰 Custo", f"R$ {custo:.2f}")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if PDF_AVAILABLE:
                if st.button("📄 Gerar PDF de Horários", type="primary", use_container_width=True):
                    with st.spinner("Gerando PDF..."):
                        try:
                            pdf_filename = "horario_alocacao.pdf"
                            sucesso_pdf = create_timetable_pdf_from_alocacoes(resultado, pdf_filename)
                            
                            if sucesso_pdf and os.path.exists(pdf_filename):
                                st.success(f"✅ PDF gerado: {pdf_filename}")
                                
                                with open(pdf_filename, "rb") as pdf_file:
                                    pdf_bytes = pdf_file.read()
                                    st.download_button(
                                        label="⬇️ Download PDF",
                                        data=pdf_bytes,
                                        file_name=pdf_filename,
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                            else:
                                st.error("❌ Erro ao gerar PDF")
                        except Exception as e:
                            st.error(f"❌ Erro ao gerar PDF: {e}")
            else:
                st.warning("⚠️ PDF generator não disponível. Instale reportlab.")
        
        with col2:
            if os.path.exists("horario_alocacao.pdf"):
                with open("horario_alocacao.pdf", "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                    st.download_button(
                        label="⬇️ Download PDF Existente",
                        data=pdf_bytes,
                        file_name="horario_alocacao.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Por Sala", "🕐 Por Horário", "📚 Por Matéria", "📍 Por Local"])
        
        with tab1:
            st.markdown("### Alocações por Sala")
            
            salas_materias = {}
            for alocacao in resultado.alocacoes:
                sala_id = alocacao.sala.id
                if sala_id not in salas_materias:
                    salas_materias[sala_id] = {'sala': alocacao.sala, 'alocacoes': []}
                salas_materias[sala_id]['alocacoes'].append(alocacao)
            
            for sala_id in sorted(salas_materias.keys()):
                info_sala = salas_materias[sala_id]
                sala = info_sala['sala']
                alocacoes = info_sala['alocacoes']
                
                with st.expander(f"🏢 {sala.nome} - {len(alocacoes)} matérias"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.caption("**Local**")
                        st.write(sala.local.value.upper())
                    
                    with col2:
                        st.caption("**Tipo**")
                        st.write(sala.tipo.value.title())
                    
                    with col3:
                        st.caption("**Capacidade**")
                        st.write(sala.capacidade)
                    
                    st.markdown("---")
                    
                    df_sala = pd.DataFrame([{
                        "Matéria": a.materia.nome,
                        "Horário": a.materia.horario,
                        "Inscritos": a.materia.inscritos,
                        "Utilização": f"{a.utilizacao_percentual:.1f}%",
                        "Ocioso": a.espaco_ocioso,
                        "Lab": "✓" if a.materia.material > 0 else ""
                    } for a in alocacoes])
                    
                    st.dataframe(df_sala, use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown("### Alocações por Horário")
            
            horarios_materias = {}
            for alocacao in resultado.alocacoes:
                horario = alocacao.materia.horario
                if horario not in horarios_materias:
                    horarios_materias[horario] = []
                horarios_materias[horario].append(alocacao)
            
            for horario in sorted(horarios_materias.keys()):
                alocacoes = horarios_materias[horario]
                total_alunos = sum(a.materia.inscritos for a in alocacoes)
                
                with st.expander(f"🕐 {horario} - {len(alocacoes)} matérias ({total_alunos} alunos)"):
                    df_horario = pd.DataFrame([{
                        "Matéria": a.materia.nome,
                        "Sala": a.sala.nome,
                        "Local": a.sala.local.value.upper(),
                        "Inscritos": a.materia.inscritos,
                        "Capacidade": a.sala.capacidade,
                        "Utilização": f"{a.utilizacao_percentual:.1f}%"
                    } for a in alocacoes])
                    
                    st.dataframe(df_horario, use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("### Todas as Matérias Alocadas")
            
            search_materia = st.text_input("🔍 Buscar matéria", "")
            
            df_materias = pd.DataFrame([{
                "Matéria": a.materia.nome,
                "Código": a.materia.id,
                "Inscritos": a.materia.inscritos,
                "Sala": a.sala.nome,
                "Local": a.sala.local.value.upper(),
                "Horário": a.materia.horario,
                "Utilização": f"{a.utilizacao_percentual:.1f}%",
                "Lab": "✓" if a.materia.material > 0 else ""
            } for a in resultado.alocacoes])
            
            if search_materia:
                df_materias = df_materias[df_materias['Matéria'].str.contains(search_materia, case=False, na=False)]
            
            st.dataframe(df_materias, use_container_width=True, height=600, hide_index=True)
            
            csv = df_materias.to_csv(index=False)
            st.download_button(
                label="📥 Download Resultados (CSV)",
                data=csv,
                file_name="resultados_alocacao.csv",
                mime="text/csv"
            )
        
        with tab4:
            st.markdown("### Distribuição por Local")
            
            locais_stats = {}
            for alocacao in resultado.alocacoes:
                local = alocacao.sala.local.value.upper()
                if local not in locais_stats:
                    locais_stats[local] = {
                        'materias': 0,
                        'inscritos': 0,
                        'capacidade': 0,
                        'salas': set()
                    }
                locais_stats[local]['materias'] += 1
                locais_stats[local]['inscritos'] += alocacao.materia.inscritos
                locais_stats[local]['capacidade'] += alocacao.sala.capacidade
                locais_stats[local]['salas'].add(alocacao.sala.id)
            
            for local, stats in locais_stats.items():
                utilizacao = (stats['inscritos'] / stats['capacidade'] * 100) if stats['capacidade'] > 0 else 0
                
                st.markdown(f"#### 📍 {local}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Matérias", stats['materias'])
                
                with col2:
                    st.metric("Salas", len(stats['salas']))
                
                with col3:
                    st.metric("Inscritos", stats['inscritos'])
                
                with col4:
                    st.metric("Utilização", f"{utilizacao:.1f}%")
                
                st.markdown("---")

elif page == "📉 Análises":
    st.markdown('<div class="main-header">📉 Análises Avançadas</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.resultado:
        st.warning("⚠️ Execute a alocação primeiro!")
    else:
        resultado = st.session_state.resultado
        
        tab1, tab2, tab3 = st.tabs(["📊 Gráficos", "🎯 Otimização", "📈 Comparações"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Utilização por Sala")
                
                df_util = pd.DataFrame([{
                    "Sala": a.sala.nome,
                    "Utilização": a.utilizacao_percentual,
                    "Local": a.sala.local.value.upper()
                } for a in resultado.alocacoes])
                
                df_util_avg = df_util.groupby('Sala')['Utilização'].mean().reset_index()
                df_util_avg = df_util_avg.sort_values('Utilização', ascending=False).head(15)
                
                fig = px.bar(df_util_avg, x='Sala', y='Utilização',
                           color='Utilização',
                           color_continuous_scale='RdYlGn')
                fig.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🪑 Espaço Ocioso")
                
                df_ocioso = pd.DataFrame([{
                    "Sala": a.sala.nome,
                    "Ocioso": a.espaco_ocioso,
                    "Local": a.sala.local.value.upper()
                } for a in resultado.alocacoes])
                
                df_ocioso_total = df_ocioso.groupby('Sala')['Ocioso'].sum().reset_index()
                df_ocioso_total = df_ocioso_total.sort_values('Ocioso', ascending=False).head(15)
                
                fig = px.bar(df_ocioso_total, x='Sala', y='Ocioso',
                           color='Ocioso',
                           color_continuous_scale='Reds_r')
                fig.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📍 Alocações por Local")
                
                locais_count = {}
                for alocacao in resultado.alocacoes:
                    local = alocacao.sala.local.value.upper()
                    locais_count[local] = locais_count.get(local, 0) + 1
                
                df_locais = pd.DataFrame([
                    {"Local": k, "Quantidade": v}
                    for k, v in locais_count.items()
                ])
                
                fig = px.pie(df_locais, values='Quantidade', names='Local',
                           color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🎓 Distribuição de Turmas")
                
                inscritos = [a.materia.inscritos for a in resultado.alocacoes]
                
                fig = go.Figure(data=[go.Box(y=inscritos, name='Inscritos',
                                            marker_color='lightblue')])
                fig.update_layout(
                    yaxis_title="Número de Inscritos",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### 🎯 Análise de Otimização")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_capacidade = sum(a.sala.capacidade for a in resultado.alocacoes)
                total_inscritos = sum(a.materia.inscritos for a in resultado.alocacoes)
                eficiencia = (total_inscritos / total_capacidade * 100) if total_capacidade > 0 else 0
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Eficiência Global</h4>
                    <h2>{eficiencia:.1f}%</h2>
                    <p>{total_inscritos} / {total_capacidade} lugares</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                salas_im = sum(1 for a in resultado.alocacoes if a.sala.local.value == 'im')
                percentual_im = (salas_im / len(resultado.alocacoes) * 100) if resultado.alocacoes else 0
                
                st.markdown(f"""
                <div class="metric-card-orange">
                    <h4>Uso de Salas IM</h4>
                    <h2>{percentual_im:.1f}%</h2>
                    <p>{salas_im} matérias</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                labs = sum(1 for a in resultado.alocacoes if a.materia.material > 0)
                percentual_labs = (labs / len(resultado.alocacoes) * 100) if resultado.alocacoes else 0
                
                st.markdown(f"""
                <div class="metric-card-green">
                    <h4>Matérias em Labs</h4>
                    <h2>{percentual_labs:.1f}%</h2>
                    <p>{labs} matérias</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("### 📊 Faixas de Utilização")
            
            faixas = {"0-50%": 0, "50-70%": 0, "70-85%": 0, "85-100%": 0, ">100%": 0}
            
            for alocacao in resultado.alocacoes:
                util = alocacao.utilizacao_percentual
                if util < 50:
                    faixas["0-50%"] += 1
                elif util < 70:
                    faixas["50-70%"] += 1
                elif util < 85:
                    faixas["70-85%"] += 1
                elif util <= 100:
                    faixas["85-100%"] += 1
                else:
                    faixas[">100%"] += 1
            
            df_faixas = pd.DataFrame([
                {"Faixa": k, "Quantidade": v}
                for k, v in faixas.items()
            ])
            
            fig = px.bar(df_faixas, x='Faixa', y='Quantidade',
                       color='Quantidade',
                       color_continuous_scale='Viridis')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ⭐ Melhores Alocações")
                
                melhores = sorted(resultado.alocacoes, 
                                key=lambda a: abs(a.utilizacao_percentual - 85))[:10]
                
                df_melhores = pd.DataFrame([{
                    "Matéria": a.materia.nome[:40],
                    "Sala": a.sala.nome,
                    "Util.": f"{a.utilizacao_percentual:.1f}%"
                } for a in melhores])
                
                st.dataframe(df_melhores, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("### ⚠️ Alocações Problemáticas")
                
                problematicas = sorted(resultado.alocacoes, 
                                     key=lambda a: a.espaco_ocioso, reverse=True)[:10]
                
                df_prob = pd.DataFrame([{
                    "Matéria": a.materia.nome[:40],
                    "Sala": a.sala.nome,
                    "Ocioso": a.espaco_ocioso
                } for a in problematicas])
                
                st.dataframe(df_prob, use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("### 📈 Comparação de Métricas")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Por Local")
                
                locais_stats = {}
                for alocacao in resultado.alocacoes:
                    local = alocacao.sala.local.value.upper()
                    if local not in locais_stats:
                        locais_stats[local] = {'inscritos': 0, 'capacidade': 0}
                    locais_stats[local]['inscritos'] += alocacao.materia.inscritos
                    locais_stats[local]['capacidade'] += alocacao.sala.capacidade
                
                df_locais_comp = pd.DataFrame([{
                    "Local": k,
                    "Utilização": (v['inscritos'] / v['capacidade'] * 100) if v['capacidade'] > 0 else 0
                } for k, v in locais_stats.items()])
                
                fig = px.bar(df_locais_comp, x='Local', y='Utilização',
                           color='Utilização',
                           color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Por Tipo de Sala")
                
                tipos_stats = {}
                for alocacao in resultado.alocacoes:
                    tipo = alocacao.sala.tipo.value
                    if tipo not in tipos_stats:
                        tipos_stats[tipo] = {'inscritos': 0, 'capacidade': 0}
                    tipos_stats[tipo]['inscritos'] += alocacao.materia.inscritos
                    tipos_stats[tipo]['capacidade'] += alocacao.sala.capacidade
                
                df_tipos_comp = pd.DataFrame([{
                    "Tipo": k.title(),
                    "Utilização": (v['inscritos'] / v['capacidade'] * 100) if v['capacidade'] > 0 else 0
                } for k, v in tipos_stats.items()])
                
                fig = px.bar(df_tipos_comp, x='Tipo', y='Utilização',
                           color='Utilização',
                           color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                st.markdown("#### Lab vs Não-Lab")
                
                lab_stats = {'Lab': {'inscritos': 0, 'capacidade': 0},
                           'Não-Lab': {'inscritos': 0, 'capacidade': 0}}
                
                for alocacao in resultado.alocacoes:
                    categoria = 'Lab' if alocacao.materia.material > 0 else 'Não-Lab'
                    lab_stats[categoria]['inscritos'] += alocacao.materia.inscritos
                    lab_stats[categoria]['capacidade'] += alocacao.sala.capacidade
                
                df_lab_comp = pd.DataFrame([{
                    "Categoria": k,
                    "Utilização": (v['inscritos'] / v['capacidade'] * 100) if v['capacidade'] > 0 else 0
                } for k, v in lab_stats.items()])
                
                fig = px.bar(df_lab_comp, x='Categoria', y='Utilização',
                           color='Utilização',
                           color_continuous_scale='Oranges')
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📊 Resumo Executivo")
            
            st.info(f"""
            **Resumo da Alocação:**
            
            - **Total de matérias alocadas**: {len(resultado.alocacoes)}
            - **Salas utilizadas**: {len(set(a.sala.id for a in resultado.alocacoes))}
            - **Utilização média**: {resultado.metricas['utilizacao_media']:.1f}%
            - **Espaço ocioso total**: {resultado.metricas['espaco_ocioso_total']} lugares
            - **Custo total**: R$ {resultado.metricas.get('custo_total', 0):.2f}
            - **Salas IM usadas**: {resultado.metricas.get('salas_im_usadas', 0)}
            
            **Recomendações:**
            - Considere redistribuir matérias com baixa utilização (<50%)
            - Avalie a possibilidade de consolidar matérias em salas maiores
            - Priorize salas IC para reduzir custos adicionais
            """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>Sistema de Alocação de Salas • Desenvolvido com Streamlit • 2025</small>
</div>
""", unsafe_allow_html=True)

