#!/usr/bin/env bash
# Monta uma pasta de execução da fixture executável de /revisar.
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
cp -r "$aqui/projeto" "$destino/projeto"
cd "$destino/projeto"

mkdir -p bootstrap/cache storage/framework/cache storage/framework/sessions \
    storage/framework/testing storage/framework/views storage/logs docs/specs
cp "$aqui/../revisar/spec-aprovar-pela-lista.md" docs/specs/0005-aprovar-pela-lista.md

git init -q -b master
git -c user.name=fixture -c user.email=fixture@example.com add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "base: loja"
git checkout -qb feature/aprovar-pela-lista
git apply "$aqui/mudanca.patch"
git -c user.name=fixture -c user.email=fixture@example.com add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "feat: Gerente aprova o Pedido pela lista"

if [ -n "$vendor_pronto" ]; then
    # Links físicos, não simbólicos: o autoload usa o caminho de cada pasta.
    # Não rode composer nesta pasta: ele reescreve arquivos compartilhados.
    cp -al "$vendor_pronto/vendor" vendor
else
    COMPOSER_ALLOW_SUPERUSER=1 composer install --no-interaction --no-progress
fi

cp "$aqui/mudanca.patch" "$destino/diff.patch"
cp "$aqui/mapa-de-fluxos.md" "$destino/mapa-de-fluxos.md"

./vendor/bin/pest > /dev/null
echo "Pronto: $destino (branch feature/aprovar-pela-lista, Pest verde)"
