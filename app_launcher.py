import webbrowser
import tkinter as tk
from tkinter import messagebox
import sys

# Configuração do aplicativo
APP_NAME = "ConsultaNF - Make Distribuidora"
APP_URL = "https://seu-nome-streamlit.streamlit.app"  # TROQUE PELO LINK FINAL DO STREAMLIT CLOUD
APP_ICON = "📦"

def abrir_aplicacao():
    """Abre a aplicação no navegador padrão"""
    try:
        messagebox.showinfo(APP_NAME, f"Abrindo a aplicação online...\n\n{APP_URL}")
        webbrowser.open(APP_URL)
        janela.quit()
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir a aplicação:\n{str(e)}")

def copiar_link():
    """Copia o link para a área de transferência"""
    janela.clipboard_clear()
    janela.clipboard_append(APP_URL)
    messagebox.showinfo(APP_NAME, "Link copiado para a área de transferência!")

# Criar interface gráfica
janela = tk.Tk()
janela.title(APP_NAME)
janela.geometry("400x250")
janela.resizable(False, False)

# Centralizar janela
janela.update_idletasks()
x = (janela.winfo_screenwidth() // 2) - (janela.winfo_width() // 2)
y = (janela.winfo_screenheight() // 2) - (janela.winfo_height() // 2)
janela.geometry(f"+{x}+{y}")

# Título
titulo = tk.Label(janela, text=f"{APP_ICON} {APP_NAME}", font=("Arial", 16, "bold"))
titulo.pack(pady=20)

# Descrição
descricao = tk.Label(janela, text="Sistema de Consulta e Extração de NF\nMake Distribuidora", 
                     font=("Arial", 10), justify=tk.CENTER)
descricao.pack(pady=10)

# Link
link_label = tk.Label(janela, text=APP_URL, font=("Arial", 9), fg="blue", cursor="hand2")
link_label.pack(pady=10)

# Botão principal
botao_abrir = tk.Button(janela, text="🌐 Abrir Aplicação", command=abrir_aplicacao, 
                        bg="#1f77b4", fg="white", font=("Arial", 12, "bold"), 
                        padx=20, pady=10, width=25)
botao_abrir.pack(pady=15)

# Botão copiar link
botao_copiar = tk.Button(janela, text="📋 Copiar Link", command=copiar_link,
                         bg="#444", fg="white", font=("Arial", 10), 
                         padx=15, pady=5, width=25)
botao_copiar.pack(pady=5)

# Rodapé
rodape = tk.Label(janela, text="Acesso 24h disponível", font=("Arial", 8), fg="gray")
rodape.pack(pady=10)

janela.mainloop()
