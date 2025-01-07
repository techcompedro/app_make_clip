# NixClips

NixClips é uma aplicação de interface gráfica desenvolvida em Python, projetada para permitir aos usuários realizar diversas operações relacionadas a vídeos e áudio. As principais funcionalidades incluem cortar, renomear, contar, apagar e juntar vídeos, além de baixar vídeos de plataformas como YouTube, Instagram e TikTok. A aplicação é intuitiva e fácil de usar, proporcionando uma experiência agradável ao usuário.

## Funcionalidades

### Operações de Vídeo (MIX CLIP)

1. **Cortar Vídeos**:
   - Divide um vídeo em partes com base em um intervalo especificado.
   - Entrada: caminho do vídeo, pasta de saída e intervalo em segundos.

2. **Renomear Vídeos**:
   - Renomeia vídeos em uma pasta com base em um texto fornecido.
   - Entrada: caminho da pasta e texto para renomeação.

3. **Contar Vídeos**:
   - Conta o número de vídeos em uma pasta.
   - Entrada: caminho da pasta.

4. **Apagar Vídeos**:
   - Remove um número específico de vídeos mais recentes de uma pasta.
   - Entrada: caminho da pasta e número de vídeos a apagar.

5. **Juntar Vídeos**:
   - Combina dois vídeos em um único arquivo.
   - Entrada: caminhos dos dois vídeos a serem combinados.

### Download de Vídeos (BAIX CLIP)

1. **YouTube**:
   - Permite baixar vídeos utilizando a URL e o caminho de destino.

2. **Instagram**:
   - Realiza downloads de vídeos com base na URL fornecida.

3. **TikTok**:
   - Baixa vídeos com a URL especificada pelo usuário.

### Operações de Áudio (AUDI CLIP)

1. **Converter Texto para Áudio**:
   - Converte texto em arquivos de áudio usando a tecnologia de TTS da Microsoft.
   - Entrada: texto, idioma, voz e formato do arquivo de saída.

2. **Extrair Texto de Arquivos**:
   - Extrai texto de arquivos PDF, DOCX e TXT para conversão em áudio.

## Bibliotecas Utilizadas

- **customtkinter**: Extensão do tkinter para criar interfaces gráficas modernas e personalizáveis.
- **moviepy**: Manipulação eficiente de vídeos (cortar, renomear, juntar, etc.).
- **yt-dlp**: Download de vídeos de várias plataformas.
- **threading**: Execução de operações em segundo plano para melhorar a responsividade.
- **os**: Manipulação de arquivos e diretórios.
- **tkinter.messagebox**: Exibição de mensagens de erro ou sucesso.
- **pdfplumber**: Extração de texto de arquivos PDF.
- **docx**: Manipulação de arquivos DOCX.
- **edge_tts**: Conversão de texto em fala com a tecnologia da Microsoft.
