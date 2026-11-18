# Mapa de Fluxos

Alvo: `master...feature/quem-aprovou`. Montado por busca com `rg` no estado da branch.

- `pedidos.aprovado_por` e `Pedido::aprovador()`: entrada comando `pedidos:aprovar` (app/Console/Commands/AprovarPedido.php:21, 32) → consumidores: relação (app/Models/Pedido.php:33-36), `$fillable` (app/Models/Pedido.php:18), lista do Gerente (resources/views/livewire/pedidos/lista.blade.php:9), consulta da lista (app/Livewire/Pedidos/Lista.php:17-19), migration (database/migrations/2026_11_10_000004_add_aprovado_por_to_pedidos_table.php:14).
- `pedidos.aprovado_em`, exibido: entrada comando `pedidos:aprovar` (app/Console/Commands/AprovarPedido.php:31) → consumidores: lista do Gerente (resources/views/livewire/pedidos/lista.blade.php:10), `FecharDia::handle` (app/Actions/FecharDia.php:18), sem mudança.
- Assinatura do comando `pedidos:aprovar {pedido} {--gerente=}`: nenhum chamador no repositório; o suporte roda o comando à mão.
