# Spec 0004 — Cancelar Pedido Pendente

## 1. Problema e Comportamento Observável
Hoje, o Cliente pede ao suporte para desistir de um Pedido. Com esta entrega, o Cliente cancela um Pedido Pendente seu na lista de pedidos, depois de confirmar. O Pedido passa a Cancelado. O Saldo não muda, porque o Fechamento do Dia só debita Pedidos aprovados.

## 2. Vocabulário de Domínio
- `StatusPedido` (existente): Pendente, Aprovado, Cancelado.
- Termos do glossário: Pedido, Cliente, Saldo, Fechamento do Dia.

## 3. Fronteira do Sistema (Livewire)
- Componente da lista de pedidos (existente). Ele ganha a ação Cancelar, que recebe o ID do Pedido.
- O botão Cancelar aparece só nos Pedidos Pendentes do próprio Cliente. O botão pede confirmação com o texto "Cancelar este pedido?".
- A ação carrega o Pedido do banco e chama a regra `cancelar` da Policy de Pedido (existente): só o dono do Pedido, só Pedido Pendente. Fora dessa regra, a ação devolve 403. Isso vale também para um Pedido que deixou de ser Pendente depois que a lista carregou.
- Depois do cancelamento, a lista mostra a mensagem "Pedido cancelado" e o status Cancelado na linha do Pedido.

## 4. Módulo Profundo e Costura
- Sem Action nova. A ação do componente atualiza o status para Cancelado: é uma só escrita, sem efeito colateral.
- Invariante: a escrita só muda o Pedido se ele ainda está Pendente no momento da gravação. Se ele não está, nada muda e a ação devolve 403.
- A data da Aprovação continua vazia.

## 5. Plano de Testes na Costura (Pest)
- Livewire: o dono cancela um Pedido Pendente seu; o status passa a Cancelado e a lista mostra "Pedido cancelado".
- Livewire: depois do cancelamento, o Fechamento do Dia roda e o Saldo do Cliente não muda.
- Livewire: um Pedido Aprovado ou Cancelado devolve 403 e não muda.
- Livewire: um Pedido aprovado depois que a lista carregou devolve 403 e não muda.
- Livewire: o Pedido de outro Cliente devolve 403 e não muda.
- Livewire: o botão Cancelar aparece só nos Pedidos Pendentes do próprio Cliente.

## 6. Fora de Escopo
- Cancelar um Pedido Aprovado.
- Cancelamento pelo Gerente.
- Reabrir um Pedido Cancelado.
- Motivo e data do cancelamento.
- Notificar o Cliente ou o Gerente.
- Mudar o comando `pedidos:aprovar`. Ele grava a Aprovação sem conferir o status de novo. Se o suporte aprova e o Cliente cancela no mesmo instante, o Pedido pode terminar Aprovado. O usuário aceitou esse risco nesta entrega: o suporte confere o status antes de rodar o comando.
