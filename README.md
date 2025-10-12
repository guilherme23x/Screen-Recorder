# Gravador de Tela Simples para Linux

Um aplicativo de gravação de tela leve e minimalista para desktops Linux, construído com Python e GTK3. Ideal para capturar a tela inteira, uma janela específica ou uma área selecionada com áudio do sistema e do microfone, de forma rápida e direta.

## ✨ Funcionalidades

* **Múltiplos Modos de Captura:**
  * **Tela Inteira:** Grava todo o seu monitor.
  * **Janela:** Permite selecionar uma janela de aplicativo específica para gravar.
  * **Seleção:** Desenhe um retângulo na tela para gravar apenas a área desejada.

* **Controle de Áudio Simplificado:**
  * **Com Áudio:** Grava simultaneamente o áudio interno do sistema (o que você ouve) e o áudio externo do seu microfone padrão.
  * **Sem Áudio:** Grava apenas o vídeo.

* **Alta Performance:**
  * Grava em **60 FPS** por padrão para garantir vídeos fluidos.
  * Utiliza a resolução nativa do seu monitor para máxima qualidade.

* **Interface Intuitiva:**
  * Todas as opções são apresentadas de forma clara e direta.
  * Selecione e salve uma pasta de destino padrão para suas gravações.

* **Empacotamento Fácil:**
  * Acompanha um script para gerar um executável independente e um instalador `.deb` para fácil distribuição em sistemas baseados em Debian (Ubuntu, Linux Mint, etc.).

## ⚙️ Dependências

Para executar o programa a partir do código-fonte ou para construir o pacote, você precisará ter as seguintes ferramentas instaladas no seu sistema:

* **Python 3**
* **GTK3**
* **PyGObject**
* **FFmpeg:** O motor por trás da gravação de vídeo e áudio.
* **xdotool:** Utilitário para obter informações da janela.
* **slop:** Utilitário para selecionar uma área na tela.

Você pode instalar todas as dependências em um sistema Debian/Ubuntu com o seguinte comando:

`sudo apt update`
`sudo apt install python3 python3-gi gir1.2-gtk-3.0 ffmpeg xdotool slop`

## 🚀 Instalação (Via Pacote .deb)

Se você já possui o arquivo .deb, a instalação é simples.

1. Abra o terminal no diretório onde o arquivo gravador-tela_*.deb está localizado.
2. Execute o comando de instalação:
   `sudo dpkg -i gravador-tela_*.deb`
3. Caso encontre erros de dependências faltantes, resolva-os com:
   `sudo apt-get install -f`

Após a instalação, o "Gravador de Tela" estará disponível no menu de aplicativos, na categoria "Som e Vídeo".

## 👨‍💻 Uso (Executando a partir do Código-Fonte)

Se preferir executar o programa diretamente do script Python:

1. Clone este repositório:
   `git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)`
   `cd seu-repositorio`
2. Certifique-se de que todas as dependências estão instaladas.
3. Execute o script:
   `python3 gravador_tela.py`

## 📦 Construindo o Executável e o Pacote .deb

O projeto inclui um script (build_deb.sh) para automatizar a criação de um executável e de um instalador .deb.

1. **Pré-requisitos:** Instale a ferramenta pyinstaller:
   `pip install pyinstaller`
2. **Organize os Arquivos:** Certifique-se de que os seguintes arquivos estão na raiz do projeto:
   * `gravador_tela.py`
   * `gravador-tela.desktop`
   * `icone.svg`
   * `build_deb.sh`
3. **Dê Permissão de Execução** ao script de construção:
   `chmod +x build_deb.sh`
4. **Execute o Script:**
   `./build_deb.sh`

Ao final do processo, um arquivo .deb (ex: gravador-tela_1.2.0_amd64.deb) será gerado na pasta do projeto, pronto para ser distribuído e instalado.

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

* **Gui23x**
* **Email:** guigomes23x@gmail.com
