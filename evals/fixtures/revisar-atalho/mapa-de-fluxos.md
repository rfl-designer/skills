# Mapa de Fluxos

Alvo: `master...feature/quem-aprovou`. Montado por busca com `rg` no estado da branch.

- `pedidos.aprovado_por` e `Pedido::aprovador()`: entrada comando `pedidos:aprovar` (app/Console/Commands/AprovarPedido.php:25, 36) → consumidores: relação (app/Models/Pedido.php:38-41), `Pedido::nomeDoAprovador()` (app/Models/Pedido.php:43-47), `$fillable` (app/Models/Pedido.php:21), consulta da lista (app/Livewire/Pedidos/Lista.php:18), lista do Gerente (resources/views/livewire/pedidos/lista.blade.php:9), migration (database/migrations/2026_11_10_000004_add_aprovado_por_to_pedidos_table.php:14).
- Assinatura do comando `pedidos:aprovar {pedido} {--gerente=}`: nenhum chamador no repositório; o suporte roda o comando à mão.
