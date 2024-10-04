import os
import instaloader
import tkinter as tk
from tkinter import messagebox
import shutil

def baixar_videos(usuario, senha, perfil):
    # Cria uma instância do Instaloader
    loader = instaloader.Instaloader()

    # Realiza login
    try:
        loader.login(usuario, senha)
    except instaloader.exceptions.BadCredentialsException:
        messagebox.showerror("Erro", "Credenciais inválidas. Verifique seu login e senha.")
        return
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        messagebox.showerror("Erro", "A autenticação em duas etapas está habilitada. Por favor, forneça o código.")
        return
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")
        return

    # Define o nome da pasta para salvar os vídeos em Downloads
    pasta_videos = os.path.join(os.path.expanduser("~"), "Downloads", f"videos_{perfil}")

    # Remove a pasta se ela já existir
    if os.path.exists(pasta_videos):
        try:
            shutil.rmtree(pasta_videos)  # Remove a pasta inteira
        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao remover pasta existente: {str(e)}")

    # Cria a nova pasta
    os.makedirs(pasta_videos, exist_ok=True)

    try:
        # Carrega o perfil
        profile = instaloader.Profile.from_username(loader.context, perfil)

        # Baixa apenas os vídeos MP4
        for post in profile.get_posts():
            if post.is_video:  # Verifica se o post é um vídeo
                # Faz o download do post apenas se for um vídeo
                loader.download_post(post, target=pasta_videos)

                # Verifica os arquivos na pasta após o download
                for filename in os.listdir(pasta_videos):
                    # Constrói o caminho completo do arquivo
                    file_path = os.path.join(pasta_videos, filename)
                    # Verifica se o arquivo não é um vídeo .mp4
                    if not filename.endswith(".mp4"):
                        os.remove(file_path)  # Remove arquivos que não são MP4

        # Exibir sucesso
        messagebox.showinfo("Sucesso", f"Vídeos do perfil '{perfil}' baixados na pasta '{pasta_videos}'!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar vídeos: {str(e)}")

def realizar_download():
    perfil = entry_perfil.get().strip()
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    
    if perfil and usuario and senha:
        baixar_videos(usuario, senha, perfil)
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")

# Interface Tkinter
root = tk.Tk()
root.title("Baixar Vídeos do Instagram")
root.configure(bg='black')  # Fundo preto

# Criando campos de entrada
tk.Label(root, text="Nome do Usuário:", bg='black', fg='white').pack(pady=10)
entry_usuario = tk.Entry(root, bg='grey', fg='white')
entry_usuario.pack(pady=5)

tk.Label(root, text="Senha:", bg='black', fg='white').pack(pady=10)
entry_senha = tk.Entry(root, show="*", bg='grey', fg='white')
entry_senha.pack(pady=5)

tk.Label(root, text="Nome do Perfil:", bg='black', fg='white').pack(pady=10)
entry_perfil = tk.Entry(root, bg='grey', fg='white')
entry_perfil.pack(pady=5)

# Botão para baixar
btn_baixar = tk.Button(root, text="Baixar Vídeos", command=realizar_download, bg='#444', fg='white')
btn_baixar.pack(pady=20)

root.mainloop()
