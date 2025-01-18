import customtkinter as ctk
import autoclip as ac
import threading
import os
from tkinter.filedialog import askdirectory
from moviepy import VideoFileClip, clips_array
import edge_tts
import asyncio
import pdfplumber

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
tabview.add("AUDI CLIP")
tabview.add("DEEP CLIP")

def clipmix():
    quadro_menu = ctk.CTkFrame(tabview.tab("MIX CLIP"))
    quadro_menu.pack()
    opicoes = ctk.CTkLabel(quadro_menu, text=(
        '1 - CORTAR OS VIDEOS\n'
        '2 - RENOMEAR VIDEOS\n'
        '3 - CONTAR VIDEOS\n'
        '4 - APAGAR VIDEOS\n'
        '5 - JUNTAR OS VIDEOS'
    ))
    opicoes.pack(pady=10)

    win = ctk.CTkFrame(tabview.tab("MIX CLIP"), fg_color="transparent")
    win.pack()

    def limpar_interface():
        for widget in win.winfo_children():
            widget.pack_forget()

    def mostrar_mensagem(texto, cor="green"):
        mensagem = ctk.CTkLabel(win, text=texto, text_color=cor)
        mensagem.pack(pady=10)

    def btn_click(opcao):
        limpar_interface()
        estilo = {"width": 300, "height": 30}

        if opcao == 1:  # Cortar Vídeos
            ctk.CTkLabel(win, text="Cortar Vídeo:").pack(pady=(10, 5))
            caminho = ctk.CTkEntry(win, placeholder_text="Caminho do vídeo", **estilo)
            caminho.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Vídeo", command=lambda: ac.selecionar_video(caminho)).pack(pady=5)
            pasta_saida = ctk.CTkEntry(win, placeholder_text="Pasta para salvar", **estilo)
            pasta_saida.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: ac.selecionar_pasta(pasta_saida)).pack(pady=5)
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
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: ac.selecionar_pasta(caminho)).pack(pady=5)
            novo_nome = ctk.CTkEntry(win, placeholder_text="Novo nome base", **estilo)
            novo_nome.pack(pady=5)

            def renomear_videos():
                try:
                    renomeados = ac.rename_clip(caminho.get(), novo_nome.get())
                    mostrar_mensagem(f"Renomeados: {renomeados} arquivos.")
                except Exception as e:
                    mostrar_mensagem(f"Erro: {e}", "red")

            ctk.CTkButton(win, text="Renomear", command=lambda: threading.Thread(target=renomear_videos).start()).pack(pady=10)

        elif opcao == 3:  # Contar Vídeos
            ctk.CTkLabel(win, text="Contar Vídeos:").pack(pady=(10, 5))
            caminho = ctk.CTkEntry(win, placeholder_text="Caminho da pasta", **estilo)
            caminho.pack(pady=5)
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: ac.selecionar_pasta(caminho)).pack(pady=5)

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
            ctk.CTkButton(win, text="Selecionar Pasta", command=lambda: ac.selecionar_pasta(caminho)).pack(pady=5)
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
                        resultado_entry.configure(text="Erro: As pastas devem conter o mesmo número de vídeos.")
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

                    resultado_entry.configure(text="Todos os vídeos foram combinados com sucesso!")
                except FileNotFoundError as e:
                    resultado_entry.configure(text=f"Erro: Arquivo ou pasta não encontrado. Detalhes: {e}")
                except Exception as e:
                    resultado_entry.configure(text=f"Erro ao combinar vídeos. Detalhes: {e}")
                
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
            resultado_entry = ctk.CTkLabel(win, text="")
            resultado_entry.pack(pady=3)
    
        
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
def tela_inicial():
        root = ctk.CTkFrame(tabview.tab("BAIX CLIP"))
        root.pack()
        frame = ctk.CTkFrame(tabview.tab("BAIX CLIP"), fg_color="transparent")
        frame.pack()
        botao_estilo = {"width": 20, "height": 30, "font": ("Arial", 14)}
        def limpar_interface():
            for widget in frame.winfo_children():
                widget.pack_forget()

        def btn_click_baixar(opc):
            limpar_interface()
            estilo = {"width": 300, "height": 30}
            
            if opc == 1:

                        label_titulo = ctk.CTkLabel(frame, text="Baixar Vídeo do YouTube", font=("Arial", 18))
                        label_titulo.pack(pady=10)

                        label_url_youtube = ctk.CTkLabel(frame, text="URL do Vídeo:")
                        label_url_youtube.pack(pady=5)
                        entry_url_youtube = ctk.CTkEntry(frame, placeholder_text="Insira a URL do vídeo", **estilo)
                        entry_url_youtube.pack(pady=5)

                        label_destino_youtube = ctk.CTkLabel(frame, text="Caminho de destino:")
                        label_destino_youtube.pack(pady=5)
                        entry_destino_youtube = ctk.CTkEntry(frame, placeholder_text="Caminho de destino", **estilo)
                        entry_destino_youtube.pack(pady=5)
                        ctk.CTkButton(frame , text="Selecionar a pasta", command=lambda: ac.selecionar_pasta(entry_destino_youtube)).pack(pady=5)
                        def baixar_video_y():
                            try:
                                ac.mostrar_mensagem(frame,"Baixando vídeo...")
                                ac.baixar_video_youtube(entry_url_youtube.get(), entry_destino_youtube.get())
                                ac.mostrar_mensagem(frame,"download concluído!")
                            except Exception as e:
                                ac.mostrar_mensagem(frame,f"Erro: {e}", "red")
                            
                        
                        ctk.CTkButton(frame, text="Baixar YouTube",  **botao_estilo,command=lambda: threading.Thread(target=baixar_video_y).start()).pack(pady=20)

            elif opc == 2:

                        label_titulo_instagram = ctk.CTkLabel(frame, text="Baixar Vídeo do Instagram", font=("Arial", 18))
                        label_titulo_instagram.pack(pady=10)

                        label_url_instagram = ctk.CTkLabel(frame, text="URL do Vídeo:", **estilo)
                        label_url_instagram.pack(pady=5)
                        entry_url_instagram = ctk.CTkEntry(frame, placeholder_text="Insira a URL do vídeo", **estilo)
                        entry_url_instagram.pack(pady=5)

                        label_destino_instagram = ctk.CTkLabel(frame, text="Caminho de destino:")
                        label_destino_instagram.pack(pady=5)
                        entry_destino_instagram = ctk.CTkEntry(frame, placeholder_text="Caminho de destino", **estilo)
                        entry_destino_instagram.pack(pady=5)
                        ctk.CTkButton(frame , text="Selecionar a pasta", command=lambda: ac.selecionar_pasta(entry_destino_instagram)).pack(pady=5)

                        def baixar_video_inst():
                            try:
                                ac.mostrar_mensagem(frame,"Baixando vídeo...")
                                ac.baixar_video_instagram(entry_url_instagram.get(), entry_destino_instagram.get())
                                ac.mostrar_mensagem(frame,"download concluído!")
                            except Exception as e:
                                ac.mostrar_mensagem(frame,f"Erro: {e}", "red")
                           
                        
                        ctk.CTkButton(frame, text="Baixar Instagram",  **botao_estilo,command=lambda: threading.Thread(target=baixar_video_inst).start()).pack(pady=20)
                        
            elif opc == 3:
                        label_titulo_tiktok = ctk.CTkLabel(frame, text="Baixar Vídeo do TikTok", font=("Arial", 18))
                        label_titulo_tiktok.pack(pady=10)

                        label_url_tiktok = ctk.CTkLabel(frame, text="URL do Vídeo:")
                        label_url_tiktok.pack(pady=5)
                        entry_url_tiktok = ctk.CTkEntry(frame, placeholder_text="Insira a URL do vídeo", **estilo)
                        entry_url_tiktok.pack(pady=5)

                        label_destino_tiktok = ctk.CTkLabel(frame, text="Caminho de destino:")
                        label_destino_tiktok.pack(pady=5)
                        
                        entry_destino_tiktok = ctk.CTkEntry(frame, placeholder_text="Caminho de destino", **estilo)
                        entry_destino_tiktok.pack(pady=5)
                        ctk.CTkButton(frame , text="Selecionar a pasta", command=lambda: ac.selecionar_pasta(entry_destino_tiktok)).pack(pady=5)
                        
                        def baixar_video_tik():
                            try:
                                ac.mostrar_mensagem(frame,"Baixando vídeo...")
                                ac.baixar_video_tiktok(entry_url_tiktok.get(), entry_destino_tiktok.get())
                                ac.mostrar_mensagem(frame,"download concluído!")
                            except Exception as e:
                                ac.mostrar_mensagem(frame,f"Erro: {e}", "red")
                            
                        
                        ctk.CTkButton(frame, text="Baixar TikTok",  **botao_estilo,command=lambda: threading.Thread(target=baixar_video_tik).start()).pack(pady=20)
                        

        botao_esti = {"width": 20, "height": 35, "font": ("Arial", 14)}
        # Título
        label_titulo = ctk.CTkLabel(root, text="Escolha a plataforma", font=("Arial", 20))
        label_titulo.pack()
        label_titulo2 = ctk.CTkLabel(root, text="para baixar o vídeo", font=("Arial", 20))
        label_titulo2.pack()

        # Botões para abrir as interfaces
        botao_youtube = ctk.CTkButton(root, text="YouTube",  **botao_esti,command=lambda: btn_click_baixar(1))
        botao_youtube.pack(pady=10)

        botao_instagram = ctk.CTkButton(root, text="Instagram",  **botao_esti,command=lambda: btn_click_baixar(2))
        botao_instagram.pack(pady=10)

        botao_tiktok = ctk.CTkButton(root, text="TikTok",  **botao_esti,command=lambda: btn_click_baixar(3))
        botao_tiktok.pack(pady=10)

tela_inicial()


def aba_audio():
    root = ctk.CTkFrame(tabview.tab("AUDI CLIP"))
    root.pack()
    frame = ctk.CTkFrame(tabview.tab("AUDI CLIP"), fg_color="transparent")
    frame.pack()

    def limpar_interface():
        for widget in frame.winfo_children():
            widget.pack_forget()
        
    def btn_audio(opc):
        limpar_interface()
        estilo = {"width": 300, "height": 30}
        botao_estilo = {"width": 20, "height": 30, "font": ("Arial", 14)}
        if opc == 1:
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
                        resultado_entry.configure(text="Formato de arquivo não suportado.")
                        return
                    
                    if texto:
                        caminho_arquivo_audio = await texto_para_audio(texto, idioma, voz, formato, nome_arquivo)
                        if caminho_arquivo_audio:
                            resultado_entry.configure(text=f"Áudio gerado com sucesso! Salvo como: {caminho_arquivo_audio}")
                        else:
                            resultado_entry.configure(text="Erro ao gerar o áudio.")
                    else:
                        resultado_entry.configure(text="Não foi possível extrair texto do arquivo.")
                else:
                    resultado_entry.configure(text="Por favor, insira o caminho do arquivo.")


            # Campo para o caminho do arquivo
            caminho_arquivo_label = ctk.CTkLabel(frame, text="converter arquivos em pdf para audio:")
            caminho_arquivo_label.pack(pady=5)
            
            caminho_arquivo_input = ctk.CTkEntry(frame, **estilo, placeholder_text="Digite o caminho ou selecione o arquivo")
            caminho_arquivo_input.pack(pady=10)

            # Botão para selecionar o arquivo
            selecionar_arquivo = ctk.CTkButton(frame, **botao_estilo,text="Selecionar Arquivo", command=lambda:ac.selecionar_arquivo(caminho_arquivo_input))
            selecionar_arquivo.pack(pady=10)

            # Combobox para idioma
            idioma_combobox = ctk.CTkComboBox(frame, values=list(VOZES.keys()), width=200)
            idioma_combobox.set('pt-BR')  # Valor padrão
            idioma_combobox.pack(pady=10)

            # Combobox para voz
            voz_combobox = ctk.CTkComboBox(frame, values=list(VOZ), width=200)
            voz_combobox.pack(pady=10)

            # Combobox para formato
            formato_combobox = ctk.CTkComboBox(frame, values=["wav", "mp3"], width=200)
            formato_combobox.set("mp3")  # Valor padrão
            formato_combobox.pack(pady=10)

            # Campo para o nome do arquivo de saída
            nome_arquivo_label = ctk.CTkLabel(frame, text="Nome do arquivo de áudio:")
            nome_arquivo_label.pack(pady=5)
            nome_arquivo_input = ctk.CTkEntry(frame, **estilo, placeholder_text="Digite o nome do arquivo de áudio")
            nome_arquivo_input.pack(pady=10)

            # Botão para gerar o áudio
            gerar_button = ctk.CTkButton(frame, **botao_estilo,text="Gerar Áudio", command=lambda: asyncio.run(gerar_audio()))
            gerar_button.pack(pady=20)

            # Label para exibir o resultado
            resultado_entry = ctk.CTkLabel(frame, text=".")
            resultado_entry.pack()

        elif opc == 2:
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

            async def gerar_audio():
                texto = texto_input.get()
                idioma = idioma_combobox.get()
                voz = voz_combobox.get()
                formato = formato_combobox.get()
                nome_arquivo = nome_arquivo_input.get() or "audio_gerado"

                if texto:
                    try:
                        # Verificar se a voz escolhida é válida
                        if voz not in VOZES.get(idioma, []):
                            resultado_entry.delete(0, ctk.END)
                            resultado_entry.insert(0, f"Erro: A voz '{voz}' não está disponível para o idioma {idioma}.")
                            return
                        
                        # Gerar o áudio
                        caminho_audio = await texto_para_audio(texto, idioma, voz, formato, nome_arquivo)
                        if caminho_audio:
                            resultado_entry.delete(0, ctk.END)
                            resultado_entry.insert(0, f"Áudio gerado com sucesso! Salvo como: {caminho_audio}")
                        else:
                            resultado_entry.delete(0, ctk.END)
                            resultado_entry.insert(0, "Erro ao gerar o áudio. Verifique os detalhes e tente novamente.")
                    except Exception as e:
                        resultado_entry.delete(0, ctk.END)
                        resultado_entry.insert(0, f"Erro inesperado: {e}")
                else:
                    resultado_entry.delete(0, ctk.END)
                    resultado_entry.insert(0, "Por favor, insira um texto válido.")

            # Componentes da interface
            
            label = ctk.CTkLabel(frame, text="Converter texto em audio:")
            label.pack(pady=5)
            texto_input = ctk.CTkEntry(frame, **estilo, placeholder_text="Digite o texto que deseja converter...")
            texto_input.pack(pady=10)

            idioma_combobox = ctk.CTkComboBox(frame, values=list(VOZES.keys()), width=200)
            idioma_combobox.set('pt-BR')  # Valor padrão
            idioma_combobox.pack(pady=10)

            voz_combobox = ctk.CTkComboBox(frame, values=VOZ, width=200)
            voz_combobox.pack(pady=10)

            formato_combobox = ctk.CTkComboBox(frame, values=["wav", "mp3"], width=200)
            formato_combobox.set("wav")  # Valor padrão
            formato_combobox.pack(pady=10)

            nome_arquivo_input = ctk.CTkEntry(frame, **estilo, placeholder_text="Digite o nome do arquivo (sem a extensão)...")
            nome_arquivo_input.pack(pady=10)

            gerar_button = ctk.CTkButton(frame, **botao_estilo, text="Gerar Áudio", command=lambda: asyncio.run(gerar_audio()))
            gerar_button.pack(pady=20)


        # Função para abrir uma nova janela com o texto gerado
        def abrir_nova_guia(texto_gerado):
            nova_janela = ctk.CTkToplevel()
            nova_janela.title("Texto Gerado")
            nova_janela.geometry("500x500")

            label_texto = ctk.CTkLabel(nova_janela, text="Texto Gerado:", font=("Arial", 14, "bold"))
            label_texto.pack(pady=10)

            texto_box = ctk.CTkTextbox(nova_janela, width=380, height=200)
            texto_box.insert("1.0", texto_gerado)
            texto_box.configure(state="disabled")  # Desativa edição
            texto_box.pack(padx=10, pady=10)

            botao_fechar = ctk.CTkButton(nova_janela, text="Fechar", command=nova_janela.destroy)
            botao_fechar.pack(pady=10)

        # Função para converter áudio em texto e exibir o resultado
        def converter_audio_texto(frame, caminho_entrada):
            try:
                ac.mostrar_mensagem(frame, "Convertendo áudio para texto...")
                texto_gerado = ac.transcribe_audio(caminho_entrada)  # Chama a função de transcrição
                ac.mostrar_mensagem(frame, "Conversão concluída!")
                abrir_nova_guia(texto_gerado)  # Abre a nova janela com o texto gerado
            except Exception as e:
                ac.mostrar_mensagem(frame, f"Erro: {e}", "red")

        # Exemplo da interface gráfica com CustomTkinter
       
        if opc == 3:
            label = ctk.CTkLabel(frame, text="Converter Áudio em Texto:")
            label.pack(pady=5)

            caminho = ctk.CTkEntry(frame, **estilo, placeholder_text='Caminho do áudio')
            caminho.pack(pady=10)

            caminhobtn = ctk.CTkButton(frame, **botao_estilo, text='Selecionar Áudio',
                                        command=lambda: ac.selecionar_audio(caminho))
            caminhobtn.pack(pady=10)

            ctk.CTkButton(frame, **botao_estilo, text="Converter",
                            command=lambda: threading.Thread(target=converter_audio_texto, 
                                                            args=(frame, caminho.get())).start()).pack(pady=10)







    btn_estilo = {"width": 20, "height": 30, "font": ("Arial", 14)}
    
    arquivo_audio_btn = ctk.CTkButton(root, text="Converter arquivos em pdf para audio", **btn_estilo, command=lambda: btn_audio(1))
    arquivo_audio_btn.pack(pady=10)
    
    texto_audio_btn  = ctk.CTkButton(root, text="Converter texto para audio", **btn_estilo, command=lambda: btn_audio(2))
    texto_audio_btn.pack(pady=10)
    
    texto_audio_btn  = ctk.CTkButton(root, text="Converter audio para texto", **btn_estilo, command=lambda: btn_audio(3))
    texto_audio_btn.pack(pady=10)
    
aba_audio()


def img_fundo_video():
    frame = ctk.CTkFrame(tabview.tab("DEEP CLIP"), fg_color="transparent")
    frame.pack()
    estilo = {"width": 300, "height": 30}

    titulo = ctk.CTkLabel(frame, text='Adicionar imagem \n'
                          'como fundo de um video', font=("Arial", 17))
    titulo.pack()
    img_caminho = ctk.CTkEntry(frame , placeholder_text="Caminho para a imagem", **estilo)
    img_caminho.pack()
    ctk.CTkButton(frame , text="Selecionar imagem", command=lambda: ac.selecionar_img(img_caminho)).pack(pady=5)
    
    caminho = ctk.CTkEntry(frame , placeholder_text="Caminho da pasta com os videos", **estilo)
    caminho.pack(pady=5)
    ctk.CTkButton(frame , text="Selecionar a pasta", command=lambda: ac.selecionar_pasta(caminho)).pack(pady=5)
    
    pasta_saida = ctk.CTkEntry(frame , placeholder_text="Pasta para salvar", **estilo)
    pasta_saida.pack(pady=5)
    ctk.CTkButton(frame , text="Selecionar Pasta", command=lambda: ac.selecionar_pasta(pasta_saida)).pack(pady=5)

    
    def deep():
        try:
            ac.mostrar_mensagem(frame, "junando o fundo da imagem com o  video...")
            ac.process_videos_in_folder(img_caminho.get(), caminho.get(), pasta_saida.get())
            ac.mostrar_mensagem(frame, "junção concluída!")
        except Exception as e:
            ac.mostrar_mensagem(frame, f"Erro: {e}", "red")
    ctk.CTkButton(frame , text="junta", command=lambda: threading.Thread(target=deep).start()).pack(pady=10)

img_fundo_video()

janela.mainloop()
