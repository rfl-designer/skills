# Tickets — Spec 0003, Aplicar Cupom ao Pedido

## Throughput Checkpoint
1. **Fundação Bloqueante:** O Pedido precisa guardar o Cupom e o Desconto antes da Action e do Fechamento do Dia.
2. **Frentes Paralelizáveis:** Depois do Ticket 1, os Tickets 2 e 3 não disputam arquivos.
3. **Estado Mutável Compartilhado:** `app/Models/Pedido.php` só no Ticket 1; `app/Policies/PedidoPolicy.php` só no Ticket 2.
4. **Menor Decomposição Segura:** 3 tickets.

## Ticket 1 — Guardar o Cupom e o Desconto no Pedido
- **Objetivo:** O Pedido guarda o Cupom aplicado e o Desconto.
- **Bloqueado por:** Nenhum.
- **Ponteiros de Contexto:** criar uma migration em `database/migrations/`; modificar `app/Models/Pedido.php`.
- **Tarefa:** Adicione ao Pedido os campos do Cupom e do Desconto, e a relação com o Cupom.
- **Critério de Aceite no Pest:** Um Pedido salvo com Cupom e Desconto devolve os dois valores e a relação.

## Ticket 2 — Aplicar Cupom na tela de detalhe
- **Objetivo:** O Cliente aplica um Cupom Válido num Pedido Pendente seu e vê o Desconto e o Total a pagar.
- **Bloqueado por:** Ticket 1.
- **Ponteiros de Contexto:** criar `app/Actions/AplicarCupom.php`; modificar `app/Livewire/Pedidos/Detalhe.php` e `resources/views/livewire/pedidos/detalhe.blade.php`; modificar `app/Policies/PedidoPolicy.php` (regra `aplicarCupom`); modificar `routes/web.php` (rota `pedidos.detalhe`, caminho `/pedidos/{pedido}`).
- **Tarefa:** A Action valida o Cupom pela seção 2 da Spec e devolve o motivo de cada erro da seção 4. O componente mostra as mensagens da seção 3.
- **Critério de Aceite no Pest:** Os testes da Action e do Livewire da seção 5 da Spec.

## Ticket 3 — Fechamento do Dia debita o Total a pagar
- **Objetivo:** O Fechamento do Dia debita o Total a pagar de cada Pedido aprovado no dia.
- **Bloqueado por:** Ticket 1.
- **Ponteiros de Contexto:** modificar `app/Actions/FecharDia.php`.
- **Tarefa:** Troque o valor debitado pelo total do Pedido menos o Desconto. Um Pedido sem Cupom tem Desconto zero.
- **Critério de Aceite no Pest:** O Fechamento do Dia com um Pedido com Cupom e outro sem Cupom debita o Total a pagar de cada um.
