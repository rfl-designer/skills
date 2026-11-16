# Skills

Pacote de skills para desenvolvimento com agentes de IA. As skills não assumem linguagem nem framework: os princípios ficam no texto de cada skill, e os comandos vêm da configuração do projeto. O pacote funciona em Claude Code, Codex e Antigravity.

Um [perfil de stack](#perfis-de-stack) opcional traduz os princípios para uma stack. Hoje há perfil para Laravel, Livewire e Pest.

O pacote adapta práticas de Addy Osmani (`agent-skills`), Matt Pocock (`skills`), Lauren Tan, poteto (`pstack`), e Robert C. Martin (`ub-mode`). A estrutura do fluxo se aproxima sobretudo de Matt. A [matriz de referências](docs/referencias.md) distingue práticas compartilhadas, correspondências e escolhas locais; não presume consenso em cada regra.

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
                                                          /depurar
```

No [herdr](https://github.com/herdrdev/herdr), `/alinhar-em-trio` substitui as 3 primeiras etapas:

```
/alinhar-em-trio → review humano (review-for-human) → /planejar → ...
```

`/prototipar` é opcional: use-o quando uma pergunta de design trava a Especificação. Antes de gravar, `/especificar` e `/planejar` passam o rascunho por um Leitor novo, sem o histórico do chat, com `leitura-independente`. `/ajustar` corrige os achados escolhidos de `/revisar`; depois, `/revisar` faz a rodada seguinte. O usuário pode aceitar um achado, com o motivo. Na rodada 3 sem veredito `pode entregar`, `/revisar` para o ciclo e pergunta como seguir. `/pausar` vale em qualquer etapa, ao trocar de sessão ou de agente. `/ensine-me` também vale em qualquer etapa, para entender um tema ou o código. `/diagramar-slice` mostra a slice de uma branch antes de `/revisar` ou do PR.

Execute `/mapear` depois do `/setup` para criar o Mapa de Features: um índice e um arquivo por Feature, com entradas do usuário, receitas de condução e prova. `/mapear` lê o código e não opera o app. Execute `/conduzir` para provar as receitas no app local. Antes da primeira condução, `/conduzir` confirma que o app e os testes usam o banco permitido. Depois, `verification` lê o Arquivo de Feature afetado e o atualiza no mesmo diff da mudança. Execute `/mapear` de novo para reconciliar mudanças acumuladas e `/mapear auditar` para comparar o mapa com o código.

Use `/implmentar-em-par` no lugar de `/implementar` para revisar a implementação por componente. O agente explica RED e pausa antes da produção. Depois, implementa e explica um componente por vez, aguardando sua revisão. O teste pode continuar vermelho entre etapas; a Fatia Vertical termina com GREEN e verificação completa.

## Skills de usuário

Use os comandos abaixo. `/setup` também pode ser solicitado em linguagem natural ao configurar o projeto.

| Skill | Função |
| --- | --- |
| `/setup` | Detecta tecnologias e comandos; configura pastas e destinos independentes de Specs e Tickets, persistidos por projeto. |
| `/alinhar` | Entrevista antes do código, uma pergunta por vez. Atualiza o `GLOSSARY.md` e registra ADRs. |
| `/alinhar-em-trio` | Só no herdr. O Julgador conduz 3 agentes de modelos diferentes pela árvore de decisão, com unanimidade em cada nó. Leva ao humano só as perguntas de negócio, os impasses e os diálogos de permissão. Condensa as decisões numa SPEC: um Leitor novo lê a SPEC, e o trio confere a fidelidade dela à ata. Publica a SPEC com a label `review-for-human`. |
| `/prototipar` | Protótipo descartável (lógica em HTML único ou variantes de tela por `?variant=`) para responder uma pergunta de design. Entrega a decisão, não o código. |
| `/especificar` | Escreve a Especificação com fronteiras, DTOs e Costuras, sem caminhos nem código. Um Leitor novo lê o rascunho e devolve a Paráfrase antes da gravação. Usa o destino configurado de Specs. |
| `/planejar` | Divide a Especificação em fatias verticais (expand–contract para refactor amplo). Um Leitor novo aponta cada decisão de design deixada ao implementador antes da gravação. Usa o destino configurado de Tickets. |
| `/implementar` | Implementa os tickets de `/planejar`; sem tickets, recomenda `/planejar`. Coordena subagentes por fatia com TDD na Costura e o portão de verificação; verifica a integração. |
| `/implmentar-em-par` | Conduz TDD na conversa principal; pausa após RED e cada componente para explicação em português e revisão humana. |
| `/depurar` | Reproduz o bug num teste, testa de 3 a 5 hipóteses e corrige na raiz. Depois de 2 correções com a mesma premissa sem GREEN, prova a premissa antes da 3ª. |
| `/revisar` | Revisão adversarial (Standards, Spec e segurança) completa numa rodada: segue cada valor alterado até todos os consumidores e consolida os achados antes do relatório. Revisores novos, cada um na sua worktree, provam cada achado por execução; o principal reexecuta cada prova na head e na base, e o defeito da base sai do veredito. Estilo e estrutura ficam com `/implementar`. Sem subagentes, o relatório declara `Independência: mesmo contexto`. Achados aceitos ficam fora do veredito, e o ciclo com `/ajustar` para na rodada 3. Só relatório, prova do fato de segurança e resumo de PR. |
| `/ajustar` | Corrige os achados escolhidos de `/revisar` com subagentes Ajustadores: Lotes por Fluxo, prova por tipo de achado (RED e GREEN quando há comportamento), busca dos consumidores de cada valor alterado e portão no estado integrado. Registra os achados aceitos e leva o vaivém ao usuário. Encaminha requisito de Fatia nova a `/implementar` e defeito sem causa a `/depurar`. |
| `/pausar` | Para numa fronteira segura e grava uma nota de handoff fora do repositório, sem commit, com as instruções de retomada. |
| `/ensine-me` | Ensina um tema ou explica código em Lições HTML curtas, em ASD-STE100, com fontes citadas e prática. Pergunta se a Lição vai para arquivo local ou artefato Claude. |
| `/mapear` | Cria, atualiza e audita o Mapa de Features contra o código, sem operar o app. Em aplicações com vários Domínios, delega cada Domínio a um subagente Mapeador. |
| `/conduzir` | Conduz as receitas do Mapa de Features no app local, em série. Antes, confirma que o app e os testes usam o banco permitido. Atualiza a linha `Estado:` e separa Deriva, lacuna de condução e defeito do produto. |
| `/diagramar-slice` | Gera um diagrama HTML descartável da slice de uma branch: arquivos do diff `base...alvo` por camada, com o diff de cada arquivo num modal. Sem git, gera um artefato Claude a partir do diff colado. No fim, pergunta se pode apagar o HTML. |

### Implementação com subagentes no Claude Code

O agente principal coordena `/implementar` e delega cada fatia completa a um implementador **Sonnet 5.5 / medium**. Até dois implementadores podem trabalhar em paralelo quando os tickets são independentes e usam worktrees separados. Tickets com arquivos compartilhados seguem em sequência. O principal confere os diffs e valida o estado integrado antes da entrega ou commit autorizado.

Depois de instalar a skill e as quatro disciplinas de modelo abaixo, copie [o template do implementador](skills/implementar/assets/implementador.md) para `.claude/agents/implementador.md` no projeto consumidor. Preserve customizações caso esse arquivo já exista. A instalação via `npx skills add` não registra o agente automaticamente. Consulte [a configuração no Claude Code](skills/implementar/references/claude-code.md) para conferir modelo, esforço e isolamento.

Em outros ambientes, a skill usa subagentes e modelos autorizados disponíveis. Sem subagentes, executa o ciclo diretamente e informa a limitação.

### Ajustadores no Claude Code

`/ajustar` delega cada Lote de achados a um Ajustador **Sonnet 5.5 / medium**, até 2 ao mesmo tempo em worktrees separados. Achados que tocam o mesmo valor ou os mesmos arquivos ficam no mesmo Lote. O principal integra os Lotes, busca regressões nos valores alterados e roda o portão completo.

Copie [o template do ajustador](skills/ajustar/assets/ajustador.md) para `.claude/agents/ajustador.md` no projeto consumidor e instale as quatro disciplinas de modelo. Sem o agente registrado, `/ajustar` usa o subagente geral, que herda o modelo do principal.

### Leitores no Claude Code

`/especificar` e `/planejar` delegam cada leitura a um Leitor novo, com `model: inherit` e só as ferramentas `Read, Grep, Glob`. O Leitor lê nas condições do implementador: sem o histórico do chat, com as instruções do projeto. Cada leitura usa um Leitor novo, nunca um `fork`.

Copie [o template do leitor](skills/leitura-independente/assets/leitor.md) para `.claude/agents/leitor.md` no projeto consumidor e instale `leitura-independente` e `ste100-clean-code`. Sem o agente registrado, as skills usam o subagente geral, que tem todas as ferramentas; a regra "só lê" fica só na instrução. Sem subagentes, o autor não lê o próprio rascunho no lugar do Leitor. Antes de gravar, ele pergunta: leitura numa sessão nova, ou gravação com `não executada`.

### Revisores no Claude Code

`/revisar` delega cada eixo a um revisor novo, com `model: inherit` e as ferramentas `Read, Grep, Glob, Bash`. Cada revisor trabalha numa worktree própria e executa só os testes, com a configuração de teste. O principal faz a guarda do ambiente de teste, cria as worktrees, executa o portão, reexecuta cada prova e prova o fato de segurança.

Copie [o template do revisor](skills/revisar/assets/revisor.md) para `.claude/agents/revisor.md` no projeto consumidor e instale `deep-modules`, `tdd-seams` e `ste100-clean-code`. Sem o agente registrado, `/revisar` usa o subagente geral, com as regras "só na sua worktree" e "só no ambiente de teste" só na instrução.

### Mapeadores no Claude Code

Em aplicações com 3 ou mais Domínios e mais de 12 Features, `/mapear` delega cada Domínio a um Mapeador **Sonnet 5.5 / medium**, até 4 ao mesmo tempo. Cada Mapeador grava só a pasta do seu Domínio e não conduz o app. O principal reconcilia o índice e roda o conferidor. Depois, `/conduzir` conduz as Features em série.

Copie [o template do mapeador](skills/mapear/assets/mapeador.md) para `.claude/agents/mapeador.md` no projeto consumidor e instale `ste100-clean-code`. Sem o agente registrado, `/mapear` usa o subagente geral, que herda o modelo do principal. Consulte [os Mapeadores](skills/mapear/references/mapeadores.md) para o contrato de delegação.

### Trio no herdr

`/alinhar-em-trio` roda só dentro de um pane do herdr (`HERDR_ENV=1`). Fora do herdr, a skill recusa a execução e recomenda `/alinhar`.

- **Julgador:** a sessão do humano, de preferência Claude Code com Fable 5.2 e esforço `medium`. Ele orquestra o trio, modera, grava a ata e escreve a SPEC. Ele não vota. Inicie o Julgador num pane do herdr com `claude --model claude-fable-5-2 --effort medium` e depois digite `/alinhar-em-trio <ideia>`.
- **Trio padrão:** cada agente roda no seu pane:
  - `opus`: Claude Code, Opus 5.5, esforço `medium`.
  - `sol`: Codex, GPT-6.1 Sol, esforço `medium`.
  - `argon`: Antigravity CLI, Gemini 4 Argon, esforço `low`.
- **Limites:** cada agente lê o repositório e pesquisa na web. Ele escreve só no seu diretório, fora do repositório. O Julgador nunca aprova um diálogo de permissão de um agente; ele mostra o diálogo ao humano.
- **Pausa:** o humano pode responder a uma escalada mais tarde. Nesse caso, o Julgador publica a pergunta numa Issue com a label `aguardando-humano` e grava uma nota de `/pausar`. Sem acesso ao tracker, a pergunta fica só na nota. Para continuar, use `/alinhar-em-trio retomar <link da Issue>` ou `retomar <caminho da nota>`.

Requisitos: herdr 0.9.5 ou mais novo e os 3 CLIs instalados e autenticados. Execute `/setup` dentro do herdr para gravar a seção `Trio de alinhamento`. O `/setup` confere as flags de cada CLI com o `--help`. A [referência de comandos](skills/alinhar-em-trio/references/herdr.md) mostra como cada flag foi verificada. A execução completa do trio ainda não está verificada.

## Skills de modelo

O agente carrega estas skills quando a tarefa exige.

| Skill | Função |
| --- | --- |
| `deep-modules` | Costuras existentes e módulos profundos; Costura e contrato de dados novos quando úteis, CRUD simples quando suficiente. Estado inválido impossível de escrever, validação só na entrada, estado do cliente sem confiança, operação repetível e um só escritor. |
| `tdd-seams` | TDD nas Costuras e nas Fronteiras, sem mocks da persistência, com testes de arquitetura quando a stack os tem. Apaga o teste que passa com a Costura vazia. Depois de 2 correções com a mesma premissa sem GREEN, prova a premissa antes da 3ª. |
| `verification` | Feedback rápido e portão completo antes da entrega: formatação, análise estática, testes, qualidade dos testes e navegador. Mede mutação e CRAP < 10 nos arquivos do diff. É a única fonte da ordem do portão. Cada evidência tem destino e validade; o artefato tem nome estável e a condução nova o substitui. |
| `leitura-independente` | Um Leitor novo lê o rascunho da Spec ou dos tickets antes da gravação: Paráfrase, Prontidão e resolução de cada achado com o usuário. |
| `ste100-clean-code` | Escrita técnica ASD-STE100 em português, sem comentários narrativos. O corpo do commit diz por que mudou e como você provou. |

## Configuração por projeto

`/setup` detecta a stack existente, pergunta só pelas escolhas faltantes e grava `docs/agents/projeto.md` (ou o arquivo já acordado). Um ponteiro nas instruções do projeto permite reutilizar a configuração em outras sessões e agentes.

O registro inclui versões e fontes da detecção, executor, comandos, URL local e pastas de domínio, protocolos e evidências. Para as evidências, ele registra também a política de versionamento: fora do Git (padrão), Git com substituição ou Git LFS. Specs e tickets têm destinos separados: Markdown local, GitHub, GitLab ou outro fluxo disponível. Por exemplo, Specs em `docs/specs/` e Tickets em Issues do GitHub.

As skills usam as escolhas salvas sem perguntar novamente. Sem configuração, continuam com seus defaults e oferecem `/setup`. Uma instrução explícita da sessão prevalece. Reexecutar o setup preserva conteúdo manual e atualiza apenas escolhas alteradas; configurar um tracker não publica issues nem instala tecnologias.

## Perfis de stack

O texto de cada skill usa só termos neutros: Costura, Fronteira, contrato de dados, teste focado e portão. Um perfil é um arquivo em `references/` que traduz esses termos para uma stack. O agente lê o perfil só quando a linha `Perfis de stack` da configuração, ou os manifests do projeto, mostram essa stack.

| Skill | Perfil Laravel | Conteúdo |
| --- | --- | --- |
| `deep-modules` | [laravel.md](skills/deep-modules/references/laravel.md) | `strict_types`, Action e DTO, `#[Locked]`, PHPStan, idempotência e travas. |
| `tdd-seams` | [laravel.md](skills/tdd-seams/references/laravel.md) | Pest, `Livewire::test()`, Factories, fakes e Arch Tests. |
| `verification` | [laravel.md](skills/verification/references/laravel.md) | Pint com Blade, PHPStan, Pest, mutação, Clover e Pest Agent. |
| `/revisar` | [laravel.md](skills/revisar/references/laravel.md) | Guarda do ambiente de teste, worktrees com `vendor/`, suspeitas e provas. |
| `/conduzir` | [laravel.md](skills/conduzir/references/laravel.md) | Comandos da guarda do banco. |
| `/mapear` | [inventario-laravel.md](skills/mapear/references/inventario-laravel.md) | Comando de cada fonte do inventário. |
| `/setup` | [laravel.md](skills/setup/references/laravel.md) | Pontos de detecção da stack. |

Numa stack sem perfil, `/setup` grava os comandos na tabela `Execução e verificação`, e cada skill aplica as regras com o mecanismo equivalente da stack. Para acrescentar um perfil, crie o arquivo `references/<stack>.md` em cada skill da tabela e cite-o no parágrafo `Perfil de stack` da skill.

## Requisitos do projeto

- Um executor de testes, com um comando de teste focado e um de suíte completa.
- Recomendado: formatador e analisador estático. Sem eles, `verification` registra a etapa como `não verificado`.
- Opcional, para a qualidade dos testes: medição de cobertura, ferramenta de mutação e um relatório Clover com complexidade por método. Sem eles, `verification` registra mutação e CRAP como `não verificado`.
- Recomendado: uma ferramenta de navegador, como o Playwright, para a verificação da interface.
- Python 3 para os scripts do pacote: o conferidor do mapa, o cálculo de CRAP e o diagrama de slice.

Os requisitos de um projeto Laravel estão no [perfil de `verification`](skills/verification/references/laravel.md).

## Migração da versão com Laravel no nome

Esta versão muda nomes e formatos. Num projeto que usa a versão anterior:

1. Reinstale as skills. `laravel-deep-modules`, `laravel-tdd-seams` e `laravel-verification` agora são `deep-modules`, `tdd-seams` e `verification`. Remova as 3 pastas antigas.
2. Copie de novo os templates de agente para `.claude/agents/`, ou troque os 3 nomes no campo `skills` de cada arquivo.
3. Em `docs/agents/projeto.md`, troque os 3 nomes e acrescente a linha `- Perfis de stack: laravel.` na seção `Execução e verificação`. `/setup` também faz essa mudança.
4. Os scripts agora são Python 3: `scripts/crap.py` e `scripts/conferir-mapa.py`. Troque `php .../crap.php` e `php .../conferir-mapa.php` nas receitas e no README do Mapa de Features.
5. A Âncora de componente agora usa o prefixo `componente:`. O conferidor ainda aceita `livewire:`. Para migrar um mapa, troque o prefixo nos Arquivos de Feature e gere o inventário de novo.

## Verificação e manutenção

Durante a edição, execute testes focados e verificadores do escopo afetado. Antes de commit, PR ou entrega de código, aplique o portão completo de `verification`. Ao pausar, registre o estado das provas sem repetir a suíte por rotina. Mudanças só de documentação usam os verificadores do pacote.

Valide o pacote com Python 3.10+ e Node 18+. Sem Node, o teste do núcleo do diagrama de `/diagramar-slice` fica pulado:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
python3 skills/mapear/scripts/conferir-mapa.py skills/mapear/references/exemplo
```

Os [cenários de avaliação](evals/cenarios.md) verificam decisões do agente. Validação estrutural não comprova eficácia; registre execução e comparação com a versão anterior antes de alegar melhoria.
