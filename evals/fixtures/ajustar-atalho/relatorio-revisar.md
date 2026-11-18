Alvo: `master...feature/estorno` em `feature/estorno`.
Rodada: 1
O que a mudança faz: A lista de pedidos ganha a ação `estornar`. O Gerente estorna um Pedido Aprovado: o Pedido passa a Cancelado e o total volta ao Saldo do Cliente.

## Standards

### [BLOCKER]

1. [BLOCKER] **Estorno grava em 2 escritas sem transação** (`app/Livewire/Pedidos/Lista.php:20-21`)
   - **O que é:** A ação `estornar` passa o Pedido a Cancelado e, em seguida, devolve o total ao Saldo do Cliente.
   - **Problema:** As 2 escritas não estão numa transação. Se a devolução do Saldo falha, o Pedido fica Cancelado e o Saldo não volta. A Spec 0007 exige que as 2 escritas aconteçam juntas ou nenhuma aconteça.
   - **Prova:** `./vendor/bin/pest tests/Feature/Revisao/EstornoSemTransacaoTest.php` força uma falha na gravação do Cliente e imprime `Failed asserting that two variables reference the same object. -App\Enums\StatusPedido Enum (Aprovado, 'aprovado') +App\Enums\StatusPedido Enum (Cancelado, 'cancelado')`. A Spec exige o Pedido Aprovado e o Saldo `1000`.
   - **Correção:** Em `Lista::estornar`, envolva as 2 escritas em `DB::transaction()`. Nada mais muda.
   - **Se não corrigir:** Um erro no meio do estorno cancela o Pedido sem devolver o dinheiro, e o suporte corrige o Saldo à mão.

Standards: 1 [BLOCKER]. Pior achado: 1.
Spec: sem achados.

Fluxos rastreados:
- `pedidos.status` (Cancelado) e `clientes.saldo_centavos`: `Lista::estornar` (app/Livewire/Pedidos/Lista.php:14-22) → `FecharDia::handle` (app/Actions/FecharDia.php:17-18, lê só Aprovado), `PedidoPolicy` (app/Policies/PedidoPolicy.php:20, 26), lista (resources/views/livewire/pedidos/lista.blade.php:8): verificado, com o achado 1.
Carga presumida: 1 servidor, até 200 Pedidos por mês, fila `sync`.
Descartados: Standards 0; Spec 0.
Veredito: corrija 1 antes.
Provas: `provas/` (caminho relativo `tests/Feature/Revisao/EstornoSemTransacaoTest.php`).
