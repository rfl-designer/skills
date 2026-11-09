---
name: alinhar-em-trio
description: Só no herdr. O Julgador conduz 3 agentes de modelos diferentes pela árvore de decisão de uma ideia, com unanimidade em cada nó, condensa as decisões numa SPEC que o trio aprova e a publica para review-for-human. Substitui /alinhar, /prototipar e /especificar nesse fluxo. Use quando o usuário digitar /alinhar-em-trio.
argument-hint: "<ideia> | retomar <link da Issue ou caminho da nota> | <link da SPEC publicada>"
disable-model-invocation: true
---

# Alinhar em Trio no herdr (`/alinhar-em-trio`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

Leia também a seção `Trio de alinhamento`. Sem essa seção, use o trio padrão de [references/herdr.md](references/herdr.md) e ofereça `/setup` uma vez.

## 1. Objetivo
Levar uma ideia ou melhoria até uma SPEC sem que o humano tome as decisões técnicas.
- Três agentes de modelos diferentes debatem cada nó da árvore de decisão até a unanimidade.
- O Julgador modera, registra a ata e escreve a SPEC.
- O trio confere a SPEC contra a ata.
- O humano responde só às perguntas de negócio, aos impasses e aos diálogos de permissão. No fim, ele recebe a SPEC para review-for-human.

Esta skill substitui `/alinhar`, `/prototipar` e `/especificar`. Depois do review humano, o próximo passo é `/planejar`.

## 2. Termos
- **Julgador:** esta sessão, que o humano inicia. O Julgador esperado vem da configuração (padrão: Claude Code, Opus 5.5, esforço `xhigh`). Ele modera e não vota.
- **Trio:** os 3 agentes da configuração, cada um num pane do herdr. Padrão:
  - `opus`: Claude Code, Opus 5.5, `medium`.
  - `sol`: Codex, GPT-6.1 Sol, `medium`.
  - `argon`: Antigravity CLI, Gemini 4 Argon, `medium`.
- **Nó:** uma decisão da árvore. Um nó filho abre só depois da decisão do nó pai.
- **Fronteira:** os nós abertos cujos pais já têm decisão.
- **Rodada:** um arquivo do Julgador e uma resposta de cada agente. As rodadas têm numeração global (`001`, `002`, ...). Uma rodada pode ter vários nós da fronteira. Cada nó conta as próprias rodadas.
- **Ata:** o registro da sessão. Ela tem a árvore e, para cada nó: a pergunta, as posições, as mudanças de posição, a decisão, a origem e as evidências. Ela também tem as perguntas ao humano, as falhas, as versões da SPEC e a publicação. A ata é a fonte da retomada.
- **Diretório da sessão:** `$TMPDIR/alinhar-em-trio/<slug>-<AAAA-MM-DD>/`, fora do repositório. Sem `$TMPDIR`, use `/tmp`.
- **Escalada:** uma pergunta do Julgador ao humano.

## 3. Regras Inegociáveis
- **Rode só no herdr:** Antes de qualquer outro passo, execute `test "${HERDR_ENV:-}" = 1`. Se o teste falha, diga que a sessão não está no herdr, recomende `/alinhar` e pare.
- **O Julgador não vota:** Não dê opinião sobre a decisão de um nó. Formule as perguntas, revele as respostas, resuma as divergências com neutralidade e confira a unanimidade.
- **Exija unanimidade explícita:** Um nó termina só quando os 3 agentes escrevem `CONCORDO` para a mesma formulação. A maioria não decide.
- **Exija o argumento da mudança:** O agente que muda de posição escreve o argumento que mudou a opinião dele e de quem veio esse argumento. Sem esse registro, a concordância não conta, e o nó continua.
- **Não invente regra de negócio:** Uma pergunta que o código, a configuração e a pesquisa não respondem vai ao humano.
- **Nunca aprove um diálogo de um agente:** Um agente `blocked` espera uma aprovação. Mostre o diálogo ao humano sem alteração. Envie teclas só com a instrução do humano.
- **Proteja o repositório:** O trio lê o repositório e escreve só no próprio diretório da sessão. Sem código de produção, sem commit e sem push. O Julgador escreve no repositório só na publicação (4.8).
- **Troque mensagens por arquivo:** O prompt a um agente só diz o arquivo para ler, o arquivo para gravar e "Responda só com o caminho". Não cole o conteúdo da rodada no prompt.
- **Atualize a ata a cada evento:** Nó decidido, escalada, falha, versão da SPEC e publicação. Uma decisão fora da ata não existe na retomada.
- **Use os comandos da referência:** [references/herdr.md](references/herdr.md) tem os comandos e o estado da verificação. Se uma flag falha, leia o `--help` do grupo ou do CLI e registre a diferença na ata.
- **Feche só o que você criou:** Feche só a tab e os panes desta sessão.

## 4. Processo

### 4.1 Guarda e entrada
1. Execute a guarda do herdr.
2. Leia a configuração e a seção `Trio de alinhamento`.
3. Escolha o modo pelo argumento:
   - `retomar <link da Issue ou caminho da nota>`: vá para 4.10.
   - Link de uma SPEC publicada: vá para 4.11.
   - Sem argumento: peça ao humano a ideia, numa frase.
4. Crie o diretório da sessão e a ata a partir de [assets/ata.md](assets/ata.md). Registre o Julgador esperado, o trio, a branch e o commit atual.

### 4.2 Preparação do trio
1. Crie as pastas `rodadas/`, `log/` e `spec/` no diretório da sessão. Crie também um diretório para cada agente, com a subpasta `prototipos/`.
2. Copie [assets/debatedor.md](assets/debatedor.md) para o diretório da sessão.
3. Grave `contexto.md` no diretório da sessão com:
   - A ideia.
   - A raiz do repositório e a configuração.
   - O glossário e a pasta de ADRs configurados.
   - Os caminhos absolutos de `laravel-deep-modules`, `ste100-clean-code` e `prototipar`, quando estão instaladas.
   - O caminho da ata e o diretório de cada agente.
4. Crie a tab `alinhar-<slug>` no workspace atual, com 3 panes. O diretório de cada pane é a raiz do repositório, exceto quando a referência indica outro diretório para o CLI.
5. Inicie cada agente com o nome, o `--kind` e os argumentos da configuração. Os argumentos limitam a escrita ao diretório do agente.
6. Envie a cada agente: "Leia `<sessao>/debatedor.md` e `<sessao>/contexto.md`. Você é `<nome>`. Responda só com OK."
7. Registre na ata a tab, os panes e o estado de cada agente.

### 4.3 Árvore de decisão
1. Inspecione o repositório em silêncio: Models, migrations, Enums, Actions, componentes Livewire, Policies, glossário e ADRs ligados à ideia. Não pergunte ao trio nem ao humano o que o código responde.
2. Monte a primeira árvore com os 5 eixos de `/alinhar`:
   - Domínio e Estado.
   - Fronteira (Livewire / HTTP).
   - Autorização.
   - Costura pública.
   - Efeitos Colaterais.
3. Dê a cada nó um número, uma pergunta e o nó pai.
4. **Rodada 0:** Grave a árvore no arquivo da primeira rodada. Cada agente lê a árvore às cegas e propõe os ramos que faltam, com o motivo.
5. Acrescente um ramo só quando a SPEC precisa da decisão dele. Registre na ata o ramo recusado, com o motivo.
6. Durante o debate, um agente também pode propor um nó filho. Aplique a mesma regra.

### 4.4 Protocolo de cada nó
Envie todos os nós da fronteira na mesma rodada. Cada nó termina de forma independente.

1. **Rodada 1, às cegas.** Para cada nó, o arquivo da rodada tem:
   - A pergunta.
   - As decisões dos nós pais.
   - Os trechos de código, citados por caminho.
   - O formato da resposta (veja `debatedor.md`).
2. **Rodadas de crítica.** A partir da rodada 2, o arquivo de cada nó tem:
   - As respostas da rodada anterior, sem alteração.
   - Um resumo neutro das divergências.
   - Quando as posições convergem, a formulação da decisão.
3. **Conferência.** Depois de cada rodada, para cada nó:
   - Uma concordância vale só para a formulação exata.
   - Uma mudança de posição vale só com o argumento e a origem. Sem esses registros, marque a concordância como recusada na ata e mantenha o nó aberto.
   - Uma afirmação sem evidência (`arquivo:linha`, URL ou protótipo) vai ao resumo como `sem evidência`.
4. **Decisão.** Com 3 `CONCORDO` válidos, registre a decisão na ata. Depois, abra os nós filhos na fronteira.
5. **Impasse.** Depois de 3 rodadas de crítica sem unanimidade, o nó espera uma escalada (4.5) com as 3 posições.
6. **Pergunta de negócio.** Um agente marca uma pergunta de negócio. Procure a resposta no código, na configuração e nos ADRs. Sem resposta, o nó espera uma escalada.
7. **Nós que esperam.** Um nó que espera o humano sai da rodada. Os outros nós da fronteira continuam. Faça a escalada quando todos os nós abertos esperam o humano, ou quando a árvore não tem outro nó para debater.

### 4.5 Escalada ao humano
Há 2 tipos de escalada:
- **Escalada de nó:** uma pergunta de negócio sem resposta, um impasse, um achado `perguntar` do Leitor ou 2 rodadas de OK da SPEC sem unanimidade. Junte as escaladas de nó, como 4.4 manda, e faça todas as perguntas numa só mensagem.
- **Escalada de agente:** um diálogo de permissão ou a segunda falha de um agente. A rodada não termina sem o agente. Por isso, faça esta escalada na hora.

Passos:
1. Atualize a ata: `Estado: aguardando humano`.
2. No seu pane, mostre ao humano, para cada pergunta: o nó, a pergunta, as posições resumidas com neutralidade, as evidências e as opções. Não recomende uma opção.
3. Se o humano responde agora, registre cada resposta na ata, em `Perguntas ao humano`. Depois:
   - **Impasse:** a resposta decide o nó. A origem do nó é `decidido pelo humano`.
   - **Pergunta de negócio:** a resposta é um fato, não a decisão do nó. Envie o fato ao trio na próxima rodada. O nó continua no protocolo de 4.4 até ter 3 `CONCORDO`.
   - **Diálogo, falha ou OK da SPEC:** siga a instrução do humano e registre-a.
4. Se o humano responde "depois":
   1. Publique as perguntas numa Issue do tracker da configuração (GitHub por padrão). A Issue tem:
      - O título `[alinhar-em-trio] <ideia>: pergunta pendente`.
      - As perguntas e as posições.
      - A ata atualizada, num bloco `<details>`.
      - A label `aguardando-humano`.
   2. Se a label não existe, pergunte ao humano antes de criar a label.
   3. A sessão tem no máximo uma Issue de escalada. Uma escalada nova vira um comentário nessa Issue, também com a ata atualizada num bloco `<details>`.
   4. Sem acesso ao tracker, não crie a Issue. As perguntas ficam na ata e na nota de `/pausar`. Registre o bloqueio na ata.
   5. Aplique `/pausar` com o foco "retomar `/alinhar-em-trio`". A nota cita as perguntas, a Issue (quando existe), a ata, o diretório da sessão, a tab e os agentes.
   6. Diga ao humano o comando de retomada: `/alinhar-em-trio retomar <link da Issue>`, ou `retomar <caminho da nota>` sem Issue.
   7. Deixe os panes abertos e pare.

### 4.6 Falhas e diálogos
1. Cada resposta tem um timeout de 15 minutos, ou o timeout da configuração.
2. Uma falha é uma destas situações:
   - Um timeout ou um `agent_prompt_stalled`.
   - Um agente que não existe mais.
   - Uma resposta fora do arquivo, ou um arquivo vazio.
3. Antes de agir, leia o agente com `agent get` e `agent read`. Um timeout não prova que o prompt não chegou. Não reenvie sem ler.
4. **Primeira falha de um agente nesta sessão:** reinicie o agente uma vez, como a referência mostra. Envie `debatedor.md`, `contexto.md`, a ata e a rodada atual. Registre a falha na ata.
5. **Segunda falha do mesmo agente:** faça uma escalada.
   - O debate só continua com 2 agentes se o humano autoriza.
   - A ata registra o trio reduzido e a autorização.
   - Daí em diante, a unanimidade é a dos 2 agentes.
6. **Agente `blocked`:** leia o diálogo e faça uma escalada. Não aprove o diálogo.

### 4.7 SPEC
1. Comece a SPEC quando a árvore não tem mais nó aberto.
2. Grave o rascunho no diretório da sessão. Use as 6 seções e as regras de `/especificar`:
   - Sem caminhos de arquivo nem código, exceto os formatos de protótipo marcados.
   - Os termos do glossário.
   - A seção Fora de Escopo.
3. Cada decisão da SPEC vem de um nó da ata. A SPEC não acrescenta decisões.
4. Prepare os termos do glossário e os ADRs no diretório da sessão. Um ADR só existe se a decisão passa nos 3 critérios de `/alinhar`. Esses arquivos entram no repositório só em 4.8.
5. **Leitura Independente:** aplique `leitura-independente` no modo Spec. Passe ao Leitor também os rascunhos do glossário e dos ADRs: o glossário do repositório ainda não tem os termos novos. Nesta skill, o trio e o humano fazem o papel do usuário de `leitura-independente`. Dê a cada achado uma classe dessa skill:
   - `corrigir`, sem mudar uma decisão da ata: o Julgador corrige o rascunho.
   - `corrigir`, quando a correção muda ou acrescenta uma decisão: o nó novo ou reaberto volta a 4.4.
   - `contestar`: só com a prova que o Leitor podia ler, como `leitura-independente` exige.
   - `perguntar`: uma regra de negócio ou um fato fora do repositório vai a uma escalada. Uma decisão técnica vai a um nó, em 4.4.
   - `mover para tickets`: registre o achado na ata. O fechamento envia o achado a `/planejar`.
6. **OK do trio:** grave uma rodada com:
   - O caminho da versão atual da SPEC.
   - A ata.
   - A Paráfrase da última leitura, sem alteração, e a versão da SPEC que o Leitor leu.

   Cada agente escreve `OK` ou `RECUSA`. Cada recusa cita o nó e o trecho da SPEC, e tem um tipo:
   - `fidelidade`: a SPEC omite, muda ou acrescenta uma decisão. Uma Paráfrase que não descreve a ata também é `fidelidade`. O Julgador corrige e grava uma versão nova.
   - `fato novo`: o agente quer reabrir um nó. A recusa vale só com código, fonte ou protótipo que a ata ainda não tem. Com o fato novo, o nó volta a 4.4. Sem o fato novo, o Julgador recusa o pedido e registra a recusa na ata.
7. **Segunda leitura:** faça a segunda leitura só quando a primeira teve um `[BLOCKER]` ou quando o trio recusou a Paráfrase. Use um Leitor novo, só com o rascunho corrigido. Depois, faça uma rodada de OK nova, com a Paráfrase nova.
   - Depois da segunda leitura, um `[BLOCKER]` ou `[IMPORTANTE]` aberto vai a uma escalada. Pergunte uma vez: publicar com os achados abertos, ou reabrir os nós.
   - Não faça uma terceira leitura.
8. Depois de 2 rodadas de OK seguidas sem unanimidade e sem nó reaberto, faça uma escalada.
9. Com OK unânime, vá para a publicação.

### 4.8 Publicação
Executar `/alinhar-em-trio` autoriza a branch, o commit, o push, a Issue e o PR draft desta etapa. Nada além disso.

1. Leia o destino de Specs da configuração. Sem destino, pergunte como `/especificar` faz.
2. Confira se a label `review-for-human` existe. Se ela não existe, pergunte ao humano antes de criar.
3. **Destino GitHub:**
   - Se há uma Issue de escalada, troque o corpo dela pela SPEC. Depois, troque a label `aguardando-humano` por `review-for-human`.
   - Sem Issue de escalada, crie uma Issue com a SPEC e a label `review-for-human`.
   - Em outro tracker, use a operação equivalente da configuração. Registre na ata o que o tracker não suporta.
   - **Destino Markdown com uma Issue de escalada:** depois do PR, comente na Issue o link do PR e tire a label `aguardando-humano`. Não feche a Issue. O humano fecha.
4. **Arquivos do repositório** (o glossário, os ADRs e, com o destino Markdown, a SPEC):
   1. Crie uma worktree a partir da branch padrão atualizada, com a branch `alinhar/<slug>`. Não mude o checkout do humano.
   2. Grave os arquivos nos caminhos da configuração.
   3. Faça o commit com `ste100-clean-code`. O corpo diz por que mudou e como você provou: o OK unânime do trio e a linha `Leitura Independente:`.
   4. Faça o push e abra um PR draft com a label `review-for-human`. Com uma Issue da SPEC ou de escalada, o corpo do PR tem o link para ela, sem palavra que feche a Issue.
   5. Remova a worktree depois do push.
   6. Sem arquivo para gravar, não crie branch nem PR.
5. Publique um comentário com o resumo da ata no PR. Sem PR, publique o comentário na Issue. O comentário tem:
   - Uma linha por nó: a decisão, o motivo principal, os agentes que mudaram de posição e a marca `decidido pelo humano`, quando ela existe.
   - O Julgador esperado e o trio, com os modelos e os esforços.
   - A linha `Leitura Independente:`, com `Paráfrase confirmada pelo trio` quando o trio aceitou a Paráfrase.
   - Os achados `mover para tickets`, quando existem.

### 4.9 Encerramento
1. Feche a tab da sessão. Isso para os agentes.
2. Apague as pastas `prototipos/` e a pasta `spec/`. A SPEC publicada substitui o rascunho, como `leitura-independente` manda. Guarde a ata e o resto do diretório da sessão.
3. Atualize a ata: `Estado: publicada`.
4. Informe ao humano:
   - Os links da SPEC, do PR e do comentário.
   - O caminho da ata.
   - A linha `Leitura Independente:`.
   - Os achados `mover para tickets`, para `/planejar`.
   - O próximo passo: depois do review, `/planejar`. Para mudar a SPEC, `/alinhar-em-trio` com o link da SPEC.

### 4.10 Retomada depois de uma pausa
1. Execute a guarda do herdr.
2. Leia a resposta do humano:
   - Com uma Issue: a resposta é o comentário do humano depois da última pergunta. Sem resposta, diga isso ao humano e pare.
   - Com uma nota de `/pausar`: leia a nota e faça as perguntas pendentes no seu pane.
3. Leia a ata no diretório da sessão. Se o diretório não existe mais, use a ata do último comentário de escalada (ou do corpo da Issue) e crie o diretório de novo.
4. Confira os agentes com `herdr agent list`. Reinicie, como a referência mostra, cada agente que não existe mais.
5. Registre a resposta na ata, como 4.5 manda, e continue no passo que esperava: 4.4, 4.6 ou 4.7.

### 4.11 Revisão de uma SPEC publicada
1. Leia a SPEC, os comentários do review e o comentário com o resumo da ata.
2. Use a ata local quando ela existe. Senão, crie uma ata nova a partir do resumo publicado. A ata cita a SPEC publicada.
3. Faça 4.1.4 e 4.2: o diretório da sessão, a tab e o trio são novos, porque o encerramento fechou a tab anterior.
4. Liste os nós que o pedido do review toca. Reabra só esses nós, com o protocolo de 4.4.
5. Continue em 4.7 e 4.8:
   - Com o destino GitHub, troque o corpo da mesma Issue pela SPEC nova. Não crie outra Issue.
   - Se o PR ainda está aberto, use a mesma branch.
   - Se o PR já foi integrado ou fechado, crie uma branch nova.
   - Publique um comentário novo com o resumo dos nós reabertos.

## 5. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Dois agentes concordam, e o terceiro só repete a objeção. Fecho o nó pela maioria." | **Proibido.** Continue o protocolo. Depois de 3 rodadas de crítica, faça uma escalada. |
| "O `sol` mudou de posição para concordar. O nó está decidido." | Sem o argumento e a origem da mudança, a concordância não conta. |
| "Sei a melhor resposta. Ponho a minha opinião no resumo." | **Proibido.** O Julgador não vota. O resumo é neutro. |
| "O `argon` pede aprovação para ler um arquivo. É inofensivo, eu aprovo." | **Proibido.** Só o humano aprova um diálogo. |
| "A pergunta de negócio tem uma resposta óbvia. O trio decide." | **Proibido.** Uma regra de negócio vem do código, da configuração ou do humano. |
| "Colo a rodada inteira no prompt. É mais rápido." | **Proibido.** O prompt aponta para arquivos. A saída do terminal perde texto, e o Julgador perde o controle da revelação. |
| "O `sol` não respondeu em 15 minutos. Reenvio o prompt." | Leia `agent get` e `agent read` primeiro. Um timeout não prova que o prompt não chegou. |
| "Não estou no herdr. Simulo o trio com subagentes." | **Proibido.** Recomende `/alinhar` e pare. |
| "Na avaliação da SPEC, o `opus` quer mudar a decisão do nó 04. Reabro o nó." | Reabra só com um fato novo que a ata ainda não tem. |
| "O trio já aprovou a SPEC. Não preciso da Leitura Independente." | **Proibido.** O trio tem o histórico do debate. O implementador não tem. |
| "A sessão vai pausar. Fecho a tab para liberar o terminal." | **Proibido.** Os panes ficam abertos durante a pausa. Os agentes guardam o contexto do debate. |

## 6. Prova de Execução (Critério de Saída)
- `[measured]` A saída da guarda `HERDR_ENV`.
- `[measured]` A ata com cada nó: as posições, as mudanças com o argumento, a decisão, a origem e os 3 `CONCORDO` (ou `decidido pelo humano`).
- `[measured]` Cada escalada com a resposta do humano, ou a Issue com a label `aguardando-humano` e a nota de `/pausar`.
- `[measured]` A Paráfrase do Leitor na rodada de OK, cada achado do Leitor com a classe, no máximo 2 leituras e a linha `Leitura Independente:`.
- `[measured]` O OK unânime do trio sobre a versão publicada da SPEC.
- `[measured]` Os links da SPEC, do PR draft (quando há arquivos) e do comentário com o resumo da ata, com a label `review-for-human`.
- `[measured]` A tab fechada e as pastas `prototipos/` e `spec/` removidas, com a ata preservada.
