import streamlit as st
import pandas as pd
import io
import re

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Make Distribuidora - ConsultaNF", layout="wide")

# Tentar importar pdfplumber
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pdfplumber = None
    PDFPLUMBER_AVAILABLE = False

st.title("📦 Sistema de Consulta e Extração de NF")
st.markdown(f"**Projeto Facilita Make:** `ConsultaNF`")

if not PDFPLUMBER_AVAILABLE:
    st.warning("⚠️ pdfplumber não está instalado. A extração de PDF ficará indisponível até a dependência ser instalada.")

# --- FUNÇÃO DE EXTRAÇÃO REAL DE DADOS DO PDF ---
def extrair_dados_nf(pdf_file):
    """
    Extrai dados reais da DANFE (Documento Auxiliar de Nota Fiscal Eletrônica):
    1. Número da NF
    2. Data de emissão
    3. Código do produto (primeira linha de DADOS DOS PRODUTOS/SERVIÇOS)
    4. Código do parceiro/cliente
    """
    try:
        if not PDFPLUMBER_AVAILABLE:
            return {
                "NF": "Erro",
                "Data de emissão": "pdfplumber não instalado",
                "Código do produto": "Erro",
                "Código do parceiro": "Erro"
            }
        
        def limpar_texto(valor):
            return re.sub(r'\s+', ' ', (valor or '')).strip()

        with pdfplumber.open(pdf_file) as pdf:
            texto_completo = ""
            linhas = []

            for page in pdf.pages:
                pagina_texto = page.extract_text() or ""
                texto_completo += pagina_texto + "\n"
                linhas.extend([linha.strip() for linha in pagina_texto.splitlines() if linha.strip()])

            def extrair_nf(texto, linhas_pdf):
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
                itens = []

                def adicionar_item(codigo, descricao):
                    codigo = limpar_texto(codigo)
                    descricao = limpar_texto(descricao)
                    if codigo and re.fullmatch(r'\d{3,}', codigo):
                        if not any(item[0] == codigo and item[1] == descricao for item in itens):
                            itens.append((codigo, descricao))

                for page in pdf_obj.pages:
                    for tabela in (page.extract_tables() or []):
                        for linha in tabela:
                            if not linha:
                                continue

                            valores = [limpar_texto(celula) for celula in linha if limpar_texto(celula)]
                            if not valores:
                                continue

                            cabecalho = " ".join(valores).upper()
                            if 'CÓD. PROD' in cabecalho or 'COD. PROD' in cabecalho or 'DESCRIÇÃO DOS PRODUTOS' in cabecalho:
                                continue

                            codigo = None
                            descricao = None

                            for indice, celula in enumerate(valores):
                                if re.fullmatch(r'\d{3,}', celula):
                                    codigo = celula
                                    if indice + 1 < len(valores):
                                        descricao = valores[indice + 1]
                                    break

                            if codigo:
                                adicionar_item(codigo, descricao or "")

                if not itens:
                    bloco_itens = re.search(r'DADOS\s+DOS\s+PRODUTOS(?:.|\n){0,7000}', texto_completo, re.IGNORECASE)
                    if bloco_itens:
                        trecho = bloco_itens.group(0)
                        padrao_item = re.compile(r'(?m)^\s*(\d{3,})\s+(.+?)\s*$', re.IGNORECASE)
                        for match in padrao_item.finditer(trecho):
                            descricao = match.group(2)
                            if re.search(r'\b(UN|PC|KG|CX|FR|LT|CXA|MT|M2|M3)\b', descricao, re.IGNORECASE):
                                adicionar_item(match.group(1), descricao)

                codigos = [codigo for codigo, _ in itens]
                return codigos

            def extrair_codigo_parceiro(texto, linhas_pdf):
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

# --- ÁREA DE UPLOAD ---
with st.sidebar:
    st.header("Upload de Arquivos")
    uploaded_files = st.file_uploader(
        "Arraste os PDFs das DANFEs aqui", 
        type="pdf", 
        accept_multiple_files=True
    )

if uploaded_files:
    lista_resultados = []
    
    with st.spinner('Processando notas fiscais...'):
        for file in uploaded_files:
            dados = extrair_dados_nf(file)
            dados['Arquivo'] = file.name
            lista_resultados.append(dados)
    
    df = pd.DataFrame(lista_resultados)
    # Reorganiza para as colunas do seu prompt 
    df = df[['Arquivo', 'NF', 'Data de emissão', 'Código do produto', 'Código do parceiro']]

    # Exibição na tela
    st.subheader("📋 Resultados da Extração")
    st.table(df) # Mostra uma tabela limpa

    # --- SEÇÃO DE EXPORTAÇÃO ---
    st.divider()
    st.subheader("📥 Escolha o formato de exportação")
    
    col1, col2, col3 = st.columns(3)

    # 1. EXPORTAR TXT (Padrão do Prompt-book)
    texto_txt = ""
    for _, row in df.iterrows():
        texto_txt += f"NF → {row['NF']}\n"
        texto_txt += f"Data de emissão → {row['Data de emissão']}\n"
        texto_txt += f"Código do produto → {row['Código do produto']}\n"
        texto_txt += f"Código do parceiro → {row['Código do parceiro']}\n"
        texto_txt += "-"*30 + "\n"

    col1.download_button(
        label="Download TXT",
        data=texto_txt,
        file_name='dados_extraidos.txt',
        mime='text/plain'
    )

    # 2. EXPORTAR CSV
    csv = df.to_csv(index=False).encode('utf-8')
    col2.download_button(
        label="Download CSV",
        data=csv,
        file_name='dados_extraidos.csv',
        mime='text/csv'
    )

    # 3. EXPORTAR EXCEL
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='NFs')
    
    col3.download_button(
        label="Download Excel",
        data=buffer.getvalue(),
        file_name='dados_extraidos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

else:
    st.info("Por favor, faça o upload de um ou mais arquivos PDF para começar.")