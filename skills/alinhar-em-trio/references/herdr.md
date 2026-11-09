# Comandos do herdr e dos CLIs do trio

Esta referência dá os comandos que `/alinhar-em-trio` usa. O binário instalado é a autoridade. Se a configuração do projeto tem flags diferentes, a configuração vale.

## Estado da verificação

Verificado em 2026-11-09:

| Ferramenta | Versão | Como foi verificado |
| --- | --- | --- |
| herdr | 0.9.5 | Referência da CLI na documentação desta versão (`docs/versions/0.9.5` em github.com/herdrdev/herdr). Não executado. |
| Claude Code | 2.1.319 | `claude --help` executado. |
| Codex | código-fonte da branch principal em 2026-11-09 | Definições das flags (`codex-rs/utils/cli`, `codex-rs/tui/src/cli.rs`) e `models-manager/models.json`. Não executado. |
| Antigravity CLI | CHANGELOG até 1.5.3 | Flags citadas no CHANGELOG. Não executado. |

A execução completa do trio está `não verificada`. Antes da primeira sessão, `/setup` executa o `--help` de cada CLI na máquina do usuário e grava as flags reais na configuração.

## Guarda e descoberta

```bash
test "${HERDR_ENV:-}" = 1
```

- O herdr define `HERDR_ENV=1`, `HERDR_WORKSPACE_ID`, `HERDR_TAB_ID` e `HERDR_PANE_ID` em cada pane.
- Não execute `herdr` sem subcomando. Esse comando abre a TUI.
- Para ver a sintaxe de um grupo, execute o grupo sem subcomando: `herdr agent`, `herdr pane`, `herdr tab`.
- Os comandos de controle devolvem JSON. Leia os IDs da resposta. Não deduza um ID.

## Layout

Crie a tab no workspace atual. O pane raiz recebe o primeiro agente:

```bash
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "<raiz do repositório>" --label "alinhar-<slug>" --no-focus
```

- A resposta tem `.result.tab.tab_id` e `.result.root_pane.pane_id`.

Crie os outros 2 panes a partir do pane raiz:

```bash
herdr pane split <pane raiz> --direction right --cwd "<cwd do segundo agente>" --no-focus
herdr pane split <segundo pane> --direction down --cwd "<cwd do terceiro agente>" --no-focus
```

- A resposta tem `.result.pane.pane_id`.
- No fim, feche só a tab que você criou: `herdr tab close <tab_id>`.

## Trio padrão

`<sessao>` é o diretório da sessão. `<dir-do-agente>` é `<sessao>/<nome>`. Os dois caminhos são absolutos.

| Nome | `--kind` | Diretório do pane | Argumentos depois de `--` |
| --- | --- | --- | --- |
| `opus` | `claude` | raiz do repositório | `--model claude-opus-5-5 --effort medium --permission-mode dontAsk --add-dir <dir-do-agente> --allowedTools "Read Grep Glob WebSearch WebFetch Write(/<dir-do-agente>/**) Edit(/<dir-do-agente>/**)"` |
| `sol` | `codex` | raiz do repositório | `-m gpt-6.1-sol -c model_reasoning_effort=medium --sandbox workspace-write -C <dir-do-agente> --ask-for-approval on-request --search` |
| `argon` | `agy` | `<dir-do-agente>` | `--model gemini-4-argon --effort medium --mode accept-edits --sandbox` |

Inicie cada agente no seu pane:

```bash
herdr agent start <nome> --kind <kind> --pane <pane_id> --timeout 120000 -- <argumentos>
```

- O nome segue `[a-z][a-z0-9_-]{0,31}` e é único entre os agentes vivos.
- O `--timeout` de `agent start` aceita de 3001 a 300000 ms.
- O pane precisa estar no prompt do shell, sem outro processo em primeiro plano.
- `agent_not_ready` significa um diálogo na inicialização. Leia o pane e leve o diálogo ao humano.

### Limites de escrita por CLI

- **Claude Code:**
  - O modo `dontAsk` nega, sem perguntar, toda ferramenta que `--allowedTools` não permite.
  - As regras permitem leitura em qualquer caminho e escrita só no diretório do agente.
  - O caminho absoluto já começa com `/`. Por isso, a regra fica com `//`, que é a forma de caminho absoluto nas regras do Claude Code.
  - A forma da regra está `não verificada`: ela vem da documentação, não de uma execução.
  - Sem `Bash`, o agente não executa protótipos. Para permitir, acrescente na configuração uma regra limitada ao diretório do agente.
- **Codex:**
  - `-C` muda a raiz de trabalho do agente para o seu diretório.
  - O sandbox `workspace-write` permite escrita só nessa raiz e nos diretórios de `--add-dir`.
  - `--search` liga a pesquisa na web.
  - Com `on-request`, o próprio modelo decide quando pedir uma aprovação. O pedido aparece como `blocked`.
  - O slug `gpt-6.1-sol` aceita `low`, `medium`, `high`, `xhigh`, `max` e `ultra`. O padrão do slug é `low`. Por isso, passe o esforço sempre.
- **Antigravity CLI:**
  - O workspace do agente é o diretório do pane. Por isso, o pane do `argon` não usa a raiz do repositório.
  - O modo `accept-edits` aceita edições no workspace. `--sandbox` liga o sandbox do terminal.
  - A leitura do repositório fica fora do workspace e pode pedir uma aprovação. Leve esse diálogo ao humano.
  - O slug `gemini-4-argon` vem da issue 1228 de google-antigravity/antigravity-cli. Confira com o subcomando `agy models`.

## Enviar uma rodada e esperar

Envie a rodada aos 3 agentes em paralelo. Guarde a saída e o código de saída de cada envio:

```bash
for a in opus sol argon; do
  herdr agent prompt "$a" "Leia <sessao>/rodadas/007.md. Grave sua resposta em <sessao>/$a/007.md. Responda só com o caminho." \
    --wait --timeout 900000 >"<sessao>/log/$a-007.json" 2>&1 &
done
wait
```

- Use `agent prompt --wait`. Um `agent wait` sozinho, logo depois de um `agent prompt` sem `--wait`, pode retornar antes do início do turno.
- Sem `--until`, `--wait` termina no primeiro estado `idle`, `done` ou `blocked`.
- `--timeout 900000` são 15 minutos. Use o timeout da configuração quando ele existe.
- Depois do envio, confira o arquivo: `test -s "<sessao>/$a/007.md"`.

Erros e o que fazer:

| Erro ou estado | Significado | Ação |
| --- | --- | --- |
| `agent_blocked` | O agente já estava num diálogo. Nada foi enviado. | Leia o diálogo e leve-o ao humano. |
| `blocked` no fim da espera | O agente abriu um diálogo durante o turno. | Leia o diálogo e leve-o ao humano. |
| `agent_prompt_stalled` | Nenhuma atividade em 5 s. | Leia o agente antes de reenviar. |
| `timeout` | O prazo terminou. | Leia o agente antes de reenviar. |
| arquivo ausente ou vazio | O agente respondeu fora do arquivo ou não terminou. | Leia o agente. Conte como falha. |

Um timeout ou um `agent_prompt_stalled` não prova que o prompt não chegou. Leia antes de reenviar:

```bash
herdr agent get <nome>
herdr agent read <nome> --source recent-unwrapped --lines 120
```

## Diálogos de aprovação

- Leia o diálogo com `herdr agent read`.
- Mostre o diálogo ao humano sem alteração.
- Envie teclas só com a instrução do humano: `herdr agent send-keys <nome> <tecla>`.

## Reiniciar um agente

1. Leia `herdr agent get <nome>` e `herdr agent read <nome>`.
2. Feche o pane do agente: `herdr pane close <pane_id>`. Feche só um pane desta sessão.
3. Crie um pane novo na tab da sessão com `herdr pane split`, com o mesmo diretório.
4. Inicie o agente com o mesmo nome e os mesmos argumentos.
5. Envie `debatedor.md`, `contexto.md`, a ata e a rodada atual.

## Retomada

```bash
herdr tab get <tab_id>
herdr agent list
```

- Um agente da configuração que não aparece em `agent list` não existe mais. Reinicie esse agente.
- Se a tab não existe mais, crie a tab de novo, com o layout acima.

## Diretório da sessão

```
<sessao>/
  ata.md
  contexto.md
  debatedor.md
  rodadas/001.md            (o Julgador grava)
  log/<agente>-001.json     (saída de cada envio)
  spec/spec-v1.md           (rascunho da SPEC)
  spec/glossario.md         (termos para o glossário do projeto)
  spec/adr-NNNN-slug.md     (rascunhos de ADR)
  opus/001.md               (só o agente opus grava)
  opus/prototipos/
  sol/...
  argon/...
```

A regra "não leia as respostas dos outros agentes antes da revelação" fica só na instrução: os agentes usam o mesmo filesystem.
