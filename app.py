import customtkinter as ctk
import autoclip as ac
import threading
import yt_dlp
from tkinter import messagebox
from tiktok_downloader import snaptik
import os
from datetime import datetime
# Configuração da janela principal
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")  # Tema azul

janela = ctk.CTk()
janela.title('CRIAÇÃO DE CLIP')
janela.geometry("450x600")
janela.configure(bg='white')

tabview = ctk.CTkTabview(janela)
tabview.pack(padx=20, pady=20, fill="both", expand=True)

# Adicionando abas
tabview.add("MIXCLIP")
tabview.add("BAIXCLIPS")
tabview.add("Aba 3")

def clipmix():
    quadro_menu = ctk.CTkFrame(tabview.tab("MIXCLIP"))
    quadro_menu.pack()
    opicoes = ctk.CTkLabel(quadro_menu, text=('1 - CORTAR OS VIDEOS\n'
                                              '2 - RENOMEAR VIDEOS\n'
                                              '3 - CONTAR VIDEOS\n'
                                              '4 - APAGAR VIDEOS\n'
                                              '5 - JUNTAR OS VIDEOS'), font=("Arial", 17))
    opicoes.pack(pady=10)
    win = ctk.CTkFrame(tabview.tab("MIXCLIP"), fg_color="transparent")
    win.pack()

    def confirmar_juncao(caminho_file, caminho_video_baixo):
        try:
            m = ctk.CTkLabel(win, text='Juntando...', text_color="green")
            m.pack(pady=10)
            ac.juntar_videos(caminho_file, caminho_video_baixo)
            mensagem_sucesso = ctk.CTkLabel(win, text='Vídeos prontos!', text_color="green")
            mensagem_sucesso.pack(pady=10)
        except Exception as e:
            mensagem_erro = ctk.CTkLabel(win, text=f'Erro: {str(e)}', text_color="red")
            mensagem_erro.pack(pady=10)

    def apagar_msg(caminho, numero_videos):
        # Validar o caminho
        if not caminho:
            erro = ctk.CTkLabel(win, text="Erro: O caminho não pode estar vazio.")
            erro.pack(pady=(10, 5))
            return
        
        # Validar o número de vídeos
        try:
            numero_videos = int(numero_videos)
            if numero_videos < 1:
                erro = ctk.CTkLabel(win, text="Erro: O número de vídeos deve ser um inteiro positivo.")
                erro.pack(pady=(10, 5))
                return
        except ValueError:
            erro = ctk.CTkLabel(win, text='Erro: Por favor, insira um inteiro válido para o número de vídeos.')
            erro.pack(pady=(10, 5))
            return

        # Prosseguir com a exclusão se as validações passarem
        ac.delete_file(caminho, numero_videos)
        r = ctk.CTkLabel(win, text='Vídeos deletados com sucesso', text_color="green")
        r.pack(pady=10)

    def rename_new(caminho, texto_renomear):
        rename_videos = ac.rename_clip(caminho, texto_renomear)
        g = ctk.CTkLabel(win, text=f'Vídeos renomeados com sucesso: {rename_videos} vídeos', text_color="green")
        g.pack(pady=(10, 5))

    def mostrar_contagem(caminho):
        a = ac.count_videos(caminho)
        o = ctk.CTkLabel(win, text=f'Número de vídeos: {a}')
        o.pack(pady=(10, 5))

    def confirmar_corte(caminho, pasta_saida, intervalo):
        try:
            m = ctk.CTkLabel(win, text='Cortando...', text_color="green")
            m.pack(pady=10)
            intervalo = int(intervalo.get())  # Use entrada do usuário para intervalo
            ac.cut_clip(caminho, pasta_saida, intervalo)
            mensagem_sucesso = ctk.CTkLabel(win, text='Vídeo cortado com sucesso!', text_color="green")
            mensagem_sucesso.pack(pady=10)
        except Exception as e:
            mensagem_erro = ctk.CTkLabel(win, text=f'Erro: {str(e)}', text_color="red")
            mensagem_erro.pack(pady=10)

    def btn_click(opcao):
        estilo = {"width": 220, "height": 30}
        # Funções para cada operação
        if opcao == 1:
            # Limpar a interface anterior
            for widget in win.winfo_children():
                widget.pack_forget()

            texto = ctk.CTkLabel(win, text='Digite o caminho do vídeo que vai ser cortado:')
            texto.pack(pady=(10, 5))

            # Campos de entrada
            caminho_pasta = ctk.CTkEntry(win, placeholder_text='Caminho do vídeo', **estilo)
            caminho_pasta.pack(pady=(0, 10))
            pasta_saida = ctk.CTkEntry(win, placeholder_text='Caminho da pasta para salvar', **estilo)
            pasta_saida.pack(pady=(0, 10))
            intervalo = ctk.CTkEntry(win, placeholder_text='Intervalo em segundos', **estilo)
            intervalo.pack(pady=(0, 10))

            botao_confirmar = ctk.CTkButton(win, text='Cortar Vídeo', command=lambda: threading.Thread(target=confirmar_corte, args=(caminho_pasta.get(), pasta_saida.get(), intervalo)).start())
            botao_confirmar.pack(pady=10)

        elif opcao == 2:
            # Limpar a interface anterior
            for widget in win.winfo_children():
                widget.pack_forget()

            texto = ctk.CTkLabel(win, text='Digite o caminho da pasta que contém os vídeos:')
            texto.pack(pady=(10, 5))

            caminho = ctk.CTkEntry(win, placeholder_text='Caminho da pasta', **estilo)
            caminho.pack(pady=(0, 10))

            texto_renomear = ctk.CTkEntry(win, placeholder_text='Texto para renomear', **estilo)
            texto_renomear.pack(pady=(0, 10))

            botao_confirmar = ctk.CTkButton(win, text='Renomear Vídeos', command=lambda: rename_new(caminho.get(), texto_renomear.get()))
            botao_confirmar.pack(pady=10)

        elif opcao == 3:
            # Limpar a interface anterior
            for widget in win.winfo_children():
                widget.pack_forget()

            texto = ctk.CTkLabel(win, text='Digite o caminho da pasta que contém os vídeos:')
            texto.pack(pady=(10, 5))

            caminho = ctk.CTkEntry(win, placeholder_text='Caminho da pasta', **estilo)
            caminho.pack(pady=(0, 10))

            botao_contar = ctk.CTkButton(win, text='Contar Vídeos', command=lambda: mostrar_contagem(caminho.get()))
            botao_contar.pack(pady=10)

        elif opcao == 4:
            # Limpar a interface anterior
            for widget in win.winfo_children():
                widget.pack_forget()

            texto = ctk.CTkLabel(win, text='Digite o caminho da pasta que contém os vídeos:')
            texto.pack(pady=(10, 5))

            caminho = ctk.CTkEntry(win, placeholder_text='Caminho da pasta dos vídeos', **estilo)
            caminho.pack(pady=(0, 10))

            numero_videos = ctk.CTkEntry(win, placeholder_text="Número de arquivos para ser apagados", **estilo)
            numero_videos.pack(pady=(0, 10))

            botao_apagar = ctk.CTkButton(win, text='Apagar Vídeos', command=lambda: apagar_msg(caminho.get(), numero_videos.get()))
            botao_apagar.pack(pady=10)

        elif opcao == 5:
            # Limpar a interface anterior
            for widget in win.winfo_children():
                widget.pack_forget()

            texto = ctk.CTkLabel(win, text='Digite o caminho da pasta que contém os vídeos:')
            texto.pack(pady=(10, 5))

            caminho_file = ctk.CTkEntry(win, placeholder_text='Vídeo de cima', **estilo)
            caminho_file.pack(pady=(0, 10))

            caminho_video_baixo = ctk.CTkEntry(win, placeholder_text='Vídeo de baixo', **estilo)
            caminho_video_baixo.pack(pady=(0, 10))

            botao_juntar = ctk.CTkButton(win, text='Juntar Vídeos', command=lambda: confirmar_juncao(caminho_file.get(), caminho_video_baixo.get()))
            botao_juntar.pack(pady=10)

    # Criando os botões e associando as funções
    botao_estilo = {"width": 20, "height": 40, "font": ("Arial", 14)}

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
       
        root = ctk.CTkFrame(tabview.tab("BAIXCLIPS"))
        root.pack()

        # Título
        label_titulo = ctk.CTkLabel(root, text="Escolha a plataforma para baixar o vídeo", font=("Arial", 20))
        label_titulo.pack(pady=20)

        # Botões para abrir as interfaces
        botao_youtube = ctk.CTkButton(root, text="YouTube", command=criar_interface_youtube)
        botao_youtube.pack(pady=10)

        botao_instagram = ctk.CTkButton(root, text="Instagram", command=criar_interface_instagram)
        botao_instagram.pack(pady=10)

        botao_tiktok = ctk.CTkButton(root, text="TikTok", command=criar_interface_tiktok)
        botao_tiktok.pack(pady=10)

      

tela_inicial()
    # Chamar a função principal para iniciar o aplicativo


# Conteúdo para a Aba 3
label3 = ctk.CTkLabel(tabview.tab("Aba 3"), text="Conteúdo da Aba 3")
label3.pack(padx=20, pady=20)






janela.mainloop()
