# Skills

Pacote de skills para desenvolvimento com agentes de IA em PHP, Laravel e Livewire. O pacote funciona em Claude Code, Codex e Antigravity.

O pacote une as práticas em que 2 ou mais destes autores concordam: Addy Osmani (`agent-skills`), Matt Pocock (`skills`) e Lauren Poteto (`pstack`).

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

As skills de usuário formam um pipeline. Cada etapa produz a entrada da próxima.

```
/alinhar → /prototipar → /especificar → /planejar → /implementar → /revisar
                                                            ↑
                                                          /bug
```

`/prototipar` é opcional: use-o quando uma pergunta de design trava a Especificação. `/pausar` vale em qualquer etapa, ao trocar de sessão ou de agente.

## Skills de usuário

O usuário chama estas skills pelo comando.

| Skill | Função |
| --- | --- |
| `/alinhar` | Entrevista antes do código, uma pergunta por vez. Atualiza o `GLOSSARY.md` e registra ADRs. |
| `/prototipar` | Protótipo descartável (lógica em HTML único ou variantes de tela por `?variant=`) para responder uma pergunta de design. Entrega a decisão, não o código. |
| `/especificar` | Escreve a Especificação com fronteiras, DTOs e Costuras, sem caminhos nem código. Pergunta onde salvar. |
| `/planejar` | Divide a Especificação em fatias verticais (expand–contract para refactor amplo). Pergunta onde salvar os tickets. |
| `/implementar` | Implementa um ticket com TDD na Costura (Pest), Larastan e Pint. |
| `/bug` | Reproduz o bug no Pest, testa de 3 a 5 hipóteses e corrige na raiz. |
| `/revisar` | Revisão adversarial (Standards, Spec e segurança) só com relatório, prova do fato de segurança e resumo de PR. |
| `/pausar` | Para numa fronteira segura e grava uma nota de handoff fora do repositório, sem commit, com as instruções de retomada. |

## Skills de modelo

O agente carrega estas skills quando a tarefa exige.

| Skill | Função |
| --- | --- |
| `laravel-deep-modules` | Módulos profundos: Actions, DTOs `readonly`, Livewire na fronteira. |
| `laravel-tdd-seams` | TDD com Pest nas Costuras, `Livewire::test()` e Arch Tests. |
| `laravel-verification` | Portão de prova de execução: Pest, Larastan e Pint (`.php` e `.blade.php`), mais navegador quando o diff toca a tela. |
| `ste100-clean-code` | Escrita técnica ASD-STE100 em português, sem comentários narrativos. |

## Requisitos do projeto

- Pest
- Larastan / PHPStan
- Laravel Pint
- Recomendado: `pestphp/pest-plugin-browser` (Pest 4) e Playwright (`npm install playwright@latest` e `npx playwright install`) para a verificação no navegador
