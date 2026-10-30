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

## Resultado: revisores

"Sim" quer dizer achado numerado. "Nota" quer dizer que o revisor descreveu o defeito fora do seu eixo, sem número, para a Consolidação.

| Execução | D1 | D2 | D3 | D4 | D5 | D6 | Controles apontados | Tokens e tempo |
|---|---|---|---|---|---|---|---|---|
| Atual, Standards A | sim | sim | sim | sim | sim | sim | 0 | 144 mil; 6,5 min |
| Atual, Standards B | sim | sim | sim | sim | sim | sim | 0 | 143 mil; 6,6 min |
| Atual, Spec A | sim | sim | sim | sim | sim | nota | 0 | 137 mil; 6,1 min |
| Atual, Spec B | sim | sim | sim | sim | sim | nota | 0 | 133 mil; 5,2 min |
| Curta, Standards A | sim | sim | sim | sim | sim | sim | 0 | 127 mil; 4,4 min |
| Curta, Standards B | sim | sim | sim | sim | sim | sim | 0 | 138 mil; 6,6 min |
| Curta, Spec A | sim | sim | sim | sim | sim | nota | 0 | 137 mil; 6,0 min |
| Curta, Spec B | sim | sim | sim | sim | sim | nota | 0 | 126 mil; 4,5 min |

- **Defeitos plantados:** cada versão achou os 6 em cada repetição, pela união dos 2 eixos. Cada revisor de Standards achou os 6; cada revisor de Spec achou os 5 do seu eixo e deixou o N+1 como nota. D4 chegou ao Fechamento do Dia ou ao Pedido Cancelado nas 8 execuções.
- **Controles:** nenhuma execução apontou a migration, o e-mail depois do commit ou a lista sem paginação como defeito. Todas citaram a Spec ao aceitar a lista sem paginação.
- **Formato:** as 8 execuções deram as 4 partes a cada achado, com `arquivo:linha`, e status aos 8 arquivos do diff e aos 5 Fluxos. Várias acrescentaram consumidores ao Mapa: `routes/web.php`, `routes/console.php` e `User`.
- **Defeitos reais não plantados:** o `User` da fixture não usa `Notifiable`, então `notify()` falha. A versão atual numerou esse defeito em 3 de 4 execuções; a curta, em 1 de 4. As outras 4 o puseram em `Não verificado`, porque a fixture não tem `vendor/`. A janela entre o Fechamento das 23h59 e a meia-noite, anterior ao diff, foi numerada em 3 de 4 (atual) e 2 de 4 (curta). Com 4 execuções por versão, a diferença pode ser acaso: a etapa 4, que pede a confirmação do fato, tem o mesmo texto nas 2 versões.
- **Severidade:** igual nos defeitos plantados. A janela das 23h59 recebeu `[BLOCKER]` em 2 execuções, uma de cada versão, embora seja anterior ao diff.
- **Custo:** a curta usou em média 132 mil tokens e 5,4 min; a atual, 139 mil e 6,1 min. A diferença é pequena para 4 execuções.
- **Só leitura:** o `md5sum` das 8 pastas ficou igual.

## Resultado: preservação das regras

O inventário da versão testada achou perdas reais, quase todas na parte do agente principal:
- o status `corrigido` em `Achados anteriores:`;
- "Não repita a suíte apenas por entrar na revisão";
- a referência do diff passada aos revisores;
- "tabela" no Raio de Explosão e o limite de "40 linhas de alto sinal" como proibição;
- a posição de `Rodada:` e de `Achados anteriores:`;
- a regra "Limite o ciclo com `/ajustar`" e a definição de vaivém;
- os detalhes dos critérios de saída: comandos e escopos do portão, Fluxos das correções, fato provado por execução.

Na parte do revisor, a versão testada estreitou 2 regras: "propriedade pública" no lugar de propriedade sensível ou ID, e "ação que grava" no lugar de ação mutável. A fixture não exercita essa diferença.

A versão corrigida devolve cada perda e cada regra estreitada ao texto da versão atual. Ela tem 3.218 palavras (−12%). Na parte do revisor, ela difere da versão testada só por voltar ao texto da versão atual.

Pendente: um leitor novo confere a versão corrigida. Até essa conferência, `skills/revisar/SKILL.md` continua na versão atual.
