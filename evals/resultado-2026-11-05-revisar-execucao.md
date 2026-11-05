# Avaliação de nível 1 de `/revisar`: prova por execução

Data: 05/11/2026. Base do pacote: `8f9cf22`. Versão atual: `skills/revisar/SKILL.md` nesse commit (3.275 palavras), com o revisor só de leitura. Candidata: a versão com prova por execução, que adapta o `interrogate` do pstack em `ab1f702` (4.389 palavras, +34%). Executor e avaliador: o autor da candidata, no papel de agente principal. Os revisores foram subagentes gerais novos, sem o histórico da sessão e sem o gabarito.

Esta avaliação mede as etapas 3 e 4, que o revisor executa, e a Reexecução da etapa 5, que o principal executa na candidata. Ela não mede o relatório, as rodadas seguintes, o vaivém nem o limite de rodadas.

## Fixture

[Fixture executável](fixtures/revisar-executavel/README.md): a mesma mudança da [fixture de leitura](fixtures/revisar/README.md), num app Laravel 12 que roda. O Gerente aprova o Pedido pela lista. O [gabarito](fixtures/revisar-executavel/gabarito/GabaritoTest.php) prova cada defeito por execução.

| Defeito plantado | Caso concreto | Eixo esperado |
|---|---|---|
| D1. Ação sem autorização | Um Cliente chama `aprovar` com o ID de um Pedido. A ação devolve 200, e o Pedido fica Aprovado. | Standards |
| D2. Aprovação repetida | 2 chamadas à Action gravam 2 vezes e enviam 2 e-mails. | Standards ou Spec |
| D3. Gerente errado no comando | O comando ignora `--gerente` e grava o primeiro Gerente do banco. | Spec |
| D4. Comando sem a recusa do status | O comando aprova de novo um Pedido aprovado ontem, e o Fechamento do Dia debita 2 vezes. Um Pedido Cancelado vira Aprovado. | Spec |
| D5. Teste que não prova | Com a Action vazia, os 2 testes do diff continuam verdes. | Spec |
| D6. N+1 do Aprovador | A lista do Gerente faz 1 consulta por Pedido aprovado. | Standards |

Controles, que não são defeitos: C1, a coluna nova é nula; C2, o e-mail sai depois do commit; C3, a lista sem paginação, que a Spec aceita.

Defeito da base, fora do diff: um Pedido aprovado entre 23h59 e 0h nunca é debitado. A mesma prova falha na base.

## Método

- **Execuções:** 2 versões × 2 eixos × 2 repetições = 8 revisores, todos ao mesmo tempo.
- **Cegueira:** cada revisor recebeu uma pasta própria, montada por `montar.sh`, com o SKILL.md no mesmo caminho. Nada no prompt ou na pasta dizia a versão.
- **Prompt:** o contrato da seção 4 de `/revisar` sem o agente `revisor` registrado: o corpo do template, o caminho do SKILL.md, o eixo e os Ponteiros de Contexto.
  - Atual: ferramentas Read, Grep e Glob.
  - Candidata: ferramentas Read, Grep, Glob e Bash, e a pasta `projeto/` como worktree, com a guarda do ambiente de teste já feita.
- **`vendor/`:** as 8 pastas receberam `vendor/` com links físicos. Assim, a versão atual também podia ler o código do Livewire e do Laravel.
- **Reexecução:** para cada revisor da candidata, o principal copiou as provas para uma cópia limpa da head e para uma cópia da base e executou cada uma.
- **Pontuação:** um defeito conta como achado quando um achado numerado descreve o defeito e o seu efeito. "Nota" quer dizer que o revisor descreveu o defeito sem número, para o outro eixo ou para a Consolidação. A cobertura de uma versão numa repetição é a união dos 2 eixos.
- **Só leitura e produção intacta:** antes e depois, comparei o `md5sum` de cada arquivo de cada pasta, sem `vendor/` e sem `.git/`.
- **Modelo:** os subagentes herdaram o modelo da sessão principal.

## Resultado: revisores

| Execução | D1 | D2 | D3 | D4 | D5 | D6 | Ruído | Tokens e tempo |
|---|---|---|---|---|---|---|---|---|
| Atual, Standards A | sim | sim | sim | sim | sim | sim | 1 `[NIT]` de estrutura | 164 mil; 4,8 min |
| Atual, Standards B | sim | sim | sim | sim | sim | sim | 1 `[NIT]` de estrutura | 168 mil; 5,2 min |
| Atual, Spec A | sim | sim | sim | sim | sim | nota | 0 | 169 mil; 4,7 min |
| Atual, Spec B | sim | sim | sim | sim | sim | não | 0 | 162 mil; 4,6 min |
| Candidata, Standards A | sim | sim | nota | sim | nota, provada | sim | 0 | 170 mil; 6,5 min |
| Candidata, Standards B | sim | sim | nota | sim | nota | sim | 0 | 162 mil; 5,7 min |
| Candidata, Spec A | sim | sim | sim | sim | sim | não | 0 | 163 mil; 5,6 min |
| Candidata, Spec B | sim | sim | sim | sim | sim | não | 0 | 177 mil; 6,6 min |

- **Defeitos plantados:** cada versão achou os 6 em cada repetição, pela união dos 2 eixos.
  - Na atual, os 2 revisores de Standards numeraram os 6.
  - Na candidata, os revisores de Standards deixaram D3 e D5 como nota para o eixo Spec, e o eixo Spec os numerou.
- **Provas:** na candidata, os 17 achados numerados vieram com arquivo de prova, comando e saída. A Reexecução confirmou os 17 na head limpa. Descartados: 0.
  - Na atual, nenhum achado veio com execução. Um revisor de Spec escreveu que a afirmação de D5 vem "da leitura dos asserts, não de uma execução".
  - Na candidata, D5 foi provado por mutação nas 3 execuções que o trataram. Os scripts desfizeram a mutação e conferiram o hash.
- **Controles:** nenhuma execução apontou C1, C2 ou C3 como defeito. Na candidata, as 4 execuções provaram C2 com testes que passam, e 2 provaram também C1.
- **Ruído:** os 2 revisores de Standards da atual numeraram o mesmo `[NIT]`: o Blade repete a regra da Policy. Ele é estrutura, sem falha atual. A candidata não teve achado de estilo ou estrutura.
- **Defeito da base (janela das 23h59):**
  - Atual: 2 de 4 execuções o citaram como nota fora do veredito, por julgamento. Nenhuma lhe deu `[BLOCKER]`. Na avaliação de 30/10, 2 de 8 lhe deram `[BLOCKER]`.
  - Candidata: 2 de 4 execuções o marcaram como candidato a `Da base`, com a prova. Na Reexecução, a prova falhou na base com a mesma saída (`10000` no lugar de `7500`). O principal o confirmou como `Da base`.
  - Nas outras provas da candidata, a execução na base falhou por código ausente (método, opção ou coluna nova). Pela regra da etapa 5, esses defeitos são do diff.
- **Risco sem prova no teste:** as 4 execuções da candidata puseram a corrida entre 2 cliques simultâneos em `Não verificado`, com o motivo, e provaram a versão em série. Uma delas simulou a corrida com 2 instâncias lidas antes da 1ª escrita.
- **Defeito real não plantado:** a Spec pede a coluna "Aprovado por", e a tabela não tem cabeçalho. Atual: 1 `[NIT]` e 1 nota. Candidata: 1 `[IMPORTANTE]` provado (`assertSee('Aprovado por')` falha) e 1 nota que deixa a decisão ao usuário.
- **Custo:**
  - A candidata usou em média 168 mil tokens e 6,1 min por revisor. A atual usou 166 mil tokens e 4,8 min.
  - A candidata usou 30 ferramentas em média; a atual, 51.
  - A Reexecução levou cerca de 5 s por revisor, na head e na base.
  - A montagem das worktrees com `vendor/` é um custo novo do principal. Ele depende do projeto.
- **Contrato:**
  - Nas 4 pastas da atual, o `md5sum` ficou igual.
  - Nas 4 pastas da candidata, a produção ficou igual ao alvo. Os arquivos novos ficaram em `tests/Feature/Revisao/` e em `storage/framework/views/`, que guarda as views que o Pest compila.
  - Desvios: um revisor gravou uma cópia temporária da Action fora de `tests/Feature/Revisao/` e a apagou no mesmo comando. Outro usou `python3` para editar o próprio script de prova.
  - Com os links físicos, o Pest grava `vendor/pestphp/pest/.temp/test-results`, que as 8 pastas compartilham. É um cache de resultados e não muda o código.

## Limites

- A fixture favorece a execução: os 6 defeitos plantados têm prova barata no Pest. Ela não tem um defeito de corrida, de memória ou de vários servidores, que a candidata põe em `Não verificado`.
- São 4 execuções por versão. As diferenças de custo e de ruído podem ser acaso.
- O executor também escreveu a candidata.

## Conclusão

- **Ganho de eficácia:** não declarado. As 2 versões acharam os 6 defeitos plantados.
- **Ganho medido:**
  - cada achado numerado da candidata tem prova executada, e a Reexecução confirmou todos;
  - o defeito da base foi separado por execução, não por julgamento;
  - a candidata não teve ruído de estrutura.
- **Custo:** os tokens ficaram iguais (+1%). O tempo por revisor subiu 26%. O principal ganhou a montagem das worktrees e a Reexecução.
- **Adotada:** a candidata (4.436 palavras), com 2 acréscimos que a avaliação mostrou:
  - na etapa 4, o revisor marca o `candidato a Da base`, como 2 revisores fizeram sem a regra;
  - na etapa 1, a cópia de `vendor/` com links físicos e o aviso de não rodar `composer` nela.
- **Mudanças ligadas:**
  - Estrutura e Enxuto passam ao refactor de `/implementar`.
  - `/ajustar` parte da prova do achado e não trata mais `[NIT]`.
- **Não medido:** o relatório, as rodadas seguintes, o vaivém, o limite de rodadas e o efeito em `/ajustar`.
