#!/bin/bash

# Diretório onde os repositórios serão clonados
BASE_DIR="TheAlgorithms"

# Criar o diretório se não existir
mkdir -p "$BASE_DIR"

# Lista dos repositórios
repos=(
  "Python"
  "C"
  "C-Plus-Plus"
  "Java"
  "JavaScript"
  "Ruby"
  "Go"
  "Scala"
  "Kotlin"
  "Rust"
  "Swift"
  "Dart"
)

# Clonar ou atualizar os repositórios dentro do diretório TheAlgorithms
for repo in "${repos[@]}"; do
  if [ -d "$BASE_DIR/$repo" ]; then
    echo "Atualizando $repo..."
    cd "$BASE_DIR/$repo"
    git pull
    cd - > /dev/null
  else
    git clone "https://github.com/TheAlgorithms/$repo.git" "$BASE_DIR/$repo"
  fi
done

