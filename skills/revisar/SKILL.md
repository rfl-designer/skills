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
- **Use subagentes com contexto limpo:** Sempre que a ferramenta suportar subagentes, dispare 2 revisores paralelos isolados passando apenas Ponteiros de Contexto (referência do diff da etapa 1, Mapa de Fluxos da etapa 2, caminho da Spec, glossário e configuração do projeto). O agente que escreveu o código tem viés de confirmação.
- **Reporte, não corrija:** `/revisar` não edita código. O usuário decide quais achados corrigir. A correção acontece depois, em `/ajustar`, `/implementar` ou `/bug`.
- **Leia o código conectado, não só o diff:** Leia os chamadores das funções alteradas, as funções chamadas, os testes e o README. Quando uma assinatura, um retorno ou um comportamento muda, busque todos os chamadores com `rg`.
- **Siga cada valor de ponta a ponta:** Um Fluxo é o caminho de um valor que o diff altera (chave, ID, coluna, status, flag, regra ou formato de retorno), da entrada até cada consumidor: consulta, lista, detalhe, texto exibido, regra, decisão, documento gerado, export, job, notificação e API. A verificação de um consumidor não prova os outros. Exemplo: a lista elimina chaves repetidas, mas o detalhe, os termos, a decisão de exigir assinatura e o PDF também leem a mesma chave. Confira cada um.
- **Entregue a revisão completa numa rodada:** A rodada termina só no Critério de Fim da etapa 5. Um `[BLOCKER]` não encerra a busca: registre-o e continue. Assim, o usuário corrige todos os achados de uma vez.
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
   - Inspecione `git status` e o diff do alvo. Registre a referência exata (ex.: `main...HEAD`) e passe a mesma referência aos dois subagentes.
   - **Rodada seguinte:** Com um relatório anterior de `/revisar` para o mesmo alvo, na conversa ou no handoff, esta é uma rodada seguinte. Use o diff completo do alvo, não só o delta da correção. Liste os achados anteriores para a etapa 6.
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
     - **Perda de dados:** Caça erro engolido em `try/catch`, várias escritas sem `DB::transaction()` e job ou evento disparado antes do commit sem `afterCommit()`.
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
     - **Teste ausente:** Aponta lógica de risco sem um teste Pest que falhe quando ela quebra: ramo, parser, dinheiro, segurança, escrita de dados ou correção de bug. Pede um teste bom, não cobertura.
     - **Mapa desatualizado:** Com Mapa de Features configurado, aponta comportamento visível alterado sem atualização do Arquivo de Feature no mesmo diff.
4. **Confirmação dos Achados:** Antes de reportar, cada subagente:
   1. Escreve o caso concreto de cada achado.
   2. Relê as linhas e confirma o fato: o chamador existe, o valor pode ser vazio, o código não tem uso.
   3. Trata como decisão, não como achado, o atalho com limite documentado em ADR, Spec ou comentário de porquê. Reporta o atalho só se a carga esperada já passa desse limite.
   4. Propõe a menor correção que funciona. Prefere a correção que apaga código. Não adiciona camadas, pacotes ou configuração que o problema não exige.
   5. Descarta gosto de estilo, "considere..." e preocupação vaga.
5. **Consolidação (agente principal):** Com os retornos dos dois eixos, antes do relatório:
   1. **Cobertura:** Confira se cada arquivo do diff e cada Fluxo têm status nos dois eixos. Devolva cada lacuna a um subagente do mesmo eixo, com contexto limpo. Sem subagentes, cubra a lacuna você mesmo.
   2. **Propagação:** Para cada achado, siga o mesmo valor em todos os consumidores do Mapa. Inclua no achado cada local com o mesmo defeito. Quando a correção difere, abra um achado próprio.
   3. **Divergência:** Investigue até resolver: os eixos afirmam fatos opostos sobre o mesmo trecho (ex.: um diz que o valor nunca é vazio, o outro diz que é); um consumidor aparece no retorno de um eixo e falta no outro; o teste citado como prova não executa o consumidor em questão.
   4. **Achados novos:** Aplique a etapa 4 a cada achado novo da Consolidação. Coloque-o no eixo do seu tema. Na rodada seguinte, marque com `(perdido na rodada anterior)` o achado em código que a rodada anterior já revisava, e rastreie de novo o Fluxo inteiro desse valor.
   - **Critério de Fim:** Todos os arquivos e Fluxos têm status nos dois eixos, sem lacuna nem divergência aberta. Só então escreva o relatório.
6. **Relatório por Eixo:**
   - Comece com `O que a mudança faz:` em 2 ou 3 frases.
   - Na rodada seguinte, escreva em seguida `Achados anteriores:`, com 1 linha por achado: `corrigido`, `corrigido em parte` ou `não corrigido`, e a prova.
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
     - Sem `[BLOCKER]` nem `[IMPORTANTE]`: `Veredito: pode entregar.` Caso contrário: `Veredito: corrija 1 e 3 antes.`, com os números desses achados.
     - `Enxuto: -N linhas possíveis.` quando houver achado de Enxuto.
     - `Não verificado:` em 1 linha, quando algo importante não pôde ser verificado.
   - Sem achados nos dois eixos: escreva `O que a mudança faz:`, depois `Sem achados. Pode entregar.`, `Fluxos rastreados:` e 1 linha com o que foi verificado.
   - Com `[BLOCKER]`, entregue o relatório completo, não execute as etapas 7 e 8 e pergunte ao usuário como seguir. Ofereça `/ajustar` com os números do veredito.
7. **Prova do Fato de Segurança:** Identifique o único fato que torna a mudança segura (ex.: "a migration só adiciona coluna nullable"). Prove esse fato com um teste Pest ou um script que executa o código real. Se não conseguir provar, escreva `não provado`.
8. **Geração do Briefing de PR (Máximo 40 linhas, padrão ASD-STE100):**
   - **Por que (Why):** 1 a 2 frases explicando o problema resolvido.
   - **O que mudou (What changed):** Bullets curtos focados nas Fronteiras (`Livewire`/HTTP) e Costuras (`Actions`/DTOs).
   - **Porta de Decisão e Raio de Explosão (Blast Radius):** Classifique a mudança como **Porta de 2 Vias** (reversível sem perda de dados) ou **Porta de 1 Via** (ex.: migration destrutiva, alteração de contrato externo) e liste exatamente quais rotas/componentes podem ser afetados. Inclua o fato de segurança da etapa 7 com a prova ou o rótulo `não provado`.
   - **Prova de Execução (`[measured]`):** Resumo dos resultados do Pest, Larastan e Pint.

## 4. Racionalizações Proibidas (Anti-Atalho)
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

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Relatório dos 2 eixos (Standards + Spec) entregue em seções separadas, sem edição de código.
- `[measured]` Mapa de Fluxos montado por busca, com status de cada arquivo do diff e de cada Fluxo nos dois eixos.
- `[measured]` Consolidação concluída antes do relatório: lacunas devolvidas, achados propagados aos consumidores do mesmo valor e divergências resolvidas.
- `[measured]` Um só relatório com todos os achados confirmados da rodada, também quando há `[BLOCKER]`.
- `[measured]` Na rodada seguinte: diff completo revisado, status de cada achado anterior e Fluxos das correções rastreados.
- `[measured]` Cada achado com caso concreto, `arquivo:linha` e as 4 partes (O que é, Problema, Correção, Se não corrigir).
- `[measured]` Busca de chamadores citada para cada assinatura, retorno ou comportamento alterado.
- `[measured]` Carga presumida declarada no relatório.
- `[measured]` Fato de segurança provado por execução, ou rotulado `não provado`.
- `[measured]` Portão completo de `laravel-verification` aprovado para o estado revisado, com comandos, escopos e resultados citados.
- `[measured]` Briefing de PR com seção de Raio de Explosão entregue ao usuário.
