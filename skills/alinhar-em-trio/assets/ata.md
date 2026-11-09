# Ata: <ideia em uma frase>

## Sessão
- Data: <AAAA-MM-DD>
- Repositório: <raiz>; branch <branch>; commit <hash curto>
- Configuração: <caminho, ou "trio padrão">
- Julgador esperado: <CLI, modelo e esforço da configuração>
- Trio:
  | Nome | `--kind` | Modelo | Esforço | Pane | Falhas |
  | --- | --- | --- | --- | --- | --- |
  | opus | claude | claude-opus-5-5 | medium | <pane_id> | 0 |
  | sol | codex | gpt-6.1-sol | medium | <pane_id> | 0 |
  | argon | agy | gemini-4-argon | medium | <pane_id> | 0 |
- Diretório da sessão: <caminho absoluto>
- Tab do herdr: <tab_id>
- Issue de escalada: nenhuma | <URL>
- Estado: em debate | aguardando humano | SPEC em avaliação | publicada
- Próxima rodada: <número>

## Árvore
- [ ] 01 <título>. Pai: nenhum. Origem: Julgador | <agente>, rodada 0.
- [x] 02 <título>. Pai: 01. Decidido na rodada <n>.

Ramos recusados:
- <ramo>. Proposto por <agente>. Motivo: <por que a SPEC não precisa dele>.

## Nós

### 01: <título>
- Pergunta: <texto>
- Rodadas: <números das rodadas globais>
- Posições finais:
  - opus: <resumo>
  - sol: <resumo>
  - argon: <resumo>
- Mudanças de posição: <agente, rodada, argumento e de quem veio; ou nenhuma>
- Concordâncias sem argumento recusadas: <agente e rodada; ou nenhuma>
- Decisão: <formulação do Julgador>
- Origem: unanimidade | decidido pelo humano (pergunta de negócio | impasse)
- Evidências: <`arquivo:linha`, URLs, protótipos e o resultado observado>
- Concordância: opus CONCORDO; sol CONCORDO; argon CONCORDO

## Perguntas ao humano
| Nó | Motivo | Pergunta | Resposta | Canal |
| --- | --- | --- | --- | --- |
| <NN> | negócio, impasse, falha, diálogo ou OK | <texto> | <texto, ou pendente> | pane, ou Issue <URL> |

## Falhas e diálogos
- <rodada>, <agente>: <timeout, stalled, ausente, arquivo vazio ou diálogo>. Ação: <reinício, escalada ou instrução do humano>.

## SPEC
- Rascunho: <caminho>; versão atual v<n>
- Leitura Independente: <linha no formato de `leitura-independente`>
- Achados do Leitor: <achado, tipo (redação, decisão ou negócio) e resolução>
- Rodadas de OK:
  - v1: opus OK; sol RECUSA (fidelidade, nó 03); argon OK
- Glossário: <termos>
- ADRs: <títulos que passam nos 3 critérios, ou nenhum>

## Publicação
- SPEC: <URL da Issue, ou caminho no PR>
- PR draft: <URL, ou "sem arquivos no repositório">
- Comentário com o resumo da ata: <URL>
- Encerramento: tab fechada; `prototipos/` removidas
