# Avaliação de nível 1 de `/revisar`: versão curta contra a atual

Data: 30/10/2026. Base do pacote: `63836f7`. Versão atual: `skills/revisar/SKILL.md` nesse commit (3.662 palavras). Candidata: a mesma skill sem repetição (2.884 palavras, −21%). Executor e avaliador: o autor das duas versões, no papel de agente principal. Os revisores foram subagentes gerais novos, sem o histórico da sessão e sem o gabarito.

Esta avaliação mede o trabalho do revisor: as etapas 3 e 4, que o subagente executa. Ela não mede a Consolidação, o relatório nem as rodadas seguintes, que o agente principal executa.

## Fixture

[Fixtures](fixtures/revisar/README.md): o Gerente aprova o Pedido pela lista. A mudança cria a Action `AprovarPedido`, a coluna `aprovado_por`, a notificação `PedidoAprovado`, a ação Aprovar no componente da lista e um teste. Ela também troca o comando `pedidos:aprovar` para usar a Action.

| Defeito plantado | Onde | Caso concreto | Eixo esperado |
|---|---|---|---|
| D1. Ação sem autorização | `Lista::aprovar` | Um Cliente chama `aprovar` com o ID do próprio Pedido. O Pedido fica Aprovado, com o Cliente como Aprovador. | Standards |
| D2. Aprovação repetida | `AprovarPedido::handle` | Dois cliques ao mesmo tempo passam pela Policy. A Action grava 2 vezes e envia 2 e-mails. A Spec exige uma Aprovação e um e-mail. | Standards ou Spec |
| D3. Gerente errado no comando | comando `pedidos:aprovar` | O comando ignora `--gerente` e grava o primeiro Gerente do banco como Aprovador. | Spec |
| D4. Comando sem a recusa do status | comando `pedidos:aprovar` e `FecharDia`, fora do diff | O suporte roda o comando num Pedido aprovado ontem. `aprovado_em` passa a hoje, e o Fechamento do Dia debita o Saldo de novo. Um Pedido Cancelado também vira Aprovado. | Spec |
| D5. Teste que não prova | `tests/Feature/AprovarPedidoTest.php` | `expect($resultado)->not->toBeNull()` passa com a Costura sem gravar nada. Faltam os casos do plano de testes da Spec. | Spec |
| D6. N+1 do Aprovador | lista do Gerente | A consulta carrega `cliente.user`, mas a view lê `aprovador`: uma query por linha. | Standards |

Controles, que não são defeitos: C1, a migration só acrescenta uma coluna nula; C2, o e-mail sai depois do commit, como a Spec pede; C3, a lista sem paginação, que a Spec aceita para menos de 200 Pedidos por mês.

## Método

- **Execuções:** 2 versões × 2 eixos × 2 repetições = 8 revisores, todos ao mesmo tempo. Ordem de envio: atual, curta, curta, atual, curta, atual, atual, curta.
- **Cegueira:** cada revisor recebeu uma pasta própria, com o SKILL.md no mesmo caminho. Nada no prompt ou na pasta dizia a versão.
- **Prompt:** o contrato da seção 4 de `/revisar` sem o agente `revisor` registrado: o template, o caminho do SKILL.md, o eixo e os Ponteiros de Contexto. Ferramentas pedidas: Read, Grep e Glob.
- **Pontuação:** um defeito conta como achado quando um achado numerado descreve o defeito e o seu efeito. D4 conta como parcial quando o achado não chega ao Fechamento do Dia nem ao Pedido Cancelado. A cobertura de uma versão numa repetição é a união dos 2 eixos.
- **Preservação das regras:** um subagente geral novo comparou as 2 versões regra a regra, sem saber da avaliação dos revisores.
- **Só leitura:** antes e depois, comparei o `md5sum` de cada arquivo de cada pasta.
- Modelo: os subagentes herdaram o modelo da sessão principal.

## Resultado

Pendente: as 8 execuções e a comparação de regras ainda não terminaram. Até o resultado, `skills/revisar/SKILL.md` continua na versão atual.
