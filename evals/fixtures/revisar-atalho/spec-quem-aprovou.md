# Spec 0006 — Quem aprovou o Pedido

## 1. Problema e Comportamento Observável
Hoje, o suporte aprova o Pedido com o comando `pedidos:aprovar`, a pedido do Gerente, e ninguém sabe depois qual Gerente pediu. Com esta entrega, o comando grava o Gerente que pediu como Aprovador. A lista do Gerente mostra, em cada Pedido aprovado, o nome do Aprovador.

## 2. Vocabulário de Domínio
- Termos do glossário: Pedido, Gerente, Aprovação.
- **Aprovador:** o Gerente que pediu a Aprovação. Coluna nova `pedidos.aprovado_por`, nula até a Aprovação.

## 3. Fronteiras do Sistema
- **Comando `pedidos:aprovar` (existente):** recebe o Gerente na opção obrigatória `--gerente=<id>` e grava esse Gerente como Aprovador. Ele continua a recusar o Pedido que não está Pendente, com a mensagem atual e o código de saída de falha.
- **Lista de pedidos (Livewire, existente):** a lista do Gerente ganha a coluna com o nome do Aprovador. A lista do Cliente não muda.

## 4. Plano de Testes (Pest)
- Comando: grava o Gerente de `--gerente`.
- Lista: o Gerente vê o nome do Aprovador.

## 5. Fora de Escopo
- Aprovar pela lista.
- Paginação da lista de pedidos. A loja tem até 200 Pedidos por mês.
