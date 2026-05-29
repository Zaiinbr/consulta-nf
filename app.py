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

# --- CSS FUTURISTA ---
FUTURISTIC_CSS = """
<style>
    /* Variáveis de cores */
    :root {
        --primary: #00f7ff;
        --secondary: #ff006e;
        --dark-bg: #0f0f1e;
        --text-primary: #ffffff;
        --text-secondary: #b0b0d0;
        --accent-yellow: #ffd700;
        --accent-purple: #9d4edd;
    }
    
    /* Background clean */
    body {
        background: #0f0f1e;
        color: var(--text-primary);
    }
    
    .stApp {
        background: #0f0f1e;
    }
    
    /* Títulos clean */
    h1 {
        color: var(--primary);
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    h2 {
        color: var(--secondary);
        font-weight: 600;
    }
    
    h3 {
        color: var(--primary);
        font-weight: 600;
    }
    
    /* Sidebar limpo */
    [data-testid="stSidebar"] {
        background: #1a1a2e;
        border-right: 1px solid var(--primary);
    }
    
    /* Botões clean */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: #000;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        cursor: pointer;
        transition: opacity 0.2s ease;
    }
    
    .stButton > button:hover {
        opacity: 0.85;
    }
    
    /* Inputs clean */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stFileUploader > div > div > input {
        background: #1a1a2e;
        border: 1px solid var(--primary);
        border-radius: 6px;
        color: var(--text-primary);
        padding: 8px 12px;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stFileUploader > div > div > input:focus {
        border-color: var(--secondary);
        background: #1a1a2e;
    }
    
    /* Tables clean */
    .stTable {
        border-collapse: collapse;
    }
    
    .stTable tbody tr {
        border-bottom: 1px solid rgba(0, 247, 255, 0.2);
    }
    
    .stTable tbody tr:hover {
        background: rgba(0, 247, 255, 0.05);
    }
    
    .stTable thead {
        background: transparent;
        border-bottom: 2px solid var(--primary);
        color: var(--primary);
        font-weight: 600;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: var(--primary);
        margin: 20px 0;
    }
    
    /* Alertas clean */
    .stAlert {
        border-radius: 6px;
        border-left: 3px solid var(--primary);
        background: rgba(0, 247, 255, 0.08);
        color: var(--text-primary);
    }
    
    .stWarning {
        border-left-color: var(--accent-yellow);
        background: rgba(255, 215, 0, 0.08);
    }
    
    .stSuccess {
        border-left-color: var(--primary);
        background: rgba(0, 247, 255, 0.08);
    }
    
    .stInfo {
        border-left-color: var(--primary);
        background: rgba(0, 247, 255, 0.08);
    }
    
    .stError {
        border-left-color: var(--secondary);
        background: rgba(255, 0, 110, 0.08);
    }
    
    /* Spinner */
    .stSpinner {
        color: var(--primary);
    }
    
    /* Download buttons */
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent-purple) 100%);
        color: #000;
        font-weight: 600;
    }
    
    [data-testid="stDownloadButton"] > button:hover {
        opacity: 0.85;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary);
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

# --- HEADER COM ESTILO FUTURISTA ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style="text-align: center; padding: 30px 0;">
            <h1>🚀 CONSULTA NF </h1>
            <p style="color: #00f7ff; font-size: 14px; letter-spacing: 2px; text-shadow: 0 0 10px #00f7ff;">
                SISTEMA AVANÇADO DE EXTRAÇÃO E ANÁLISE DE NOTAS FISCAIS
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
        <h2 style="text-align: center; color: #00f7ff; text-shadow: 0 0 15px #00f7ff;">
            📤 PAINEL DE CONTROLE
        </h2>
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
    <div style="background: rgba(0, 247, 255, 0.1); border: 1px solid #00f7ff; border-radius: 8px; padding: 15px; margin-top: 20px;">
        <h4 style="color: #ffd700; margin-top: 0;">💡 INFORMAÇÕES</h4>
        <p style="font-size: 12px; color: #e0e0ff; line-height: 1.6;">
            <strong>Formatos aceitos:</strong> PDF<br>
            <strong>Tamanho máximo:</strong> 200 MB<br>
            <strong>Arquivos:</strong> Múltiplos<br>
            <br>
            <strong>O sistema extrai:</strong><br>
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
    
    # Container de processamento
    with st.container():
        st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(0, 247, 255, 0.1), rgba(255, 0, 110, 0.1)); border: 2px solid #00f7ff; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #00f7ff; text-shadow: 0 0 10px #00f7ff; margin-top: 0;">
                    ⚙️ PROCESSANDO DADOS...
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        lista_resultados = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_files = len(uploaded_files)
        
        for idx, file in enumerate(uploaded_files):
            status_text.text(f"📊 Processando: {file.name} ({idx + 1}/{total_files})")
            dados = extrair_dados_nf(file)
            dados['Arquivo'] = file.name
            lista_resultados.append(dados)
            progress_bar.progress((idx + 1) / total_files)
        
        status_text.text("✅ Processamento concluído!")
        
    # Criar DataFrame
    df = pd.DataFrame(lista_resultados)
    df = df[['Arquivo', 'NF', 'Data de emissão', 'Código do produto', 'Código do parceiro']]

    # TABELA DE RESULTADOS
    st.markdown("---")
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 247, 255, 0.15), rgba(255, 0, 110, 0.15)); border: 2px solid #00f7ff; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <h2 style="color: #00f7ff; text-shadow: 0 0 10px #00f7ff; margin-top: 0;">
                📋 RESULTADOS DA EXTRAÇÃO
            </h2>
            <p style="color: #9d4edd; margin-bottom: 0;">Total de arquivos processados: <strong style="color: #00f7ff;">""" + str(total_files) + """</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display da tabela com estilo
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Arquivo": st.column_config.TextColumn("📁 Arquivo", width="medium"),
            "NF": st.column_config.TextColumn("🎯 NF", width="small"),
            "Data de emissão": st.column_config.TextColumn("📅 Data", width="small"),
            "Código do produto": st.column_config.TextColumn("🏷️ Produtos", width="large"),
            "Código do parceiro": st.column_config.TextColumn("🤝 Parceiro", width="medium"),
        }
    )

    # ====================================================================
    # SEÇÃO DE EXPORTAÇÃO COM ESTILO FUTURISTA
    # ====================================================================
    
    st.markdown("---")
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 0, 110, 0.15), rgba(0, 247, 255, 0.15)); border: 2px solid #ff006e; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <h2 style="color: #ff006e; text-shadow: 0 0 10px #ff006e; margin-top: 0;">
                📥 EXPORTAR DADOS
            </h2>
            <p style="color: #e0e0ff; margin-bottom: 0;">Escolha o formato de exportação desejado</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_export1, col_export2, col_export3 = st.columns(3, gap="medium")

    # ---- EXPORTAR TXT ----
    texto_txt = ""
    for _, row in df.iterrows():
        texto_txt += f"📄 Arquivo: {row['Arquivo']}\n"
        texto_txt += f"🎯 NF: {row['NF']}\n"
        texto_txt += f"📅 Data: {row['Data de emissão']}\n"
        texto_txt += f"🏷️  Produtos: {row['Código do produto']}\n"
        texto_txt += f"🤝 Parceiro: {row['Código do parceiro']}\n"
        texto_txt += "━" * 50 + "\n\n"

    with col_export1:
        st.markdown("""
            <div style="background: rgba(0, 247, 255, 0.1); border: 1px solid #00f7ff; border-radius: 8px; padding: 15px; text-align: center;">
                <p style="color: #00f7ff; margin: 0; font-weight: bold;">📄 FORMATO TXT</p>
            </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download TXT",
            data=texto_txt,
            file_name='dados_extraidos.txt',
            mime='text/plain',
            use_container_width=True
        )

    # ---- EXPORTAR CSV ----
    csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    
    with col_export2:
        st.markdown("""
            <div style="background: rgba(255, 0, 110, 0.1); border: 1px solid #ff006e; border-radius: 8px; padding: 15px; text-align: center;">
                <p style="color: #ff006e; margin: 0; font-weight: bold;">📊 FORMATO CSV</p>
            </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name='dados_extraidos.csv',
            mime='text/csv',
            use_container_width=True
        )

    # ---- EXPORTAR EXCEL ----
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='NFs')
        
        # Adiciona formatação ao Excel
        workbook = writer.book
        worksheet = writer.sheets['NFs']
        
        # Cria um formato com header especial
        header_format = workbook.add_format({
            'bg_color': '#00f7ff',
            'font_color': '#000000',
            'bold': True,
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

    with col_export3:
        st.markdown("""
            <div style="background: rgba(157, 78, 221, 0.1); border: 1px solid #9d4edd; border-radius: 8px; padding: 15px; text-align: center;">
                <p style="9d4edd; margin: 0; font-weight: bold;">📈 FORMATO EXCEL</p>
            </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Excel",
            data=buffer.getvalue(),
            file_name='dados_extraidos.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True
        )

    # ====================================================================
    # SEÇÃO DE ESTATÍSTICAS
    # ====================================================================
    
    st.markdown("---")
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(0, 247, 255, 0.15)); border: 2px solid #ffd700; border-radius: 12px; padding: 20px;">
            <h2 style="color: #ffd700; text-shadow: 0 0 10px #ffd700; margin-top: 0;">
                📊 ESTATÍSTICAS
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total de Arquivos", len(df), delta=None, label_visibility="visible")
    
    with stat_col2:
        nfs_validas = len(df[df['NF'] != 'N/A'])
        st.metric("NFs Encontradas", nfs_validas, delta=None, label_visibility="visible")
    
    with stat_col3:
        produtos_total = sum(len(str(p).split('\n')) for p in df['Código do produto'] if p != 'N/A')
        st.metric("Produtos Extraídos", produtos_total, delta=None, label_visibility="visible")
    
    with stat_col4:
        parceiros = len(df[df['Código do parceiro'] != 'N/A'])
        st.metric("Parceiros Identificados", parceiros, delta=None, label_visibility="visible")

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
    <div style="text-align: center; padding: 20px 0; color: #9d4edd;">
        <p style="margin: 0; font-size: 12px;">
            🔧 <strong>Make Distribuidora</strong> • Projeto ConsultaNF • Versão 2.0<br>
            <span style="color: #00f7ff; text-shadow: 0 0 5px #00f7ff;">Powered by Streamlit + Python</span>
        </p>
    </div>
""", unsafe_allow_html=True)
