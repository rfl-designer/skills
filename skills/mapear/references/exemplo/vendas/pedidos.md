# Pedidos

O cliente monta o carrinho, finaliza o pedido, acompanha a lista de pedidos e cancela um pedido pendente. Toda noite, o sistema fecha o dia e envia um resumo ao administrador.

Âncoras: `rota:pedidos.*`, `rota:carrinho`, `rota:checkout`, `livewire:carrinho`, `livewire:pedidos.tabela`, `comando:pedidos:fechar-dia`, `agenda:pedidos:fechar-dia`, `notificacao:PedidoConfirmado`, `notificacao:ResumoDoDia`, `flag:checkout-pix`
Estado: conduzida em 2026-10-28, commit 3f9c2ab

## Sub-features

- `pedidos-carrinho`: adiciona e remove produtos; o total muda na hora.
- `pedidos-checkout`: confirma o pedido e envia o e-mail de confirmação.
- `pedidos-checkout-pix`: mostra o pagamento por Pix quando a flag `checkout-pix` está ativa.
- `pedidos-lista`: lista os pedidos do cliente, com filtro por estado e estado vazio.
- `pedidos-cancelar`: cancela um pedido pendente depois de uma confirmação.
- `pedidos-fechar-dia`: fecha o dia e envia o resumo, pela agenda ou pelo comando.

## Como chegar (visão do usuário)

- Escolha `Adicionar ao carrinho` na página de um produto.
- Escolha o ícone `Carrinho` no topo para abrir o carrinho, ou abra `/carrinho`.
- Escolha `Finalizar pedido` no carrinho.
- Escolha `Meus pedidos` no menu da conta, ou abra `/pedidos`.
- Escolha `Cancelar` na linha de um pedido pendente.
- A agenda fecha o dia às 23h50. O administrador também roda `php artisan pedidos:fechar-dia`.

## Como conduzir

Pré-condições:

- Banco local com seed recente.
- Nenhum pedido pendente do `cliente@loja.test`.
- Flag `checkout-pix` inativa, exceto no item Pix.

- **Adicionar ao carrinho.** Ação: escolha `Adicionar ao carrinho` em `Caneca Azul`. Conduza: `./vendor/bin/pest --agent='$this->actingAs(App\Models\User::firstWhere("email", "cliente@loja.test")); visit("/produtos/caneca-azul")->click("Adicionar ao carrinho")->assertSee("1 item");'`. Resultado: o contador do carrinho mostra `1 item`.
- **Finalizar pedido.** Ação: abra o carrinho e escolha `Finalizar pedido`. Conduza no navegador configurado, com a sessão do cliente. Resultado: a página mostra `Pedido confirmado` e o número do pedido.
- **Conferir o efeito.** Conduza: `php artisan tinker --execute='echo App\Models\Pedido::latest("id")->value("estado");'`. Resultado: `pendente`. O Mailpit mostra `Pedido confirmado` para `cliente@loja.test`.
- **Lista vazia.** Ação: filtre `Meus pedidos` por `Entregue`. Resultado: a lista mostra `Nenhum pedido entregue`.
- **Cancelar.** Ação: escolha `Cancelar` e depois `Voltar` no diálogo. Resultado: o pedido continua `pendente`. Ação: escolha `Cancelar` de novo e confirme. Resultado: a linha mostra `cancelado`. Recarregue a página: o estado continua `cancelado`.
- **Pix.** Ative a flag: `php artisan tinker --execute='Laravel\Pennant\Feature::for(App\Models\User::firstWhere("email", "cliente@loja.test"))->activate("checkout-pix");'`. Ação: finalize um pedido. Resultado: o checkout mostra `Pagar com Pix`. Desative a flag no fim com `deactivate`.
- **Fechar o dia.** Conduza: `php artisan pedidos:fechar-dia --data=2026-10-28`. Resultado: código de saída `0` e a saída `1 pedido fechado`. O Mailpit mostra `Resumo do dia 28/10/2026`.
- **Regressão.** Conduza: `./vendor/bin/pest tests/Feature/Pedidos`.
- **Prova.** Capture a lista depois do cancelamento em `vendas/pedidos/pedidos-cancelar.png` e a saída do fechamento em `vendas/pedidos/pedidos-fechar-dia.saida.log`, na pasta de evidências.

## Armadilhas

- O total do carrinho muda depois da resposta Livewire. Espere o texto novo antes de ler o valor.
- Sem `--data`, `pedidos:fechar-dia` usa o dia atual no fuso da loja. Passe `--data` para uma prova repetível.
- Sem worker de fila, o e-mail de confirmação não sai no app local. Rode `queue:work --once`.
- O seed cria pedidos antigos só para o administrador. A lista do cliente começa vazia.
