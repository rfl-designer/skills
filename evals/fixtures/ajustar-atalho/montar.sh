#!/usr/bin/env bash
# Monta uma pasta de execução da fixture de atalho de /ajustar.
# Uso: montar.sh <destino> [<pasta com vendor/ pronto>]
# Com a segunda pasta, copia vendor/ com links físicos (cp -al). Sem ela, roda composer install.
set -euo pipefail

aqui="$(cd "$(dirname "$0")" && pwd)"
destino="${1:?informe a pasta de destino}"
vendor_pronto="${2:-}"

if [ -e "$destino" ]; then
    echo "O destino já existe: $destino" >&2
    exit 1
fi

mkdir -p "$destino"
cp -r "$aqui/../revisar-executavel/projeto" "$destino/projeto"
cd "$destino/projeto"

# A base ganha o teste de arquitetura, a suíte Arch e a Spec 0007.
git init -q -b master
git apply "$aqui/base.patch"
mkdir -p bootstrap/cache storage/framework/cache storage/framework/sessions \
    storage/framework/testing storage/framework/views storage/logs
git -c user.name=fixture -c user.email=fixture@example.com add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "base: loja"
git checkout -qb feature/estorno
git apply "$aqui/mudanca.patch"
git -c user.name=fixture -c user.email=fixture@example.com add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "feat: estorno pela lista"

if [ -n "$vendor_pronto" ]; then
    # Links físicos, não simbólicos: o autoload usa o caminho de cada pasta.
    # Não rode composer nesta pasta: ele reescreve arquivos compartilhados.
    cp -al "$vendor_pronto/vendor" vendor
else
    COMPOSER_ALLOW_SUPERUSER=1 composer install --no-interaction --no-progress
fi

cp "$aqui/relatorio-revisar.md" "$destino/relatorio-revisar.md"
cp -r "$aqui/provas" "$destino/provas"

./vendor/bin/pest > /dev/null
echo "Pronto: $destino (branch feature/estorno, Pest verde)"
