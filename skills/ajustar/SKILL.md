---
name: ajustar
description: Corrige os achados de um relatório de /revisar com subagentes Ajustadores. Agrupa os achados em Lotes, prova cada correção pelo tipo do achado, segue cada valor alterado até os consumidores e verifica o estado integrado. Use quando o usuário digitar /ajustar.
argument-hint: "[números dos achados, ex.: 2 5]"
disable-model-invocation: true
---

# Corrigir os Achados da Revisão (`/ajustar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

**Perfil de stack:** Esta skill não assume linguagem nem framework. Se a configuração ou os manifests mostram Laravel, leia também [references/laravel.md](references/laravel.md): ele dá a configuração dos verificadores, os marcadores de exceção e o lugar de cada `Regra:`. Passe o caminho do perfil a cada Ajustador. Sem perfil para a stack do projeto, aplique cada regra com o mecanismo equivalente da stack.

## 1. Objetivo
Corrigir os achados escolhidos do relatório de `/revisar`. O agente principal agrupa os achados em Lotes e delega cada Lote a um Ajustador. O Ajustador prova cada correção. O principal integra os Lotes, procura regressões nos valores alterados e verifica o estado integrado. Depois, o usuário roda `/revisar` para a rodada seguinte.

## 2. Termos
- **Achado:** item numerado do relatório de `/revisar`, com caso concreto, `arquivo:linha`, as 4 partes (O que é, Problema, Correção, Se não corrigir) e a Prova: o arquivo de prova, o comando e a saída. O achado pode ter o campo `Regra:`.
- **Regra:** verificação determinística que impede a classe de erro do achado de voltar: trava do framework, teste de arquitetura, análise estática ou lint. O campo `Regra:` dá o mecanismo, a proibição e a mensagem com a correção.
- **Correção do humano:** pedido do usuário que corrige uma classe de erro do diff sem um achado do relatório, como "não use `DB::` em componente Livewire".
- **Configuração dos verificadores:** os arquivos que dizem o que os testes, a análise estática e o lint verificam: suítes, nível, baseline e regras. O perfil de stack dá os nomes.
- **Fluxo:** o caminho de um valor, da entrada até cada consumidor, como em `/revisar`.
- **Lote:** grupo de achados que um só Ajustador corrige.
- **Ajustador:** subagente que corrige um Lote.
- **Valor alterado:** o que a correção muda e outro código lê: chave, ID, coluna, status, flag, regra, assinatura ou formato de retorno. É a mesma lista de `/revisar`.

## 3. Regras Inegociáveis
- **Carregue as disciplinas de modelo:** Aplique `deep-modules`, `tdd-seams`, `verification` e `ste100-clean-code`.
- **Corrija os achados escolhidos:** O argumento ou a mensagem do usuário escolhe os achados ("corrija 2 e 5"). Sem escolha, use os achados do `Veredito:` do relatório: todos os `[BLOCKER]` e `[IMPORTANTE]`.
- **Registre os achados aceitos:** Quando o usuário decide não corrigir um achado, ele o aceita. Registre o achado em `Aceitos:`, com o motivo do usuário. Sem motivo, pergunte o motivo. Um achado que o usuário não escolheu não está aceito: ele continua aberto.
- **Leve o vaivém ao usuário:** Um achado com `(vaivém do achado N)` não entra num Lote antes da resposta do usuário. A Correção dele traz as duas direções e a pergunta.
- **Mande cada achado à skill certa:** `/ajustar` corrige achados com correção localizada. O requisito faltante que pede uma Fatia nova (tela, rota, Costura ou tabela nova) vai para `/implementar`. O defeito sem causa localizada vai para `/depurar`. Esses achados ficam fora dos Lotes.
- **Use o relatório como contrato:** A Correção do achado é o ponto de partida. O Ajustador pode aplicar uma correção menor que resolve o mesmo caso concreto. Uma correção que muda a Spec, muda um contrato externo ou exige escolha entre opções recebe o status `bloqueado`, com a pergunta para o usuário.
- **Prove cada correção pelo tipo do achado:**
  - **Com comportamento:** O caso concreto vira um teste. Parta do arquivo de prova do achado, na pasta de `Provas:` do relatório. O teste falha antes da correção pelo motivo do achado (RED) e passa depois (GREEN).
  - **Teste ausente:** Escreva o teste. Quebre a lógica de propósito, veja o teste falhar e desfaça a quebra. Aqui, o teste verde na primeira execução é o resultado esperado.
  - **Mapa desatualizado:** A prova é o conferidor de `/mapear` e a condução da entrada afetada, segundo `verification`.
  - **Sem teste viável** (condição de corrida, carga): Registre o motivo e use a prova mais próxima, como a contagem de consultas ou o índice único no schema. Marque a prova como `parcial`.
- **Mantenha os verificadores:** Um marcador de exceção novo não serve para obter verde. O marcador é o comentário ou a chamada que manda a análise estática, o teste de arquitetura ou o lint ignorar um trecho. Outro caminho que escapa do mesmo verificador também não serve. Se a correção só fica verde assim, marque o achado `bloqueado`, com o verificador, a saída vermelha e a pergunta ao usuário.
- **Escreva e prove a regra:** Para cada achado com `Regra:`, o Ajustador escreve a regra e a roda no repositório inteiro depois da correção.
  - **Entra no Lote** só com o repositório verde, sem alterar a configuração dos verificadores e sem marcador de exceção. A prova tem 3 partes: RED, a regra falha no código com o defeito, e a saída nomeia o alvo proibido, com o `arquivo:linha` do achado quando a ferramenta não o dá; GREEN, a regra passa depois da correção; e a suíte completa verde com a regra.
  - **Senão, vai para `Regras propostas:`.** Desfaça a regra no Lote e devolva o esboço, a mensagem e as ocorrências antigas, com `arquivo:linha`. Uma ocorrência antiga é um local fora dos locais do achado que a regra pega. Não a corrija nesta rodada: a regra e as ocorrências são decisão do usuário.
  - Sem o campo `Regra:`, o Ajustador não escreve regra.
- **Leve a correção do humano à regra:** O principal registra a correção do humano como achado `H1`, `H2` etc., com o caso concreto, os locais do diff que `rg` acha, a Correção do usuário e a prova do seu tipo. Depois, confere as 3 condições da etapa 5.9 de `/revisar`:
  1. O defeito é uma classe de erro que uma ferramenta determinística detecta sem executar o caso.
  2. A regra não dá falso positivo no repositório depois da correção: cada ponto que ela pega tem o mesmo defeito.
  3. A mensagem da regra diz a correção, não só a proibição.

  Com as 3, o principal escreve o campo `Regra:` no achado, e ele segue o caminho dos outros achados. Sem uma delas, o achado segue sem `Regra:`. Os locais fora do diff são ocorrências antigas.
- **Prove o `não reproduz`:** No achado com comportamento, o teste pode passar antes da correção. Antes de concluir, altere a linha do achado de propósito e veja o teste falhar; depois, desfaça a alteração. Com a falha, o teste executa o caso: registre `não reproduz` com o teste e as duas saídas, e mantenha a produção sem alteração. Sem a falha, o teste não executa o caso: reescreva-o para o caso concreto.
- **Corrija em todos os locais:** Corrija cada local que o achado lista. Depois, busque com `rg` o mesmo padrão no repositório inteiro. Um local com o mesmo defeito e a mesma correção entra no achado. Um local que pede outra correção vira achado novo. O padrão é o do caso concreto, como a mesma relação ou a mesma chave, e não a classe do erro inteira: o local que só a regra pega é ocorrência antiga.
- **Siga cada valor alterado:** Para cada valor que a correção altera, busque com `rg` todos os consumidores e confira cada um. Um consumidor quebrado pela correção é regressão do Lote. Nos arquivos do Lote, corrija-a. Fora deles, devolva o local ao principal, que atribui a regressão.
- **Fique no escopo do Lote:** Um defeito sem relação com os achados do Lote volta ao principal como achado novo, com caso concreto e `arquivo:linha`. O principal o reporta no fim, sem corrigi-lo nesta rodada.
- **Delegue com contexto limpo:** Passe ponteiros e o contrato da seção 4, sem o histórico do chat. Cada Ajustador carrega as disciplinas de modelo; não presuma que herdou as skills do principal.
- **Limite a concorrência:** Use até 2 Ajustadores ao mesmo tempo, só em Lotes independentes e worktrees separados. Cada worktree precisa do diff revisado. Com o diff sem commit, transfira-o de forma revisável para cada worktree, ou use um Ajustador por vez no checkout atual. Não crie commit para fabricar a base.
- **Faça commit só no fim:** O Ajustador não faz commit. Com autorização da sessão, o principal faz um commit por Lote depois do portão integrado, com os números dos achados na mensagem. Nenhum commit entra com o portão vermelho. Sem autorização, mantenha o diff no working tree.
- **Deixe o veredito para `/revisar`:** `/ajustar` prova as correções. A rodada seguinte de `/revisar` revisa o diff completo e confirma o resultado.

## 4. Preparar e delegar (agente principal)
1. **Relatório:** Use o relatório mais recente de `/revisar` para o mesmo alvo, da conversa ou do arquivo citado no handoff. Os números dos achados valem só nesse relatório. Sem relatório, ou com achados sem as 4 partes e a Prova, peça o relatório ao usuário ou ofereça uma nova rodada de `/revisar`. Os achados vêm do relatório, não de memória ou resumo.
2. **Seleção:** Aplique a regra de seleção. Mostre a lista com número, nível e título, e continue. Mostre à parte os achados que vão para `/implementar` ou `/depurar`.
   - Seleção vazia (`Veredito: pode entregar.` ou `Sem achados.`, sem escolha do usuário): informe e pare.
   - Número que o relatório não tem: informe e não o delegue.
   - Correção do humano: registre o achado `H` pela seção 3 e mostre-o na lista, com o campo `Regra:` ou o motivo da falta dele.
   - Outro pedido sem achado no relatório: ofereça `/depurar` ou `/revisar`.
   - Pedido ambíguo: pergunte e espere a resposta.
   - Achado com `(vaivém do achado N)`: faça a pergunta da Correção antes de delegar. Com a direção escolhida, ele entra num Lote. Com a decisão de manter o código, ele vira `aceito`.
3. **Estado:** Confira `git status` e a linha `Alvo:` do relatório. Com outra branch no checkout, pare e pergunte. Releia o `arquivo:linha` de cada achado; com código alterado depois do relatório, localize o trecho de novo. Sem o trecho, marque o achado `desatualizado` e não o delegue.
4. **Lotes:** Coloque no mesmo Lote os achados que tocam o mesmo valor, o mesmo Fluxo ou os mesmos arquivos. Assim, um só Ajustador corrige o valor em todos os consumidores. Coloque achados sem nada em comum em Lotes separados. Delegue primeiro os Lotes com `[BLOCKER]`. Um Lote que depende de outro espera a integração desse outro.
5. **Agente:** No Claude Code, siga a seção 7. Em outros ambientes, use o mecanismo e os modelos autorizados disponíveis; não traduza IDs da Anthropic para outro provedor. Sem subagentes, corrija um Lote por vez no agente principal e informe a limitação.
6. **Contrato:** Envie a cada Ajustador, com caminhos válidos no diretório dele:
   - Os achados do Lote, copiados do relatório com as 4 partes, todos os locais e o campo `Regra:`, quando houver.
   - As linhas de `Fluxos rastreados:` que passam por esses achados.
   - Spec, configuração do projeto, instruções locais, o perfil de stack e os caminhos das 4 disciplinas de modelo.
   - Base e diretório de execução, com o diff revisado presente. Arquivos sob sua responsabilidade e limites de escopo.
   - Comandos e recursos de verificação. Banco, portas e app local compartilhados exigem isolamento ou serialização. Um worktree sozinho não isola esses recursos.
   - O formato de retorno da seção 5.

Avise cada Ajustador que há outros agentes no repositório: não reverta mudanças alheias. O Ajustador não delega de novo e não faz commit.

## 5. Processo do Ajustador (por Lote)
1. **Base:** Confirme o diretório, a base, o diff revisado e os achados do Lote. Não selecione outros achados.
2. **Prova antes:** Escolha a prova de cada achado pela seção 3. No achado com comportamento, parta do arquivo de prova do achado e ponha o teste na Costura ou na Fronteira. Sem o arquivo, escreva o teste do caso concreto. Execute o teste focado, com o comando da configuração, e confirme a falha pelo motivo do achado. No achado com `Regra:`, escreva também a regra no lugar que o perfil de stack indica e execute-a no código com o defeito: confirme o RED e o alvo proibido na saída.
3. **Correção:** Aplique a menor correção que resolve o caso em todos os locais. Prefira a correção que apaga código.
4. **Prova depois:** Execute a prova de cada achado até ela passar. A regra do achado também passa (GREEN). Depois de 2 correções com a mesma premissa sem GREEN, aplique "Ataque a premissa" de `tdd-seams`. Se a premissa vem da Correção do achado, marque o achado `bloqueado`, com a premissa, a prova e a pergunta.
5. **Propagação:** Busque com `rg` o padrão corrigido e cada valor alterado. Confira cada consumidor. Trate a regressão e o defeito sem relação pela seção 3.
6. **Regra no repositório:** Execute cada regra do Lote no repositório inteiro: a suíte completa, ou a ferramenta da regra sem filtro de caminho. Pela seção 3, a regra fica no Lote ou vai para `Regras propostas:`.
7. **Portão:** Aplique o portão completo de `verification`, sem as regras desfeitas.
8. **Retorno:** Devolva neste formato, sem colar os arquivos. Os nomes e caminhos do exemplo são ilustrativos:

```markdown
Lote: A (achados 2, 5 e 6)
Achado 2: corrigido. RED: o teste focado `agrupa itens por chave` falhou com "esperado 3 itens, recebido 4". GREEN: passou. Locais: pedidos/agrupar_itens:31, pdf/termos:18, jobs/enviar_resumo:19 (mesmo defeito, achado na busca).
Achado 5: não reproduz. O teste focado `exige assinatura` passou antes da correção. Com pedidos/exigir_assinatura:12 alterada de propósito, o teste falhou; alteração desfeita. Produção sem alteração.
Achado 6: bloqueado. Pergunta: nos pedidos já assinados, o PDF mostra a chave antiga ou a nova? A Spec não responde.
Regra do achado 2: testes/arquitetura/pedidos. RED: no código com o defeito, a regra `os itens não usam a chave do produto: agrupe pela chave do item` falhou com "pedidos/agrupar_itens usa produto.chave" (pedidos/agrupar_itens:31, do achado). GREEN: passou depois da correção. Repositório: verde.
Regras propostas:
- Achado 5: lint que proíbe ler a assinatura fora de pedidos/exigir_assinatura. Motivo: a regra pega 2 ocorrências antigas. Mensagem: "Leia a assinatura por exigirAssinatura()". Ocorrências antigas: pdf/termos:40, jobs/lembrete:12. Esboço: a regra, com o caminho onde ela mora.
Valores alterados: `agruparItens()` agora devolve um mapa de chave para Item. Consumidores conferidos: pedidos/detalhe:44, jobs/gerar_pdf:27.
Regressão fora do Lote: exportacoes/pedidos:52 lê o retorno antigo de `agruparItens()`.
Achados novos: cupons/aplicar:30 aceita cupom vencido; caso: cupom vencido ontem dá desconto hoje.
Portão: formatação ok, análise estática ok, testes 412 aprovados (suíte completa), diretório ../wt-lote-a, diff sem commit.
Pendências: achado 6.
```

## 6. Integrar e verificar (agente principal)
1. **Conferência:** Cada achado do Lote tem status (`corrigido`, `não reproduz` ou `bloqueado`) e a prova do seu tipo, da seção 3. Com prova faltante, retome o mesmo Ajustador com a pendência e preserve o trabalho válido.
2. **Bloqueados:** Termine os outros Lotes. Faça as perguntas dos achados `bloqueado` no relatório, sem parar a rodada. A resposta "fica como está", com o motivo, torna o achado `aceito`.
3. **Integração:** Integre um Lote por vez, só com o delta do Lote. Um conflito que muda comportamento volta ao ciclo de prova do Lote afetado.
4. **Regressões:** Junte os `Valores alterados` de todos os Lotes. No estado integrado, busque de novo com `rg` os consumidores de cada valor e confira cada um. Dois Lotes podem alterar o mesmo Fluxo de formas incompatíveis. Atribua cada regressão ao Lote dono do arquivo, ou a um Lote novo.
5. **Portão:** Execute o portão completo de `verification` no estado integrado. A evidência de worktrees isolados não prova a combinação.
6. **Fechamento:** Com o portão aprovado e a autorização da sessão, faça um commit por Lote. A mensagem segue `ste100-clean-code` e cita os números dos achados. A evidência de um worktree é temporária. Grave na pasta de Evidências só os artefatos do estado integrado, segundo `verification`. Depois, limpe só os worktrees criados por este fluxo. Antes de remover um worktree, confira com `git -C <worktree> status` e o diff que todo o delta dele está integrado. Um worktree com mudança não integrada espera a decisão do usuário.
7. **Relatório:**
   - 1 linha por achado: número, título, status (`corrigido`, `não reproduz`, `bloqueado` ou `desatualizado`) e prova. O achado `H` da correção do humano também.
   - 1 linha por regra no Lote: `Regra do achado N: <arquivo>. RED: … GREEN: … Repositório: verde.` Só a regra no Lote tem essa linha; a regra fora do Lote aparece só em `Regras propostas:`.
   - `Regras propostas:` 1 item por regra fora do Lote, quando houver: `Achado N:`, o mecanismo, o `Motivo:` (ocorrências antigas, configuração dos verificadores ou marcador de exceção), a `Mensagem:`, as `Ocorrências antigas:` com `arquivo:linha` e o `Esboço:`. O usuário decide cada uma.
   - Os achados enviados a `/implementar` ou `/depurar`, quando houver.
   - `Valores alterados:` 1 linha por valor, com os consumidores conferidos. A rodada seguinte de `/revisar` coloca esses valores no Mapa de Fluxos.
   - `Achados novos:` caso concreto e `arquivo:linha`, quando houver. Ofereça `/depurar` para cada um. A rodada seguinte de `/revisar` também os confere.
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
| "Já estou no arquivo; refatoro também o trecho ao lado." | **Proibido.** Corrija só os achados escolhidos. O refactor é de `/implementar`. |
| "A correção exige mudar a Spec; decido sozinho." | **Proibido.** Marque `bloqueado` com a pergunta. O principal a faz ao usuário no relatório. |
| "O usuário escolheu 2 e 5; os outros achados do Veredito estão aceitos." | **Proibido.** O aceite exige a decisão e o motivo do usuário. Um achado não escolhido continua aberto. |
| "O verificador só fica verde com uma exceção; acrescento só para este arquivo." | **Proibido.** Um marcador de exceção novo não serve para obter verde, nem outro caminho que escapa do mesmo verificador. Marque o achado `bloqueado`, com o verificador, a saída e a pergunta. |
| "A regra está escrita e verde; o RED é dispensável." | **Proibido.** Sem o RED no código com o defeito, nada prova que a regra pega a classe do erro. |
| "A regra fica vermelha só em código antigo; corrijo as ocorrências também." | **Proibido.** As ocorrências antigas ficam fora do Lote. Desfaça a regra e registre-a em `Regras propostas:`, com as ocorrências. |
| "A regra só roda com uma linha a mais na configuração dos verificadores." | **Proibido.** Ponha a regra num lugar que já roda, pelo perfil de stack. Sem esse lugar, ela vai para `Regras propostas:`. |
| "O vaivém tem uma direção óbvia; delego a correção." | **Proibido.** As duas correções puxam o código em direções opostas. A direção é decisão do usuário. |

## 9. Prova de Execução (Critério de Saída)
- `[measured]` Seleção mostrada antes da delegação, com os achados enviados a outra skill à parte.
- `[measured]` Cada achado com status e a prova do seu tipo, com comando e saída. O `não reproduz` traz também a falha com a linha alterada.
- `[measured]` Busca do padrão e dos valores alterados citada para cada correção, no Lote e no estado integrado.
- `[measured]` Cada achado com `Regra:` tem a linha `Regra do achado N:`, com RED, GREEN e o repositório verde, ou um item em `Regras propostas:`, com o motivo, a mensagem, as ocorrências antigas e o esboço.
- `[measured]` Portão completo de `verification` aprovado no estado integrado antes de qualquer commit, com comandos, escopos e resultados citados.
- `[measured]` Vaivém perguntado ao usuário antes da delegação.
- `[measured]` Relatório com `Valores alterados`, achados novos, perguntas dos bloqueados, `Aceitos:` com o motivo de cada achado e a indicação de `/revisar`.
