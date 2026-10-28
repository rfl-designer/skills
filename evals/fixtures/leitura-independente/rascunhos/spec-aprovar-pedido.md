# Spec 0002 — Aprovar Pedido na tela de pedidos

## 1. Problema e Comportamento Observável
Hoje, o Gerente pede ao suporte a Aprovação de cada Pedido, e o suporte roda um comando. A espera chega a um dia. Com esta entrega, o Gerente aprova um Pedido Pendente direto na lista de pedidos. Na Aprovação, o Saldo do Cliente cai no total do Pedido, e a lista mostra o Saldo novo.

## 2. Vocabulário de Domínio
- `StatusPedido` (existente): Pendente, Aprovado, Cancelado.
- Termos do glossário: Pedido, Cliente, Saldo, Gerente, Aprovação.

## 3. Fronteira do Sistema (Livewire)
- Componente da lista de pedidos (existente). Ele ganha a ação Aprovar, que recebe o ID do Pedido.
- O botão Aprovar aparece só para o Gerente e só em Pedido Pendente.
- A ação carrega o Pedido e chama a regra `aprovar` da Policy de Pedido (existente): só o Gerente, só Pedido Pendente.
- Depois da Aprovação, a lista mostra a mensagem "Pedido aprovado" e o Saldo atual do Cliente na linha do Pedido.

## 4. Módulo Profundo e Costura
- Costura proposta: Action `AprovarPedido`.
- Entrada: o Pedido e o Gerente.
- Efeito, numa transação: o status passa a Aprovado, a data e a hora da Aprovação ficam gravadas e o Saldo do Cliente cai no total do Pedido.
- Invariante: só um Pedido Pendente muda. Se o status mudou depois da carga, nada muda e a Action informa "O pedido não está mais pendente".
- O comando do suporte passa a chamar a mesma Action.
- Justificativa da Action: duas escritas na mesma transação e duas Fronteiras (tela e comando).

## 5. Plano de Testes na Costura (Pest)
- Action: um Pedido Pendente passa a Aprovado, com a data da Aprovação, e o Saldo do Cliente cai no total.
- Action: um Pedido Aprovado ou Cancelado não muda, e o Saldo não muda.
- Livewire: o Gerente aprova; a lista mostra "Pedido aprovado" e o Saldo novo.
- Livewire: um Cliente que chama a ação recebe 403, e o Pedido não muda.
- Comando: `pedidos:aprovar` aprova pela mesma Action.

## 6. Fora de Escopo
- Desfazer uma Aprovação.
- Aprovar vários Pedidos de uma vez.
- Notificar o Cliente.
