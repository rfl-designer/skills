# Spec 0003 — Aplicar Cupom ao Pedido

## 1. Problema e Comportamento Observável
O Cliente não tem onde usar um Cupom. Com esta entrega, o Cliente digita o código de um Cupom na tela de detalhe de um Pedido Pendente seu. Com um Cupom Válido, a tela mostra o Desconto e o Total a pagar. Com um Cupom inválido, nada muda e a tela mostra o motivo.

## 2. Vocabulário de Domínio
- Cupom (existente): código, percentual, data de validade e indicador de ativo.
- **Cupom Válido** (termo novo): Cupom ativo, com a data de hoje até a data de validade, inclusive, no fuso da aplicação.
- **Desconto** (termo novo): percentual do Cupom sobre o total do Pedido, em centavos, arredondado para baixo.
- **Total a pagar** (termo novo): total do Pedido menos o Desconto. O total do Pedido não muda.
- `StatusPedido` (existente): Pendente, Aprovado, Cancelado.

## 3. Fronteira do Sistema (Livewire)
- Componente novo: detalhe do Pedido, na rota de detalhe de um Pedido. A propriedade do Pedido usa `#[Locked]`.
- Abrir o detalhe exige a regra `view` da Policy de Pedido (existente).
- Campo do código: obrigatório, até 20 caracteres.
- Ação Aplicar: chama a regra nova `aplicarCupom` da Policy de Pedido: só o dono do Pedido, só Pedido Pendente.
- Mensagens: "Cupom aplicado", "Cupom inexistente", "Cupom vencido", "Cupom inativo" e "Este pedido já tem um cupom".

## 4. Módulo Profundo e Costura
- Costura proposta: Action `AplicarCupom`.
- Entrada: o Pedido e o código digitado.
- Saída: o Pedido com o Cupom e o Desconto gravados, ou um erro com o motivo: inexistente, vencido, inativo ou já aplicado.
- Invariantes: no máximo um Cupom por Pedido; o Pedido guarda o Cupom aplicado e o Desconto em centavos; o total do Pedido não muda.
- O Fechamento do Dia passa a debitar o Total a pagar, não o total do Pedido.
- Justificativa da Action: regra de validade e cálculo com quatro erros de domínio.

## 5. Plano de Testes na Costura (Pest)
- Action: um Cupom Válido grava o Cupom e o Desconto; 10% sobre 999 centavos dá Desconto de 99.
- Action: um Cupom vencido, inativo ou inexistente devolve o motivo e não muda o Pedido.
- Action: um segundo Cupom no mesmo Pedido devolve "já aplicado".
- Action: um Cupom com validade hoje é válido.
- Livewire: o dono aplica um Cupom Válido e vê o Desconto e o Total a pagar.
- Livewire: outro Cliente recebe 403.
- Livewire: um Pedido Aprovado não mostra o campo, e a ação devolve 403.
- Fechamento do Dia: debita o Total a pagar de um Pedido com Cupom.

## 6. Fora de Escopo
- Remover um Cupom aplicado.
- Limite de uso por Cupom ou por Cliente.
- Mais de um Cupom por Pedido.
