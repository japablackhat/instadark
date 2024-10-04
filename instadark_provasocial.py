import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from instagrapi import Client
import threading  # Importando o módulo threading

def selecionar_pasta_stories():
    pasta = filedialog.askdirectory(title="Selecione a Pasta com os Stories")
    if pasta:
        entry_pasta_stories.delete(0, tk.END)
        entry_pasta_stories.insert(0, pasta)

def selecionar_contas():
    contas_file = filedialog.askopenfilename(title="Selecione o arquivo contas.txt", filetypes=[("Text Files", "*.txt")])
    if contas_file:
        entry_contas.delete(0, tk.END)
        entry_contas.insert(0, contas_file)

def ler_contas(file_path):
    with open(file_path, 'r') as f:
        contas = f.readlines()
    return [conta.strip().split(':') for conta in contas if conta.strip()]

def postar_stories_thread():
    try:
        contas_file = entry_contas.get()
        contas = ler_contas(contas_file)

        # Login nas contas e postagem dos stories
        for username, password in contas:
            client = Client()
            client.login(username, password)
            print(f"Login bem-sucedido para: {username}")

            folder_path = entry_pasta_stories.get()
            story_ids = []

            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')):
                    try:
                        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            story = client.photo_upload_to_story(file_path, caption="Sua legenda aqui!")
                            story_ids.append(story.id)
                            print(f"Story de imagem postado: {filename}")
                        elif filename.endswith('.mp4'):
                            story = client.video_upload_to_story(file_path, caption="Sua legenda aqui!")
                            story_ids.append(story.id)
                            print(f"Story de vídeo postado: {filename}")

                        time.sleep(5)

                    except Exception as e:
                        print(f"Erro ao postar {filename}: {e}")

            if story_ids:
                highlight_title = "ref🎓"
                client.create_highlight(title=highlight_title, media_ids=story_ids)
                print(f"Destaque criado com sucesso: {highlight_title}")

        messagebox.showinfo("Sucesso", "Processo de postagem de stories concluído!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def postar_stories():
    threading.Thread(target=postar_stories_thread).start()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Postar Stories no Instagram")
root.geometry("600x400")

# Campo para selecionar a pasta de stories
tk.Label(root, text="Pasta com Stories:", bg='#2e2e2e', fg='white').pack(pady=5)
entry_pasta_stories = tk.Entry(root, width=40)
entry_pasta_stories.pack(pady=5)
tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta_stories, bg='#4caf50', fg='white').pack(pady=5)

# Campo para selecionar o arquivo de contas
tk.Label(root, text="Arquivo de Contas:", bg='#2e2e2e', fg='white').pack(pady=5)
entry_contas = tk.Entry(root, width=40)
entry_contas.pack(pady=5)
tk.Button(root, text="Selecionar Contas", command=selecionar_contas, bg='#4caf50', fg='white').pack(pady=5)

# Botão para postar stories
tk.Button(root, text="Postar Stories", command=postar_stories, bg='#2196F3', fg='white').pack(pady=10)

# Iniciar a interface gráfica
root.mainloop()
