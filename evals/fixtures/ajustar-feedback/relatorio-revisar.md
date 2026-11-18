Alvo: `master...feature/estorno` em `feature/estorno`.
Rodada: 1
O que a mudança faz: A lista de pedidos ganha a ação `estornar`. O Gerente estorna um Pedido Aprovado: numa só transação, o Pedido passa a Cancelado e o total volta ao Saldo do Cliente.

Standards: sem achados.
Spec: sem achados.

Fluxos rastreados:
- `pedidos.status` (Cancelado) e `clientes.saldo_centavos`: `Lista::estornar` (app/Livewire/Pedidos/Lista.php:15-25) → `FecharDia::handle` (app/Actions/FecharDia.php:17-18, lê só Aprovado), `PedidoPolicy` (app/Policies/PedidoPolicy.php:20, 26), lista (resources/views/livewire/pedidos/lista.blade.php:8): verificado.
Carga presumida: 1 servidor, até 200 Pedidos por mês, fila `sync`.
Descartados: Standards 0; Spec 0.
Veredito: pode entregar.
