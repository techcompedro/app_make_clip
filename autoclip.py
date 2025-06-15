from PIL import Image
import moviepy as mp
import os
import customtkinter as ctk
import yt_dlp
from tkinter import messagebox, filedialog
from tiktok_downloader import snaptik
from tkinter.filedialog import askdirectory, askopenfilename
from moviepy import VideoFileClip, clips_array
import whisper
import warnings
from datetime import datetime
import customtkinter as ctk
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
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv','.pdf','.png']
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



def create_frame_with_video(image_path, video_path, output_path, video_size=(1280, 720)):
    # Abrir a imagem base
    base_image = Image.open(image_path).resize((video_size[1], video_size[0]))

    # Salvar a imagem redimensionada temporariamente
    temp_image_path = "temp_frame.png"
    base_image.save(temp_image_path)

    # Definir a área central onde o vídeo ficará (12% menor que a moldura)
    video_width = int(video_size[1] * 0.88)  # 88% da largura da moldura
    video_height = int(video_size[0] * 0.88)  # 88% da altura da moldura
    video_x = (video_size[1] - video_width) // 2
    video_y = (video_size[0] - video_height) // 2

    # Carregar e redimensionar o vídeo
    video = mp.VideoFileClip(video_path).resized((video_width, video_height))
    
    # Criar uma imagem de fundo com a moldura
    background = mp.ImageClip(temp_image_path).with_duration(video.duration)  # A duração será ajustada ao vídeo

    # Posicionar o vídeo sobre a moldura
    final_video = mp.CompositeVideoClip([
        background,  # Moldura de fundo
        video.with_position((video_x, video_y))  # Vídeo centralizado
    ])

    # Exportar o vídeo final com aceleração
    final_video.write_videofile(output_path, codec="libx264", fps=24)

    # Remover o arquivo temporário
    os.remove(temp_image_path)

def process_videos_in_folder(image_path, videos_folder, output_folder, video_size=(1280, 720)):
    # Criar a pasta de saída, se não existir
    os.makedirs(output_folder, exist_ok=True)

    # Iterar sobre todos os arquivos na pasta de vídeos
    for video_file in os.listdir(videos_folder):
        if video_file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_path = os.path.join(videos_folder, video_file)
            output_path = os.path.join(output_folder, f"framed_{video_file}")

            # Processar o vídeo com a moldura
            print(f"Processando: {video_file}")
            create_frame_with_video(image_path, video_path, output_path, video_size)


    # Funções para baixar vídeos



def baixar_video_youtube(url, caminho_destino):

        if not url or not caminho_destino:
            messagebox.showerror("Erro", "A URL ou o Caminho de Destino não podem estar vazios!")
            return

        try:
            ydl_opts = {
                'ffmpeg_location': r'C:\ffmpeg\bin\ffmpeg.exe',  # Caminho para o ffmpeg
                'outtmpl': f'{caminho_destino}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'postprocessors': [
                    {
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                messagebox.showinfo("Iniciado", f"Iniciando o download do vídeo: {url}")
                ydl.download([url])
                messagebox.showinfo("Concluído", "Download concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar o vídeo: {e}")

def baixar_video_instagram(url, caminho_destino):

        if not url or not caminho_destino:
            messagebox.showerror("Erro", "A URL ou o Caminho de Destino não podem estar vazios!")
            return

        try:
            ydl_opts = {
                'ffmpeg_location': r'C:\ffmpeg\bin\ffmpeg.exe',
                'outtmpl': f'{caminho_destino}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'postprocessors': [
                    {
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                messagebox.showinfo("Iniciado", f"Iniciando o download do vídeo: {url}")
                ydl.download([url])
                messagebox.showinfo("Concluído", "Download concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar o vídeo: {e}")

def baixar_video_tiktok(url, pasta_destino):

        if not url or not pasta_destino:
            messagebox.showerror("Erro", "A URL ou o Caminho de Destino não podem estar vazios!")
            return
        # Certifique-se de que a pasta existe
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        # Baixando o vídeo
        d = snaptik(url)
        messagebox.showinfo("Iniciado", f"Iniciando o download do vídeo: {url}")
        # Nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Formato: AAAAMMDD_HHMMSS
        nome_arquivo = f'video_{timestamp}.mp4'
        # Caminho completo para salvar o vídeo
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        d[0].download(caminho_completo)
        messagebox.showinfo("Concluído", f"Download concluído com sucesso! Vídeo salvo em: {caminho_completo}")



warnings.filterwarnings("ignore", category=UserWarning)  # Ignora avisos do tipo UserWarning
warnings.filterwarnings("ignore", category=FutureWarning)  # Ignora avisos de futuro
def transcribe_audio(input_file):
    try:
        # Carrega o modelo de transcrição do Whisper
        model = whisper.load_model("base")  # Escolha o modelo adequado ao seu hardware

        # Realiza a transcrição do áudio
        result = model.transcribe(input_file, language='pt')  # Define o idioma como português

        # Retorna o texto transcrito
        return result['text']
    except Exception as e:
        # Retorna uma mensagem de erro em caso de falha
        return f"Erro na transcrição: {e}"



def mostrar_mensagem(frame,texto, cor="green"):
    mensagem = ctk.CTkLabel(frame,text=texto, text_color=cor)
    mensagem.pack(pady=10)

def selecionar_video(entry_widget):
        arquivo_selecionado = askopenfilename(filetypes=[("Vídeos", "*.mp4;*.avi;*.mkv")])
        if arquivo_selecionado:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, arquivo_selecionado)

def selecionar_pasta(entry_widget):
        pasta_selecionada = askdirectory()
        if pasta_selecionada:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, pasta_selecionada)

def selecionar_img(entry_widget):
    arquivo_selecionado = askopenfilename(filetypes=[("Vídeos", "*.png;*")])
    if arquivo_selecionado:
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, arquivo_selecionado)

def selecionar_audio(entry_widget):
    arquivo_selecionado = askopenfilename(filetypes=[("Audios", "*.mp3;*")])
    if arquivo_selecionado:
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, arquivo_selecionado)

def selecionar_arquivo(entry_widget):
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos PDF", "*.pdf"), ("Arquivos Word", "*.docx"), ("Arquivos Texto", "*.txt")])
    if caminho_arquivo:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, caminho_arquivo)