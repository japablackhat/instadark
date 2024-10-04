import tkinter as tk
from tkinter import filedialog, messagebox
from instagrapi import Client
import os
import time
import threading
import random
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
USERNAME = os.getenv('LOGIN')
PASSWORD = os.getenv('SENHA')

LEGENDA_FIXA = """🚨 Não seguiu? Virou CLT!"""

def selecionar_pasta_videos():
    pasta = filedialog.askdirectory(title="Selecione a Pasta com os Vídeos")
    if pasta:
        entry_pasta_videos.delete(0, tk.END)
        entry_pasta_videos.insert(0, pasta)

def postar_videos_thread():
    # Função para postar os vídeos em um thread separado
    try:
        client = Client()
        client.login(USERNAME, PASSWORD)

        pasta_videos = entry_pasta_videos.get()
        delay_inicial = int(entry_delay_inicial.get())
        delay_final = int(entry_delay_final.get())

        # Verifica se a pasta de vídeos existe
        if not os.path.exists(pasta_videos):
            raise FileNotFoundError("A pasta selecionada não existe.")

        videos = [f for f in os.listdir(pasta_videos) if f.endswith('.mp4')]

        if not videos:
            raise FileNotFoundError("Nenhum vídeo encontrado na pasta selecionada.")

        for video in videos:
            video_path = os.path.join(pasta_videos, video)
            client.video_upload(video_path, caption=LEGENDA_FIXA)
            log.insert(tk.END, f"Vídeo {video} postado com sucesso!")
            log.yview(tk.END)

            # Delay entre postagens
            delay = random.randint(delay_inicial * 60, delay_final * 60)
            time.sleep(delay)

        messagebox.showinfo("Sucesso", "Todos os vídeos foram postados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        log.insert(tk.END, f"Erro: {str(e)}")
        log.yview(tk.END)

def postar_videos():
    # Inicia o processo de postagem em um thread separado
    threading.Thread(target=postar_videos_thread).start()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Postar Vídeos no Instagram")
root.geometry("600x500")
root.configure(bg='#2e2e2e')

# Título
tk.Label(root, text="Postar Vídeos no Instagram", font=("Helvetica", 16), bg='#2e2e2e', fg='white').pack(pady=10)

# Campo para selecionar a pasta de vídeos
frame_pasta_videos = tk.Frame(root, bg='#2e2e2e')
frame_pasta_videos.pack(pady=5)
tk.Label(frame_pasta_videos, text="Pasta com Vídeos:", bg='#2e2e2e', fg='white').pack(side=tk.LEFT)
entry_pasta_videos = tk.Entry(frame_pasta_videos, width=40)
entry_pasta_videos.pack(side=tk.LEFT, padx=5)
tk.Button(frame_pasta_videos, text="Selecionar Pasta", command=selecionar_pasta_videos, bg='#4caf50', fg='white').pack(side=tk.LEFT)

# Campos para o delay
frame_delay = tk.Frame(root, bg='#2e2e2e')
frame_delay.pack(pady=5)
tk.Label(frame_delay, text="Delay entre postagens (minutos):", bg='#2e2e2e', fg='white').pack(side=tk.LEFT)
entry_delay_inicial = tk.Entry(frame_delay, width=10)
entry_delay_inicial.pack(side=tk.LEFT, padx=5)
tk.Label(frame_delay, text="até", bg='#2e2e2e', fg='white').pack(side=tk.LEFT)
entry_delay_final = tk.Entry(frame_delay, width=10)
entry_delay_final.pack(side=tk.LEFT, padx=5)

# Botão para postar vídeos
tk.Button(root, text="Postar Vídeos", command=postar_videos, bg='#2196F3', fg='white').pack(pady=10)

# Log
log = tk.Listbox(root, width=70, height=15, bg='#333', fg='white')
log.pack(pady=5)

# Iniciar a interface gráfica
root.mainloop()
