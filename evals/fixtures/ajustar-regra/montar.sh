#!/usr/bin/env bash
# Monta uma pasta de execução da fixture de Regra de /ajustar.
# Uso: montar.sh <destino> <limpa|antigos> [<pasta com vendor/ pronto>]
# Com a terceira pasta, copia vendor/ com links físicos (cp -al). Sem ela, roda composer install.
set -euo pipefail

aqui="$(cd "$(dirname "$0")" && pwd)"
destino="${1:?informe a pasta de destino}"
variante="${2:?informe a variante: limpa ou antigos}"
vendor_pronto="${3:-}"

case "$variante" in
    limpa | antigos) ;;
    *) echo "Variante desconhecida: $variante (use limpa ou antigos)" >&2; exit 1 ;;
esac

if [ -e "$destino" ]; then
    echo "O destino já existe: $destino" >&2
    exit 1
fi

mkdir -p "$destino"
cp -r "$aqui/../revisar-executavel/projeto" "$destino/projeto"
cd "$destino/projeto"

mkdir -p bootstrap/cache storage/framework/cache storage/framework/sessions \
    storage/framework/testing storage/framework/views storage/logs docs/specs
cp "$aqui/../revisar-regra/spec-quem-aprovou.md" docs/specs/0006-quem-aprovou.md

# Na variante antigos, a base ganha 3 N+1 antigos, cada um com um teste de 2 registros.
git init -q -b master
if [ "$variante" = antigos ]; then
    git apply "$aqui/base-antigos.patch"
fi
git -c user.name=fixture -c user.email=fixture@example.com add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "base: loja"
git checkout -qb feature/quem-aprovou
git apply "$aqui/../revisar-regra/mudanca.patch"
git -c user.name=fixture -c user.email=fixture@example.com add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "feat: lista mostra quem aprovou o Pedido"

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
echo "Pronto: $destino (variante $variante, branch feature/quem-aprovou, Pest verde)"
