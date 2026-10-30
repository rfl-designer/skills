---
name: revisar
description: Executa Revisão Adversarial em contexto limpo (Standards + Spec + Segurança Livewire/Laravel) e gera o resumo de PR com Raio de Explosão. Use quando o usuário digitar /revisar.
disable-model-invocation: true
---

# Revisão Adversarial e Briefing de Entrega (`/revisar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Revise o diff da entrega numa só rodada, em 2 eixos isolados: Standards (padrões e segurança Laravel/Livewire) e Spec. Depois, escreva um briefing de PR conciso, com o Raio de Explosão.

Revise como o desenvolvedor que recebe o alerta quando a mudança quebra. Em cada eixo, priorize nesta ordem: correto, seguro, aguenta a carga esperada, testado, rápido, enxuto.

## 2. Regras Inegociáveis
- **Use revisores novos e só de leitura:** Com subagentes, dispare 2 revisores paralelos e isolados, um por eixo. Use revisores novos a cada rodada e a cada lacuna. Não use `fork` nem retome um revisor anterior: os dois herdam contexto, e o autor tem viés de confirmação. Passe só Ponteiros de Contexto: o arquivo do diff e a referência, o Mapa de Fluxos, o caminho da Spec, o glossário e a configuração. O revisor só lê; no Claude Code, siga a seção 4.
- **Sem subagentes, declare:** Avise o usuário que a revisão no mesmo contexto não é independente e ofereça `/revisar` numa sessão nova, sem o histórico da implementação. Se o usuário pedir para continuar, revise e escreva `Independência: mesmo contexto` no relatório.
- **Só reporte:** `/revisar` não edita código. O usuário escolhe os achados. `/ajustar` faz a correção localizada; `/implementar`, o requisito que pede uma Fatia nova; `/bug`, o defeito sem causa localizada.
- **Siga cada valor de ponta a ponta:** Um Fluxo é o caminho de um valor que o diff altera (chave, ID, coluna, status, flag, regra, assinatura ou formato de retorno), da entrada até cada consumidor: consulta, lista, detalhe, texto exibido, regra, decisão, documento gerado, export, job, notificação e API. Leia o código conectado, não só o diff: os chamadores das funções alteradas, as funções chamadas, os testes e o README. Quando uma assinatura, um retorno ou um comportamento muda, busque todos os chamadores com `rg`. Um consumidor verificado não prova os outros. Um teste verde prova só os caminhos que executa; a aprovação de um revisor, só o código que ele leu. Nenhum dos dois substitui o rastreio dos Fluxos.
- **Entregue uma rodada completa:** A rodada termina só no Critério de Fim da etapa 5. Um `[BLOCKER]` não encerra a busca: registre-o e continue.
- **Limite o ciclo com `/ajustar`:** Um achado que o usuário aceita, com o motivo, sai do `Veredito:`. Uma correção que desfaz outra é vaivém: as duas puxam o código em direções opostas, e a decisão é do usuário. Na rodada 3 sem `pode entregar`, pare o ciclo e pergunte ao usuário como seguir.
- **Passe o pente-fino anti-ruído:** Aponte comentários óbvios, código morto e imports sem uso, segundo `ste100-clean-code`.
- **Mantenha os eixos separados:** Standards e Spec ficam em seções próprias. Não junte nem reordene achados entre eixos. Um eixo aprovado não compensa o outro.
- **Classifique por severidade, em cada eixo:**
  - `[BLOCKER]`: bug, falha de segurança, perda de dados ou quebra com a carga esperada.
  - `[IMPORTANTE]`: lógica de risco sem teste, lentidão real, duplicação, função com várias responsabilidades ou código que não devia existir.
  - `[NIT]`: ganho pequeno de velocidade ou forma mais curta.
- **Exija um caso concreto:** Todo achado descreve uma entrada ou situação e o resultado errado que ela produz. Sem caso concreto, não há achado.

## 3. Processo
1. **Diff e portão:**
   - Use o alvo do usuário: mudanças locais, staged, branch, PR ou arquivos. Sem alvo, use o diff contra a branch base, com as mudanças locais. Sem diferença, use o último commit.
   - Inspecione `git status` e o diff do alvo. Registre a referência exata (ex.: `main...HEAD`). Grave o diff num arquivo temporário fora do repositório, como `$TMPDIR/diff-<branch>-<AAAA-MM-DD>.patch`. Passe o caminho e a referência aos 2 revisores. O revisor não executa git.
   - **Rodada seguinte:** Com relatório anterior de `/revisar` para o mesmo alvo, na conversa ou no handoff, esta é uma rodada seguinte. Revise o diff completo, não só o delta. A `Rodada:` é a anterior mais 1. Liste os achados anteriores para a etapa 6. Com relatório de `/ajustar`, leia também o status de cada achado, `Valores alterados:`, `Achados novos:` e `Aceitos:`. Um achado que o usuário aceitou nesta conversa, com o motivo, também conta como aceito.
   - Aplique o portão completo de `laravel-verification`, ou reutilize evidência válida para o mesmo estado. Não repita a suíte apenas por entrar na revisão.
2. **Mapa de Fluxos:** Antes dos revisores:
   - Liste os valores que o diff altera. Na rodada seguinte, inclua os valores que cada correção alterou; o relatório de `/ajustar` os lista em `Valores alterados:`.
   - Para cada valor, busque com `rg` todos os pontos que o leem ou gravam, também fora do diff: Models, Actions, Livewire, Blade, Policies, jobs, listeners, exports, PDF, e-mail, API e testes. A lista vem da busca, não da memória.
   - Registre cada Fluxo como `valor: entrada → consumidor → saída`, com `arquivo:linha` de cada ponto.
3. **Revisão em 2 eixos:** Cada revisor lê o código conectado, completa o Mapa com os consumidores que achar e rastreia cada Fluxo até a saída. Ele ordena os achados pela prioridade da seção 1. Ele devolve o status de cada arquivo do diff e de cada Fluxo no seu eixo: `verificado`, `achado` (com o título) ou `não verificado` (com o motivo). Ele termina só quando tudo tem status. Um `[BLOCKER]` não encerra o trabalho do revisor.
   - **Eixo Standards (padrões e segurança Laravel/Livewire):**
     - **Carga esperada:** Procure a carga no repositório (README, filas, Horizon, Octane, scheduler, deploy). Declare a carga presumida.
     - **Segurança:** Propriedade sensível ou ID em componente Livewire sem `#[Locked]`. Ação mutável sem `$this->authorize()` ou Policy.
     - **Perda de dados:** Erro engolido em `try/catch`. Várias escritas sem `DB::transaction()`. Job ou evento antes do commit sem `afterCommit()`. Operação que, executada 2 vezes, grava, cobra ou envia em dobro: job com retry, webhook, comando agendado, duplo clique.
     - **Escala:** N+1 (falta de `with()` ou `preventLazyLoading`). Corrida entre leitura e escrita: `firstOrCreate` sem índice único, falta de `lockForUpdate()` ou `increment()`. Tarefa repetida em cada processo: falta de `onOneServer()`, `withoutOverlapping()` ou `ShouldBeUnique`. Memória que só cresce: `->get()` em tabela grande no lugar de `chunkById()` ou `lazy()`. Algoritmo O(n²) sobre entrada grande. Estado local que devia ser compartilhado: propriedade estática no Octane, disco local com vários servidores.
     - **Velocidade:** Lentidão real é `[IMPORTANTE]`. Ganho pequeno, como trabalho repetido num laço quente, é `[NIT]`.
     - **Estrutura:** Regras e coordenação sem encapsulamento, abstração sem benefício, falta de `declare(strict_types=1);`. Aceite CRUD simples e Costuras existentes, segundo `laravel-deep-modules`.
     - **Enxuto:**
       - Apagar: código morto, import sem uso, opção sem uso, funcionalidade especulativa, comentário óbvio ou desnecessário (`ste100-clean-code`).
       - Reutilizar: o helper, a Action ou o Scope que o repositório já tem. Cite o caminho.
       - Nativo: o Laravel ou o PHP já resolve (`Collection`, `Str`, `Arr`, regras de validação). Uma dependência nova para poucas linhas também entra aqui.
       - YAGNI: interface com uma só implementação, configuração que ninguém altera.
       - Juntar: quase-cópias que precisam mudar juntas.
       - Separar: função com várias responsabilidades, difícil de ler ou testar. Separe por responsabilidade, nunca por número de linhas.
   - **Eixo Spec e comportamento:**
     - Compare o diff linha a linha com a Especificação de `/especificar`. Aponte requisito faltante e escopo extra não solicitado (*scope creep*).
     - **Bug:** Resultado errado e caso de borda (vazio, zero, último item, arredondamento, fuso horário). Chamador quebrado pela mudança. Correção num só chamador, com a função compartilhada ainda errada.
     - **Teste ausente:** Lógica de risco sem teste Pest que falhe quando ela quebra: ramo, parser, dinheiro, segurança, escrita de dados ou correção de bug. Teste que ainda passa com a Costura a devolver vazio, sem gravar nada. Peça um teste bom, não cobertura.
     - **Mapa desatualizado:** Com Mapa de Features configurado, comportamento visível alterado sem atualização do Arquivo de Feature no mesmo diff.
4. **Confirmação:** Antes de reportar, o revisor, para cada achado:
   1. Escreve o caso concreto.
   2. Relê as linhas e confirma o fato: o chamador existe, o valor pode ser vazio, o código não tem uso.
   3. Trata como decisão, não como achado, o atalho com limite documentado em ADR, Spec ou comentário de porquê. Reporta o atalho só se a carga esperada já passa desse limite.
   4. Propõe a menor correção que funciona e prefere a que apaga código. Não acrescenta camadas, pacotes ou configuração que o problema não exige.
   5. Descarta gosto de estilo, "considere..." e preocupação vaga.
5. **Consolidação (agente principal):** Antes do relatório:
   1. **Cobertura:** Confira se cada arquivo do diff e cada Fluxo têm status nos 2 eixos. Devolva cada lacuna a um revisor novo do mesmo eixo. Um revisor que falha, para antes do fim ou devolve outro formato não revisou: dispare um novo uma vez. Na segunda falha, marque o que falta `não verificado` e cite o eixo em `Não verificado:`. Sem subagentes, cubra a lacuna você mesmo.
   2. **Propagação:** Siga o valor de cada achado em todos os consumidores do Mapa. Inclua no achado cada local com o mesmo defeito. Com correção diferente, abra outro achado.
   3. **Divergência:** Investigue até resolver: os eixos afirmam fatos opostos sobre o mesmo trecho; um consumidor aparece num eixo e falta no outro; o teste citado como prova não executa o consumidor.
   4. **Achados novos:** Aplique a etapa 4 e ponha cada achado novo no eixo do seu tema. Na rodada seguinte, marque com `(perdido na rodada anterior)` o achado em código que a rodada anterior já revisava, e rastreie de novo o Fluxo inteiro desse valor. Confirme cada item de `Achados novos:` de `/ajustar` e numere o confirmado no eixo do seu tema.
   5. **Vaivém:** Na rodada seguinte, marque com `(vaivém do achado N)` o achado no trecho de uma correção de `/ajustar` que desfazer essa correção resolveria. Na **Correção**, escreva as 2 direções e a pergunta ao usuário.
   - **Critério de Fim:** Todos os arquivos e Fluxos têm status nos 2 eixos, sem lacuna nem divergência aberta. Só então escreva o relatório.
6. **Relatório:**
   - Comece com `Alvo:` (referência, branch e commit, ex.: `main...HEAD` em `feature/pedidos@3f9c2ab`). Na linha seguinte, escreva `Rodada: N`; a primeira é 1. Sem subagentes, escreva `Independência: mesmo contexto`. Depois, `O que a mudança faz:` em 2 ou 3 frases.
   - Na rodada seguinte, escreva em seguida `Achados anteriores:`, 1 linha por achado: `corrigido`, `corrigido em parte`, `não corrigido`, `não reproduz` ou `aceito`, com a prova ou o motivo.
     - `corrigido em parte` ou `não corrigido`: volta numerado no seu eixo e entra no `Veredito:`.
     - `não reproduz` de `/ajustar`, com a prova de que o teste executa o caso: fica fora do `Veredito:`. Só volta numerado com um caso concreto novo que o refuta.
     - `aceito`: o usuário decidiu não corrigir, com o motivo. Fica fora do `Veredito:`. Só volta numerado com um caso concreto novo que o motivo do aceite não cobre. Sem motivo, o aceite não vale: pergunte o motivo.
   - Apresente os achados sob `## Standards` e `## Spec`, cada um com seus `[BLOCKER]`, `[IMPORTANTE]` e `[NIT]`, nesta ordem. Omita o nível sem achados. Numere em sequência contínua entre os eixos, sem reordenar, para o usuário responder "corrija 2 e 5". Explique cada termo técnico na primeira vez: o leitor pode não conhecer o código.
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
     - `Carga presumida:` a carga do eixo Standards.
     - `Aceitos:` 1 linha por achado aceito, com o motivo, quando houver.
     - Sem `[BLOCKER]` nem `[IMPORTANTE]`: `Veredito: pode entregar.` Caso contrário: `Veredito: corrija 1 e 3 antes.`, com os números.
     - `Enxuto: -N linhas possíveis.` quando houver achado de Enxuto.
     - `Não verificado:` em 1 linha, quando algo importante ficou sem verificação.
   - Sem achados nos 2 eixos: `Alvo:`, `Rodada:`, `O que a mudança faz:`, `Sem achados. Pode entregar.`, `Fluxos rastreados:`, `Aceitos:` quando houver e 1 linha com o que foi verificado.
   - Com `Veredito: corrija ...` antes da rodada 3, ofereça `/ajustar` com os números do veredito.
   - **Limite de rodadas:** Na rodada 3 com `Veredito: corrija ...`, não ofereça `/ajustar`. Liste os achados abertos por nível e faça uma pergunta ao usuário: aceitar os abertos, com o motivo, e entregar; fazer mais uma rodada; ou voltar a `/especificar` ou `/planejar`. Três rodadas sem convergir indicam, em geral, uma Spec ou um desenho errado. Com mais uma rodada, repita a pergunta no fim de cada rodada seguinte.
   - Com `[BLOCKER]`, entregue o relatório completo, não execute as etapas 7 e 8 e pergunte ao usuário como seguir.
7. **Fato de segurança:** Identifique o único fato que torna a mudança segura (ex.: "a migration só adiciona coluna nullable"). Prove-o com um teste Pest ou um script que executa o código real. Sem prova, escreva `não provado`.
8. **Briefing de PR (no máximo 40 linhas de alto sinal, ASD-STE100):**
   - **Por que (Why):** 1 ou 2 frases sobre o problema resolvido.
   - **O que mudou (What changed):** bullets curtos sobre as Fronteiras (`Livewire`/HTTP) e as Costuras (`Actions`/DTOs). Não liste cada arquivo: o Git já mostra.
   - **Porta de Decisão e Raio de Explosão (Blast Radius):** Classifique a mudança como **Porta de 2 Vias** (reversível sem perda de dados) ou **Porta de 1 Via** (ex.: migration destrutiva, alteração de contrato externo). Liste exatamente as rotas, tabelas e componentes que a mudança pode afetar: toda mudança toca algum. Inclua o fato de segurança com a prova ou `não provado`. Liste os achados `aceito` como **Riscos aceitos**, com o motivo.
   - **Prova de Execução (`[measured]`):** resumo do portão completo de `laravel-verification`.

## 4. No Claude Code
Use o agente customizado `revisor`, com `model: inherit` e as ferramentas `Read, Grep, Glob`.

1. Copie o [template](assets/revisor.md) para `.claude/agents/revisor.md` na raiz do projeto consumidor. Se o arquivo já existe, preserve as customizações.
2. Instale `laravel-deep-modules`, `laravel-tdd-seams` e `ste100-clean-code` para o Claude Code. O campo `skills` do template pré-carrega essas disciplinas.
3. Delegue com `subagent_type: revisor`, um por eixo, na mesma mensagem. Passe o eixo, o caminho deste SKILL.md e os Ponteiros de Contexto. Não use o tipo `fork`.
4. O revisor não executa git nem testes. Por isso, a etapa 1 grava o diff num arquivo, e o principal executa o portão e a prova do fato de segurança.
5. Sem o agente registrado, use o subagente geral com o mesmo contrato. Avise o usuário: o subagente geral tem todas as ferramentas, e a regra "só lê" fica só na instrução. Criar o primeiro diretório de agentes durante a sessão pode exigir reiniciar o Claude Code.

Fonte: [subagentes do Claude Code](https://code.claude.com/docs/en/sub-agents).

## 5. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Achei um `[BLOCKER]`; paro e reporto agora." | **Proibido.** Conclua os 2 eixos e a Consolidação. Reporte todos os achados juntos. |
| "Os revisores aprovaram e os testes passam; a revisão acabou." | **Proibido.** Teste e revisor provam só o que executam ou leem. A revisão acaba no Critério de Fim. |
| "A lista elimina chaves repetidas; a chave está certa." | **Proibido.** Um consumidor não prova os outros. Siga a mesma chave no detalhe, nos termos, nas decisões e nos documentos. |
| "Nesta rodada, basta revisar o delta da correção." | **Proibido.** Revise o diff completo e os Fluxos que a correção toca. |
| "O diff está correto; o resto do código não mudou." | **Proibido.** Uma assinatura, um retorno ou um comportamento novo quebra chamadores fora do diff. Busque todos. |
| "O `[BLOCKER]` é simples; corrijo durante a revisão." | **Proibido.** Corrigir mistura autor e revisor e esconde a decisão do usuário. |
| "Junto os achados dos 2 eixos numa lista por prioridade." | **Proibido.** Um eixo mascararia o outro. |
| "Não há impacto nenhum no Raio de Explosão." | **Proibido.** Toda mudança toca alguma rota, tabela ou componente. Nomeie cada um. |
| "O raio de explosão está claro; não preciso rodar nada." | **Proibido.** Execute código que prove o fato de segurança, ou escreva `não provado`. |
| "Escrevo um PR de 200 linhas com cada arquivo modificado." | **Proibido.** O briefing tem no máximo 40 linhas de alto sinal. |
| "Sem caso concreto, anoto 'considere...' por precaução." | **Proibido.** A preocupação vaga esconde os achados reais. |
| "A correção certa é um Service, uma Interface e uma configuração nova." | **Proibido.** Proponha a menor correção. Prefira a que apaga código. |
| "Não há subagente; reviso aqui e entrego como revisão normal." | **Proibido.** Avise, ofereça uma sessão nova e escreva `Independência: mesmo contexto`. |
| "Uso um `fork` ou o revisor da rodada anterior; ele já conhece o código." | **Proibido.** Os dois herdam contexto. Use um revisor novo. |
| "O revisor do eixo Spec falhou; o eixo está sem achados." | **Proibido.** Um revisor que falha não revisou. Dispare um novo; na segunda falha, marque `não verificado`. |
| "O achado aceito apareceu de novo; numero outra vez." | **Proibido.** Ele só volta com um caso concreto novo que o motivo do aceite não cobre. |
| "A correção nova desfaz a anterior; proponho só a nova." | **Proibido.** Marque o vaivém e leve as 2 direções ao usuário. |
| "Na rodada 4 ainda há achados; ofereço mais um `/ajustar`." | **Proibido.** Na rodada 3, pare o ciclo e pergunte ao usuário como seguir. |

## 6. Prova de Execução (Critério de Saída)
- `[measured]` Relatório com `Alvo:` e `Rodada:`, eixos em seções próprias, sem edição de código.
- `[measured]` Revisores novos e só de leitura, com o diff em arquivo; ou a linha `Independência: mesmo contexto`.
- `[measured]` Mapa de Fluxos por busca; status de cada arquivo e Fluxo nos 2 eixos.
- `[measured]` Consolidação concluída antes do relatório: lacunas devolvidas, achados propagados aos consumidores do mesmo valor e divergências resolvidas.
- `[measured]` Um só relatório com todos os achados confirmados da rodada, também com `[BLOCKER]`.
- `[measured]` Cada achado com caso concreto, `arquivo:linha` e as 4 partes; busca de chamadores citada para cada assinatura, retorno ou comportamento alterado.
- `[measured]` Achado `aceito` fora do `Veredito:`, com o motivo. Na rodada seguinte: diff completo, status de cada achado anterior, Fluxos das correções rastreados e vaivém marcado com as 2 direções e a pergunta. Na rodada 3 sem `pode entregar`: a pergunta, sem oferta de `/ajustar`.
- `[measured]` Carga presumida declarada e fato de segurança provado por execução, ou `não provado`.
- `[measured]` Portão completo de `laravel-verification` aprovado para o estado revisado, com comandos, escopos e resultados citados.
- `[measured]` Briefing de PR com o Raio de Explosão entregue ao usuário.
