# Spec 0005 — Aprovar Pedido pela lista

## 1. Problema e Comportamento Observável
Hoje, o Gerente pede ao suporte para rodar o comando `pedidos:aprovar`. Com esta entrega, o Gerente aprova um Pedido Pendente na lista de pedidos. A Aprovação grava o status Aprovado, a data e a hora da aprovação e o Gerente que aprovou. O Cliente recebe o e-mail "Pedido aprovado" uma só vez. O Saldo não muda na Aprovação: o Fechamento do Dia debita o Saldo dos Pedidos aprovados no dia.

## 2. Vocabulário de Domínio
- `StatusPedido` (existente): Pendente, Aprovado, Cancelado.
- Termos do glossário: Pedido, Gerente, Aprovação, Fechamento do Dia, Saldo.
- **Aprovador:** o Gerente que aprovou o Pedido. Coluna nova `pedidos.aprovado_por`, nula até a Aprovação.

## 3. Fronteiras do Sistema
- **Lista de pedidos (Livewire, existente):** ganha a ação Aprovar, que recebe o ID do Pedido. A ação carrega o Pedido e chama a regra `aprovar` da Policy de Pedido (existente): só o Gerente, só Pedido Pendente. Fora dessa regra, a ação devolve 403.
- A lista do Gerente mostra a coluna "Aprovado por", com o nome do Aprovador, e o botão Aprovar nos Pedidos Pendentes.
- **Comando `pedidos:aprovar` (existente):** passa a usar a mesma Costura. Ele recebe o Gerente na opção obrigatória `--gerente=<id>` e grava esse Gerente como Aprovador. Ele continua a recusar o Pedido que não está Pendente, com a mensagem atual e o código de saída de falha.

## 4. Módulo Profundo e Costura
- Action nova `AprovarPedido::handle(Pedido $pedido, User $gerente): Pedido`.
- Invariante: a Action só muda um Pedido Pendente. Aprovar 2 vezes o mesmo Pedido, também com 2 cliques ao mesmo tempo, grava uma só Aprovação e envia um só e-mail.
- A Action grava status, `aprovado_em` e `aprovado_por` numa transação. O e-mail sai depois do commit da transação.

## 5. Plano de Testes na Costura (Pest)
- Action: aprova um Pedido Pendente; status Aprovado, `aprovado_em` e `aprovado_por` gravados; um e-mail ao Cliente.
- Action: um Pedido Aprovado ou Cancelado não muda, e nenhum e-mail sai.
- Action: 2 chamadas para o mesmo Pedido gravam uma Aprovação e enviam um e-mail.
- Livewire: o Gerente aprova; o Cliente recebe 403, e o Pedido não muda.
- Comando: grava o Gerente de `--gerente`; recusa o Pedido que não está Pendente.

## 6. Fora de Escopo
- Desfazer a Aprovação.
- Aprovação em lote.
- Paginação da lista de pedidos. A loja tem menos de 200 Pedidos por mês; a lista sem paginação é aceita nesta entrega.
