# NixClips

## Descrição do Projeto
NixClips é uma aplicação de interface gráfica desenvolvida em Python, projetada para permitir aos usuários realizar diversas operações relacionadas a vídeos. As principais funcionalidades incluem cortar, renomear, contar, apagar e juntar vídeos, além de baixar vídeos de plataformas como YouTube, Instagram e TikTok. A aplicação é intuitiva e fácil de usar, proporcionando uma experiência agradável ao usuário.

## Funcionalidades
- **Cortar Vídeos**: Divide um vídeo em partes com base em um intervalo especificado.
- **Renomear Vídeos**: Renomeia vídeos em uma pasta com um texto fornecido.
- **Contar Vídeos**: Conta o número de vídeos em uma pasta.
- **Apagar Vídeos**: Remove um número específico de vídeos mais recentes de uma pasta.
- **Juntar Vídeos**: Combina dois vídeos em um único arquivo.
- **Download de Vídeos**: Permite baixar vídeos de plataformas como YouTube, Instagram e TikTok.

## Bibliotecas Utilizadas
1. **customtkinter**  
   - **Descrição**: Extensão da biblioteca padrão tkinter, que permite a criação de interfaces gráficas mais modernas e personalizáveis.  
   - **Motivo do Uso**: Proporciona uma aparência mais atraente e amigável. Facilita a criação de componentes como janelas, abas, botões e entradas de texto.

2. **moviepy**  
   - **Descrição**: Biblioteca para edição de vídeos em Python.  
   - **Motivo do Uso**: Permite manipular vídeos de forma eficiente, como cortar, renomear, juntar e contar vídeos. Suporta diversos formatos de vídeo e oferece funcionalidades avançadas de edição.

3. **yt-dlp**  
   - **Descrição**: Ferramenta de download de vídeos de várias plataformas, uma versão melhorada do youtube-dl.  
   - **Motivo do Uso**: Facilita o download de vídeos de plataformas como YouTube, Instagram e TikTok. Permite especificar opções como formato de saída e qualidade do vídeo.

4. **threading**  
   - **Descrição**: Biblioteca que permite a execução de operações em segundo plano.  
   - **Motivo do Uso**: Garante que operações de longa duração, como o corte de vídeos e downloads, não bloqueiem a interface gráfica. Melhora a responsividade da aplicação.

5. **os**  
   - **Descrição**: Biblioteca que fornece uma interface para interagir com o sistema operacional.  
   - **Motivo do Uso**: Permite manipulação de arquivos e diretórios, como verificar a existência de arquivos, criar diretórios e listar arquivos.

6. **tkinter.messagebox**  
   - **Descrição**: Módulo que permite exibir caixas de mensagem para interagir com o usuário.  
   - **Motivo do Uso**: Utilizado para mostrar mensagens de erro ou sucesso durante as operações, como downloads e manipulações de vídeo.

## Funcionamento da Aplicação

### 1. Interface Gráfica
A aplicação inicia com uma janela principal que contém um título e três abas:
- **MIXCLIP**: Para operações de manipulação de vídeos.
- **BAIXCLIPS**: Para baixar vídeos de plataformas online.
- **Aba 3**: Um espaço reservado para conteúdo adicional.

### 2. Operações de Vídeo (MIXCLIP)
Os usuários podem escolher entre cinco operações principais:
- **Cortar Vídeos**: O usuário insere o caminho do vídeo, o caminho de saída e o intervalo em segundos. O vídeo é cortado em partes de acordo com o intervalo especificado e salvo na pasta de saída.
- **Renomear Vídeos**: O usuário fornece um caminho para a pasta contendo os vídeos e um texto para renomeá-los. Os vídeos na pasta são renomeados sequencialmente com base no texto fornecido.
- **Contar Vídeos**: O usuário insere o caminho da pasta que contém os vídeos. A aplicação conta quantos vídeos estão presentes na pasta e exibe o resultado.
- **Apagar Vídeos**: O usuário fornece o caminho da pasta e o número de vídeos a serem apagados. A aplicação apaga os vídeos mais recentes na pasta, conforme o número especificado.
- **Juntar Vídeos**: O usuário insere os caminhos de dois vídeos. A aplicação junta os dois vídeos em um único arquivo e salva o resultado.

### 3. Download de Vídeos (BAIXCLIPS)
Os usuários podem escolher entre baixar vídeos de três plataformas:
- **YouTube**: O usuário insere a URL do vídeo e o caminho de destino. A aplicação utiliza yt-dlp para realizar o download do vídeo, exibindo mensagens de progresso e conclusão.
- **Instagram**: O usuário insere a URL do vídeo e o caminho de destino. A aplicação baixa o vídeo utilizando yt-dlp, garantindo que o usuário receba feedback sobre o progresso e a conclusão do download.
- **TikTok**: O usuário insere a URL do vídeo e o caminho de destino. A aplicação também utiliza yt-dlp para baixar vídeos do TikTok, seguindo o mesmo processo de feedback ao usuário.

## Conclusão
NixClips é uma ferramenta poderosa e versátil para quem trabalha com vídeos, oferecendo uma interface amigável e funcionalidades robustas. Com a capacidade de manipular e baixar vídeos de várias plataformas, a aplicação se destaca como uma solução prática para editores de vídeo e usuários que desejam gerenciar seu conteúdo de forma eficiente.
