import customtkinter as ctk
import autoclip as ac
import threading
import yt_dlp
from tkinter import messagebox
from tiktok_downloader import snaptik
import os
from datetime import datetime
from tkinter.filedialog import askdirectory, askopenfilename
from moviepy import VideoFileClip, clips_array
import edge_tts
import asyncio
import pdfplumber
from tkinter import filedialog
from docx import Document

# Configuração da janela principal
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")  # Tema azul

janela = ctk.CTk()
janela.title('CRIAÇÃO DE CLIP')
janela.geometry("400x670")
janela.configure(bg='white')

tabview = ctk.CTkTabview(janela)
tabview.pack(padx=20, pady=20, fill="both", expand=True)

# Adicionando abas
tabview.add("MIX CLIP")
tabview.add("BAIX CLIP")
tabview.add("TESTIN AUDI")
tabview.add("TEXT AUDI")

def clipmix():
    quadro_menu = ctk.CTkFrame(tabview.tab("MIX CLIP"))
    quadro_menu.pack()
    opicoes = ctk.CTkLabel(quadro_menu, text=(
        '1 - CORTAR OS VIDEOS\n'
        '2 - RENOMEAR VIDEOS\n'
        '3 - CONTAR VIDEOS\n'
        '4 - APAGAR VIDEOS\n'
        '5 - JUNTAR OS VIDEOS'
    ), font=("Arial", 17))
    opicoes.pack(pady=10)

    win = ctk.CTkFrame(tabview.tab("MIX CLIP"), fg_color="transparent")
    win.pack()

    def limpar_interface():
        for widget in win.winfo_children():
            widget.pack_forget()

    def mostrar_mensagem(texto, cor="green"):
        mensagem = ctk.CTkLabel(win, text=texto, text_color=cor)
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
    
    def btn_click(opcao):
        limpar_interface()
        estilo = {"width": 300, "height": 30}

        if opcao == 1:  # Cortar Vídeos
            ctk.CTkLabel(win, text="Cortar Vídeo:").pack(pady=(10, 5))
            caminho = ctk.CTkEntry(win, placeholder_text="Caminho do vídeo", **estilo)
            caminho.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Vídeo", command=lambda: selecionar_video(caminho)).pack(pady=5)
            pasta_saida = ctk.CTkEntry(win, placeholder_text="Pasta para salvar", **estilo)
            pasta_saida.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: selecionar_pasta(pasta_saida)).pack(pady=5)
            intervalo = ctk.CTkEntry(win, placeholder_text="Intervalo (segundos)", **estilo)
            intervalo.pack(pady=5)
            def cortar_video():
                try:
                    mostrar_mensagem("Cortando vídeo...")
                    ac.cut_clip(caminho.get(), pasta_saida.get(), int(intervalo.get()))
                    mostrar_mensagem("Corte concluído!")
                except Exception as e:
                    mostrar_mensagem(f"Erro: {e}", "red")

            ctk.CTkButton(win, text="Cortar", command=lambda: threading.Thread(target=cortar_video).start()).pack(pady=10)

        elif opcao == 2:  # Renomear Vídeos
            ctk.CTkLabel(win, text="Renomear Vídeos:").pack(pady=(10, 5))
            caminho = ctk.CTkEntry(win, placeholder_text="Caminho da pasta", **estilo)
            caminho.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: selecionar_pasta(caminho)).pack(pady=5)
            novo_nome = ctk.CTkEntry(win, placeholder_text="Novo nome base", **estilo)
            novo_nome.pack(pady=5)

            def renomear_videos():
                try:
                    renomeados = ac.rename_clip(caminho.get(), novo_nome.get())
                    mostrar_mensagem(f"Renomeados: {renomeados} vídeos.")
                except Exception as e:
                    mostrar_mensagem(f"Erro: {e}", "red")

            ctk.CTkButton(win, text="Renomear", command=lambda: threading.Thread(target=renomear_videos).start()).pack(pady=10)

        elif opcao == 3:  # Contar Vídeos
            ctk.CTkLabel(win, text="Contar Vídeos:").pack(pady=(10, 5))
            caminho = ctk.CTkEntry(win, placeholder_text="Caminho da pasta", **estilo)
            caminho.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: selecionar_pasta(caminho)).pack(pady=5)

            def contar_videos():
                try:
                    contagem = ac.count_videos(caminho.get())
                    mostrar_mensagem(f"Número de vídeos: {contagem}")
                except Exception as e:
                    mostrar_mensagem(f"Erro: {e}", "red")

            ctk.CTkButton(win, text="Contar", command=lambda: threading.Thread(target=contar_videos).start()).pack(pady=10)

        elif opcao == 4:  # Apagar Vídeos
            ctk.CTkLabel(win, text="Apagar Vídeos:").pack(pady=(10, 5))
            caminho = ctk.CTkEntry(win, placeholder_text="Caminho da pasta", **estilo)
            caminho.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: selecionar_pasta(caminho)).pack(pady=5)
            numero = ctk.CTkEntry(win, placeholder_text="Quantidade", **estilo)
            numero.pack(pady=5)

            def apagar_videos():
                try:
                    ac.delete_file(caminho.get(), int(numero.get()))
                    mostrar_mensagem("Vídeos apagados com sucesso!")
                except Exception as e:
                    mostrar_mensagem(f"Erro: {e}", "red")

            ctk.CTkButton(win, text="Apagar", command=lambda: threading.Thread(target=apagar_videos).start()).pack(pady=10)

        elif opcao == 5:  # Juntar Vídeos
                    
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
                
                # Widgets de seleção de pastas
                # Widgets de seleção de pastas
            label_pasta1 = ctk.CTkLabel(win, text="Pasta 1:", **estilo)
            label_pasta1.pack(pady=3)

            entrada_pasta1 = ctk.CTkEntry(win, placeholder_text='pasta ccom o video que vai em cima', **estilo)
            entrada_pasta1.pack(pady=3)

            botao_pasta1 = ctk.CTkButton(win, text="Selecionar Pasta 1", command=lambda: selecionar_diretorio(entrada_pasta1))
            botao_pasta1.pack(pady=3)

            label_pasta2 = ctk.CTkLabel(win, text="Pasta 2:")
            label_pasta2.pack(pady=3)

            entrada_pasta2 = ctk.CTkEntry(win, placeholder_text='pasta ccom o video que vai em baixo', **estilo)
            entrada_pasta2.pack(pady=3)

            botao_pasta2 = ctk.CTkButton(win, text="Selecionar Pasta 2", command=lambda: selecionar_diretorio(entrada_pasta2))
            botao_pasta2.pack(pady=3)

            # Widgets para selecionar diretório de saída
            label_saida = ctk.CTkLabel(win, text="Diretório de saída:")
            label_saida.pack(pady=3)

            entrada_saida = ctk.CTkEntry(win,placeholder_text='pasta ccom o video que vai em cima',  **estilo)
            entrada_saida.pack(pady=3)

            botao_saida = ctk.CTkButton(win, text="Selecionar Diretório", command=lambda: selecionar_diretorio(entrada_saida))
            botao_saida.pack(pady=3)
            # Botão para combinar vídeos
            botao_combinar = ctk.CTkButton(win, text="Combinar Vídeos", command=combinar_videos)
            botao_combinar.pack(pady=3)

            # Label para exibir o resultado
            resultado_label = ctk.CTkLabel(win, text="")
            resultado_label.pack(pady=3)
    
        
    # Criando os botões e associando as funções
    botao_estilo = {"width": 20, "height": 30, "font": ("Arial", 14)}

    quadro_botoes1 = ctk.CTkFrame(quadro_menu, fg_color="transparent")
    quadro_botoes1.pack(pady=5)

    op1 = ctk.CTkButton(quadro_botoes1, text='1 - CORTAR', command=lambda: btn_click(1), **botao_estilo)
    op1.pack(side="left", padx=10)
    op2 = ctk.CTkButton(quadro_botoes1, text='2 - RENOMEAR', command=lambda: btn_click(2), **botao_estilo)
    op2.pack(side="left", padx=10)

    quadro_botoes2 = ctk.CTkFrame(quadro_menu, fg_color="transparent")
    quadro_botoes2.pack(pady=5)

    op3 = ctk.CTkButton(quadro_botoes2, text='3 - CONTAR', command=lambda: btn_click(3), **botao_estilo)
    op3.pack(side="left", padx=10)
    op4 = ctk.CTkButton(quadro_botoes2, text='4 - APAGAR', command=lambda: btn_click(4), **botao_estilo)
    op4.pack(side="left", padx=10)

    quadro_botoes3 = ctk.CTkFrame(quadro_menu, fg_color="transparent")
    quadro_botoes3.pack(pady=5)

    op5 = ctk.CTkButton(quadro_botoes3, text='5 - JUNTAR', command=lambda: btn_click(5), **botao_estilo)
    op5.pack(side="left", padx=10)

clipmix()

    # Funções para baixar vídeos
def baixar_video_youtube():
        url = entry_url_youtube.get()
        caminho_destino = entry_destino_youtube.get()

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
def baixar_video_instagram():
        url = entry_url_instagram.get()
        caminho_destino = entry_destino_instagram.get()

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
def baixar_video_tiktok():
        url = entry_url_tiktok.get()
        pasta_destino = entry_destino_tiktok.get()
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
    
     


    # Função para criar a interface de download do YouTube
def criar_interface_youtube():
        global entry_url_youtube, entry_destino_youtube
        root_youtube = ctk.CTk()
        root_youtube.geometry("400x400")

        label_titulo = ctk.CTkLabel(root_youtube, text="Baixar Vídeo do YouTube", font=("Arial", 18))
        label_titulo.pack(pady=10)

        label_url_youtube = ctk.CTkLabel(root_youtube, text="URL do Vídeo:")
        label_url_youtube.pack(pady=5)
        entry_url_youtube = ctk.CTkEntry(root_youtube, placeholder_text="Insira a URL do vídeo", width=300, height=30)
        entry_url_youtube.pack(pady=5)

        label_destino_youtube = ctk.CTkLabel(root_youtube, text="Caminho de destino:")
        label_destino_youtube.pack(pady=5)
        entry_destino_youtube = ctk.CTkEntry(root_youtube, placeholder_text="Caminho de destino", width=300, height=30)
        entry_destino_youtube.pack(pady=5)

        botao_download_youtube = ctk.CTkButton(root_youtube, text="Baixar YouTube", command=baixar_video_youtube)
        botao_download_youtube.pack(pady=20)

        root_youtube.mainloop()


    # Função para criar a interface de download do Instagram
def criar_interface_instagram():
        global entry_url_instagram, entry_destino_instagram
        root_instagram = ctk.CTk()
        root_instagram.geometry("400x400")

        label_titulo_instagram = ctk.CTkLabel(root_instagram, text="Baixar Vídeo do Instagram", font=("Arial", 18))
        label_titulo_instagram.pack(pady=10)

        label_url_instagram = ctk.CTkLabel(root_instagram, text="URL do Vídeo:")
        label_url_instagram.pack(pady=5)
        entry_url_instagram = ctk.CTkEntry(root_instagram, placeholder_text="Insira a URL do vídeo", width=300, height=30)
        entry_url_instagram.pack(pady=5)

        label_destino_instagram = ctk.CTkLabel(root_instagram, text="Caminho de destino:")
        label_destino_instagram.pack(pady=5)
        entry_destino_instagram = ctk.CTkEntry(root_instagram, placeholder_text="Caminho de destino", width=300, height=30)
        entry_destino_instagram.pack(pady=5)

        botao_download_instagram = ctk.CTkButton(root_instagram, text="Baixar Instagram", command=baixar_video_instagram)
        botao_download_instagram.pack(pady=20)

        root_instagram.mainloop()


    # Função para criar a interface de download do TikTok
def criar_interface_tiktok():
        global entry_url_tiktok, entry_destino_tiktok
        root_tiktok = ctk.CTk()
        root_tiktok.geometry("400x400")

        label_titulo_tiktok = ctk.CTkLabel(root_tiktok, text="Baixar Vídeo do TikTok", font=("Arial", 18))
        label_titulo_tiktok.pack(pady=10)

        label_url_tiktok = ctk.CTkLabel(root_tiktok, text="URL do Vídeo:")
        label_url_tiktok.pack(pady=5)
        entry_url_tiktok = ctk.CTkEntry(root_tiktok, placeholder_text="Insira a URL do vídeo", width=300, height=30)
        entry_url_tiktok.pack(pady=5)

        label_destino_tiktok = ctk.CTkLabel(root_tiktok, text="Caminho de destino:")
        label_destino_tiktok.pack(pady=5)
        entry_destino_tiktok = ctk.CTkEntry(root_tiktok, placeholder_text="Caminho de destino", width=300, height=30)
        entry_destino_tiktok.pack(pady=5)

        botao_download_tiktok = ctk.CTkButton(root_tiktok, text="Baixar TikTok", command=baixar_video_tiktok)
        botao_download_tiktok.pack(pady=20)

        root_tiktok.mainloop()


    # Função principal para a tela inicial com botões
def tela_inicial():
       
        root = ctk.CTkFrame(tabview.tab("BAIX CLIP"))
        root.pack()

        # Título
        label_titulo = ctk.CTkLabel(root, text="Escolha a plataforma", font=("Arial", 20))
        label_titulo.pack()
        label_titulo2 = ctk.CTkLabel(root, text="para baixar o vídeo", font=("Arial", 20))
        label_titulo2.pack()

        # Botões para abrir as interfaces
        botao_youtube = ctk.CTkButton(root, text="YouTube", command=criar_interface_youtube)
        botao_youtube.pack(pady=10)

        botao_instagram = ctk.CTkButton(root, text="Instagram", command=criar_interface_instagram)
        botao_instagram.pack(pady=10)

        botao_tiktok = ctk.CTkButton(root, text="TikTok", command=criar_interface_tiktok)
        botao_tiktok.pack(pady=10)

# Chamar a função principal para iniciar o aplicativo
tela_inicial()



# Conteúdo para a Aba 3
label3 = ctk.CTkLabel(tabview.tab("TESTIN AUDI"), text="Conteúdo da DEEP CLIP")
label3.pack(padx=20, pady=20)

# Conteúdo para a Aba 3
label3 = ctk.CTkLabel(tabview.tab("TEXT AUDI"), text="Conteúdo da TEXT AUDI")
label3.pack(padx=20, pady=20)

def text_into_audio():
    # Lista de vozes disponíveis
    VOZES = {
        'pt-BR': ['pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural', 'pt-BR-ValerioNeural'],
        'en-US': ['en-US-AriaNeural', 'en-US-GuyNeural', 'en-US-JennyNeural'],
        'es-ES': ['es-ES-AlvaroNeural', 'es-ES-ElviraNeural', 'es-ES-LuciaNeural'],
        'fr-FR': ['fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'fr-FR-CelesteNeural'],
        'de-DE': ['de-DE-KatjaNeural', 'de-DE-ConradNeural'],
        'it-IT': ['it-IT-ElsaNeural', 'it-IT-DanteNeural']
    }

    VOZ = ['pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural', 'pt-BR-ValerioNeural',
        'en-US-AriaNeural', 'en-US-GuyNeural', 'en-US-JennyNeural',
        'es-ES-AlvaroNeural', 'es-ES-ElviraNeural', 'es-ES-LuciaNeural',
        'fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'fr-FR-CelesteNeural',
        'de-DE-KatjaNeural', 'de-DE-ConradNeural',
        'it-IT-ElsaNeural', 'it-IT-DanteNeural']

    # Função para converter texto em áudio e salvar no formato escolhido
    async def texto_para_audio(texto, idioma, voz, formato="wav", arquivo_output="audio_gerado"):
        try:
            # Verificar se a voz escolhida existe no idioma
            if voz not in VOZES.get(idioma, []):
                raise ValueError(f"A voz '{voz}' não está disponível para o idioma {idioma}.")
            
            # Inicializar o cliente de TTS com a voz escolhida
            communicate = edge_tts.Communicate(texto, voice=voz)

            # Definir o caminho para o arquivo de saída com a extensão
            caminho_arquivo = f"{arquivo_output}.{formato}"
            
            # Gerar e salvar o áudio
            await communicate.save(caminho_arquivo)
            print(f"Áudio gerado com sucesso! Salvo como: {caminho_arquivo}")
        
        except Exception as e:
            print(f"Erro ao gerar áudio: {e}")

    # Função para o botão de conversão de texto para áudio
    async def gerar_audio():
        texto = texto_input.get()
        idioma = idioma_combobox.get()
        voz = voz_combobox.get()
        formato = formato_combobox.get()
        nome_arquivo = nome_arquivo_input.get()  # Nome do arquivo
        
        if nome_arquivo == "":
            nome_arquivo = "audio_gerado"  # Nome padrão se o campo estiver vazio
        
        if texto:
            await texto_para_audio(texto, idioma, voz, formato, nome_arquivo)
            resultado_label.configure(text=f"Áudio gerado com sucesso! Salvo como: {nome_arquivo}.{formato}")
        else:
            resultado_label.configure(text="Por favor, insira um texto.")




    # Campo para texto
    texto_input = ctk.CTkEntry(tabview.tab("TEXT AUDI"), width=500, height=40, placeholder_text="Digite o texto que deseja converter...")
    texto_input.pack(pady=10)

    # Combobox para idioma
    idioma_combobox = ctk.CTkComboBox(tabview.tab("TEXT AUDI"), values=list(VOZES.keys()), width=200)
    idioma_combobox.set('pt-BR')  # Valor padrão
    idioma_combobox.pack(pady=10)

    # Combobox para voz
    voz_combobox = ctk.CTkComboBox(tabview.tab("TEXT AUDI"), values=list(VOZ), width=200)
    voz_combobox.pack(pady=10)

    # Combobox para formato
    formato_combobox = ctk.CTkComboBox(tabview.tab("TEXT AUDI"), values=["wav", "mp3"], width=200)
    formato_combobox.set("wav")  # Valor padrão
    formato_combobox.pack(pady=10)

    # Campo para o nome do arquivo de áudio
    nome_arquivo_input = ctk.CTkEntry(tabview.tab("TEXT AUDI"), width=500, height=40, placeholder_text="Digite o nome do arquivo (sem a extensão)...")
    nome_arquivo_input.pack(pady=10)

    # Botão para gerar o áudio
    gerar_button = ctk.CTkButton(tabview.tab("TEXT AUDI"), text="Gerar Áudio", command=lambda: asyncio.run(gerar_audio()))
    gerar_button.pack(pady=20)

    # Label para mostrar resultado ou erro
    resultado_label = ctk.CTkLabel(tabview.tab("TEXT AUDI"), text="", width=400)
    resultado_label.pack(pady=10)

text_into_audio()
def texto_audio_file():
    # Lista de vozes disponíveis por idioma
    VOZES = {
        'pt-BR': ['pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural', 'pt-BR-ValerioNeural'],
        'en-US': ['en-US-AriaNeural', 'en-US-GuyNeural', 'en-US-JennyNeural'],
        'es-ES': ['es-ES-AlvaroNeural', 'es-ES-ElviraNeural', 'es-ES-LuciaNeural'],
        'fr-FR': ['fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'fr-FR-CelesteNeural'],
        'de-DE': ['de-DE-KatjaNeural', 'de-DE-ConradNeural'],
        'it-IT': ['it-IT-ElsaNeural', 'it-IT-DanteNeural']
    }

    VOZ = ['pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural', 'pt-BR-ValerioNeural',
        'en-US-AriaNeural', 'en-US-GuyNeural', 'en-US-JennyNeural',
        'es-ES-AlvaroNeural', 'es-ES-ElviraNeural', 'es-ES-LuciaNeural',
        'fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'fr-FR-CelesteNeural',
        'de-DE-KatjaNeural', 'de-DE-ConradNeural',
        'it-IT-ElsaNeural', 'it-IT-DanteNeural']

    # Função para extrair texto de um arquivo PDF
    def extrair_texto_pdf(caminho_pdf):
        texto_extraido = ""
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto_extraido += pagina.extract_text() or ""
        except Exception as e:
            print(f"Erro ao ler o PDF: {e}")
        return texto_extraido

    # Função para extrair texto de um arquivo Word (DOCX)
    def extrair_texto_docx(caminho_docx):
        texto_extraido = ""
        try:
            doc = Document(caminho_docx)
            for paragrafo in doc.paragraphs:
                texto_extraido += paragrafo.text + "\n"
        except Exception as e:
            print(f"Erro ao ler o arquivo DOCX: {e}")
        return texto_extraido

    # Função para extrair texto de arquivos de texto (.txt)
    def extrair_texto_txt(caminho_txt):
        texto_extraido = ""
        try:
            with open(caminho_txt, "r", encoding="utf-8") as file:
                texto_extraido = file.read()
        except Exception as e:
            print(f"Erro ao ler o arquivo TXT: {e}")
        return texto_extraido

    # Função para selecionar o arquivo de entrada
    def selecionar_arquivo():
        caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos PDF", "*.pdf"), ("Arquivos Word", "*.docx"), ("Arquivos Texto", "*.txt")])
        if caminho_arquivo:
            caminho_arquivo_input.delete(0, ctk.END)
            caminho_arquivo_input.insert(0, caminho_arquivo)

    # Função para converter texto em áudio e salvar no formato escolhido
    async def texto_para_audio(texto, idioma, voz, formato="wav", arquivo_output="audio_gerado"):
        try:
            # Verificar se a voz escolhida existe no idioma
            if voz not in VOZES.get(idioma, []):
                raise ValueError(f"A voz '{voz}' não está disponível para o idioma {idioma}.")
            
            # Inicializar o cliente de TTS com a voz escolhida
            communicate = edge_tts.Communicate(texto, voice=voz)

            # Definir o caminho para o arquivo de saída com a extensão
            caminho_arquivo = f"{arquivo_output}.{formato}"
            
            # Gerar e salvar o áudio
            await communicate.save(caminho_arquivo)
            print(f"Áudio gerado com sucesso! Salvo como: {caminho_arquivo}")
            return caminho_arquivo
        
        except Exception as e:
            print(f"Erro ao gerar áudio: {e}")
            return None

    # Função para o botão de conversão de texto para áudio
    async def gerar_audio():
        caminho_arquivo = caminho_arquivo_input.get()  # Caminho do arquivo
        idioma = idioma_combobox.get()
        voz = voz_combobox.get()
        formato = formato_combobox.get()
        nome_arquivo = nome_arquivo_input.get()  # Nome do arquivo
        
        if nome_arquivo == "":
            nome_arquivo = "audio_gerado"  # Nome padrão se o campo estiver vazio
        
        if caminho_arquivo:
            # Determinar a extensão do arquivo e extrair o texto
            extensao = os.path.splitext(caminho_arquivo)[1].lower()
            if extensao == ".pdf":
                texto = extrair_texto_pdf(caminho_arquivo)
            elif extensao == ".docx":
                texto = extrair_texto_docx(caminho_arquivo)
            elif extensao == ".txt":
                texto = extrair_texto_txt(caminho_arquivo)
            else:
                resultado_label.configure(text="Formato de arquivo não suportado.")
                return
            
            if texto:
                caminho_arquivo_audio = await texto_para_audio(texto, idioma, voz, formato, nome_arquivo)
                if caminho_arquivo_audio:
                    resultado_label.configure(text=f"Áudio gerado com sucesso! Salvo como: {caminho_arquivo_audio}")
                else:
                    resultado_label.configure(text="Erro ao gerar o áudio.")
            else:
                resultado_label.configure(text="Não foi possível extrair texto do arquivo.")
        else:
            resultado_label.configure(text="Por favor, insira o caminho do arquivo.")


    # Campo para o caminho do arquivo
    caminho_arquivo_label = ctk.CTkLabel(tabview.tab("TESTIN AUDI"), text="Caminho do arquivo:")
    caminho_arquivo_label.pack(pady=5)
    caminho_arquivo_input = ctk.CTkEntry(tabview.tab("TESTIN AUDI"), width=400, placeholder_text="Digite o caminho ou selecione o arquivo")
    caminho_arquivo_input.pack(pady=10)

    # Botão para selecionar o arquivo
    selecionar_button = ctk.CTkButton(tabview.tab("TESTIN AUDI"), text="Selecionar Arquivo", command=selecionar_arquivo)
    selecionar_button.pack(pady=10)

    # Combobox para idioma
    idioma_combobox = ctk.CTkComboBox(tabview.tab("TESTIN AUDI"), values=list(VOZES.keys()), width=200)
    idioma_combobox.set('pt-BR')  # Valor padrão
    idioma_combobox.pack(pady=10)

    # Combobox para voz
    voz_combobox = ctk.CTkComboBox(tabview.tab("TESTIN AUDI"), values=list(VOZ), width=200)
    voz_combobox.pack(pady=10)

    # Combobox para formato
    formato_combobox = ctk.CTkComboBox(tabview.tab("TESTIN AUDI"), values=["wav", "mp3"], width=200)
    formato_combobox.set("wav")  # Valor padrão
    formato_combobox.pack(pady=10)

    # Campo para o nome do arquivo de saída
    nome_arquivo_label = ctk.CTkLabel(tabview.tab("TESTIN AUDI"), text="Nome do arquivo de áudio:")
    nome_arquivo_label.pack(pady=5)
    nome_arquivo_input = ctk.CTkEntry(tabview.tab("TESTIN AUDI"), width=400, placeholder_text="Digite o nome do arquivo de áudio")
    nome_arquivo_input.pack(pady=10)

    # Botão para gerar o áudio
    gerar_button = ctk.CTkButton(tabview.tab("TESTIN AUDI"), text="Gerar Áudio", command=lambda: asyncio.run(gerar_audio()))
    gerar_button.pack(pady=20)

    # Label para exibir o resultado
    resultado_label = ctk.CTkLabel(tabview.tab("TESTIN AUDI"), text="", width=400)
    resultado_label.pack(pady=10)

texto_audio_file()
janela.mainloop()
