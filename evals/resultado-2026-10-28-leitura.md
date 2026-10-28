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
| Controle | `spec-cancelar-pedido.md` | Nenhuma. A Spec responde a quem cancela, em que status, o efeito no Saldo, a disputa com o comando de aprovação, as mensagens e o fora de escopo. O arquivo guarda a versão 2; a versão 1 está descrita no resultado. |
| Sem subagentes | `spec-aprovar-pedido.md` | O executor de `/especificar` não pode criar subagentes. |

## Método

- **Leitor:** 2 execuções por caso, com o prompt que a seção 6 da skill prevê sem o agente `leitor` registrado: o template, o SKILL.md, o modo e os ponteiros. Ferramentas pedidas: Read, Grep e Glob. O controle teve 2 versões, com 2 execuções cada.
- **Autor com subagentes:** 1 executor de `/especificar`, a partir da etapa 3, com o rascunho do caso Lacuna. O usuário não responde; o executor termina com a mensagem ao usuário e um anexo com as ferramentas usadas, o prompt enviado ao Leitor e o retorno bruto dele.
- **Autor com o retorno do Leitor:** 1 executor recebe o retorno real de Lacuna A e continua a partir da Conferência (etapa 3 do Processo do Autor).
- **Autor sem subagentes:** 1 executor com a instrução de não usar ferramentas de subagente, na versão `0558e08`. Depois da correção, 1 executor igual na versão `1e72ab3`.
- Modelo: os subagentes herdaram o modelo da sessão principal.

## Resultado: Leitor

Conferi cada achado no fixture. "Real" quer dizer: a pergunta não tem resposta no rascunho, ou o rascunho contradiz o código ou o glossário.

| Execução | Lacuna plantada | `[BLOCKER]` | `[IMPORTANTE]` | Estilo ou sem pergunta | Tempo e tokens |
|---|---|---|---|---|---|
| Lacuna A | achada, `[BLOCKER]` | 2 | 3 | 0 | 2,1 min; 91 mil |
| Lacuna B | achada, `[BLOCKER]` | 3 | 2 | 0 | 2,5 min; 95 mil |
| Tickets A | as 2 achadas: schema `[BLOCKER]`, Ponteiro `[IMPORTANTE]` | 4 | 6 | 0 | 4,2 min; 108 mil |
| Tickets B | as 2 achadas, as duas `[BLOCKER]` | 3 | 7 | 0 | 5,0 min; 111 mil |
| Controle v1 A | — | 2 | 0 | 0 | 2,7 min; 96 mil |
| Controle v1 B | — | 1 | 2 | 0 | 2,2 min; 92 mil |
| Controle v2 A | — | 0 | 1 | 0 | 2,8 min; 95 mil |
| Controle v2 B | — | 0 | 2 | 0 | 3,8 min; 102 mil |

- **Achados:** 38 no total. 37 são reais. 1 é contestável: no Controle v2 B, a seção 3 já diz que o botão aparece só nos Pedidos do próprio Cliente; falta só um teste com a visão do Gerente. Nenhum achado de estilo e nenhum achado sem pergunta concreta.
- **Paráfrase:** todas as execuções escreveram a Paráfrase antes dos achados. Em Lacuna A e B, a Paráfrase já mostra a lacuna: "A Spec não diz quando o Saldo cai hoje".
- **Lacunas não plantadas:** os Leitores acharam lacunas reais que o autor do fixture não viu. Exemplos: o comando de aprovação não tem Gerente para passar à Action; um Cupom acima de 100% deixa o Total a pagar negativo e aumenta o Saldo no Fechamento do Dia; o Ticket 2 pode ir para produção antes do Ticket 3.
- **Controle v1:** o autor escreveu o controle como "sem lacuna". Os dois Leitores acharam a mesma contradição: a seção 3 devolve 403 para todo Pedido não Pendente, e a seção 5 espera uma mensagem para um Pedido aprovado depois da carga da lista. Os dois também acharam a disputa com `pedidos:aprovar`. As duas lacunas são reais. O controle v2 corrige as duas e declara a disputa como risco aceito. Os dois Leitores do v2 reconheceram o risco declarado e não o apontaram como lacuna.
- **Concordância:** cada par achou os mesmos temas. Lacuna: 5 de 5. Tickets: 9 de 10, e cada Leitor teve 1 achado próprio. Controle v1 e v2: o mesmo achado principal.
- **Severidade:** a severidade de 6 temas mudou entre as duas execuções do mesmo caso, por exemplo o Ponteiro inexistente (`[IMPORTANTE]` em A, `[BLOCKER]` em B).
- **Só leitura:** depois das execuções, `diff -r` mostrou o projeto de cada execução igual ao fixture. Os Leitores eram subagentes gerais; a regra "só lê" ficou só na instrução.

## Resultado: Autor

| Execução | O que o agente fez | Resultado |
|---|---|---|
| Com subagentes | Neste ambiente, um subagente não cria outro. O executor não leu o rascunho no mesmo contexto. Ele ofereceu uma sessão nova, com o pedido pronto, e perguntou antes de gravar. | O caso com subagentes não rodou de ponta a ponta. O comportamento sem subagentes foi correto. |
| Sem subagentes, versão `0558e08` | Não leu o rascunho no mesmo contexto. Gravou a Spec com `não executada` e ofereceu a sessão nova depois da gravação. | Divergiu da execução anterior: a regra tinha duas leituras. Corrigida em `1e72ab3`. |
| Sem subagentes, versão `1e72ab3` | Não leu o rascunho no mesmo contexto. Antes de gravar, perguntou: leitura numa sessão nova, com o pedido pronto, ou gravação com `não executada`. Não gravou nada. | Passou. |
| Autor com o retorno do Leitor | Recebeu o retorno real de Lacuna A. Mostrou a Paráfrase idêntica ao retorno (comparação de texto). Deu 4 `perguntar` e 1 `corrigir`; a correção espera a confirmação, porque muda a entrada da Costura. Não contestou nenhum achado e não mudou nenhuma severidade. Fez só a pergunta da Paráfrase e anunciou as outras. Não gravou a Spec nem alterou o rascunho. Avisou que o Leitor era um subagente geral. Anunciou a 2ª leitura, porque houve `[BLOCKER]`. | Passou. |

## Critérios de `cenarios.md`

| Cenário | Resultado |
|---|---|
| Leitura: lacuna plantada | Passou. Leitor: 2 de 2. Autor com o retorno: 1 de 1. |
| Leitura: decisão aberta no ticket | Passou: 2 de 2. Nenhum Leitor escolheu o schema nem editou arquivos. |
| Leitura: Spec sem lacuna (controle) | Versão 1: o fixture tinha 2 lacunas reais, e os 2 Leitores as acharam. Versão 2: passou, 2 de 2, com 1 achado contestável. |
| Leitura sem subagentes | Versão `0558e08`: 1 de 2. Versão `1e72ab3`: 1 de 1. |

## Mudanças depois da execução

- Sem subagentes, o Autor pergunta antes de gravar (`1e72ab3`).
- O rascunho de controle passou à versão 2.

## Limites

- O autor da skill escreveu os fixtures, executou e avaliou. Os agentes avaliados não viram a rubrica, mas a avaliação não é independente.
- O caso "o Autor dispara o Leitor" não rodou de ponta a ponta: neste ambiente, um subagente não cria outro. O Autor foi testado em duas partes: sem subagentes, e com um retorno real entregue.
- Os Leitores eram subagentes gerais. A regra "só lê" ficou só na instrução; o template `leitor` com `tools: Read, Grep, Glob` não foi testado.
- No modo Tickets, cada Leitor devolveu 10 achados. Todos eram reais, mas o volume pesa para o usuário. O nível 2 deve medir se o usuário responde aos achados ou pula a etapa.
- A severidade variou entre execuções do mesmo caso. Duas leituras do mesmo rascunho podem dar vereditos diferentes.
- 2 execuções por caso, com um só modelo. A amostra é pequena.

## Pendente: nível 2

Rodar `/implementar` num app Laravel de teste com a mesma Spec, com e sem a Leitura Independente. Contar as decisões silenciosas do implementador e os achados de `/revisar`. Repetir as execuções e alternar a ordem das versões.
