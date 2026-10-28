---
name: ajustar
description: Corrige os achados de um relatório de /revisar com subagentes Ajustadores. Agrupa os achados em Lotes, prova cada correção pelo tipo do achado, segue cada valor alterado até os consumidores e verifica o estado integrado. Use quando o usuário digitar /ajustar.
argument-hint: "[números dos achados, ex.: 2 5]"
disable-model-invocation: true
---

# Corrigir os Achados da Revisão (`/ajustar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Corrigir os achados escolhidos do relatório de `/revisar`. O agente principal agrupa os achados em Lotes e delega cada Lote a um Ajustador. O Ajustador prova cada correção. O principal integra os Lotes, procura regressões nos valores alterados e verifica o estado integrado. Depois, o usuário roda `/revisar` para a rodada seguinte.

## 2. Termos
- **Achado:** item numerado do relatório de `/revisar`, com caso concreto, `arquivo:linha` e as 4 partes (O que é, Problema, Correção, Se não corrigir).
- **Fluxo:** o caminho de um valor, da entrada até cada consumidor, como em `/revisar`.
- **Lote:** grupo de achados que um só Ajustador corrige.
- **Ajustador:** subagente que corrige um Lote.
- **Valor alterado:** o que a correção muda e outro código lê: chave, ID, coluna, status, flag, regra, assinatura ou formato de retorno. É a mesma lista de `/revisar`.

## 3. Regras Inegociáveis
- **Carregue as disciplinas de modelo:** Aplique `laravel-deep-modules`, `laravel-tdd-seams`, `laravel-verification` e `ste100-clean-code`.
- **Corrija os achados escolhidos:** O argumento ou a mensagem do usuário escolhe os achados ("corrija 2 e 5"). Sem escolha, use os achados do `Veredito:` do relatório: todos os `[BLOCKER]` e `[IMPORTANTE]`. Um `[NIT]` entra só quando o usuário o escolhe.
- **Registre os achados aceitos:** Quando o usuário decide não corrigir um achado, ele o aceita. Registre o achado em `Aceitos:`, com o motivo do usuário. Sem motivo, pergunte o motivo. Um achado que o usuário não escolheu não está aceito: ele continua aberto.
- **Leve o vaivém ao usuário:** Um achado com `(vaivém do achado N)` não entra num Lote antes da resposta do usuário. A Correção dele traz as duas direções e a pergunta.
- **Mande cada achado à skill certa:** `/ajustar` corrige achados com correção localizada. O requisito faltante que pede uma Fatia nova (tela, rota, Action ou tabela nova) vai para `/implementar`. O defeito sem causa localizada vai para `/bug`. Esses achados ficam fora dos Lotes.
- **Use o relatório como contrato:** A Correção do achado é o ponto de partida. O Ajustador pode aplicar uma correção menor que resolve o mesmo caso concreto. Uma correção que muda a Spec, muda um contrato externo ou exige escolha entre opções recebe o status `bloqueado`, com a pergunta para o usuário.
- **Prove cada correção pelo tipo do achado:**
  - **Com comportamento:** O caso concreto vira um teste Pest. O teste falha antes da correção pelo motivo do achado (RED) e passa depois (GREEN).
  - **Teste ausente:** Escreva o teste. Quebre a lógica de propósito, veja o teste falhar e desfaça a quebra. Aqui, o teste verde na primeira execução é o resultado esperado.
  - **Estrutura ou duplicação:** Os testes do trecho e o portão são a prova. Sem teste no trecho, escreva antes um teste de caracterização: ele fixa o comportamento atual e fica verde antes e depois.
  - **Código morto, import ou comentário:** A prova é a busca com `rg` sem uso e o portão.
  - **Mapa desatualizado:** A prova é o conferidor de `/mapear` e a condução da entrada afetada, segundo `laravel-verification`.
  - **Sem teste viável** (condição de corrida, carga): Registre o motivo e use a prova mais próxima, como a contagem de queries ou o índice único no schema. Marque a prova como `parcial`.
- **Prove o `não reproduz`:** No achado com comportamento, o teste pode passar antes da correção. Antes de concluir, altere a linha do achado de propósito e veja o teste falhar; depois, desfaça a alteração. Com a falha, o teste executa o caso: registre `não reproduz` com o teste e as duas saídas, e mantenha a produção sem alteração. Sem a falha, o teste não executa o caso: reescreva-o para o caso concreto.
- **Corrija em todos os locais:** Corrija cada local que o achado lista. Depois, busque com `rg` o mesmo padrão no repositório inteiro. Um local com o mesmo defeito e a mesma correção entra no achado. Um local que pede outra correção vira achado novo.
- **Siga cada valor alterado:** Para cada valor que a correção altera, busque com `rg` todos os consumidores e confira cada um. Um consumidor quebrado pela correção é regressão do Lote. Nos arquivos do Lote, corrija-a. Fora deles, devolva o local ao principal, que atribui a regressão.
- **Fique no escopo do Lote:** Um defeito sem relação com os achados do Lote volta ao principal como achado novo, com caso concreto e `arquivo:linha`. O principal o reporta no fim, sem corrigi-lo nesta rodada.
- **Delegue com contexto limpo:** Passe ponteiros e o contrato da seção 4, sem o histórico do chat. Cada Ajustador carrega as disciplinas de modelo; não presuma que herdou as skills do principal.
- **Limite a concorrência:** Use até 2 Ajustadores ao mesmo tempo, só em Lotes independentes e worktrees separados. Cada worktree precisa do diff revisado. Com o diff sem commit, transfira-o de forma revisável para cada worktree, ou use um Ajustador por vez no checkout atual. Não crie commit para fabricar a base.
- **Faça commit só no fim:** O Ajustador não faz commit. Com autorização da sessão, o principal faz um commit por Lote depois do portão integrado, com os números dos achados na mensagem. Nenhum commit entra com o portão vermelho. Sem autorização, mantenha o diff no working tree.
- **Deixe o veredito para `/revisar`:** `/ajustar` prova as correções. A rodada seguinte de `/revisar` revisa o diff completo e confirma o resultado.

## 4. Preparar e delegar (agente principal)
1. **Relatório:** Use o relatório mais recente de `/revisar` para o mesmo alvo, da conversa ou do arquivo citado no handoff. Os números dos achados valem só nesse relatório. Sem relatório, ou com achados sem as 4 partes, peça o relatório ao usuário ou ofereça uma nova rodada de `/revisar`. Os achados vêm do relatório, não de memória ou resumo.
2. **Seleção:** Aplique a regra de seleção. Mostre a lista com número, nível e título, e continue. Mostre à parte os achados que vão para `/implementar` ou `/bug`.
   - Seleção vazia (`Veredito: pode entregar.` ou `Sem achados.`, sem escolha do usuário): informe e pare.
   - Número que o relatório não tem: informe e não o delegue.
   - Pedido sem achado no relatório: ofereça `/bug` ou `/revisar`.
   - Pedido ambíguo: pergunte e espere a resposta.
   - Achado com `(vaivém do achado N)`: faça a pergunta da Correção antes de delegar. Com a direção escolhida, ele entra num Lote. Com a decisão de manter o código, ele vira `aceito`.
3. **Estado:** Confira `git status` e a linha `Alvo:` do relatório. Com outra branch no checkout, pare e pergunte. Releia o `arquivo:linha` de cada achado; com código alterado depois do relatório, localize o trecho de novo. Sem o trecho, marque o achado `desatualizado` e não o delegue.
4. **Lotes:** Coloque no mesmo Lote os achados que tocam o mesmo valor, o mesmo Fluxo ou os mesmos arquivos. Assim, um só Ajustador corrige o valor em todos os consumidores. Coloque achados sem nada em comum em Lotes separados. Delegue primeiro os Lotes com `[BLOCKER]`. Um Lote que depende de outro espera a integração desse outro.
5. **Agente:** No Claude Code, siga a seção 7. Em outros ambientes, use o mecanismo e os modelos autorizados disponíveis; não traduza IDs da Anthropic para outro provedor. Sem subagentes, corrija um Lote por vez no agente principal e informe a limitação.
6. **Contrato:** Envie a cada Ajustador, com caminhos válidos no diretório dele:
   - Os achados do Lote, copiados do relatório com as 4 partes e todos os locais.
   - As linhas de `Fluxos rastreados:` que passam por esses achados.
   - Spec, configuração do projeto, instruções locais e os caminhos das 4 disciplinas de modelo.
   - Base e diretório de execução, com o diff revisado presente. Arquivos sob sua responsabilidade e limites de escopo.
   - Comandos e recursos de verificação. Banco, portas e app local compartilhados exigem isolamento ou serialização. Um worktree sozinho não isola esses recursos.
   - O formato de retorno da seção 5.

Avise cada Ajustador que há outros agentes no repositório: não reverta mudanças alheias. O Ajustador não delega de novo e não faz commit.

## 5. Processo do Ajustador (por Lote)
1. **Base:** Confirme o diretório, a base, o diff revisado e os achados do Lote. Não selecione outros achados.
2. **Prova antes:** Escolha a prova de cada achado pela seção 3. No achado com comportamento, escreva o teste do caso concreto na Costura ou na Fronteira. Execute `./vendor/bin/pest --filter=<Teste>` e confirme a falha pelo motivo do achado.
3. **Correção:** Aplique a menor correção que resolve o caso em todos os locais. Prefira a correção que apaga código.
4. **Prova depois:** Execute a prova de cada achado até ela passar.
5. **Propagação:** Busque com `rg` o padrão corrigido e cada valor alterado. Confira cada consumidor. Trate a regressão e o defeito sem relação pela seção 3.
6. **Portão:** Aplique o portão completo de `laravel-verification`: Pint com Blade habilitado → PHPStan → Pest, mais navegador quando necessário.
7. **Retorno:** Devolva neste formato, sem colar os arquivos:

```markdown
Lote: A (achados 2, 5 e 6)
Achado 2: corrigido. RED: `pest --filter=AgrupaItensPorChave` falhou com "esperado 3 itens, recebido 4". GREEN: passou. Locais: app/Actions/AgruparItens.php:31, resources/views/pdf/termos.blade.php:18, app/Jobs/EnviarResumo.php:19 (mesmo defeito, achado na busca).
Achado 5: não reproduz. `pest --filter=ExigeAssinatura` passou antes da correção. Com app/Actions/ExigirAssinatura.php:12 alterada de propósito, o teste falhou; alteração desfeita. Produção sem alteração.
Achado 6: bloqueado. Pergunta: nos pedidos já assinados, o PDF mostra a chave antiga ou a nova? A Spec não responde.
Valores alterados: `AgruparItens::handle()` agora devolve `Collection<string, Item>`. Consumidores conferidos: app/Livewire/Pedido/Detalhe.php:44, app/Jobs/GerarPdf.php:27.
Regressão fora do Lote: app/Exports/PedidosExport.php:52 lê o retorno antigo de `AgruparItens::handle()`.
Achados novos: app/Http/Controllers/CupomController.php:30 aceita cupom vencido; caso: cupom vencido ontem dá desconto hoje.
Portão: Pint ok, PHPStan ok, Pest 412 passed (suíte completa), diretório ../wt-lote-a, diff sem commit.
Pendências: achado 6.
```

## 6. Integrar e verificar (agente principal)
1. **Conferência:** Cada achado do Lote tem status (`corrigido`, `não reproduz` ou `bloqueado`) e a prova do seu tipo, da seção 3. Com prova faltante, retome o mesmo Ajustador com a pendência e preserve o trabalho válido.
2. **Bloqueados:** Termine os outros Lotes. Faça as perguntas dos achados `bloqueado` no relatório, sem parar a rodada. A resposta "fica como está", com o motivo, torna o achado `aceito`.
3. **Integração:** Integre um Lote por vez, só com o delta do Lote. Um conflito que muda comportamento volta ao ciclo de prova do Lote afetado.
4. **Regressões:** Junte os `Valores alterados` de todos os Lotes. No estado integrado, busque de novo com `rg` os consumidores de cada valor e confira cada um. Dois Lotes podem alterar o mesmo Fluxo de formas incompatíveis. Atribua cada regressão ao Lote dono do arquivo, ou a um Lote novo.
5. **Portão:** Execute o portão completo de `laravel-verification` no estado integrado. A evidência de worktrees isolados não prova a combinação.
6. **Fechamento:** Com o portão aprovado e a autorização da sessão, faça um commit por Lote. Limpe só os worktrees criados por este fluxo, depois de preservar a integração e as evidências.
7. **Relatório:**
   - 1 linha por achado: número, título, status (`corrigido`, `não reproduz`, `bloqueado` ou `desatualizado`) e prova.
   - Os achados enviados a `/implementar` ou `/bug`, quando houver.
   - `Valores alterados:` 1 linha por valor, com os consumidores conferidos. A rodada seguinte de `/revisar` coloca esses valores no Mapa de Fluxos.
   - `Achados novos:` caso concreto e `arquivo:linha`, quando houver. Ofereça `/bug` para cada um. A rodada seguinte de `/revisar` também os confere.
   - As perguntas dos achados `bloqueado`.
   - `Aceitos:` 1 linha por achado aceito, com o motivo, quando houver. A rodada seguinte de `/revisar` os deixa fora do `Veredito:`.
   - `Portão:` comandos, escopo e resultado no estado integrado.
   - Última linha: `Próximo passo: rode /revisar para a rodada seguinte.`

## 7. No Claude Code
Use o agente customizado `ajustador`, com `model: claude-sonnet-5-5` e `effort: medium`. O principal mantém o próprio modelo.

1. Copie o [template](assets/ajustador.md) para `.claude/agents/ajustador.md` na raiz do projeto consumidor. Se o arquivo já existe, preserve as customizações.
2. Instale as 4 disciplinas de modelo para o Claude Code. O campo `skills` do template pré-carrega essas disciplinas.
3. Delegue com `subagent_type: ajustador`, sem override de modelo. Com 2 Lotes independentes, envie os 2 Ajustadores na mesma mensagem para rodarem em paralelo.
4. Confira o modelo e o esforço efetivos em `/tasks`. `CLAUDE_CODE_EFFORT_LEVEL` e políticas de modelo podem substituir o template. Se o resultado diverge, informe a causa; não declare Sonnet 5.5 medium sem confirmação.
5. O isolamento nativo pode partir da branch padrão, não do HEAD da sessão, e não leva o diff sem commit. Confira o commit-base e o diff revisado em cada worktree antes da correção.
6. Sem o agente registrado, use o subagente geral com o mesmo contrato. Informe que ele herda o modelo do principal. Criar o primeiro diretório de agentes durante a sessão pode exigir reiniciar o Claude Code.

Fonte: [subagentes do Claude Code](https://code.claude.com/docs/en/sub-agents).

## 8. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "O achado é óbvio; corrijo sem teste RED." | **Proibido.** Sem RED, nada prova que o teste captura o achado. |
| "O relatório indica o local; corrijo só ali." | **Proibido.** Busque o padrão e o valor no repositório inteiro. Um consumidor sem correção mantém o defeito. |
| "O teste passou antes da correção; ajusto o teste até falhar." | **Proibido.** Altere a linha do achado de propósito. Se o teste falha, registre `não reproduz`. Se não falha, reescreva o teste para o caso concreto. |
| "Achei outro defeito antigo no caminho; corrijo também." | **Proibido.** Devolva como achado novo. Só o mesmo defeito com a mesma correção e a regressão da correção entram no Lote. |
| "O diff está sem commit; faço um commit para criar a base do worktree." | **Proibido.** Transfira o diff de forma revisável ou use um Ajustador por vez no checkout atual. |
| "O requisito faltante é só uma tela nova; implemento como correção." | **Proibido.** Uma Fatia nova vai para `/implementar`, com teste na Costura e na Fronteira. |
| "Cada Lote passou nos testes; a integração está verde." | **Proibido.** Busque os consumidores dos valores alterados e rode o portão no estado integrado. |
| "As correções têm prova; a revisão está aprovada." | **Proibido.** A rodada seguinte de `/revisar` dá o veredito. |
| "Já estou no arquivo; corrijo os `[NIT]` também." | **Proibido.** Um `[NIT]` entra só com a escolha do usuário. |
| "A correção exige mudar a Spec; decido sozinho." | **Proibido.** Marque `bloqueado` com a pergunta. O principal a faz ao usuário no relatório. |
| "O usuário escolheu 2 e 5; os outros achados do Veredito estão aceitos." | **Proibido.** O aceite exige a decisão e o motivo do usuário. Um achado não escolhido continua aberto. |
| "O vaivém tem uma direção óbvia; delego a correção." | **Proibido.** As duas correções puxam o código em direções opostas. A direção é decisão do usuário. |

## 9. Prova de Execução (Critério de Saída)
- `[measured]` Seleção mostrada antes da delegação, com os achados enviados a outra skill à parte.
- `[measured]` Cada achado com status e a prova do seu tipo, com comando e saída. O `não reproduz` traz também a falha com a linha alterada.
- `[measured]` Busca do padrão e dos valores alterados citada para cada correção, no Lote e no estado integrado.
- `[measured]` Portão completo de `laravel-verification` aprovado no estado integrado antes de qualquer commit, com comandos, escopos e resultados citados.
- `[measured]` Vaivém perguntado ao usuário antes da delegação.
- `[measured]` Relatório com `Valores alterados`, achados novos, perguntas dos bloqueados, `Aceitos:` com o motivo de cada achado e a indicação de `/revisar`.
