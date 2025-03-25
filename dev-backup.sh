#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório de origem (seus projetos)
SOURCE_DIR="$HOME/dev"

# Diretório onde os backups serão salvos
BACKUP_DIR="$HOME/backups/dev"

# Data atual para nome do arquivo
DATE=$(date +"%Y%m%d_%H%M%S")

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

echo -e "${YELLOW}Iniciando backup dos projetos...${NC}"

# Criar arquivo de backup excluindo diretórios desnecessários
tar --exclude='*/node_modules' \
    --exclude='*/.venv' \
    --exclude='*/venv' \
    --exclude='*/__pycache__' \
    --exclude='*/.git' \
    --exclude='*/dist' \
    --exclude='*/build' \
    -czf "$BACKUP_DIR/dev_backup_$DATE.tar.gz" \
    -C "$SOURCE_DIR" .

# Verificar se o backup foi criado com sucesso
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Backup criado com sucesso em:${NC}"
    echo -e "${GREEN}$BACKUP_DIR/dev_backup_$DATE.tar.gz${NC}"
    
    # Mostrar os backups mais recentes
    echo -e "\n${YELLOW}Backups mais recentes:${NC}"
    ls -lh "$BACKUP_DIR" | grep "dev_backup_" | sort -r | head -n 5
    
    # Mostrar espaço em disco no diretório de backup
    echo -e "\n${YELLOW}Espaço em disco no diretório de backup:${NC}"
    du -sh "$BACKUP_DIR"
else
    echo -e "${RED}Erro ao criar backup!${NC}"
    exit 1
fi
