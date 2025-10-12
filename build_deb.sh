#!/bin/bash

# --- Configuração ---
APP_NAME="gravador-tela"
VERSION="1.2.0" # Versão incrementada com as correções
ARCH="amd64"
ICON_SOURCE="icone.svg" # Seu ícone SVG no projeto
MAINTAINER="Gui23x <guigomes23x@gmail.com>" # Seus dados de criador

# --- Limpeza ---
echo "Limpando compilações anteriores..."
rm -rf dist/ build/ *.spec "${APP_NAME}_${VERSION}_${ARCH}.deb" "${APP_NAME}_${VERSION}_${ARCH}"

# --- Passo 1: Criar o executável com PyInstaller ---
echo "Criando o executável com PyInstaller..."
pyinstaller --name "$APP_NAME" \
            --onefile \
            --windowed \
            gravador_tela.py

if [ ! -f "dist/$APP_NAME" ]; then
    echo "Falha ao criar o executável. Abortando."
    exit 1
fi
echo "Executável criado com sucesso."

# --- Passo 2: Preparar a estrutura do pacote ---
echo "Criando a estrutura de diretórios para o pacote .deb..."
PACKAGE_DIR="${APP_NAME}_${VERSION}_${ARCH}"
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR/usr/bin"
mkdir -p "$PACKAGE_DIR/usr/share/applications"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/scalable/apps"

# --- Passo 3: Criar o arquivo de controle DEBIAN/control ---
echo "Criando o arquivo de controle (control)..."
cat <<EOF > "$PACKAGE_DIR/DEBIAN/control"
Package: $APP_NAME
Version: $VERSION
Architecture: $ARCH
Maintainer: $MAINTAINER
Description: Um gravador de tela simples para Linux.
 Este aplicativo permite gravar a tela inteira, uma janela específica ou uma área selecionada, com ou sem áudio.
Depends: ffmpeg, xdotool, slop, libxcb-xinerama0
EOF

# --- Passo 4: Criar o script de pós-instalação DEBIAN/postinst ---
echo "Criando o script de pós-instalação (postinst)..."
cat <<EOF > "$PACKAGE_DIR/DEBIAN/postinst"
#!/bin/sh
set -e
echo "Atualizando o cache de ícones..."
gtk-update-icon-cache /usr/share/icons/hicolor/ || true
echo "Atualizando a base de dados do menu..."
update-desktop-database -q
echo "Pós-instalação concluída."
exit 0
EOF
# Dar permissão de execução ao script postinst
chmod 0755 "$PACKAGE_DIR/DEBIAN/postinst"

# --- Passo 5: Copiar os arquivos para a estrutura ---
echo "Copiando os arquivos para a estrutura do pacote..."
cp "dist/$APP_NAME" "$PACKAGE_DIR/usr/bin/"
cp "${APP_NAME}.desktop" "$PACKAGE_DIR/usr/share/applications/"
cp "$ICON_SOURCE" "$PACKAGE_DIR/usr/share/icons/hicolor/scalable/apps/${APP_NAME}.svg"

# --- Passo 6: Construir o pacote .deb ---
echo "Construindo o pacote .deb..."
dpkg-deb --build "$PACKAGE_DIR"

echo "Processo concluído!"
echo "Seu instalador é: ${PACKAGE_DIR}.deb"

