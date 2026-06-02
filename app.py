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

# --- CSS MINIMALISTA PREMIUM (COSMOS/LAYERS AESTHETIC) ---
FUTURISTIC_CSS = """
<style>
    /* Paleta ultra-minimalista */
    :root {
        --bg-app: #09090b;
        --bg-sidebar: #09090b;
        --bg-card: #141416;
        --border-line: #222226;
        --accent: #3ecf9e;
        --accent-soft: rgba(62, 207, 158, 0.15);
        --text-white: #f4f4f5;
        --text-secondary: #a3a3a8;
    }
    
    /* Animações fluidas */
    @keyframes fadeInSlide {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes auroraAmbient {
        0% {
            background-position: 0% 50%;
            background-size: 200% 200%;
        }
        25% {
            background-position: 50% 50%;
            background-size: 210% 210%;
        }
        50% {
            background-position: 100% 50%;
            background-size: 200% 200%;
        }
        75% {
            background-position: 50% 0%;
            background-size: 210% 210%;
        }
        100% {
            background-position: 0% 50%;
            background-size: 200% 200%;
        }
    }
    
    @keyframes shimmerSwipe {
        0% {
            background-position: -1200px 0;
        }
        100% {
            background-position: 1200px 0;
        }
    }
    
    @keyframes shimmerText {
        0% {
            background-position: -2000px 0;
        }
        100% {
            background-position: 2000px 0;
        }
    }
    
    @keyframes shimmerButton {
        0% {
            left: -100%;
            opacity: 0;
        }
        50% {
            opacity: 0.8;
        }
        100% {
            left: 100%;
            opacity: 0;
        }
    }
    
    @keyframes breathingPulse {
        0%, 100% {
            box-shadow: inset 0 0 0 1px rgba(62, 207, 158, 0.2), 0 0 8px rgba(62, 207, 158, 0.08);
        }
        50% {
            box-shadow: inset 0 0 0 1px rgba(62, 207, 158, 0.4), 0 0 16px rgba(62, 207, 158, 0.16);
        }
    }
    
    @keyframes elasticPulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(62, 207, 158, 0.08), inset 0 0 0 1px rgba(62, 207, 158, 0.15);
        }
        50% {
            transform: scale(1.03);
            box-shadow: 0 0 24px 4px rgba(62, 207, 158, 0.12), inset 0 0 0 2px rgba(62, 207, 158, 0.25);
        }
    }
    
    @keyframes rippleWave {
        0% {
            background-color: var(--bg-card);
            box-shadow: inset 0 0 0 0 rgba(62, 207, 158, 0);
        }
        50% {
            box-shadow: inset 0 0 0 4px rgba(62, 207, 158, 0.06);
        }
        100% {
            background-color: #1c1c1f;
            box-shadow: inset 0 0 0 0 rgba(62, 207, 158, 0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-16px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(16px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scaleInBouncy {
        0% {
            opacity: 0;
            transform: scale(0.6);
        }
        60% {
            opacity: 1;
            transform: scale(1.08);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.96);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulseGlow {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(62, 207, 158, 0);
        }
        50% {
            box-shadow: 0 0 0 8px rgba(62, 207, 158, 0.08);
        }
    }
    
    @keyframes spinSlide {
        from {
            opacity: 0;
            transform: translateY(12px) rotate(-4deg);
        }
        to {
            opacity: 1;
            transform: translateY(0) rotate(0deg);
        }
    }
    
    @keyframes floatIn {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes floatLift {
        0%, 100% {
            transform: translateY(0) scale(1);
        }
        50% {
            transform: translateY(-2px) scale(1.001);
        }
    }
    
    @keyframes glowBorder {
        0%, 100% {
            border-color: var(--border-line);
            box-shadow: inset 0 0 0 1px var(--border-line);
        }
        50% {
            border-color: rgba(62, 207, 158, 0.4);
            box-shadow: inset 0 0 0 1px rgba(62, 207, 158, 0.2);
        }
    }
    
    /* Background com Aurora Ambient */
    body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg-app) !important;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(62, 207, 158, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(62, 207, 158, 0.03) 0%, transparent 60%) !important;
        animation: auroraAmbient 16s ease-in-out infinite !important;
        color: var(--text-white) !important;
    }
    
    /* Texto e tipografia base */
    * {
        color: var(--text-white);
    }
    
    /* Títulos - Cascata em carregamento */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-white) !important;
        font-weight: 500;
        letter-spacing: 0.05em;
        animation: fadeInSlide 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    h1 {
        animation-delay: 0s;
    }
    
    h2 {
        animation-delay: 0.1s;
    }
    
    h3 {
        animation-delay: 0.2s;
    }
    
    h4 {
        animation-delay: 0.3s;
    }
    
    h5 {
        animation-delay: 0.4s;
    }
    
    h6 {
        animation-delay: 0.5s;
    }
    
    /* Sidebar com Glassmorphism Avançado */
    [data-testid="stSidebar"] {
        background: rgba(9, 9, 11, 0.75) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid var(--border-line);
        -webkit-backdrop-filter: blur(16px);
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] > div > div > div > p,
    [data-testid="stSidebar"] > div > div > div > span {
        animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    [data-testid="stSidebar"] h2 {
        animation-delay: 0.05s;
    }
    
    [data-testid="stSidebar"] h3 {
        animation-delay: 0.15s;
    }
    
    [data-testid="stSidebar"] > div > div > div > div:nth-child(1) {
        animation-delay: 0.25s;
    }
    
    [data-testid="stSidebar"] > div > div > div > div:nth-child(2) {
        animation-delay: 0.35s;
    }
    
    [data-testid="stSidebar"] > div > div > div > div:nth-child(n+3) {
        animation-delay: 0.45s;
    }
    
    /* Markdown text */
    .stMarkdown p, .stMarkdown span, .stMarkdown a {
        color: var(--text-white) !important;
    }
    
    /* Botões - Com efeito de brilho de varredura */
    .stButton > button {
        background: transparent !important;
        border: 1px solid var(--border-line) !important;
        color: var(--text-secondary) !important;
        border-radius: 4px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInSlide 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.1s backwards;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stButton > button:hover {
        background: var(--accent-soft) !important;
        border-color: var(--accent) !important;
        color: var(--text-white) !important;
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 8px 24px rgba(62, 207, 158, 0.16);
    }
    
    .stButton > button:hover::after {
        opacity: 1;
        animation: shimmerButton 0.6s ease-in-out;
    }
    
    .stButton > button:active {
        transform: scale(0.95) translateY(0);
    }
    
    /* Download buttons - Com efeito de brilho */
    [data-testid="stDownloadButton"] > button {
        background: transparent !important;
        border: 1px solid var(--border-line) !important;
        color: var(--text-secondary) !important;
        font-weight: 500;
        border-radius: 4px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideInRight 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s backwards;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stDownloadButton"] > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    [data-testid="stDownloadButton"] > button:hover {
        background: var(--accent-soft) !important;
        border-color: var(--accent) !important;
        color: var(--text-white) !important;
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 8px 24px rgba(62, 207, 158, 0.16);
    }
    
    [data-testid="stDownloadButton"] > button:hover::after {
        opacity: 1;
        animation: shimmerButton 0.6s ease-in-out;
    }
    
    [data-testid="stDownloadButton"] > button:active {
        transform: scale(0.95) translateY(0);
    }
    
    /* Inputs - Com efeito de respiração e expansão de foco */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stFileUploader > div > div > input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-line) !important;
        color: var(--text-white) !important;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.15s backwards;
        position: relative;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stFileUploader > div > div > input:focus {
        border-color: var(--accent) !important;
        background: var(--bg-card) !important;
        color: var(--text-white) !important;
        transform: scale(1.01);
        animation: breathingPulse 2s cubic-bezier(0.4, 0, 0.2, 1) infinite !important;
    }
    
    /* Tabelas - Com efeito de ondulação */
    .stTable tbody tr {
        background: var(--bg-card) !important;
        border-bottom: 1px solid var(--border-line) !important;
        transition: background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: floatIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        position: relative;
        overflow: hidden;
    }
    
    .stTable tbody tr::before {
        content: '';
        position: absolute;
        left: -2px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: transparent;
        transition: background-color 0.3s ease;
    }
    
    .stTable tbody tr:hover {
        animation: rippleWave 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        cursor: pointer;
        transform: translateX(4px);
        box-shadow: -2px 0 12px rgba(62, 207, 158, 0.1);
    }
    
    .stTable tbody tr:hover::before {
        background: var(--accent);
    }
    
    .stTable thead {
        background: transparent !important;
        border-bottom: 1px solid var(--border-line) !important;
        color: var(--text-secondary) !important;
        font-weight: 500;
        animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.05s backwards;
    }
    
    /* Cascata de linhas da tabela */
    .stTable tbody tr:nth-child(1) {
        animation-delay: 0.05s !important;
    }
    
    .stTable tbody tr:nth-child(2) {
        animation-delay: 0.1s !important;
    }
    
    .stTable tbody tr:nth-child(3) {
        animation-delay: 0.15s !important;
    }
    
    .stTable tbody tr:nth-child(4) {
        animation-delay: 0.2s !important;
    }
    
    .stTable tbody tr:nth-child(5) {
        animation-delay: 0.25s !important;
    }
    
    .stTable tbody tr:nth-child(n+6) {
        animation-delay: 0.3s !important;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: var(--border-line);
        margin: 20px 0;
    }
    
    /* Alertas */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 4px;
        border: 1px solid var(--border-line) !important;
        background: var(--bg-card) !important;
        color: var(--text-white) !important;
        animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    .stSuccess, .stInfo, .stWarning, .stError {
        border-left: 1.5px solid var(--accent) !important;
        animation: spinSlide 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Spinner */
    .stSpinner {
        color: var(--accent) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-line);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Progress bar com Super-Glow Incandescente */
    .stProgress > div > div > div > div {
        background: linear-gradient(
            90deg,
            var(--accent) 0%,
            rgba(62, 207, 158, 0.5) 50%,
            var(--accent) 100%
        ) !important;
        background-size: 1000px 100%;
        animation: shimmerSwipe 2s infinite !important;
        height: 2px !important;
        box-shadow: 0 0 20px var(--accent), 0 0 8px rgba(62, 207, 158, 0.6) !important;
    }
    
    /* Spinner com Elasticidade */
    .stSpinner {
        color: var(--accent) !important;
        animation: scaleInBouncy 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards !important;
    }
    
    /* File Uploader Magnético e Reativo */
    .stFileUploader > div {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border-line) !important;
        border-radius: 8px;
        padding: 32px 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: elasticPulse 3s ease-in-out infinite;
        position: relative;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--accent) !important;
        transform: scale(1.02);
        box-shadow: 
            0 0 24px rgba(62, 207, 158, 0.2),
            inset 0 0 0 2px rgba(62, 207, 158, 0.15) !important;
    }
    
    .stFileUploader > div::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 8px;
        background: radial-gradient(circle at center, rgba(62, 207, 158, 0.02), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stFileUploader > div:hover::before {
        opacity: 1;
    }
    /* Containers e métricas - Com efeito de flutuação magnética */
    .stMetric > div,
    .stContainer > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-line) !important;
        border-radius: 4px !important;
        padding: 12px !important;
        animation: floatIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    /* Cascata para métricas */
    .stMetric:nth-child(1) > div,
    .stContainer:nth-child(1) > div {
        animation-delay: 0.3s;
    }
    
    .stMetric:nth-child(2) > div,
    .stContainer:nth-child(2) > div {
        animation-delay: 0.4s;
    }
    
    .stMetric:nth-child(3) > div,
    .stContainer:nth-child(3) > div {
        animation-delay: 0.5s;
    }
    
    .stMetric:nth-child(4) > div,
    .stContainer:nth-child(4) > div {
        animation-delay: 0.6s;
    }
    
    .stMetric:nth-child(n+5) > div,
    .stContainer:nth-child(n+5) > div {
        animation-delay: 0.7s;
    }
    
    .stMetric > div:hover,
    .stContainer > div:hover {
        border-color: rgba(62, 207, 158, 0.3) !important;
        box-shadow: 0 12px 32px rgba(62, 207, 158, 0.12), inset 0 0 0 1px rgba(62, 207, 158, 0.1) !important;
        background: rgba(62, 207, 158, 0.06) !important;
        transform: translateY(-4px) scale(1.01);
        filter: brightness(1.05);
        animation: floatLift 2s ease-in-out infinite;
    }

    [aria-selected="true"] {
        border-bottom: 1.5px solid var(--accent) !important;
        color: var(--text-white) !important;
        background: rgba(62, 207, 158, 0.08) !important;
        animation: pulseGlow 2s infinite;
    }

    [aria-selected="false"] {
        color: var(--text-secondary) !important;
        border-bottom: 1px solid transparent !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [aria-selected="false"]:hover {
        color: var(--text-white) !important;
        border-bottom: 1px solid rgba(62, 207, 158, 0.2) !important;
    }
    
    [role="tab"] {
        font-weight: 500;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Feedback Cinemático - Abas com Sequência */
    [role="tabpanel"] {
        animation: floatIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    [role="tabpanel"]:nth-child(1) {
        animation-delay: 0.1s;
    }
    
    [role="tabpanel"]:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    [role="tabpanel"]:nth-child(3) {
        animation-delay: 0.3s;
    }
    
    /* Cards de Métricas com Cascata Cinemática */
    .stMetric {
        animation: floatIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    .stMetric:nth-child(1) {
        animation-delay: 0.4s;
    }
    
    .stMetric:nth-child(2) {
        animation-delay: 0.5s;
    }
    
    .stMetric:nth-child(3) {
        animation-delay: 0.6s;
    }
    
    .stMetric:nth-child(4) {
        animation-delay: 0.7s;
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

# --- HEADER MINIMALISTA COM TÍTULO METÁLICO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style="text-align: center; padding: 40px 0 20px 0;">
            <h1 style="
                margin: 0;
                font-size: 28px;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                color: var(--text-white);
                background: linear-gradient(
                    90deg,
                    var(--accent),
                    #ffffff,
                    var(--accent)
                );
                background-size: 200% 100%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: shimmerText 4s linear infinite;
            ">CONSULTA NF</h1>
            <p style="
                margin: 12px 0 0 0;
                font-size: 12px;
                letter-spacing: 0.08em;
                color: var(--text-secondary);
                text-transform: uppercase;
                animation: fadeInSlide 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.2s backwards;
            ">Extração de Notas Fiscais</p>
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
# SEÇÃO DE UPLOAD - SIDEBAR COM GLASSMORPHISM
# ============================================================================

st.sidebar.markdown("""
    <div style="
        padding: 20px 0;
        animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.05s backwards;
    ">
        <h2 style="
            text-align: center;
            margin: 0;
            font-size: 14px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-white);
        "> Painel de Controle</h2>
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
    <div style="
        padding: 15px 0;
        animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.15s backwards;
    ">
        <p style="
            margin: 0 0 12px 0;
            font-size: 11px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--text-secondary);
            font-weight: 500;
        ">Suporta</p>
        <p style="
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.8;
            margin: 0;
        ">
            Arquivos PDF • Até 200 MB • Processamento em lote<br>
            <br>
            <span style="color: var(--accent);">•</span> Número da NF<br>
            <span style="color: var(--accent);">•</span> Data de emissão<br>
            <span style="color: var(--accent);">•</span> Códigos de produtos<br>
            <span style="color: var(--accent);">•</span> Código do parceiro
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

    # UX: loader ultra-fino discreto com animação elástica
    with st.spinner("🔄 Processando arquivos..."):
        for idx, file in enumerate(uploaded_files):
            dados = extrair_dados_nf(file)
            dados['Arquivo'] = file.name
            lista_resultados.append(dados)
            progress_bar.progress((idx + 1) / total_files)

    # Criar DataFrame (ordenado em colunas desejadas)
    df = pd.DataFrame(lista_resultados)
    df = df[['Arquivo', 'NF', 'Data de emissão', 'Código do produto', 'Código do parceiro']]

    # Exibir em abas minimalistas com feedback cinemático
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs([" VISÃO GERAL", " ESTATÍSTICAS", " EXPORTAR"])

    # Aba 1: Dados com animação
    with tab1:
        st.markdown(f"""
            <div style="animation: scaleInBouncy 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;">
                <p style="font-size: 14px; color: var(--text-white); font-weight: 500;">
                    <span style="color: var(--accent);">✓</span> <strong>{total_files} arquivo(s) processado(s)</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    # Aba 2: Estatísticas com cascata
    with tab2:
        cols = st.columns(4)
        with cols[0]:
            with st.container():
                st.metric("ARQUIVOS", len(df), delta=None)
        with cols[1]:
            with st.container():
                nfs_validas = len(df[df['NF'] != 'N/A'])
                st.metric("NFS", nfs_validas, delta=None)
        with cols[2]:
            with st.container():
                produtos_total = sum(len(str(p).split('\n')) for p in df['Código do produto'] if p != 'N/A')
                st.metric("PRODUTOS", produtos_total, delta=None)
        with cols[3]:
            with st.container():
                parceiros = len(df[df['Código do parceiro'] != 'N/A'])
                st.metric("PARCEIROS", parceiros, delta=None)

    # Aba 3: Exportação com feedback de clique
    with tab3:
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
                'bg_color': '#141416',
                'font_color': '#f4f4f5',
                'bold': True,
                'border': 1,
                'border_color': '#222226'
            })
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

        with col_export1:
            st.download_button(
                label=" TXT",
                data=texto_txt,
                file_name='dados_extraidos.txt',
                mime='text/plain',
                use_container_width=True
            )

        with col_export2:
            st.download_button(
                label=" CSV",
                data=csv,
                file_name='dados_extraidos.csv',
                mime='text/csv',
                use_container_width=True
            )

        with col_export3:
            st.download_button(
                label=" EXCEL",
                data=buffer.getvalue(),
                file_name='dados_extraidos.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

else:
    # Interface quando nenhum arquivo é carregado com animação
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
             Como Usar:
            
            1. Acesse o painel lateral
            2. Selecione seus arquivos PDF
            3. O sistema processa automaticamente
            4. Exporte em TXT, CSV ou Excel
        """)
        
        st.success("""
             Dica: Você pode fazer upload de múltiplos PDFs simultaneamente.
        """)

# ============================================================================
# FOOTER MINIMALISTA COM ANIMAÇÃO
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="
        text-align: center;
        padding: 20px 0;
        animation: fadeInSlide 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    ">
        <p style="
            margin: 0;
            font-size: 11px;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        ">
            Make Distribuidora • ConsultaNF • 2.0 
        </p>
    </div>
""", unsafe_allow_html=True)
