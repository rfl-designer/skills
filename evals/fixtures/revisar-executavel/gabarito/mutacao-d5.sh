#!/usr/bin/env bash
# D5. Mutação: a Action deixa de gravar. O teste do diff continua verde.
set -u
cd "$1"
cp app/Actions/AprovarPedido.php /tmp/AprovarPedido.php.orig
python3 - <<'PY'
import pathlib
p = pathlib.Path("app/Actions/AprovarPedido.php")
s = p.read_text()
s = s.replace("            $pedido->update([", "            $pedido->fill([", 1)
p.write_text(s)
PY
./vendor/bin/pest tests/Feature/AprovarPedidoTest.php --filter='aprova o pedido na Action'
status=$?
cp /tmp/AprovarPedido.php.orig app/Actions/AprovarPedido.php
exit $status
