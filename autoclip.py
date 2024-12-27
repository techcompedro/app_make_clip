import os
from moviepy import VideoFileClip, clips_array 
from datetime import datetime
from moviepy import VideoFileClip, clips_array
import customtkinter as ctk
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from moviepy import VideoFileClip, clips_array
import os
from datetime import datetime
def cut_clip(caminho_video, pasta_saida, intervalo):
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_video):
        raise FileNotFoundError(f"O arquivo de vídeo '{caminho_video}' não foi encontrado.")
    # Cria a pasta de saída, se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    try:
        # Carrega o vídeo
        video = VideoFileClip(caminho_video)
        duracao_total = video.duration  # Duração total do vídeo em segundos
        # Divide o vídeo em partes de tamanho especificado
        for i, inicio in enumerate(range(0, int(duracao_total), intervalo), start=1):
            fim = min(inicio + intervalo, duracao_total)  # Garante que o último clipe não exceda a duração total
            clipe = video.subclip(inicio, fim)
            # Nome do arquivo de saída com "parte X"
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Formato: AAAAMMDD_HHMMSS
            nome_arquivo = f'video_{timestamp}.mp4'
            nome_arquivo = os.path.join(pasta_saida, f"parte_{nome_arquivo}.mp4")
            # Salva o clipe se ele ainda não existir
            if not os.path.exists(nome_arquivo):
                clipe.write_videofile(nome_arquivo, codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"Erro ao processar o vídeo: {e}")
    finally:
        # Fecha o vídeo para liberar recursos
        if 'video' in locals():
            video.close()

def mix_clip():
    

    # Função para selecionar diretório
    def selecionar_diretorio(entry_widget):
        caminho = askdirectory()
        if caminho:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, caminho)

    # Função para combinar vídeos correspondentes
    def combinar_videos():
        pasta1_path = entrada_pasta1.get()
        pasta2_path = entrada_pasta2.get()
        output_dir = entrada_saida.get()

        try:
            # Listar vídeos em cada pasta, ordenados alfabeticamente
            videos_pasta1 = sorted([os.path.join(pasta1_path, f) for f in os.listdir(pasta1_path) if f.endswith('.mp4')])
            videos_pasta2 = sorted([os.path.join(pasta2_path, f) for f in os.listdir(pasta2_path) if f.endswith('.mp4')])

            # Verificar se há o mesmo número de vídeos em ambas as pastas
            if len(videos_pasta1) != len(videos_pasta2):
                resultado_label.configure(text="Erro: As pastas devem conter o mesmo número de vídeos.")
                return

            # Combinar vídeos correspondentes
            for i, (video1, video2) in enumerate(zip(videos_pasta1, videos_pasta2)):
                clip1 = VideoFileClip(video1)
                clip2 = VideoFileClip(video2)

                # Combinar os dois vídeos
                final_clip = clips_array([[clip1], 
                                        [clip2]])

                # Salvar o vídeo final
                output_path = os.path.join(output_dir, f"video_combinado_{i+1}.mp4")
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            resultado_label.configure(text="Todos os vídeos foram combinados com sucesso!")
        except FileNotFoundError as e:
            resultado_label.configure(text=f"Erro: Arquivo ou pasta não encontrado. Detalhes: {e}")
        except Exception as e:
            resultado_label.configure(text=f"Erro ao combinar vídeos. Detalhes: {e}")

        # Configuração da janela principal
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        janela = ctk.CTk()
        janela.title("Combinar Vídeos Correspondentes")
        janela.geometry("600x500")

        # Widgets de seleção de pastas
        label_pasta1 = ctk.CTkLabel(janela, text="Pasta 1:")
        label_pasta1.pack(pady=10)

        entrada_pasta1 = ctk.CTkEntry(janela, width=400)
        entrada_pasta1.pack(pady=5)

        botao_pasta1 = ctk.CTkButton(janela, text="Selecionar Pasta 1", command=lambda: selecionar_diretorio(entrada_pasta1))
        botao_pasta1.pack(pady=5)

        label_pasta2 = ctk.CTkLabel(janela, text="Pasta 2:")
        label_pasta2.pack(pady=10)

        entrada_pasta2 = ctk.CTkEntry(janela, width=400)
        entrada_pasta2.pack(pady=5)

        botao_pasta2 = ctk.CTkButton(janela, text="Selecionar Pasta 2", command=lambda: selecionar_diretorio(entrada_pasta2))
        botao_pasta2.pack(pady=5)

        # Widgets para selecionar diretório de saída
        label_saida = ctk.CTkLabel(janela, text="Diretório de saída:")
        label_saida.pack(pady=10)

        entrada_saida = ctk.CTkEntry(janela, width=400)
        entrada_saida.pack(pady=5)

        botao_saida = ctk.CTkButton(janela, text="Selecionar Diretório", command=lambda: selecionar_diretorio(entrada_saida))
        botao_saida.pack(pady=5)

        # Botão para combinar vídeos
        botao_combinar = ctk.CTkButton(janela, text="Combinar Vídeos", command=combinar_videos)
        botao_combinar.pack(pady=20)

        # Label para exibir o resultado
        resultado_label = ctk.CTkLabel(janela, text="")
        resultado_label.pack(pady=10)

        janela.mainloop()

def rename_clip(caminho, texto):
    try:
        # Obtém a lista de arquivos no diretório
        files = sorted(os.listdir(caminho))

        # Filtra apenas arquivos de vídeo
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv']
        videos = [f for f in files if os.path.splitext(f)[1].lower() in video_extensions]

        # Renomeia cada vídeo
        for index, video in enumerate(videos, start=1):
            # Gera o novo nome com base no índice
            new_name = f"{texto} {index}{os.path.splitext(video)[1]}"
            old_path = os.path.join(caminho, video)
            new_path = os.path.join(caminho, new_name)

            # Renomeia o arquivo
            os.rename(old_path, new_path)

        rename_videos=(f"{len(videos)}")
        return rename_videos
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def count_videos(directory):
    try:
        # Itera pelas subpastas
        for root, dirs, files in os.walk(directory):
            # Filtra apenas arquivos de vídeo
            video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv']
            videos = [f for f in files if os.path.splitext(f)[1].lower() in video_extensions]

            # Conta os vídeos na subpasta
            num_videos=(f"{len(videos)}")
            return num_videos

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def delete_file(directory, choice):
    try:
        # Lista todos os arquivos no diretório
        arquivos = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Ordena os arquivos por data de modificação em ordem decrescente
        arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        # Verifica se há arquivos suficientes para apagar
        if len(arquivos) < choice:
            choice = len(arquivos)

        # Apaga os arquivos especificados
        for i in range(choice):
            arquivo_a_apagar = os.path.join(directory, arquivos[i])
            os.remove(arquivo_a_apagar)

        num_videos_apagados = f"{choice}"
        return num_videos_apagados
    except Exception as e:
        print(f"Erro: {e}")


