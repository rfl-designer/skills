# Jornadas entre Features

Jornadas que passam por várias Features. Os seletores e comandos ficam nos Arquivos de Feature; leia-os antes. As pré-condições base do [índice](README.md) valem aqui.

## Pedido entre duas sessões

- Features: [Acesso](conta/acesso.md) e [Pedidos](vendas/pedidos.md).
- Entre como `cliente@loja.test`, finalize um pedido e saia. Entre de novo e abra `Meus pedidos`.
- Resultado: o pedido aparece uma vez, com estado `pendente`. O Mailpit tem um só e-mail de confirmação.

## Sessão expirada no checkout

- Features: [Acesso](conta/acesso.md) e [Pedidos](vendas/pedidos.md).
- Adicione um produto ao carrinho. Apague o cookie de sessão e escolha `Finalizar pedido`.
- Resultado: o app pede login. Depois do login, o carrinho volta com o produto.
