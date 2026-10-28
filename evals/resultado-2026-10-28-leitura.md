# Avaliação de nível 1 de `leitura-independente`

Data: 28/10/2026. Base do pacote: `ca76d17`; candidato: alterações no working tree desta sessão. Executor e avaliador: o autor da skill, no papel de agente principal. Os agentes avaliados foram subagentes gerais novos, sem o histórico desta sessão e sem a rubrica.

Esta avaliação é de nível 1: ela mede decisões do Leitor e do Autor em fixtures com lacunas plantadas. Ela não mede o efeito no implementador nem compara com a versão anterior. Esse é o nível 2, ainda pendente.

## Fixture

[Fixtures](fixtures/leitura-independente/README.md): um app Laravel mínimo, só para leitura, com Pedido, Cliente, Saldo, Cupom, a Action `FecharDia`, o comando `pedidos:aprovar`, a Policy de Pedido e o componente da lista de pedidos. O app não roda.

Cada execução recebeu uma cópia do projeto, do rascunho e das skills numa pasta própria, fora do repositório. Nenhum agente recebeu `evals/cenarios.md` nem este arquivo.

| Caso | Rascunho | Lacuna plantada |
|---|---|---|
| Lacuna | `spec-aprovar-pedido.md` | A Spec debita o Saldo na Aprovação. O glossário e `FecharDia` já debitam o Saldo dos Pedidos aprovados no Fechamento do Dia. A Spec não cita o Fechamento do Dia. Resultado: débito em dobro. Todos os termos estão definidos. |
| Tickets | `tickets-aplicar-cupom.md`, com a Spec aprovada `spec-aplicar-cupom.md` | Ticket 1 deixa ao implementador as colunas, os tipos, a chave estrangeira e o valor vazio do Cupom e do Desconto. Ticket 2 manda modificar `app/Livewire/Pedidos/Detalhe.php` e a view de detalhe, que não existem. |
| Controle | `spec-cancelar-pedido.md` | Nenhuma. A Spec responde a quem cancela, em que status, o efeito no Saldo, a condição de corrida, as mensagens e o fora de escopo. |
| Sem subagentes | `spec-aprovar-pedido.md` | O executor de `/especificar` não pode criar subagentes. |

## Método

- **Leitor:** 2 execuções por caso, com o prompt que a seção 6 da skill prevê sem o agente `leitor` registrado: o template, o SKILL.md, o modo e os ponteiros. Ferramentas pedidas: Read, Grep e Glob.
- **Autor com subagentes:** 1 executor de `/especificar`, a partir da etapa 3, com o rascunho do caso Lacuna. O usuário não responde; o executor termina com a mensagem ao usuário e um anexo com as ferramentas usadas, o prompt enviado ao Leitor e o retorno bruto dele.
- **Autor sem subagentes:** 1 executor igual, com a instrução de não usar ferramentas de subagente.
- Modelo: o subagente herdou o modelo da sessão principal.
