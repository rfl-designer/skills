Alvo: `master...feature/quem-aprovou` em `feature/quem-aprovou`.
Rodada: 1
O que a mudança faz: O comando `pedidos:aprovar` grava o Gerente que pediu a Aprovação, na coluna nova `pedidos.aprovado_por`. A lista do Gerente mostra, em cada Pedido, o nome do Aprovador e a data da Aprovação.

## Standards

### [IMPORTANTE]

1. [IMPORTANTE] **N+1 do Aprovador na lista do Gerente** (`app/Livewire/Pedidos/Lista.php:18`, `resources/views/livewire/pedidos/lista.blade.php:9`)
   - **O que é:** A consulta da lista do Gerente carrega `cliente.user`, mas não `aprovador`. A view lê `$pedido->aprovador?->name` em cada linha.
   - **Problema:** Cada Pedido faz 1 consulta a mais. Com a carga presumida de 200 Pedidos, a lista faz 203 consultas no lugar de 5.
   - **Prova:** `./vendor/bin/pest tests/Feature/Revisao/AprovadorNMais1Test.php` imprime `Failed asserting that 203 is identical to 5.` e `Attempted to lazy load [aprovador] on model [App\Models\Pedido] but lazy loading is disabled.` A Spec não fixa o número de consultas; a carga presumida pede o mesmo número com 2 e com 200 Pedidos.
   - **Correção:** Em `Lista::render`, troque `with('cliente.user')` por `with(['cliente.user', 'aprovador'])`. Nada mais muda.
   - **Se não corrigir:** A lista do Gerente fica mais lenta a cada Pedido, e o próximo campo de relação na lista repete o defeito.
   - **Regra:** `Model::preventLazyLoading(! $this->app->isProduction())` no `AppServiceProvider::boot()`, proíbe carregar uma relação por linha numa coleção, mensagem "Carregamento preguiçoso de [<relação>] em [<Model>]. Acrescente [<relação>] ao with() da consulta que carregou a lista." por `Model::handleLazyLoadingViolationUsing()`.

Standards: 1 [IMPORTANTE]. Pior achado: 1.
Spec: sem achados.

Fluxos rastreados:
- `pedidos.aprovado_por`: `AprovarPedido::handle` (app/Console/Commands/AprovarPedido.php:29-33) → `Pedido::aprovador` (app/Models/Pedido.php:33-36) → lista do Gerente (resources/views/livewire/pedidos/lista.blade.php:9): verificado, com o achado 1.
Carga presumida: 1 servidor, até 200 Pedidos por mês, fila `sync`.
Descartados: Standards 0; Spec 0.
Veredito: corrija 1 antes.
Provas: `provas/` (caminho relativo `tests/Feature/Revisao/AprovadorNMais1Test.php`).
