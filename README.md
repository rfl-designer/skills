# Skills

Pacote de skills para desenvolvimento com agentes de IA em PHP, Laravel e Livewire. O pacote funciona em Claude Code, Codex e Antigravity.

O pacote adapta práticas de Addy Osmani (`agent-skills`), Matt Pocock (`skills`) e Lauren Tan, poteto (`pstack`) para Laravel/Livewire. A estrutura do fluxo se aproxima sobretudo de Matt. A [matriz de referências](docs/referencias.md) distingue práticas compartilhadas, correspondências e escolhas locais; não presume consenso em cada regra.

## Instalação

Instale todas as skills no projeto atual:

```bash
npx skills add rfl-designer/skills
```

Instale para todos os projetos (escopo global):

```bash
npx skills add rfl-designer/skills -g
```

Instale para um agente específico:

```bash
npx skills add rfl-designer/skills -a claude-code
npx skills add rfl-designer/skills -a codex
npx skills add rfl-designer/skills -a antigravity
```

Instale uma skill só:

```bash
npx skills add rfl-designer/skills --skill revisar
```

Veja as skills disponíveis sem instalar:

```bash
npx skills add rfl-designer/skills --list
```

## Fluxo

Execute `/setup` uma vez no projeto consumidor para combinar tecnologias, pastas e destinos. Reexecute quando essas escolhas mudarem. Depois, cada etapa do fluxo produz a entrada da próxima.

```
/alinhar → /prototipar → /especificar → /planejar → /implementar → /revisar ⇄ /ajustar
                                                            ↑
                                                          /bug
```

`/prototipar` é opcional: use-o quando uma pergunta de design trava a Especificação. `/ajustar` corrige os achados escolhidos de `/revisar`; depois, `/revisar` faz a rodada seguinte. `/pausar` vale em qualquer etapa, ao trocar de sessão ou de agente. `/ensine-me` também vale em qualquer etapa, para entender um tema ou o código. `/diagramar-slice` mostra a slice de uma branch antes de `/revisar` ou do PR.

Execute `/mapear` depois do `/setup` para criar o Mapa de Features: um índice e um arquivo por Feature, com entradas do usuário, condução e prova. Depois, `laravel-verification` lê o Arquivo de Feature afetado e o atualiza no mesmo diff da mudança. Execute `/mapear` de novo para reconciliar mudanças acumuladas e `/mapear auditar` para comparar o mapa com o app real.

Use `/implmentar-em-par` no lugar de `/implementar` para revisar a implementação por componente. O agente explica RED e pausa antes da produção. Depois, implementa e explica um componente por vez, aguardando sua revisão. O teste pode continuar vermelho entre etapas; a Fatia Vertical termina com GREEN e verificação completa.

## Skills de usuário

Use os comandos abaixo. `/setup` também pode ser solicitado em linguagem natural ao configurar o projeto.

| Skill | Função |
| --- | --- |
| `/setup` | Detecta tecnologias e comandos; configura pastas e destinos independentes de Specs e Tickets, persistidos por projeto. |
| `/alinhar` | Entrevista antes do código, uma pergunta por vez. Atualiza o `GLOSSARY.md` e registra ADRs. |
| `/prototipar` | Protótipo descartável (lógica em HTML único ou variantes de tela por `?variant=`) para responder uma pergunta de design. Entrega a decisão, não o código. |
| `/especificar` | Escreve a Especificação com fronteiras, DTOs e Costuras, sem caminhos nem código. Usa o destino configurado de Specs. |
| `/planejar` | Divide a Especificação em fatias verticais (expand–contract para refactor amplo). Usa o destino configurado de Tickets. |
| `/implementar` | Coordena subagentes por fatia com TDD na Costura (Pest), Larastan e Pint; verifica a integração. |
| `/implmentar-em-par` | Conduz TDD na conversa principal; pausa após RED e cada componente para explicação em português e revisão humana. |
| `/bug` | Reproduz o bug no Pest, testa de 3 a 5 hipóteses e corrige na raiz. |
| `/revisar` | Revisão adversarial (Standards, Spec e segurança) completa numa rodada: segue cada valor alterado até todos os consumidores e consolida os achados antes do relatório. Só relatório, prova do fato de segurança e resumo de PR. |
| `/ajustar` | Corrige os achados escolhidos de `/revisar` com subagentes Ajustadores: Lotes por Fluxo, teste RED e GREEN por achado, busca dos consumidores de cada valor alterado e portão no estado integrado. |
| `/pausar` | Para numa fronteira segura e grava uma nota de handoff fora do repositório, sem commit, com as instruções de retomada. |
| `/ensine-me` | Ensina um tema ou explica código em Lições HTML curtas, em ASD-STE100, com fontes citadas e prática. Pergunta se a Lição vai para arquivo local ou artefato Claude. |
| `/mapear` | Cria, atualiza e audita o Mapa de Features da aplicação. Em aplicações com vários Domínios, delega cada Domínio a um subagente Mapeador e conduz o app ao vivo. |
| `/diagramar-slice` | Gera um diagrama HTML descartável da slice de uma branch: arquivos do diff `base...alvo` por camada, com o diff de cada arquivo num modal. Sem git, gera um artefato Claude a partir do diff colado. No fim, pergunta se pode apagar o HTML. |

### Implementação com subagentes no Claude Code

O agente principal coordena `/implementar` e delega cada fatia completa a um implementador **Sonnet 5.5 / medium**. Até dois implementadores podem trabalhar em paralelo quando os tickets são independentes e usam worktrees separados. Tickets com arquivos compartilhados seguem em sequência. O principal confere os diffs e valida o estado integrado antes da entrega ou commit autorizado.

Depois de instalar a skill e as quatro disciplinas de modelo abaixo, copie [o template do implementador](skills/implementar/assets/implementador.md) para `.claude/agents/implementador.md` no projeto consumidor. Preserve customizações caso esse arquivo já exista. A instalação via `npx skills add` não registra o agente automaticamente. Consulte [a configuração no Claude Code](skills/implementar/references/claude-code.md) para conferir modelo, esforço e isolamento.

Em outros ambientes, a skill usa subagentes e modelos autorizados disponíveis. Sem subagentes, executa o ciclo diretamente e informa a limitação.

### Ajustadores no Claude Code

`/ajustar` delega cada Lote de achados a um Ajustador **Sonnet 5.5 / medium**, até 2 ao mesmo tempo em worktrees separados. Achados que tocam o mesmo valor ou os mesmos arquivos ficam no mesmo Lote. O principal integra os Lotes, busca regressões nos valores alterados e roda o portão completo.

Copie [o template do ajustador](skills/ajustar/assets/ajustador.md) para `.claude/agents/ajustador.md` no projeto consumidor e instale as quatro disciplinas de modelo. Sem o agente registrado, `/ajustar` usa o subagente geral, que herda o modelo do principal.

### Mapeadores no Claude Code

Em aplicações com 3 ou mais Domínios e mais de 12 Features, `/mapear` delega cada Domínio a um Mapeador **Sonnet 5.5 / medium**, até 4 ao mesmo tempo. Cada Mapeador grava só a pasta do seu Domínio e não conduz o app. O principal reconcilia o índice, roda o conferidor e conduz as Features em série.

Copie [o template do mapeador](skills/mapear/assets/mapeador.md) para `.claude/agents/mapeador.md` no projeto consumidor e instale `ste100-clean-code`. Sem o agente registrado, `/mapear` usa o subagente geral, que herda o modelo do principal. Consulte [os Mapeadores](skills/mapear/references/mapeadores.md) para o contrato de delegação.

## Skills de modelo

O agente carrega estas skills quando a tarefa exige.

| Skill | Função |
| --- | --- |
| `laravel-deep-modules` | Costuras existentes e módulos profundos; Action/DTO quando úteis, CRUD simples quando suficiente. |
| `laravel-tdd-seams` | TDD com Pest nas Costuras, `Livewire::test()` e Arch Tests. |
| `laravel-verification` | Feedback rápido, portão completo antes da entrega, Blade habilitado no Pint e probes Pest Agent quando disponíveis. |
| `ste100-clean-code` | Escrita técnica ASD-STE100 em português, sem comentários narrativos. |

## Configuração por projeto

`/setup` detecta a stack existente, pergunta só pelas escolhas faltantes e grava `docs/agents/projeto.md` (ou o arquivo já acordado). Um ponteiro nas instruções do projeto permite reutilizar a configuração em outras sessões e agentes.

O registro inclui versões e fontes da detecção, executor, comandos, URL local e pastas de domínio, protocolos e evidências. Specs e tickets têm destinos separados: Markdown local, GitHub, GitLab ou outro fluxo disponível. Por exemplo, Specs em `docs/specs/` e Tickets em Issues do GitHub.

As skills usam as escolhas salvas sem perguntar novamente. Sem configuração, continuam com seus defaults e oferecem `/setup`. Uma instrução explícita da sessão prevalece. Reexecutar o setup preserva conteúdo manual e atualiza apenas escolhas alteradas; configurar um tracker não publica issues nem instala tecnologias.

## Requisitos do projeto

- Pest
- Larastan / PHPStan
- Laravel Pint com `"Pint/laravel_blade": true` em `rules` do `pint.json` para cobrir Blade (ou `--blade` numa execução compatível). Preserve as demais regras.
- Opcional: `pestphp/pest-plugin-agent`, detectado por `pest --help`. Pest 5 exige PHP 8.4+; não é atualizado automaticamente por estas skills.
- Recomendado: `pestphp/pest-plugin-browser` (versão compatível com o Pest instalado) e Playwright (`npm install playwright@latest` e `npx playwright install`) para a verificação no navegador

## Verificação e manutenção

Durante a edição, execute testes focados e verificadores do escopo afetado. Antes de commit, PR ou entrega de código, aplique o portão completo de `laravel-verification`. Ao pausar, registre o estado das provas sem repetir a suíte por rotina. Mudanças só de documentação usam os verificadores do pacote.

Valide o pacote com Python 3.10+, PHP 8.1+ e Node 18+. Sem PHP, o teste do conferidor do mapa fica pulado. Sem Node, o teste do núcleo do diagrama de `/diagramar-slice` fica pulado:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
php skills/mapear/scripts/conferir-mapa.php skills/mapear/references/exemplo
```

Os [cenários de avaliação](evals/cenarios.md) verificam decisões do agente. Validação estrutural não comprova eficácia; registre execução e comparação com a versão anterior antes de alegar melhoria.
