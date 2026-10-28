# Spec 0004 — Cancelar Pedido Pendente

## 1. Problema e Comportamento Observável
Hoje, o Cliente pede ao suporte para desistir de um Pedido. Com esta entrega, o Cliente cancela um Pedido Pendente seu na lista de pedidos, depois de confirmar. O Pedido passa a Cancelado. O Saldo não muda, porque o Fechamento do Dia só debita Pedidos aprovados.

## 2. Vocabulário de Domínio
- `StatusPedido` (existente): Pendente, Aprovado, Cancelado.
- Termos do glossário: Pedido, Cliente, Saldo, Fechamento do Dia.

## 3. Fronteira do Sistema (Livewire)
- Componente da lista de pedidos (existente). Ele ganha a ação Cancelar, que recebe o ID do Pedido.
- O botão Cancelar aparece só nos Pedidos Pendentes do próprio Cliente. O botão pede confirmação com o texto "Cancelar este pedido?".
- A ação carrega o Pedido e chama a regra `cancelar` da Policy de Pedido (existente): só o dono do Pedido, só Pedido Pendente. Fora dessa regra, a ação devolve 403.
- Depois do cancelamento, a lista mostra a mensagem "Pedido cancelado" e o status Cancelado na linha do Pedido.

## 4. Módulo Profundo e Costura
- Sem Action nova. A ação do componente atualiza o status para Cancelado: é uma só escrita, sem efeito colateral.
- Invariante: a atualização só muda um Pedido ainda Pendente. Se o status mudou depois da carga, nada muda e a lista mostra "Este pedido não está mais pendente".
- A data da Aprovação continua vazia.

## 5. Plano de Testes na Costura (Pest)
- Livewire: o dono cancela um Pedido Pendente seu; o status passa a Cancelado e a lista mostra "Pedido cancelado".
- Livewire: o Saldo do Cliente não muda depois do cancelamento.
- Livewire: um Pedido Aprovado ou Cancelado devolve 403 e não muda.
- Livewire: o Pedido de outro Cliente devolve 403 e não muda.
- Livewire: um Pedido aprovado entre a carga e a ação não muda, e a lista mostra "Este pedido não está mais pendente".
- Livewire: o botão Cancelar aparece só nos Pedidos Pendentes do próprio Cliente.

## 6. Fora de Escopo
- Cancelar um Pedido Aprovado.
- Cancelamento pelo Gerente.
- Reabrir um Pedido Cancelado.
- Motivo e data do cancelamento.
- Notificar o Cliente ou o Gerente.
