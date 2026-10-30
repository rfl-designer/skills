---
name: revisar
description: Executa Revisão Adversarial em contexto limpo (Standards + Spec + Segurança Livewire/Laravel) e gera o resumo de PR com Raio de Explosão. Use quando o usuário digitar /revisar.
disable-model-invocation: true
---

# Revisão Adversarial e Briefing de Entrega (`/revisar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Submeter o `git diff` da entrega a uma Revisão Adversarial completa, numa só rodada, em dois eixos isolados (Padrões Laravel/Livewire vs. Especificação) e gerar um briefing de Pull Request conciso com análise de Raio de Explosão.

Revise como o desenvolvedor que recebe o alerta quando a mudança quebra. Dentro de cada eixo, priorize nesta ordem: correto, seguro, aguenta a carga esperada, testado, rápido, enxuto.

## 2. Regras Inegociáveis
- **Use subagentes novos e só de leitura:** Sempre que a ferramenta suportar subagentes, dispare 2 revisores paralelos isolados passando apenas Ponteiros de Contexto (arquivo do diff da etapa 1, Mapa de Fluxos da etapa 2, caminho da Spec, glossário e configuração do projeto). O agente que escreveu o código tem viés de confirmação. Use subagentes novos a cada rodada e a cada lacuna. Não use `fork` nem retome um subagente anterior: os dois herdam contexto. O revisor só lê; no Claude Code, siga a seção 4.
- **Declare a revisão sem independência:** Sem subagentes, avise o usuário: a revisão no mesmo contexto não é independente. Ofereça `/revisar` numa sessão nova, sem o histórico da implementação. Se o usuário pedir para continuar, revise você mesmo e escreva `Independência: mesmo contexto` no relatório.
- **Reporte, não corrija:** `/revisar` não edita código. O usuário decide quais achados corrigir. A correção acontece depois: `/ajustar` corrige os achados com correção localizada; `/implementar`, o requisito que pede uma Fatia nova; `/bug`, o defeito sem causa localizada.
- **Leia o código conectado, não só o diff:** Leia os chamadores das funções alteradas, as funções chamadas, os testes e o README. Quando uma assinatura, um retorno ou um comportamento muda, busque todos os chamadores com `rg`.
- **Siga cada valor de ponta a ponta:** Um Fluxo é o caminho de um valor que o diff altera (chave, ID, coluna, status, flag, regra, assinatura ou formato de retorno), da entrada até cada consumidor: consulta, lista, detalhe, texto exibido, regra, decisão, documento gerado, export, job, notificação e API. A verificação de um consumidor não prova os outros. Exemplo: a lista elimina chaves repetidas, mas o detalhe, os termos, a decisão de exigir assinatura e o PDF também leem a mesma chave. Confira cada um.
- **Entregue a revisão completa numa rodada:** A rodada termina só no Critério de Fim da etapa 5. Um `[BLOCKER]` não encerra a busca: registre-o e continue. Assim, o usuário corrige todos os achados de uma vez.
- **Limite o ciclo com `/ajustar`:** Um achado que o usuário aceita, com o motivo, sai do `Veredito:`. Uma correção que desfaz outra é vaivém, e a decisão é do usuário. Na rodada 3 sem `pode entregar`, pare o ciclo e pergunte ao usuário como seguir.
- **Pese a evidência pelo que ela cobre:** Um teste verde prova só os caminhos que ele executa. A aprovação de um subagente prova só o código que ele leu. Nenhum dos dois substitui o rastreio dos Fluxos.
- **Passe o pente-fino anti-ruído:** Aponte comentários óbvios, código morto e imports não utilizados segundo `ste100-clean-code`.
- **Mantenha os eixos separados:** Apresente Standards e Spec em seções próprias. Não junte nem reordene achados entre eixos. Um eixo aprovado não compensa o outro reprovado.
- **Classifique os achados por severidade dentro de cada eixo:**
  - `[BLOCKER]`: bug, falha de segurança, perda de dados ou quebra com a carga esperada.
  - `[IMPORTANTE]`: lógica de risco sem teste, lentidão real, duplicação, função com várias responsabilidades ou código que não devia existir.
  - `[NIT]`: ganho pequeno de velocidade ou forma mais curta.
- **Exija um caso concreto:** Todo achado descreve uma entrada ou situação e o resultado errado que ela produz. Sem caso concreto, não há achado.

## 3. Processo
1. **Coleta do Diff e Verificação Base:**
   - Use o alvo que o usuário indicar: mudanças locais, staged, branch, PR ou arquivos. Sem alvo, use o diff contra a branch base, com as mudanças locais. Sem diferença, use o último commit.
   - Inspecione `git status` e o diff do alvo. Registre a referência exata (ex.: `main...HEAD`). Grave o diff do alvo num arquivo temporário fora do repositório, como `$TMPDIR/diff-<branch>-<AAAA-MM-DD>.patch`. Passe o caminho e a referência aos dois subagentes. O revisor não executa git.
   - **Rodada seguinte:** Com um relatório anterior de `/revisar` para o mesmo alvo, na conversa ou no handoff, esta é uma rodada seguinte. Use o diff completo do alvo, não só o delta da correção. Liste os achados anteriores para a etapa 6. Com relatório de `/ajustar`, leia também o status de cada achado, `Valores alterados:`, `Achados novos:` e `Aceitos:`. Um achado que o usuário aceitou nesta conversa, com o motivo, também conta como aceito. A rodada atual é a `Rodada:` do relatório anterior mais 1.
   - Aplique o portão completo de `laravel-verification` ou reutilize evidência ainda válida para o mesmo estado. Não repita a suíte apenas por entrar na revisão.
2. **Mapa de Fluxos:** Antes de disparar os subagentes:
   - Liste os valores que o diff altera. Na rodada seguinte, inclua os valores que cada correção alterou. O relatório de `/ajustar` lista esses valores em `Valores alterados:`.
   - Para cada valor, busque com `rg` todos os pontos que o leem ou gravam, também fora do diff: Models, Actions, componentes Livewire, views Blade, Policies, jobs, listeners, exports, templates de PDF ou e-mail, rotas de API e testes. A lista vem da busca, não da memória de quem escreveu o código.
   - Registre cada Fluxo como `valor: entrada → consumidor → saída`, com `arquivo:linha` de cada ponto.
3. **Revisão Adversarial em 2 Eixos (Subagentes Paralelos):** Cada subagente lê o código conectado e ordena seus achados pela prioridade da seção 1. Cada subagente também:
   - Completa o Mapa com os consumidores que achar e rastreia cada Fluxo até a saída.
   - Devolve o status de cada arquivo do diff e de cada Fluxo no seu eixo: `verificado`, `achado` (com o título) ou `não verificado` (com o motivo).
   - Termina só quando todos os arquivos e Fluxos têm status. Um `[BLOCKER]` não encerra o trabalho do subagente.
   - **Subagente 1 — Eixo Standards & Laravel/Livewire Security:**
     - **Carga esperada:** Procura a carga no repositório (README, filas, Horizon, Octane, scheduler, deploy). Declara a carga presumida.
     - **Segurança:** Verifica se propriedades sensíveis/IDs em componentes `Livewire` possuem `#[Locked]`. Verifica se toda ação mutável chama `$this->authorize()` / `Policy`.
     - **Perda de dados:** Caça erro engolido em `try/catch`, várias escritas sem `DB::transaction()` e job ou evento disparado antes do commit sem `afterCommit()`. Caça a operação que, executada 2 vezes, grava, cobra ou envia em dobro: job com retry, webhook, comando agendado, duplo clique.
     - **Escala:**
       - N+1 queries Eloquent (falta de `with()` ou `preventLazyLoading`).
       - Condição de corrida entre leitura e escrita: `firstOrCreate` sem índice único, falta de `lockForUpdate()` ou `increment()`.
       - Tarefa repetida em cada processo: falta de `onOneServer()`, `withoutOverlapping()` ou `ShouldBeUnique`.
       - Memória que só cresce: `->get()` em tabela grande no lugar de `chunkById()` ou `lazy()`.
       - Algoritmo O(n²) sobre entrada grande.
       - Estado local do processo que devia ser compartilhado: propriedade estática no Octane, disco local com vários servidores.
     - **Velocidade:** Reporta lentidão real como `[IMPORTANTE]`. Reporta ganho pequeno, como trabalho repetido num laço quente, como `[NIT]`.
     - **Estrutura:** Verifica regras e coordenação sem encapsulamento, abstrações sem benefício e ausência de `declare(strict_types=1);`. Aceita CRUD simples e Costuras existentes conforme `laravel-deep-modules`.
     - **Enxuto:**
       - Apagar: código morto, opções sem uso, funcionalidade especulativa, comentários desnecessários (`ste100-clean-code`).
       - Reutilizar: o repositório já tem o helper, a Action ou o Scope. Cite o caminho.
       - Nativo: o Laravel ou o PHP já resolve (`Collection`, `Str`, `Arr`, regras de validação). Uma dependência nova para poucas linhas também entra aqui.
       - YAGNI: Interface com uma só implementação, configuração que ninguém altera.
       - Juntar: quase-cópias que precisam mudar juntas.
       - Separar: função com várias responsabilidades, difícil de ler ou testar. Separe por responsabilidade, nunca por número de linhas.
   - **Subagente 2 — Eixo Spec & Comportamento:**
     - Compara o diff linha a linha com a Especificação gerada em `/especificar`.
     - Aponta requisitos faltantes e escopo extra não solicitado (*scope creep*).
     - **Bug:** Caça resultado errado e erro em casos de borda (vazio, zero, último item, arredondamento, fuso horário). Caça chamador quebrado pela mudança. Caça correção feita num só chamador, com a função compartilhada ainda errada.
     - **Teste ausente:** Aponta lógica de risco sem um teste Pest que falhe quando ela quebra: ramo, parser, dinheiro, segurança, escrita de dados ou correção de bug. Pede um teste bom, não cobertura. Aponta também o teste que ainda passa com a Costura a devolver vazio, sem gravar nada.
     - **Mapa desatualizado:** Com Mapa de Features configurado, aponta comportamento visível alterado sem atualização do Arquivo de Feature no mesmo diff.
4. **Confirmação dos Achados:** Antes de reportar, cada subagente:
   1. Escreve o caso concreto de cada achado.
   2. Relê as linhas e confirma o fato: o chamador existe, o valor pode ser vazio, o código não tem uso.
   3. Trata como decisão, não como achado, o atalho com limite documentado em ADR, Spec ou comentário de porquê. Reporta o atalho só se a carga esperada já passa desse limite.
   4. Propõe a menor correção que funciona. Prefere a correção que apaga código. Não adiciona camadas, pacotes ou configuração que o problema não exige.
   5. Descarta gosto de estilo, "considere..." e preocupação vaga.
5. **Consolidação (agente principal):** Com os retornos dos dois eixos, antes do relatório:
   1. **Cobertura:** Confira se cada arquivo do diff e cada Fluxo têm status nos dois eixos. Devolva cada lacuna a um subagente novo do mesmo eixo. Um subagente que falha, para antes do fim ou devolve outro formato não revisou: dispare um subagente novo uma vez. Na segunda falha, marque os arquivos e Fluxos sem status como `não verificado` e cite o eixo em `Não verificado:`. Sem subagentes, cubra a lacuna você mesmo.
   2. **Propagação:** Para cada achado, siga o mesmo valor em todos os consumidores do Mapa. Inclua no achado cada local com o mesmo defeito. Quando a correção difere, abra um achado próprio.
   3. **Divergência:** Investigue até resolver: os eixos afirmam fatos opostos sobre o mesmo trecho (ex.: um diz que o valor nunca é vazio, o outro diz que é); um consumidor aparece no retorno de um eixo e falta no outro; o teste citado como prova não executa o consumidor em questão.
   4. **Achados novos:** Aplique a etapa 4 a cada achado novo da Consolidação. Coloque-o no eixo do seu tema. Na rodada seguinte, marque com `(perdido na rodada anterior)` o achado em código que a rodada anterior já revisava, e rastreie de novo o Fluxo inteiro desse valor. Confirme também cada item de `Achados novos:` de `/ajustar` e numere o confirmado no eixo do seu tema.
   5. **Vaivém:** Na rodada seguinte, marque com `(vaivém do achado N)` o achado no trecho de uma correção de `/ajustar` que desfazer essa correção resolveria. As duas correções puxam o código em direções opostas. Na **Correção**, escreva as duas direções e a pergunta ao usuário.
   - **Critério de Fim:** Todos os arquivos e Fluxos têm status nos dois eixos, sem lacuna nem divergência aberta. Só então escreva o relatório.
6. **Relatório por Eixo:**
   - Comece com `Alvo:`, seguido da referência, da branch e do commit revisados (ex.: `main...HEAD` em `feature/pedidos@3f9c2ab`). Na linha seguinte, escreva `Rodada: N`; a primeira rodada é 1. Sem subagentes, escreva também `Independência: mesmo contexto`. Depois, escreva `O que a mudança faz:` em 2 ou 3 frases.
   - Na rodada seguinte, escreva em seguida `Achados anteriores:`, com 1 linha por achado: `corrigido`, `corrigido em parte`, `não corrigido`, `não reproduz` ou `aceito`, e a prova ou o motivo.
     - O achado `corrigido em parte` ou `não corrigido` volta numerado no seu eixo e entra no `Veredito:`.
     - O `não reproduz` de `/ajustar`, com a prova de que o teste executa o caso, fica fora do `Veredito:`. Ele só volta numerado com um caso concreto novo que o refuta.
     - O `aceito` é um achado que o usuário decidiu não corrigir, com o motivo. Ele fica fora do `Veredito:`. Ele só volta numerado com um caso concreto novo que o motivo do aceite não cobre. Sem motivo, o aceite não vale: pergunte o motivo.
   - Apresente os achados sob `## Standards` e `## Spec`, cada um com seus `[BLOCKER]`, `[IMPORTANTE]` e `[NIT]`. Omita o nível sem achados.
   - Numere os achados em sequência contínua de um eixo para o outro, sem reordenar. Assim, o usuário pode responder "corrija 2 e 5".
   - Explique cada termo técnico na primeira vez que ele aparecer. O leitor pode não conhecer o código.
   - Escreva cada achado neste formato, com 1 ou 2 frases curtas por parte:
     ```markdown
     2. [BLOCKER] **Pedido entra no dia errado** (`app/Actions/FecharDia.php:40-52`)
        - **O que é:** À meia-noite, esta Action fecha o dia e fatura os pedidos desse dia.
        - **Problema:** A Action usa `now()` no fuso UTC da aplicação. Um pedido feito às 22h em São Paulo já é 01h do dia seguinte em UTC.
        - **Correção:** Calcule o dia uma vez no fuso da loja: `now('America/Sao_Paulo')->toDateString()`. Nada mais muda.
        - **Se não corrigir:** Pedidos da noite saem com a data errada, e o financeiro corrige à mão.
     ```
   - Termine com:
     - 1 linha por eixo: total por nível e o pior achado.
     - `Fluxos rastreados:` 1 linha por Fluxo, com os consumidores e o status.
     - `Carga presumida:` a carga usada no eixo Standards.
     - `Aceitos:` 1 linha por achado aceito, com o motivo, quando houver.
     - Sem `[BLOCKER]` nem `[IMPORTANTE]`: `Veredito: pode entregar.` Caso contrário: `Veredito: corrija 1 e 3 antes.`, com os números desses achados.
     - `Enxuto: -N linhas possíveis.` quando houver achado de Enxuto.
     - `Não verificado:` em 1 linha, quando algo importante não pôde ser verificado.
   - Sem achados nos dois eixos: escreva `Alvo:`, `Rodada:`, `O que a mudança faz:`, depois `Sem achados. Pode entregar.`, `Fluxos rastreados:`, `Aceitos:` quando houver e 1 linha com o que foi verificado.
   - Com `Veredito: corrija ...` antes da rodada 3, ofereça `/ajustar` com os números do veredito.
   - **Limite de rodadas:** Na rodada 3 com `Veredito: corrija ...`, não ofereça `/ajustar`. Liste os achados abertos por nível e faça uma pergunta ao usuário: aceitar os abertos, com o motivo, e entregar, fazer mais uma rodada, ou voltar a `/especificar` ou `/planejar`. Três rodadas sem convergir indicam, em geral, uma Spec ou um desenho errado. Com a escolha de mais uma rodada, repita a pergunta no fim de cada rodada seguinte.
   - Com `[BLOCKER]`, entregue o relatório completo, não execute as etapas 7 e 8 e pergunte ao usuário como seguir.
7. **Prova do Fato de Segurança:** Identifique o único fato que torna a mudança segura (ex.: "a migration só adiciona coluna nullable"). Prove esse fato com um teste Pest ou um script que executa o código real. Se não conseguir provar, escreva `não provado`.
8. **Geração do Briefing de PR (Máximo 40 linhas, padrão ASD-STE100):**
   - **Por que (Why):** 1 a 2 frases explicando o problema resolvido.
   - **O que mudou (What changed):** Bullets curtos focados nas Fronteiras (`Livewire`/HTTP) e Costuras (`Actions`/DTOs).
   - **Porta de Decisão e Raio de Explosão (Blast Radius):** Classifique a mudança como **Porta de 2 Vias** (reversível sem perda de dados) ou **Porta de 1 Via** (ex.: migration destrutiva, alteração de contrato externo) e liste exatamente quais rotas/componentes podem ser afetados. Inclua o fato de segurança da etapa 7 com a prova ou o rótulo `não provado`. Liste os achados `aceito` como **Riscos aceitos**, com o motivo.
   - **Prova de Execução (`[measured]`):** Resumo do portão completo de `laravel-verification`.

## 4. No Claude Code
Use o agente customizado `revisor`, com `model: inherit` e as ferramentas `Read, Grep, Glob`.

1. Copie o [template](assets/revisor.md) para `.claude/agents/revisor.md` na raiz do projeto consumidor. Se o arquivo já existe, preserve as customizações.
2. Instale `laravel-deep-modules`, `laravel-tdd-seams` e `ste100-clean-code` para o Claude Code. O campo `skills` do template pré-carrega essas disciplinas.
3. Delegue com `subagent_type: revisor`, um por eixo, na mesma mensagem. Passe o eixo, o caminho deste SKILL.md e os Ponteiros de Contexto. Não use o tipo `fork`.
4. O revisor não executa git nem testes. Por isso, a etapa 1 grava o diff num arquivo, e o agente principal executa o portão e a prova do fato de segurança.
5. Sem o agente registrado, use o subagente geral com o mesmo contrato. Avise o usuário: o subagente geral tem todas as ferramentas, e a regra "só lê" fica só na instrução. Criar o primeiro diretório de agentes durante a sessão pode exigir reiniciar o Claude Code.

Fonte: [subagentes do Claude Code](https://code.claude.com/docs/en/sub-agents).

## 5. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Eu mesmo acabei de escrever o código, posso apenas olhar rápido sem seguir os 2 eixos." | **Proibido.** A Revisão Adversarial exige checagem independente de Standards (Segurança/N+1/Livewire) e Spec. |
| "Achei um `[BLOCKER]`; posso parar e reportar agora." | **Proibido.** O `[BLOCKER]` não encerra a rodada. Conclua os dois eixos e a Consolidação e reporte todos os achados juntos. |
| "Os dois revisores aprovaram e os testes passam; a revisão acabou." | **Proibido.** Teste e revisor provam só o que executam ou leem. A revisão acaba no Critério de Fim da Consolidação. |
| "Conferi que a lista elimina chaves repetidas; a chave está certa." | **Proibido.** Um consumidor não prova os outros. Siga a mesma chave no detalhe, nos termos, nas decisões e nos documentos gerados. |
| "Nesta rodada, basta revisar o delta da correção." | **Proibido.** A correção pode quebrar outro consumidor, e a rodada anterior pode ter perdido um achado. Revise o diff completo e os Fluxos que a correção toca. |
| "Não há impacto nenhum no Raio de Explosão." | **Proibido.** Toda alteração toca alguma rota, tabela ou componente. Nomeie os pontos afetados explicitamente. |
| "Vou escrever um PR de 200 linhas listando cada arquivo modificado." | **Proibido.** O Git já mostra os arquivos. O briefing de PR deve ter no máximo 40 linhas de alto sinal. |
| "O `[BLOCKER]` é simples, eu mesmo corrijo durante a revisão." | **Proibido.** A revisão só reporta. Corrigir no meio mistura autor e revisor e esconde a decisão do usuário. |
| "Vou juntar os achados dos 2 eixos numa lista única por prioridade." | **Proibido.** Reordenar entre eixos deixa um eixo mascarar o outro. |
| "O raio de explosão está bem descrito, não preciso rodar nada." | **Proibido.** Texto convincente não prova nada. Execute código que prove o fato de segurança. |
| "O diff está correto; o resto do código não mudou." | **Proibido.** Uma mudança de assinatura, retorno ou comportamento quebra chamadores fora do diff. Busque todos os chamadores. |
| "Não tenho um caso concreto, mas vou anotar 'considere...' por precaução." | **Proibido.** Sem caso concreto, não há achado. A preocupação vaga vira ruído e esconde os achados reais. |
| "A correção certa é criar um Service, uma Interface e uma configuração nova." | **Proibido.** Proponha a menor correção que funciona. Prefira a correção que apaga código. |
| "Não há subagente; reviso aqui e entrego como revisão normal." | **Proibido.** Avise que a revisão no mesmo contexto não é independente, ofereça uma sessão nova e escreva `Independência: mesmo contexto`. |
| "Uso um `fork` ou retomo o revisor da rodada anterior; ele já conhece o código." | **Proibido.** Os dois herdam contexto. Use um subagente novo. |
| "O revisor do eixo Spec falhou; o eixo está sem achados." | **Proibido.** Um revisor que falha não revisou. Dispare um novo; na segunda falha, marque `não verificado`. |
| "O usuário aceitou o achado, mas ele apareceu de novo; numero outra vez." | **Proibido.** O `aceito` só volta com um caso concreto novo que o motivo do aceite não cobre. |
| "A correção nova desfaz a anterior; proponho só a nova." | **Proibido.** Marque o vaivém e leve as duas direções ao usuário. |
| "Na rodada 4 ainda há achados; ofereço mais um `/ajustar`." | **Proibido.** Na rodada 3, pare o ciclo e pergunte ao usuário como seguir. |

## 6. Prova de Execução (Critério de Saída)
- `[measured]` Relatório dos 2 eixos (Standards + Spec) entregue em seções separadas, sem edição de código, com a linha `Alvo:`.
- `[measured]` Mapa de Fluxos montado por busca, com status de cada arquivo do diff e de cada Fluxo nos dois eixos.
- `[measured]` Subagentes novos e só de leitura, com o diff em arquivo; ou a linha `Independência: mesmo contexto`.
- `[measured]` Consolidação concluída antes do relatório: lacunas devolvidas, achados propagados aos consumidores do mesmo valor e divergências resolvidas.
- `[measured]` Um só relatório com todos os achados confirmados da rodada, também quando há `[BLOCKER]`.
- `[measured]` Na rodada seguinte: diff completo revisado, status de cada achado anterior e Fluxos das correções rastreados.
- `[measured]` Linha `Rodada:` no relatório. Achado `aceito` fora do `Veredito:`, com o motivo. Vaivém marcado com as duas direções e a pergunta.
- `[measured]` Na rodada 3 sem `pode entregar`: pergunta ao usuário, sem oferta de `/ajustar`.
- `[measured]` Cada achado com caso concreto, `arquivo:linha` e as 4 partes (O que é, Problema, Correção, Se não corrigir).
- `[measured]` Busca de chamadores citada para cada assinatura, retorno ou comportamento alterado.
- `[measured]` Carga presumida declarada no relatório.
- `[measured]` Fato de segurança provado por execução, ou rotulado `não provado`.
- `[measured]` Portão completo de `laravel-verification` aprovado para o estado revisado, com comandos, escopos e resultados citados.
- `[measured]` Briefing de PR com seção de Raio de Explosão entregue ao usuário.
