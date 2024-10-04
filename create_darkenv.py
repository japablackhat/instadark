import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def salvar_env():
    login = entry_login.get()
    senha = entry_senha.get()
    legenda = entry_legenda.get()
    logomarca = entry_logomarca.get()
    
    # Cria ou sobrescreve o arquivo .env com codificação UTF-8
    with open('.env', 'w', encoding='utf-8') as env_file:
        env_file.write(f"LOGIN={login}\n")
        env_file.write(f"SENHA={senha}\n")
        env_file.write(f"LEGENDA={legenda}\n")
        env_file.write(f"LOGOMARCA={logomarca}\n")
    
    messagebox.showinfo("Sucesso", "As informações foram salvas no .env com sucesso!")

def selecionar_logomarca():
    caminho = filedialog.askopenfilename(title="Selecione a Logomarca", filetypes=[("Arquivos PNG", "*.png"), ("Todos os Arquivos", "*.*")])
    entry_logomarca.delete(0, tk.END)  # Limpa a entrada
    entry_logomarca.insert(0, caminho)  # Insere o caminho selecionado

# Interface Tkinter
root = tk.Tk()
root.title("Configuração do .env")
root.configure(bg='black')  # Fundo preto

# Estilo
label_color = 'white'
entry_color = 'grey'
button_color = '#444'  # Cor dos botões

# Criando campos de entrada
tk.Label(root, text="Login:", bg='black', fg=label_color).grid(row=0, column=0, padx=5, pady=5)
entry_login = tk.Entry(root, bg=entry_color, fg='white')
entry_login.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Senha:", bg='black', fg=label_color).grid(row=1, column=0, padx=5, pady=5)
entry_senha = tk.Entry(root, show="*", bg=entry_color, fg='white')
entry_senha.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Legenda do Vídeo:", bg='black', fg=label_color).grid(row=2, column=0, padx=5, pady=5)
entry_legenda = tk.Entry(root, bg=entry_color, fg='white')
entry_legenda.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Logomarca Padrão:", bg='black', fg=label_color).grid(row=3, column=0, padx=5, pady=5)
entry_logomarca = tk.Entry(root, bg=entry_color, fg='white')
entry_logomarca.grid(row=3, column=1, padx=5, pady=5)

# Botão para selecionar logomarca
btn_selecionar_logomarca = tk.Button(root, text="Selecionar Logomarca", command=selecionar_logomarca, bg=button_color, fg='white')
btn_selecionar_logomarca.grid(row=3, column=2, padx=5, pady=5)

# Botão para salvar
btn_salvar = tk.Button(root, text="Salvar .env", command=salvar_env, bg=button_color, fg='white')
btn_salvar.grid(row=4, columnspan=3, pady=10)

root.mainloop()
