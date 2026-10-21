---
name: implementar
description: Implementa uma Especificação ou ticket em Laravel e Livewire usando TDD na Costura (Pest), Larastan e Pint (.php e .blade.php), com commits atômicos. Use quando o usuário digitar /implementar.
disable-model-invocation: true
---

# Implementar Fatia Vertical com TDD (`/implementar`)

## 1. Objetivo
Executar os tickets planejados uma Fatia Vertical por vez, aplicando o ciclo Red-Green-Refactor na Costura da `Action` e na Fronteira `Livewire`/HTTP, validando com Pest, Larastan e Pint antes de cada commit.

## 2. Regras Inegociáveis
- **Carregue as disciplinas de modelo:** Aplique rigorosamente `laravel-deep-modules`, `laravel-tdd-seams`, `laravel-verification` e `ste100-clean-code`.
- **Siga o ciclo Red-Green-Refactor:** Escreva o teste Pest falhando antes de escrever o código de produção da fatia.
- **Proteja a janela de contexto ao delegar:** Se houver frentes desbloqueadas paralelizáveis e o ambiente suportar subagentes + `git worktree`, passe apenas **Ponteiros de Contexto** (caminho da Spec, número do ticket e arquivos-alvo). Nunca cole o histórico bruto do chat.
- **Faça commits como pontos de salvamento:** Cada fatia concluída e 100% verde gera um commit atômico (~100 linhas).

## 3. Processo (Por Fatia Vertical Desbloqueada)
1. **Seleção da Fatia:** Identifique o próximo ticket desbloqueado no plano.
2. **Passo RED (Teste Falhando na Costura e Fronteira):**
   - Crie ou atualize o teste no Pest exercitando a Costura (`Action::handle($dto)`) e/ou a superfície (`Livewire::test()` / rota HTTP).
   - Execute `./vendor/bin/pest --filter=<NomeDoTeste>` e confirme que falha pelo motivo esperado.
3. **Passo GREEN (Implementação Mínima Profunda):**
   - Crie/atualize o Enum, o DTO `final readonly`, a `Action` e a fronteira `Livewire` (com `#[Locked]` e `$this->authorize()`) ou `Controller` + `.blade.php`.
   - Execute `./vendor/bin/pest --filter=<NomeDoTeste>` até ficar verde.
4. **Passo REFACTOR & PORTÃO DE VERIFICAÇÃO:**
   - Remova código morto e comentários desnecessários (`ste100-clean-code`).
   - Execute a tríade completa de `laravel-verification`:
     1. `./vendor/bin/pest`
     2. `./vendor/bin/phpstan analyse`
     3. `./vendor/bin/pint --test` (cobrindo `.php` e `.blade.php`)
5. **Commit da Fatia:** Quando os 3 comandos estiverem verdes (`[measured]`), faça um commit atômico da fatia e avance para o próximo ticket desbloqueado.
6. **Fechamento:** Ao concluir todos os tickets, instrua o usuário a rodar `/revisar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou implementar os 4 tickets de uma vez e rodar o Pest apenas no final." | **Proibido.** Implemente, teste, valide no Larastan/Pint e faça commit de 1 fatia por vez. |
| "O teste da Action passou, não preciso testar o componente Livewire." | **Proibido.** Teste a lógica na Costura da `Action` e a integração/autorização em `Livewire::test()`. |
| "Vou commitar agora e corrigir os erros do Larastan e do Pint no último commit." | **Proibido.** Nenhum commit entra na branch com erro de tipo ou formatação pendente. |

## 5. Prova de Execução (Critério de Saída)
Para cada fatia entregue, apresente evidência medida:
- `[measured]` Saída verde de `./vendor/bin/pest`.
- `[measured]` Saída sem erros de `./vendor/bin/phpstan analyse`.
- `[measured]` Saída limpa de `./vendor/bin/pint --test` em arquivos `.php` e `.blade.php`.
