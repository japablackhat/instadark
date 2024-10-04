import os
import tkinter as tk
from tkinter import messagebox, filedialog

def delete_non_mp4_files(directory):
    try:
        # Lista todos os arquivos no diretório
        for filename in os.listdir(directory):
            # Cria o caminho completo do arquivo
            file_path = os.path.join(directory, filename)
            # Verifica se não é um arquivo .mp4
            if not filename.endswith('.mp4'):
                os.remove(file_path)  # Remove o arquivo
        return "Todos os arquivos que não são .mp4 foram excluídos com sucesso."
    except Exception as e:
        return f"Erro ao excluir arquivos: {e}"

class NonMp4DeleterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deletar Arquivos Não .mp4")
        self.root.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Selecione a pasta para excluir arquivos que não são .mp4:").pack(pady=20)

        self.directory_entry = tk.Entry(self.root, width=50)
        self.directory_entry.pack(pady=5)

        browse_button = tk.Button(self.root, text="Procurar", command=self.browse_directory)
        browse_button.pack(pady=5)

        delete_button = tk.Button(self.root, text="Deletar", command=self.delete_non_mp4_files)
        delete_button.pack(pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)

    def delete_non_mp4_files(self):
        directory = self.directory_entry.get().strip()
        if not directory:
            messagebox.showerror("Erro de Entrada", "Por favor, selecione um diretório.")
            return

        confirmation = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir todos os arquivos que não são .mp4?")
        if confirmation:
            result_message = delete_non_mp4_files(directory)
            messagebox.showinfo("Resultado", result_message)

def main():
    root = tk.Tk()
    app = NonMp4DeleterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
