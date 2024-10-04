import instaloader
import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

class InstagramReelDownloader:
    def __init__(self, username, password):
        self.loader = instaloader.Instaloader()  # Inicializa o Instaloader
        self.loader.login(username, password)  # Faz login usando nome de usuário e senha

    def download_reels_from_profile(self, profile_url, save_path):
        try:
            # Extrai o nome do perfil da URL
            profile_name = profile_url.split('/')[-2] if profile_url.endswith('/') else profile_url.split('/')[-1]
            profile = instaloader.Profile.from_username(self.loader.context, profile_name)

            # Cria uma pasta para o perfil
            profile_folder = os.path.join(save_path, profile_name)
            os.makedirs(profile_folder, exist_ok=True)

            downloaded_files = []
            for post in profile.get_posts():
                # Verifica se o post é um vídeo
                if post.is_video:
                    # Faz o download do post na pasta do perfil
                    self.loader.download_post(post, target=profile_folder)

                    # Filtra e renomeia os arquivos para garantir que sejam .mp4
                    for file in os.listdir(profile_folder):
                        if file.endswith('.mp4'):
                            downloaded_files.append(os.path.join(profile_folder, file))  # Adiciona o caminho completo

            if not downloaded_files:
                return "Nenhum vídeo .mp4 encontrado para baixar."
            
            return f"Vídeos .mp4 foram baixados para: {profile_folder}"
        except Exception as e:
            raise RuntimeError(f"Erro: {e}")

class InstagramReelDownloaderApp:
    def __init__(self, root, downloader):
        self.root = root
        self.downloader = downloader
        self.root.title("Instagram Reel Downloader")
        self.root.geometry("500x300")
        self.root.configure(bg="white")
        self.create_widgets()

    def create_widgets(self):
        margin = 15

        tk.Label(self.root, text="Digite a URL do perfil do Instagram:", bg="white").pack(pady=(margin, 5))
        self.url_entry = tk.Entry(self.root, width=60, font=('Arial', 12))
        self.url_entry.pack(pady=5, padx=margin)

        tk.Label(self.root, text="Selecione o diretório para salvar os vídeos:", bg="white").pack(pady=(margin, 5))
        self.save_path_entry = tk.Entry(self.root, width=60, font=('Arial', 12))
        self.save_path_entry.pack(pady=5, padx=margin)
        
        browse_button = tk.Button(self.root, text="Procurar", command=self.browse_directory, width=10)
        browse_button.pack(pady=(0, 10))

        download_button = tk.Button(self.root, text="Baixar", command=self.start_download, width=15)
        download_button.pack(pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, directory)

    def start_download(self):
        url = self.url_entry.get().strip()
        save_path = self.save_path_entry.get().strip()

        if not url or not save_path:
            messagebox.showerror("Erro de Entrada", "Por favor, forneça tanto a URL quanto o caminho de salvamento.")
            return

        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except Exception as e:
                messagebox.showerror("Erro de Diretório", f"Falha ao criar diretório: {e}")
                return

        # Executa o download em uma thread separada
        download_thread = threading.Thread(target=self.download_reels, args=(url, save_path))
        download_thread.start()

    def download_reels(self, url, save_path):
        try:
            result_message = self.downloader.download_reels_from_profile(url, save_path)
            messagebox.showinfo("Sucesso", result_message)
        except RuntimeError as e:
            messagebox.showerror("Erro de Download", str(e))

def main():
    # Solicita o nome de usuário e senha
    username = input("Digite seu nome de usuário do Instagram: ")
    password = input("Digite sua senha do Instagram: ")

    downloader = InstagramReelDownloader(username, password)

    root = tk.Tk()
    app = InstagramReelDownloaderApp(root, downloader)
    root.mainloop()

if __name__ == "__main__":
    main()
