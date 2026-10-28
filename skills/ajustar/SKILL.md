---
name: ajustar
description: Corrige os achados de um relatório de /revisar com subagentes Ajustadores. Agrupa os achados em Lotes, prova cada correção com teste RED e GREEN, segue cada valor alterado até os consumidores e verifica o estado integrado. Use quando o usuário digitar /ajustar.
argument-hint: "[números dos achados, ex.: 2 5]"
disable-model-invocation: true
---

# Corrigir os Achados da Revisão (`/ajustar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Corrigir os achados escolhidos do relatório de `/revisar`. O agente principal agrupa os achados em Lotes e delega cada Lote a um Ajustador. O Ajustador prova cada correção com um teste que falha antes e passa depois. O principal integra os Lotes, procura regressões nos valores alterados e verifica o estado integrado. Depois, o usuário roda `/revisar` para a rodada seguinte.

## 2. Termos
- **Achado:** item numerado do relatório de `/revisar`, com caso concreto, `arquivo:linha` e as 4 partes (O que é, Problema, Correção, Se não corrigir).
- **Fluxo:** o caminho de um valor, da entrada até cada consumidor, como em `/revisar`.
- **Lote:** grupo de achados que um só Ajustador corrige.
- **Ajustador:** subagente que corrige um Lote.
- **Valor alterado:** o que a correção muda e outro código lê: assinatura, retorno, coluna, chave, status ou formato.

## 3. Regras Inegociáveis
- **Carregue as disciplinas de modelo:** Aplique `laravel-deep-modules`, `laravel-tdd-seams`, `laravel-verification` e `ste100-clean-code`.
- **Corrija os achados escolhidos:** O argumento ou a mensagem do usuário escolhe os achados ("corrija 2 e 5"). Sem escolha, use os achados do `Veredito:` do relatório: todos os `[BLOCKER]` e `[IMPORTANTE]`. Um `[NIT]` entra só quando o usuário o escolhe.
- **Use o relatório como contrato:** A Correção do achado é o ponto de partida. O Ajustador pode aplicar uma correção menor que resolve o mesmo caso concreto. Uma correção que muda a Spec, muda um contrato externo ou exige escolha entre opções volta ao principal, e o principal pergunta ao usuário.
- **Prove cada correção com RED e GREEN:** O caso concreto do achado vira um teste Pest. O teste falha antes da correção pelo motivo do achado e passa depois.
  - **Teste ausente:** Escreva o teste e prove que ele detecta a quebra. Quebre a lógica de propósito, veja o teste falhar e desfaça a quebra.
  - **Achado sem mudança de comportamento** (estrutura, duplicação, código morto, import, comentário, Enxuto): os testes do trecho e o portão de `laravel-verification` são a prova. Sem teste no trecho, escreva um teste de caracterização antes da mudança: ele fixa o comportamento atual e fica verde antes e depois.
  - **Sem teste viável** (condição de corrida, carga): registre o motivo e use a prova mais próxima, como a contagem de queries ou o índice único no schema. Marque a prova como `parcial`.
  - **Teste verde antes da correção:** O achado não se reproduz. Registre `não reproduz` com o teste e a saída, e não altere a produção.
- **Corrija em todos os locais:** Corrija cada local que o achado lista. Depois, busque com `rg` o mesmo padrão e o mesmo valor no repositório inteiro.
- **Siga cada valor alterado:** Para cada valor que a correção altera, busque com `rg` todos os consumidores e confira cada um. Um consumidor quebrado pela correção é regressão do Lote e entra na correção.
- **Fique no escopo do Lote:** Um defeito que já existia antes desta rodada volta ao principal como achado novo, com caso concreto e `arquivo:linha`. O usuário decide se ele entra.
- **Delegue com contexto limpo:** Passe ponteiros e o contrato da seção 4, sem o histórico do chat. Cada Ajustador carrega as disciplinas de modelo; não presuma que herdou as skills do principal.
- **Limite a concorrência:** Use até 2 Ajustadores ao mesmo tempo, só em Lotes independentes e worktrees separados. Sem isolamento, use um Ajustador por vez no checkout atual.
- **Faça commit só com autorização da sessão:** Um commit por Lote verde, com os números dos achados na mensagem. Sem autorização, mantenha o diff no working tree.
- **Deixe o veredito para `/revisar`:** `/ajustar` prova as correções. A rodada seguinte de `/revisar` revisa o diff completo e confirma o resultado.

## 4. Preparar e delegar (agente principal)
1. **Relatório:** Use o relatório de `/revisar` da conversa ou do handoff. Sem relatório, peça ao usuário o texto ou o caminho. Os achados vêm do relatório, não da memória.
2. **Seleção:** Aplique a regra de seleção. Mostre a lista com número, nível e título, e continue. Espere a resposta só quando o pedido é ambíguo.
3. **Estado:** Confira `git status` e a referência do diff do relatório. Releia o `arquivo:linha` de cada achado. Com código alterado depois do relatório, localize o trecho de novo. Sem o trecho, marque o achado `desatualizado` e não o delegue.
4. **Lotes:** Coloque no mesmo Lote os achados que tocam o mesmo valor, o mesmo Fluxo ou os mesmos arquivos. Assim, um só Ajustador corrige o valor em todos os consumidores. Coloque achados sem nada em comum em Lotes separados. Delegue primeiro os Lotes com `[BLOCKER]`. Um Lote que depende de outro espera a integração desse outro.
5. **Agente:** No Claude Code, siga a seção 7. Em outros ambientes, use o mecanismo e os modelos autorizados disponíveis; não traduza IDs da Anthropic para outro provedor. Sem subagentes, corrija um Lote por vez no agente principal e informe a limitação.
6. **Contrato:** Envie a cada Ajustador, com caminhos válidos no diretório dele:
   - Os achados do Lote, copiados do relatório com as 4 partes e todos os locais.
   - As linhas de `Fluxos rastreados:` que passam por esses achados.
   - Spec, configuração do projeto, instruções locais e os caminhos das 4 disciplinas de modelo.
   - Base, diretório de execução, arquivos sob sua responsabilidade e limites de escopo.
   - Comandos e recursos de verificação. Banco, portas e app local compartilhados exigem isolamento ou serialização. Um worktree sozinho não isola esses recursos.
   - Autorização de commits e o formato de retorno da seção 5.

Avise cada Ajustador que há outros agentes no repositório: não reverta mudanças alheias. O Ajustador não delega de novo.

## 5. Processo do Ajustador (por Lote)
1. Confirme o diretório, a base e os achados do Lote. Não selecione outros achados.
2. **RED:** Para cada achado com comportamento, escreva o teste do caso concreto na Costura ou na Fronteira. Execute `./vendor/bin/pest --filter=<Teste>` e confirme a falha pelo motivo do achado.
3. **Correção:** Aplique a menor correção que resolve o caso em todos os locais. Prefira a correção que apaga código.
4. **GREEN:** Execute o teste de cada achado até ficar verde.
5. **Propagação:** Busque com `rg` o padrão corrigido e cada valor alterado. Confira cada consumidor. Corrija a regressão do Lote; devolva o defeito anterior como achado novo.
6. **Portão:** Aplique o portão completo de `laravel-verification`: Pint com Blade habilitado → PHPStan → Pest, mais navegador quando necessário.
7. **Retorno:** Devolva neste formato, sem colar os arquivos:

```markdown
Lote: A (achados 2 e 5)
Achado 2: corrigido. RED: `pest --filter=AgrupaItensPorChave` falhou com "esperado 3 itens, recebido 4". GREEN: passou. Locais: app/Actions/AgruparItens.php:31, resources/views/pdf/termos.blade.php:18.
Achado 5: não reproduz. `pest --filter=ExigeAssinatura` passou antes da correção. Produção sem alteração.
Valores alterados: `AgruparItens::handle()` agora devolve `Collection<string, Item>`. Consumidores conferidos: app/Livewire/Pedido/Detalhe.php:44, app/Jobs/GerarPdf.php:27.
Achados novos: `app/Jobs/EnviarResumo.php:19` soma itens repetidos desde antes desta rodada; caso: pedido com 2 itens iguais envia total em dobro.
Portão: Pint ok, PHPStan ok, Pest 412 passed (suíte completa), diretório ../wt-lote-a, diff sem commit.
Pendências: nenhuma.
```

## 6. Integrar e verificar (agente principal)
1. **Conferência:** Cada achado do Lote tem status (`corrigido`, `não reproduz` ou `bloqueado`) e prova. Um achado com comportamento sem RED não está corrigido. Retome o mesmo Ajustador com a pendência e preserve o trabalho válido.
2. **Integração:** Integre um Lote por vez. Um conflito que muda comportamento volta ao ciclo RED e GREEN do Lote afetado.
3. **Regressões:** Junte os `Valores alterados` de todos os Lotes. No estado integrado, busque de novo com `rg` os consumidores de cada valor e confira cada um. Dois Lotes podem alterar o mesmo Fluxo de formas incompatíveis. Uma regressão volta ao Lote que a causou.
4. **Portão:** Execute o portão completo de `laravel-verification` no estado integrado. A evidência de worktrees isolados não prova a combinação.
5. **Fechamento:** Com o portão aprovado, faça commit se autorizado. Limpe só os worktrees criados por este fluxo, depois de preservar a integração e as evidências.
6. **Relatório:**
   - 1 linha por achado: número, título, status (`corrigido`, `não reproduz`, `bloqueado` ou `desatualizado`) e prova.
   - `Valores alterados:` 1 linha por valor, com os consumidores conferidos. A rodada seguinte de `/revisar` coloca esses valores no Mapa de Fluxos.
   - `Achados novos:` caso concreto e `arquivo:linha`, quando houver.
   - `Portão:` comandos, escopo e resultado no estado integrado.
   - Última linha: `Próximo passo: rode /revisar para a rodada seguinte.`

## 7. No Claude Code
Use o agente customizado `ajustador`, com `model: claude-sonnet-5-5` e `effort: medium`. O principal mantém o próprio modelo.

1. Copie o [template](assets/ajustador.md) para `.claude/agents/ajustador.md` na raiz do projeto consumidor. Se o arquivo já existe, preserve as customizações.
2. Instale as 4 disciplinas de modelo para o Claude Code. O campo `skills` do template pré-carrega essas disciplinas.
3. Delegue com `subagent_type: ajustador`, sem override de modelo. Com 2 Lotes independentes, envie os 2 Ajustadores na mesma mensagem para rodarem em paralelo.
4. Confira o modelo e o esforço efetivos em `/tasks`. `CLAUDE_CODE_EFFORT_LEVEL` e políticas de modelo podem substituir o template. Se o resultado diverge, informe a causa; não declare Sonnet 5.5 medium sem confirmação.
5. O isolamento nativo pode partir da branch padrão, não do HEAD da sessão. Confira o commit-base de cada worktree antes da correção.
6. Sem o agente registrado, use o subagente geral com o mesmo contrato. Informe que ele herda o modelo do principal. Criar o primeiro diretório de agentes durante a sessão pode exigir reiniciar o Claude Code.

Fonte: [subagentes do Claude Code](https://code.claude.com/docs/en/sub-agents).

## 8. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "O achado é óbvio; corrijo sem teste RED." | **Proibido.** Sem RED, nada prova que o teste captura o achado. |
| "O relatório indica o local; corrijo só ali." | **Proibido.** Busque o padrão e o valor no repositório inteiro. Um consumidor sem correção mantém o defeito. |
| "O teste passou antes da correção; ajusto o teste até falhar." | **Proibido.** O achado não se reproduz. Registre `não reproduz` com a saída. |
| "Achei outro defeito antigo no caminho; corrijo também." | **Proibido.** Devolva como achado novo. Só a regressão causada pela correção entra no Lote. |
| "Cada Lote passou nos testes; a integração está verde." | **Proibido.** Busque os consumidores dos valores alterados e rode o portão no estado integrado. |
| "As correções têm prova; a revisão está aprovada." | **Proibido.** A rodada seguinte de `/revisar` dá o veredito. |
| "Já estou no arquivo; corrijo os `[NIT]` também." | **Proibido.** Um `[NIT]` entra só com a escolha do usuário. |
| "A correção exige mudar a Spec; decido sozinho." | **Proibido.** A decisão de Spec é do usuário. Volte ao principal e pergunte. |

## 9. Prova de Execução (Critério de Saída)
- `[measured]` Seleção de achados mostrada antes da delegação.
- `[measured]` Cada achado com status e prova: RED e GREEN com comando e saída, prova de detecção para teste ausente, testes do trecho e portão para achado sem mudança de comportamento, prova `parcial` com o motivo, ou `não reproduz` com a saída.
- `[measured]` Busca do padrão e dos valores alterados citada para cada correção, no Lote e no estado integrado.
- `[measured]` Portão completo de `laravel-verification` aprovado no estado integrado, com comandos, escopos e resultados citados.
- `[measured]` Relatório com `Valores alterados`, achados novos e a indicação de `/revisar`.
