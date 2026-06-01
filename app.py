import streamlit as st 
import pandas as pd
import io
import re

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(
    page_title="Make Distribuidora - ConsultaNF", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CORPORATIVO PREMIUM (GRAFITE + VERDE SÁLVIA + PLATINA) ---
FUTURISTIC_CSS = """
<style>
    /* Paleta de cores premium */
    :root {
        --bg-app: #12141c;
        --bg-sidebar: #0e1015;
        --bg-card: #1e222b;
        --border-card: #2d333f;
        --green-mint: #10b981;
        --text-white: #f8fafc;
        --text-secondary: #94a3b8;
    }
    
    /* Background do App */
    body, .stApp {
        background: var(--bg-app);
        color: var(--text-white);
    }
    
    /* Títulos clean */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-white);
        font-weight: 600;
        letter-spacing: 0px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--bg-sidebar);
        border-right: 1px solid var(--border-card);
    }
    
    /* Botões Primary */
    .stButton > button {
        background: transparent;
        border: 1px solid var(--green-mint);
        color: var(--text-white);
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--green-mint);
        color: var(--bg-app);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    /* Download Buttons */
    [data-testid="stDownloadButton"] > button {
        background: transparent;
        border: 1px solid var(--green-mint);
        color: var(--text-white);
        font-weight: 600;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    [data-testid="stDownloadButton"] > button:hover {
        background: var(--green-mint);
        color: var(--bg-app);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stFileUploader > div > div > input {
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        color: var(--text-white);
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stFileUploader > div > div > input:focus {
        border-color: var(--green-mint);
        background: var(--bg-card);
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
    }
    
    /* Tabelas */
    .stTable tbody tr {
        background: var(--bg-card);
        border-bottom: 1px solid var(--border-card);
        transition: all 0.2s ease;
    }
    
    .stTable tbody tr:hover {
        background: #252b36 !important;
        cursor: pointer;
    }
    
    .stTable thead {
        background: transparent;
        border-bottom: 2px solid var(--green-mint);
        color: var(--green-mint);
        font-weight: 600;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: var(--border-card);
        margin: 20px 0;
    }
    
    /* Alertas e Info Boxes */
    .stAlert {
        border-radius: 6px;
        border-left: 3px solid var(--green-mint);
        background: var(--bg-card);
        border-right: 1px solid var(--border-card);
        border-top: 1px solid var(--border-card);
        border-bottom: 1px solid var(--border-card);
        color: var(--text-white);
    }
    
    .stSuccess {
        border-left-color: var(--green-mint);
        background: var(--bg-card);
    }
    
    .stInfo {
        border-left-color: var(--green-mint);
        background: var(--bg-card);
    }
    
    .stWarning {
        border-left-color: var(--green-mint);
        background: var(--bg-card);
    }
    
    .stError {
        border-left-color: var(--green-mint);
        background: var(--bg-card);
    }
    
    /* Spinner */
    .stSpinner {
        color: var(--green-mint);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-app);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-card);
        border-radius: 10px;
        transition: all 0.2s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--green-mint);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: var(--green-mint) !important;
    }
    
    /* Fade-in animation */
    .fade-in {
        animation: fadeIn 0.45s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Métricas e containers */
    .stMetric > div,
    .stContainer > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-card) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Tabs */
    [role="tablist"] {
        border-bottom-color: var(--border-card);
    }
    
    [aria-selected="true"] {
        border-bottom: 2px solid var(--green-mint) !important;
        color: var(--green-mint) !important;
    }
    
    [aria-selected="false"] {
        color: var(--text-secondary) !important;
    }
</style>
"""

st.markdown(FUTURISTIC_CSS, unsafe_allow_html=True)

# Tentar importar pdfplumber
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pdfplumber = None
    PDFPLUMBER_AVAILABLE = False

# --- HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style="text-align: center; padding: 30px 0;">
            <h1 style="margin: 0; color: var(--text-white);">🚀 CONSULTA NF</h1>
            <p style="margin: 8px 0 0 0; font-size: 13px; color: var(--text-secondary);">
                Sistema avançado de extração e análise de notas fiscais
            </p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- VERIFICAÇÃO DE DEPENDÊNCIAS ---
if not PDFPLUMBER_AVAILABLE:
    st.error("""
        ⚠️ **AVISO CRÍTICO** - Dependência não encontrada!
        
        A biblioteca `pdfplumber` não está instalada. 
        Execute `pip install pdfplumber` para ativar a extração de PDF.
    """)
    st.stop()

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def limpar_texto(valor):
    """Remove espaços extras e normaliza texto."""
    return re.sub(r'\s+', ' ', (valor or '')).strip()

# ============================================================================
# FUNÇÕES DE EXTRAÇÃO
# ============================================================================

def extrair_nf(texto, linhas_pdf):
    """Extrai o número da Nota Fiscal do texto do PDF."""
    padroes_nf = [
        r'\bN\.?\s*(\d{1,3}(?:\.\d{3})*|\d{3,})\b',
        r'\bNF[-\s]*e?\s*(?:n[ºo]\.?|n[úu]mero)?\s*[:\-]?\s*(\d{3,})\b',
        r'\bN[ºo]\.?\s*(\d{3,})\b',
        r'\bNúmero\s+da\s+NF\s*[:\-]?\s*(\d{3,})\b',
        r'\bNúmero\s*[:\-]?\s*(\d{3,})\b'
    ]

    for padrao in padroes_nf:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            return match.group(1).replace('.', '')

    for linha in linhas_pdf:
        if re.search(r'\bNF\b|N[ºo]\.?|N[úu]mero', linha, re.IGNORECASE):
            match = re.search(r'(\d{1,3}(?:\.\d{3})*|\d{3,})', linha)
            if match:
                return match.group(1).replace('.', '')

    return "N/A"


def extrair_itens_produtos(pdf_obj):
    """Extrai códigos de produtos da DANFE com múltiplas estratégias."""
    itens = []

    def adicionar_item(codigo, descricao):
        codigo = limpar_texto(codigo)
        descricao = limpar_texto(descricao)
        
        if codigo and re.fullmatch(r'\d{3,}', codigo):
            if not any(item[0] == codigo for item in itens):
                itens.append((codigo, descricao))

    # Estratégia 1: Extrai de tabelas
    for page in pdf_obj.pages:
        for tabela in (page.extract_tables() or []):
            for linha_idx, linha in enumerate(tabela):
                if not linha:
                    continue

                valores = [limpar_texto(celula) for celula in linha if limpar_texto(celula)]
                if not valores:
                    continue

                # Pula cabeçalho apenas se TODA a linha parecer um cabeçalho
                cabecalho = " ".join(valores).upper()
                is_cabecalho = ('CÓD' in cabecalho and 'PROD' in cabecalho) or ('DESCRIÇÃO' in cabecalho and 'PRODUTO' in cabecalho)
                
                if is_cabecalho:
                    continue

                # Procura por códigos de 3+ dígitos
                for indice, celula in enumerate(valores):
                    if re.fullmatch(r'\d{3,}', celula):
                        codigo = celula
                        descricao = valores[indice + 1] if indice + 1 < len(valores) else ""
                        adicionar_item(codigo, descricao)
                        break

    # Estratégia 2: Se não achou nada, busca no texto completo
    if not itens:
        texto_completo = ""
        for page in pdf_obj.pages:
            texto_completo += (page.extract_text() or "") + "\n"
        
        # Procura por blocos de produtos
        blocos = re.finditer(r'DADOS\s+DOS\s+PRODUTOS(?:.(?!DADOS\s+DOS\s+PRODUTOS)){0,5000}', texto_completo, re.IGNORECASE | re.DOTALL)
        for bloco_match in blocos:
            bloco = bloco_match.group(0)
            # Procura por linhas com código + descrição
            linhas_prod = re.findall(r'^\s*(\d{3,})\s+(.+?)\s*$', bloco, re.MULTILINE)
            for codigo, descricao in linhas_prod:
                if re.search(r'\b(UN|PC|KG|CX|FR|LT|CXA|MT|M2|M3|L)\b', descricao, re.IGNORECASE):
                    adicionar_item(codigo, descricao)

    codigos = [codigo for codigo, _ in itens]
    return codigos


def extrair_codigo_parceiro(texto, linhas_pdf):
    """Extrai o código do parceiro/cliente da DANFE."""
    texto_normalizado = re.sub(r'\s+', ' ', texto)

    for indice, linha in enumerate(linhas_pdf):
        if re.search(r'NOME/RAZ[ÃA]O SOCIAL', linha, re.IGNORECASE):
            janela = ' '.join(linhas_pdf[indice:indice + 6])
            match = re.search(r'NOME/RAZ[ÃA]O SOCIAL\s+(.+?)\s+(\d{3,8})\b', janela, re.IGNORECASE)
            if match:
                return match.group(2)

    match = re.search(r'NOME/RAZ[ÃA]O SOCIAL.*?\b(\d{3,8})\b', texto_normalizado, re.IGNORECASE)
    if match:
        return match.group(1)

    inicio = re.search(r'DESTINAT[ÁA]RIO/REMETENTE|DESTINAT[ÁA]RIO', texto_normalizado, re.IGNORECASE)
    fim = re.search(r'DADOS\s+DOS\s+PRODUTOS|DADOS\s+DOS\s+PRODUTOS/SERVIÇOS|DATA\s+DE\s+EMISS[ÃA]O|HORA\s+DA\s+SA[ÍI]DA', texto_normalizado, re.IGNORECASE)

    if inicio and fim and fim.start() > inicio.end():
        bloco = texto_normalizado[inicio.start():fim.start()]
        match = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', bloco)
        if match:
            return match.group(1)

    for indice, linha in enumerate(linhas_pdf):
        if re.search(r'DESTINAT[ÁA]RIO/REMETENTE|DESTINAT[ÁA]RIO', linha, re.IGNORECASE):
            janela = ' '.join(linhas_pdf[indice:indice + 20])
            match = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', janela)
            if match:
                return match.group(1)

    match = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto_normalizado)
    if match:
        return match.group(1)

    return "N/A"


def extrair_dados_nf(pdf_file):
    """
    Função principal de extração de dados da DANFE.
    
    Extrai:
    - Número da NF
    - Data de emissão
    - Código do produto
    - Código do parceiro
    """
    try:
        def limpar_texto_local(valor):
            return re.sub(r'\s+', ' ', (valor or '')).strip()

        with pdfplumber.open(pdf_file) as pdf:
            texto_completo = ""
            linhas = []

            for page in pdf.pages:
                pagina_texto = page.extract_text() or ""
                texto_completo += pagina_texto + "\n"
                linhas.extend([linha.strip() for linha in pagina_texto.splitlines() if linha.strip()])

            dados = {
                "NF": extrair_nf(texto_completo, linhas),
                "Data de emissão": "N/A",
                "Código do produto": "N/A",
                "Código do parceiro": "N/A"
            }

            match_data = re.search(r'(\d{2}/\d{2}/\d{4})', texto_completo)
            if match_data:
                dados["Data de emissão"] = match_data.group(1)

            codigos_produtos = extrair_itens_produtos(pdf)
            dados["Código do produto"] = "\n".join(codigos_produtos) if codigos_produtos else "N/A"
            dados["Código do parceiro"] = extrair_codigo_parceiro(texto_completo, linhas)

            return dados

    except Exception as e:
        return {
            "NF": "Erro",
            "Data de emissão": str(e),
            "Código do produto": "Erro",
            "Código do parceiro": "Erro"
        }



# ============================================================================
# SEÇÃO DE UPLOAD - SIDEBAR
# ============================================================================

st.sidebar.markdown("""
    <div style="padding: 20px 0;">
        <h2 style="text-align: center; margin: 0; color: var(--text-white);">📤 Painel de Controle</h2>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.subheader("📁 Selecione seus arquivos PDF")
uploaded_files = st.sidebar.file_uploader(
    "Arraste ou clique para selecionar PDFs",
    type="pdf", 
    accept_multiple_files=True,
    help="Suporta múltiplos arquivos de uma vez"
)

# Informações adicionais na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="background: var(--bg-card); border: 1px solid var(--border-card); border-left: 3px solid var(--green-mint); border-radius: 6px; padding: 15px; margin-top: 20px;">
        <h4 style="margin-top: 0; color: var(--green-mint); font-weight: 600;">💡 Informações</h4>
        <p style="font-size: 12px; color: var(--text-secondary); line-height: 1.6; margin: 0;">
            <strong>Formatos:</strong> PDF<br>
            <strong>Tamanho máximo:</strong> 200 MB<br>
            <strong>Arquivos:</strong> Múltiplos<br>
            <br>
            <strong>Extração:</strong><br>
            ✓ Número da NF<br>
            ✓ Data de emissão<br>
            ✓ Códigos de produtos<br>
            ✓ Código do parceiro
        </p>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# PROCESSAMENTO DOS ARQUIVOS
# ============================================================================

if uploaded_files:
    st.markdown("---")

    total_files = len(uploaded_files)
    lista_resultados = []
    progress_bar = st.progress(0)

    # UX: spinner nativo durante o processamento
    with st.spinner("⚙️ Processando arquivos, aguarde..."):
        for idx, file in enumerate(uploaded_files):
            dados = extrair_dados_nf(file)
            dados['Arquivo'] = file.name
            lista_resultados.append(dados)
            progress_bar.progress((idx + 1) / total_files)

    # Criar DataFrame (ordenado em colunas desejadas)
    df = pd.DataFrame(lista_resultados)
    df = df[['Arquivo', 'NF', 'Data de emissão', 'Código do produto', 'Código do parceiro']]

    # Exibir os resultados organizados em abas para UX mais fluida
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📋 Visão Geral dos Dados", "📊 Estatísticas e Métricas", "📥 Painel de Exportação"])

    # Aba 1: Visão Geral
    with tab1:
        st.markdown(f"**Total de arquivos processados:** {total_files}")
        # Dataframe com busca e ordenação nativas, sem índice
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    # Aba 2: Estatísticas
    with tab2:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]:
            with st.container():
                st.metric("Total de Arquivos", len(df))
        with cols[1]:
            with st.container():
                nfs_validas = len(df[df['NF'] != 'N/A'])
                st.metric("NFs Encontradas", nfs_validas)
        with cols[2]:
            with st.container():
                produtos_total = sum(len(str(p).split('\n')) for p in df['Código do produto'] if p != 'N/A')
                st.metric("Produtos Extraídos", produtos_total)
        with cols[3]:
            with st.container():
                parceiros = len(df[df['Código do parceiro'] != 'N/A'])
                st.metric("Parceiros Identificados", parceiros)
        st.markdown("</div>", unsafe_allow_html=True)

    # Aba 3: Exportação
    with tab3:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        col_export1, col_export2, col_export3 = st.columns(3, gap="medium")

        # Preparar textos/arquivos
        texto_txt = ""
        for _, row in df.iterrows():
            texto_txt += f"Arquivo: {row['Arquivo']}\n"
            texto_txt += f"NF: {row['NF']}\n"
            texto_txt += f"Data: {row['Data de emissão']}\n"
            texto_txt += f"Produtos: {row['Código do produto']}\n"
            texto_txt += f"Parceiro: {row['Código do parceiro']}\n"
            texto_txt += "-" * 40 + "\n\n"

        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='NFs')
            workbook = writer.book
            worksheet = writer.sheets['NFs']
            header_format = workbook.add_format({
                'bg_color': '#151b22',
                'font_color': '#ffffff',
                'bold': True,
                'border': 1
            })
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

        with col_export1:
            st.download_button(
                label="⬇️ Download TXT",
                data=texto_txt,
                file_name='dados_extraidos.txt',
                mime='text/plain',
                use_container_width=True
            )

        with col_export2:
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name='dados_extraidos.csv',
                mime='text/csv',
                use_container_width=True
            )

        with col_export3:
            st.download_button(
                label="⬇️ Download Excel",
                data=buffer.getvalue(),
                file_name='dados_extraidos.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Interface quando nenhum arquivo é carregado
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
            ### 📚 Como Usar:
            
            **1️⃣ Painel Lateral** → Acesse o menu à esquerda  
            **2️⃣ Selecione PDFs** → Clique em "Arraste ou clique"  
            **3️⃣ Processamento** → O sistema analisa automaticamente  
            **4️⃣ Exporte** → Escolha TXT, CSV ou Excel  
        """)
        
        st.success("""
            💡 **Dica:** Você pode fazer upload de múltiplos PDFs simultaneamente para processamento em lote!
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: var(--text-secondary);">
        <p style="margin: 0; font-size: 12px;">
            🔧 <strong>Make Distribuidora</strong> • Projeto ConsultaNF • Versão 2.0<br>
            Powered by Streamlit + Python
        </p>
    </div>
""", unsafe_allow_html=True)
