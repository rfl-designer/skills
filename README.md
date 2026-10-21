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
/alinhar → /especificar → /planejar → /implementar → /revisar
                                            ↑
                                          /bug
```

## Skills de usuário

O usuário chama estas skills pelo comando.

| Skill | Função |
| --- | --- |
| `/alinhar` | Entrevista antes do código, uma pergunta por vez. Atualiza o `GLOSSARY.md`. |
| `/especificar` | Escreve a Especificação com fronteiras, DTOs e Costuras. Pergunta onde salvar. |
| `/planejar` | Divide a Especificação em fatias verticais. Pergunta onde salvar os tickets. |
| `/implementar` | Implementa um ticket com TDD na Costura (Pest), Larastan e Pint. |
| `/bug` | Reproduz o bug no Pest, localiza a causa e corrige na raiz. |
| `/revisar` | Revisão adversarial (Standards, Spec e segurança) e resumo de PR. |

## Skills de modelo

O agente carrega estas skills quando a tarefa exige.

| Skill | Função |
| --- | --- |
| `laravel-deep-modules` | Módulos profundos: Actions, DTOs `readonly`, Livewire na fronteira. |
| `laravel-tdd-seams` | TDD com Pest nas Costuras, `Livewire::test()` e Arch Tests. |
| `laravel-verification` | Portão de prova de execução: Pest, Larastan e Pint (`.php` e `.blade.php`). |
| `ste100-clean-code` | Escrita técnica ASD-STE100 em português, sem comentários narrativos. |

## Requisitos do projeto

- Pest
- Larastan / PHPStan
- Laravel Pint
