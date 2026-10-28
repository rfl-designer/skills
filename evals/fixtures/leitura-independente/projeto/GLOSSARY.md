# Glossário

- **Cliente:** pessoa que faz Pedidos. Cada Cliente tem um Saldo.
- **Saldo:** crédito do Cliente na loja, em centavos.
- **Pedido:** compra de um Cliente. Tem um total em centavos e um status: Pendente, Aprovado ou Cancelado.
- **Gerente:** usuário com o papel `gerente`. Só o Gerente aprova Pedidos.
- **Aprovação:** passagem de um Pedido de Pendente para Aprovado. Grava a data e a hora da aprovação.
- **Fechamento do Dia:** rotina agendada às 23h59. Debita do Saldo de cada Cliente o total dos Pedidos aprovados no dia.
- **Cupom:** código de desconto com percentual, data de validade e indicador de ativo.
