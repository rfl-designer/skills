---
name: pausar
description: Para o trabalho numa fronteira segura e grava uma nota de handoff para que um agente novo retome sem refazer nada. Use quando o usuário digitar /pausar.
argument-hint: "Qual é o foco da próxima sessão?"
disable-model-invocation: true
---

# Pausar e Passar o Trabalho (`/pausar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Parar o trabalho num ponto seguro e gravar uma nota de handoff. Um agente novo, sem o histórico do chat, lê a nota e continua do ponto exato. Ele não refaz investigação, teste ou decisão já concluída.

## 2. Regras Inegociáveis
- **Pare numa fronteira segura:** Termine o passo atômico atual ou desfaça-o. Não comece trabalho novo. Cancele os subagentes em execução.
- **Não faça ação irreversível para pausar:** Sem commit, sem push e sem PR. Registre na nota que as alterações ficam sem commit no working tree.
- **Preserve a configuração na retomada:** Cite o arquivo de configuração e o escopo da aplicação na nota. Specs e tickets podem estar em destinos diferentes.
- **Aponte para os artefatos, não os copie:** Spec, tickets, ADRs, glossário configurado, commits e diffs já guardam o conteúdo. Cite cada um por caminho ou URL.
- **Separe fato de suposição:** Cada afirmação sobre o estado leva o rótulo `[measured]`, `[inferred]` ou `[guess]`. Uma decisão do usuário só entra como decidida se ele a declarou nesta sessão ou se um artefato a registra.
- **Remova dados sensíveis:** Tire da nota chaves de API, senhas, tokens, dados de `.env` e dados pessoais.
- **Grave a nota fora do repositório:** Use o diretório temporário do sistema (`$TMPDIR`, senão `/tmp`).

## 3. Processo
1. **Fronteira:** Conclua ou desfaça o passo atual. Remova a instrumentação temporária (`dd`, `dump`, `Log::debug`) ou registre na nota onde ela está.
2. **Estado do repositório:** Execute `git status`, `git branch --show-current` e `git log --oneline -5`. Aplique o modo pausa de `laravel-verification`: registre resultados existentes e o estado que cobrem; marque os invalidados como `desatualizado`. Não execute a suíte completa apenas para pausar.
3. **Foco:** Se o usuário passou argumento, use-o como foco da próxima sessão e corte da nota o que não serve a esse foco.
4. **Nota:** Normalize a branch para um nome de arquivo (troque `/` e caracteres especiais por `-`). Grave `$TMPDIR/handoff-<branch>-<AAAA-MM-DD>.md` com estas seções, nesta ordem:
   - **Objetivo:** O que o usuário quer, em 1 a 3 frases.
   - **Feito:** O que está pronto e qual verificação provou isso (comando e resultado).
   - **Estado atual:** Branch, arquivos alterados sem commit e o resultado do portão de verificação.
   - **Próximo passo:** A primeira ação concreta na retomada.
   - **Pendências:** Perguntas abertas, riscos e aprovações que o usuário ainda não deu.
   - **Armadilhas:** O que o agente novo não descobre lendo o código: hipóteses refutadas, caminhos sem saída, convenções não escritas.
   - **Artefatos:** Caminhos e URLs da Spec, dos tickets, dos ADRs e de outros arquivos-chave. Um relatório de `/revisar` ou `/ajustar` que existe só no chat vai sem alteração para `$TMPDIR/relatorio-<skill>-<branch>-<AAAA-MM-DD>.md`; cite o caminho aqui.
   - **Skills sugeridas:** As skills que o agente novo deve carregar (por exemplo `/implementar` e `laravel-verification`).
   - **Para retomar:** Copie as 4 instruções do passo 5.
5. **Instruções de retomada (vão dentro da nota):**
   1. Leia esta nota e os artefatos citados antes de agir.
   2. Execute `git status` e `git log --oneline -5`. Se o repositório diverge da nota, o repositório vale. Informe a diferença ao usuário.
   3. Não refaça o trabalho da seção Feito. Execute de novo só a verificação que o próximo passo exige ou que o código alterado invalidou.
   4. Não trate como aprovado o que esta nota não registra como decisão do usuário.
6. **Resposta:** Informe ao usuário o caminho da nota, o estado do working tree e o próximo passo. Não cole a nota no chat.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou fazer um commit `wip:` para não perder as alterações." | **Proibido.** A pausa não autoriza um novo commit. Preserve commits já autorizados e registre as alterações restantes sem commit. |
| "Vou copiar a Spec inteira na nota para o próximo agente ter tudo." | **Proibido.** A cópia envelhece e diverge da fonte. Cite o caminho. |
| "Os testes passaram mais cedo, vou escrever que está tudo verde." | Confira o estado coberto. Preserve `[measured]` se nada relevante mudou; caso contrário, marque `desatualizado` e registre o comando pendente. |
| "O usuário pareceu concordar com a opção A, vou registrar como decidido." | **Proibido.** Registre como decisão só o que o usuário declarou. O resto vai para Pendências. |
| "Vou começar o próximo ticket antes de pausar." | **Proibido.** Pausar significa parar na fronteira atual. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Saída de `git status` e da branch atual citada na nota.
- `[measured]` Últimos resultados com escopo e estado coberto, distinguindo válidos, desatualizados, não executados e não aplicáveis.
- `[measured]` Caminho da nota gravada, com as 9 seções preenchidas ou marcadas como "nenhuma".
- `[measured]` Nenhum segredo na nota: busca por `KEY`, `SECRET`, `PASSWORD` e `TOKEN` sem resultado.
