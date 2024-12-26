import moviepy as m
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import yt_dlp
import customtkinter as ctk
from tkinter import messagebox


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
            clipe = video.subclipped(inicio, fim)

            # Nome do arquivo de saída com "parte X"
            nome_arquivo = os.path.join(pasta_saida, f"parte_{i}.mp4")

            # Salva o clipe se ele ainda não existir
            if not os.path.exists(nome_arquivo):
                clipe.write_videofile(nome_arquivo, codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"Erro ao processar o vídeo: {e}")

    finally:
        # Fecha o vídeo para liberar recursos
        if 'video' in locals():
            video.close()

def mix_clip (caminho_file, caminho_video_baixo):
    # Inicializa listas para armazenar os nomes dos arquivos
    arquivos = []
    quivos = []

# Itera sobre os itens da pasta caminho_file
    for item in os.listdir(caminho_file):
        caminho_completo = os.path.join(caminho_file, item)
            
        if os.path.isfile(caminho_completo):
            arquivos.append(item)

    # Itera sobre os itens da pasta caminho_video_baixo
    for item in os.listdir(caminho_video_baixo):
        caminho_complet = os.path.join(caminho_video_baixo, item)
            
        if os.path.isfile(caminho_complet):
            quivos.append(item)

        # Verifica se as listas possuem o mesmo número de arquivos
        if len(arquivos) != len(quivos):
            print("")
        else:
            # Processa cada par de vídeos
            for arquivo, ivos in zip(arquivos, quivos):
                video1 = arquivo
                video2 = ivos
                
                # Carrega os vídeos
                v1 = m.VideoFileClip(os.path.join(caminho_file, video1))
                v2 = m.VideoFileClip(os.path.join(caminho_video_baixo, video2))
                
                # Junta os vídeos
                video_junto = m.clips_array([[v1], [v2]])
                
                # Salva o vídeo final
                video_junto.write_videofile(f"teste_{video1}", codec="libx264")
                
                videos_junto = (f"{video1} e {video2}")
                return videos_junto

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


