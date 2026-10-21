---
name: bug
description: Diagnostica e corrige bugs em PHP, Laravel e Livewire por método científico (reproduzir no Pest, localizar por busca binária, corrigir na causa raiz e validar). Use quando o usuário digitar /bug.
disable-model-invocation: true
---

# Diagnóstico Científico e Correção de Bugs (`/bug`)

## 1. Objetivo
Localizar a causa raiz de um defeito em Laravel/Livewire através de hipóteses verificáveis e provar a correção com um teste de regressão no Pest que falha antes do fix e passa depois.

## 2. Regras Inegociáveis
- **Pare a linha (Regra Stop-the-Line):** Nunca aplique um "chute" ou correção cosmética sem antes reproduzir o defeito de forma confiável.
- **Reproduza antes de corrigir:** Escreva um teste no Pest (na `Action` ou com `Livewire::test()`) que reproduza exatamente o bug e falhe (`RED`).
- **Corrija a causa raiz, não o sintoma:** Se um dado inválido chegou à `Action`, corrija a validação na Fronteira (`Livewire\Form` / `FormRequest`) e a tipagem no DTO, em vez de espalhar `if ($x !== null)` defensivos pelo código.
- **Separe a reprodução da correção:** Verifique que o teste de regressão falha sem a correção e passa com ela.

## 3. Processo (Loop de 5 Etapas)
1. **Reproduzir (Loop Vermelho):**
   - Colete o stack trace, log (`storage/logs/laravel.log`) ou comportamento incorreto relatado.
   - Crie um teste mínimo no Pest que reproduza a falha. Execute `./vendor/bin/pest --filter=<Teste>` e meça a falha (`[measured]`).
2. **Localizar e Minimizar (Busca Binária):**
   - Trace o fluxo da Fronteira (`Livewire` / `Controller`) até a Costura (`Action` / Model / Banco).
   - Formule até 2 hipóteses falsificáveis e use logs temporários, `dump()` em teste ou leitura de queries (`DB::enableQueryLog()`) para confirmar qual linha exata corrompe o estado.
3. **Corrigir na Causa Raiz:**
   - Aplique a menor alteração estrutural que elimina a causa raiz respeitando `laravel-deep-modules`.
   - Remova qualquer instrumentação temporária (`dd`, `dump`, `Log::debug`).
4. **Proteger (Guard & Verification):**
   - Execute o teste de regressão e toda a suíte: `./vendor/bin/pest`, `./vendor/bin/phpstan analyse` e `./vendor/bin/pint --test`.
5. **Relatório Curto de Causa Raiz:**
   - Explique em 3 bullets: (1) Qual era a causa raiz, (2) Qual teste Pest agora impede a regressão, (3) Qual foi o resultado medido da verificação.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Já sei qual é o erro olhando o código, vou alterar direto sem criar o teste antes." | **Proibido.** Sem ver o teste falhar antes da alteração, você não provou que o teste realmente captura o bug. |
| "O primeiro fix não funcionou, vou adicionar mais um try/catch por cima." | **Proibido.** Releia o erro, reverta a tentativa falha e formule uma hipótese baseada em evidência medida. |
| "Vou colocar `@` ou `optional()` para silenciar o erro de propriedade nula." | **Proibido.** Silenciar exceção oculta corrupção de estado. Corrija a origem do dado nulo. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Teste de regressão no Pest visto falhando (`RED`) antes do fix.
- `[measured]` Mesmo teste visto passando (`GREEN`) após o fix.
- `[measured]` `./vendor/bin/pest`, `./vendor/bin/phpstan analyse` e `./vendor/bin/pint --test` 100% verdes.
