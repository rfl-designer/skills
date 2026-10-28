---
name: leitura-independente
description: Um Leitor novo, sem o histórico do chat, lê o rascunho de uma Spec ou de um plano de tickets antes da gravação. Ele devolve a Paráfrase e os achados; o autor resolve cada achado com o usuário. Use em /especificar e /planejar, antes de gravar o documento.
---

# Leitura Independente da Spec e dos Tickets (`leitura-independente`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
O implementador lê a Spec e o ticket sem o histórico do chat. Uma suposição que o documento não escreve vira uma decisão silenciosa dele. Antes da gravação, um Leitor novo lê o rascunho nas mesmas condições. Ele devolve a Paráfrase e os achados. O Autor resolve cada achado com o usuário.

## 2. Termos
- **Autor:** o agente principal que escreveu o rascunho. Ele tem o histórico do chat.
- **Leitor:** subagente novo, sem o histórico do chat. Ele só lê: o rascunho, o glossário, a configuração, os ADRs e o código.
- **Paráfrase:** o texto do Leitor, com as palavras dele, sobre o que o documento propõe e como o sistema atual funciona segundo o documento.
- **Decisão aberta:** escolha que o documento deixa ao implementador.
- **Modo Spec:** leitura do rascunho de `/especificar`.
- **Modo Tickets:** leitura do rascunho de `/planejar`, com a Spec aprovada.

## 3. Regras Inegociáveis
- **Use um Leitor novo a cada leitura:** Não use `fork` nem retome um Leitor anterior. Os dois herdam contexto.
- **Passe só ponteiros:** Envie o modo, o caminho do rascunho, a Spec aprovada (modo Tickets), o glossário, a pasta de ADRs e a configuração do projeto. Não envie o histórico do chat, sua opinião sobre o rascunho ou o motivo das escolhas. A leitura procura justamente o motivo que o documento não escreve.
- **Grave o rascunho fora do repositório:** Use um arquivo temporário, como `$TMPDIR/leitura-<slug>-<AAAA-MM-DD>.md`. Assim, a leitura vale para todo destino: Markdown, Issue do GitHub ou do GitLab.
- **O Leitor só lê:** Ele não edita arquivos, não executa comandos e não cria subagentes.
- **Não leia no mesmo contexto:** O Autor lê o que quis dizer, não o que escreveu. Sem subagentes, não faça a leitura você mesmo. Escreva `Leitura Independente: não executada (sem subagentes)` no fechamento. Ofereça a leitura numa sessão nova: uma sessão sem o histórico também lê sem contexto.
- **Mostre a Paráfrase sem alteração:** Só o usuário conhece a intenção. Uma Paráfrase errada é um achado, mesmo sem outro achado.
- **Grave o documento só depois da resposta do usuário.**
- **Faça no máximo 2 leituras por documento:** Cada Leitor novo acha coisas diferentes. Zero achados não é o alvo.

## 4. Processo do Leitor
Você não conhece este projeto. Você conhece Laravel, Livewire e PHP. Um termo geral dessas ferramentas não é achado.

1. **Leitura:** Leia o rascunho inteiro, o glossário, a configuração e os ADRs citados. No modo Tickets, leia também a Spec aprovada.
2. **Paráfrase:** Antes de procurar achados, escreva com suas palavras, em 2 a 5 frases por título:
   - Modo Spec: `O que a Spec propõe` e `Como o sistema atual funciona, segundo a Spec`.
   - Modo Tickets: `O que o plano entrega, em ordem`, e 1 frase por ticket.

   Use só o documento. Uma seção que você não consegue parafrasear é um `[BLOCKER]`.
3. **Código:** Busque com Grep e Glob cada nome do projeto que o documento cita: Costura, Model, Enum, Policy, componente, tabela e coluna. No modo Tickets, confira cada Ponteiro de Contexto: o arquivo a modificar existe; o arquivo a criar ainda não existe.
4. **Prontidão:** Responda por escrito:
   - Modo Spec: "Só com este documento, sei o que construir, o resultado de cada caso e quem pode fazer cada ação?"
   - Modo Tickets, por ticket: "Sei o que escrever, onde e como, sem tomar decisão de design?"

   Cada "não" é um achado.
5. **Achados:** Procure:
   - Partes sem ligação ou em contradição.
   - Decisão aberta. No modo Tickets: assinatura, formato de retorno, regra de erro, autorização, tabela ou coluna deixadas ao implementador.
   - Termo do projeto sem definição no documento e no glossário.
   - Pré-requisito ou efeito colateral não declarado: job, evento, notificação ou dado existente.
   - Divergência entre o documento e o código.
   - Modo Tickets: Ponteiro de Contexto errado, e requisito ou cenário de teste da Spec sem ticket.
6. **Severidade:**
   - `[BLOCKER]`: seção sem Paráfrase possível, contradição, ou decisão aberta que muda o comportamento observável, os dados ou a autorização.
   - `[IMPORTANTE]`: os outros achados da etapa 5.
   - Não reporte estilo, redação ou gosto. Esse ruído esconde os achados reais.
7. **Caso concreto:** Todo achado cita o trecho e escreve a pergunta que o implementador não consegue responder com o documento. Sem pergunta concreta, não há achado.
8. **Retorno:** Use o formato abaixo. Sem achados, escreva `Sem achados.` depois da Paráfrase.

Se você não consegue ler o rascunho ou um arquivo necessário, informe o limite e pare, sem veredito.

```markdown
Documento: $TMPDIR/leitura-reservar-estoque-2026-10-28.md (modo Spec)

## O que a Spec propõe
O cliente reserva um item do estoque ao entrar no checkout. A reserva some quando o pagamento falha.

## Como o sistema atual funciona, segundo a Spec
Hoje, o estoque só cai na confirmação do pagamento. Nada impede dois clientes de pagarem pelo último item.

## Achados
1. [BLOCKER] **A reserva tem dois prazos** (seção 1, "a reserva expira em 30 minutos"; seção 5, "a reserva dura até o pagamento")
   - **Pergunta sem resposta:** Um cliente que abre o checkout e paga 40 minutos depois ainda tem o item reservado?
   - **Por que importa:** O implementador escolhe uma das duas frases. O teste da seção 5 ou a regra da seção 1 fica falso.

Lido: o rascunho, GLOSSARY.md e docs/agents/projeto.md. Buscas: `ReservarItem`, `StatusReserva`, `PagamentoConfirmado`.
Não lido: docs/adr/ (pasta ausente).
```

## 5. Processo do Autor
1. **Rascunho:** Grave o rascunho no arquivo temporário da seção 3.
2. **Delegação:** Dispare um Leitor novo com o modo, o caminho do rascunho e os ponteiros da seção 3. No Claude Code, siga a seção 6.
3. **Conferência:** O retorno traz a Paráfrase, e cada achado traz o trecho e a pergunta. Um Leitor que falha ou devolve outro formato não leu. Dispare um Leitor novo uma vez. Na segunda falha, escreva `Leitura Independente: falhou` no fechamento e siga.
4. **Classificação:** Dê uma classe a cada achado:
   - `corrigir`: o achado vale. Corrija o rascunho.
   - `contestar`: o Leitor errou. Cite a prova que ele podia ler: trecho do rascunho, termo do glossário, ADR, ou arquivo e símbolo do código. "Foi intencional" não é prova.
   - `perguntar`: só o usuário responde. São comportamento, regra de negócio ou fato fora do repositório, como uma convenção da equipe. Depois da resposta, escreva o fato no rascunho, no glossário ou num ADR. O implementador também não lê a conversa.
   - `mover para tickets` (só modo Spec): o achado pede caminho de arquivo ou código. A Spec não muda. `/planejar` recebe o achado.

   Siga estas regras:
   - Não conteste uma lacuna de compreensão. Se o Leitor não entendeu, o implementador também não vai entender.
   - Não mude a severidade. Se um `[BLOCKER]` parece menor, conteste-o com a prova.
   - O contexto que o Leitor pede é o contexto que o implementador precisa. Não descarte um achado porque "só um agente sem contexto precisa disso".
   - Você escreveu o rascunho. A vontade de contestar não prova que o Leitor errou.
5. **Usuário:** Mostre numa mensagem, nesta ordem:
   1. A Paráfrase, sem alteração.
   2. Cada achado, com a classe e a correção proposta ou a prova.

   Depois, pergunte se a Paráfrase corresponde à intenção do usuário. Em seguida, faça as perguntas dos achados `perguntar`, uma por vez. Espere cada resposta.
6. **Correção:** Aplique ao rascunho as correções e as respostas. Quando o usuário decide manter um achado aberto, registre o achado e o motivo para o fechamento.
7. **Segunda leitura:** Faça a segunda leitura só quando a primeira teve `[BLOCKER]` ou Paráfrase errada. Use um Leitor novo, só com o rascunho corrigido. Compare os achados com os da primeira leitura:
   - Um achado igual a um achado contestado (mesmo trecho e mesmo problema) continua contestado.
   - Um achado no trecho de uma correção mostra que a correção falhou. Corrija de novo.

   Depois da segunda leitura, leve ao usuário cada `[BLOCKER]` ou `[IMPORTANTE]` ainda aberto. Pergunte uma vez: gravar com os achados abertos, ou voltar à etapa anterior (`/alinhar` para a Spec, `/especificar` para os tickets).
8. **Fechamento:** Depois da gravação no destino, apague o rascunho temporário. Escreva 1 linha na mensagem de fechamento, por exemplo:
   `Leitura Independente: 2 leituras; 4 achados: 2 corrigidos, 1 contestado, 1 aberto por decisão do usuário (motivo); Paráfrase confirmada.`
   Nos outros casos, escreva `não executada (sem subagentes)` ou `falhou`.

## 6. No Claude Code
Use o agente customizado `leitor`, com `model: inherit` e as ferramentas `Read, Grep, Glob`.

1. Copie o [template](assets/leitor.md) para `.claude/agents/leitor.md` na raiz do projeto consumidor. Se o arquivo já existe, preserve as customizações.
2. Instale `leitura-independente` e `ste100-clean-code` para o Claude Code. O campo `skills` do template pré-carrega as duas.
3. Delegue com `subagent_type: leitor`. Não use o tipo `fork`.
4. O template não usa `omitClaudeMd`. O implementador lê as instruções do projeto (`CLAUDE.md`), e o Leitor lê nas mesmas condições.
5. Sem o agente registrado, use o subagente geral com o mesmo contrato e o caminho desta skill. Avise o usuário: o subagente geral tem todas as ferramentas, e a regra "só lê" fica só na instrução. Criar o primeiro diretório de agentes durante a sessão pode exigir reiniciar o Claude Code.

Fonte: [subagentes do Claude Code](https://code.claude.com/docs/en/sub-agents).

## 7. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Eu escrevi o rascunho; releio eu mesmo." | **Proibido.** O Autor lê o que quis dizer, não o que escreveu. Use um Leitor novo. |
| "Passo o histórico ao Leitor para ele entender melhor." | **Proibido.** O implementador não recebe o histórico. O Leitor lê nas mesmas condições. |
| "Uso um `fork`; é mais rápido." | **Proibido.** O `fork` herda a conversa e lê com o contexto do Autor. |
| "A Paráfrase está quase certa; resumo para o usuário." | **Proibido.** Mostre a Paráfrase sem alteração. Só o usuário a compara com a intenção. |
| "O Leitor não entendeu; contesto." | **Proibido.** Uma lacuna de compreensão não se contesta. Falta contexto no documento. |
| "Foi intencional; contesto." | **Proibido.** Cite a prova que o Leitor podia ler, ou pergunte ao usuário. |
| "Só um agente sem contexto precisa desse detalhe." | **Proibido.** O implementador também lê sem contexto. Escreva o detalhe, ou mova-o para os tickets se ele é caminho ou código. |
| "Faço leituras até não ter achados." | **Proibido.** Faça no máximo 2 leituras. Depois, leve os achados abertos ao usuário. |
| "Sem subagente, faço a leitura aqui mesmo." | **Proibido.** Registre `não executada (sem subagentes)` e ofereça a leitura numa sessão nova. |

## 8. Prova de Execução (Critério de Saída)
- `[measured]` Leitor novo, só com ponteiros e sem histórico. Tipo de agente informado: `leitor` registrado ou subagente geral.
- `[measured]` Paráfrase mostrada ao usuário sem alteração, antes da gravação.
- `[measured]` Cada achado com classe. Contestação com prova que o Leitor podia ler. Resposta de cada pergunta escrita no documento, no glossário ou num ADR.
- `[measured]` No máximo 2 leituras.
- `[measured]` Linha `Leitura Independente:` na mensagem de fechamento.
