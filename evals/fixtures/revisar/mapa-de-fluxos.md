# Mapa de Fluxos

Alvo: `master...feature/aprovar-pela-lista`. Montado por busca com `rg` no estado da branch.

- `pedidos.status` e `pedidos.aprovado_em`: entrada `Lista::aprovar` (app/Livewire/Pedidos/Lista.php:14-18) e comando `pedidos:aprovar` (app/Console/Commands/AprovarPedido.php:18-23) → `AprovarPedido::handle` (app/Actions/AprovarPedido.php:15-23) → consumidores: `FecharDia::handle` (app/Actions/FecharDia.php:17-18), `PedidoPolicy::aprovar` e `PedidoPolicy::cancelar` (app/Policies/PedidoPolicy.php:20, 26), lista (resources/views/livewire/pedidos/lista.blade.php:7, 11).
- `pedidos.aprovado_por` e `Pedido::aprovador()`: entrada `AprovarPedido::handle` (app/Actions/AprovarPedido.php:21), com o Gerente de `Lista::aprovar` (app/Livewire/Pedidos/Lista.php:18) e do comando (app/Console/Commands/AprovarPedido.php:21) → consumidores: relação (app/Models/Pedido.php:28-31), lista (resources/views/livewire/pedidos/lista.blade.php:9), migration (database/migrations/2026_10_30_000004_add_aprovado_por_to_pedidos_table.php:14).
- `AprovarPedido::handle(Pedido, User): Pedido`, assinatura nova: chamadores `Lista::aprovar` (app/Livewire/Pedidos/Lista.php:18), comando (app/Console/Commands/AprovarPedido.php:23), teste (tests/Feature/AprovarPedidoTest.php:18).
- Notificação `PedidoAprovado`: entrada `AprovarPedido::handle` (app/Actions/AprovarPedido.php:25) → saída: e-mail (app/Notifications/PedidoAprovado.php:24-27).
- Assinatura do comando `pedidos:aprovar {pedido} {--gerente=}`: nenhum chamador no repositório; o suporte roda o comando à mão.
