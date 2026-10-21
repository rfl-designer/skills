---
name: revisar
description: Executa Revisão Adversarial em contexto limpo (Standards + Spec + Segurança Livewire/Laravel) e gera o resumo de PR com Raio de Explosão. Use quando o usuário digitar /revisar.
disable-model-invocation: true
---

# Revisão Adversarial e Briefing de Entrega (`/revisar`)

## 1. Objetivo
Submeter o `git diff` da entrega a uma Revisão Adversarial em dois eixos isolados (Padrões Laravel/Livewire vs. Especificação) e gerar um briefing de Pull Request conciso com análise de Raio de Explosão.

## 2. Regras Inegociáveis
- **Use subagentes com contexto limpo:** Sempre que a ferramenta suportar subagentes, dispare 2 revisores paralelos isolados passando apenas Ponteiros de Contexto (`git diff`, caminho da Spec e `GLOSSARY.md`). O agente que escreveu o código tem viés de confirmação.
- **Passe o pente-fino anti-ruído:** Aplique `ste100-clean-code` para remover comentários óbvios, código morto e imports não utilizados.
- **Classifique os achados por severidade:** Separe bloqueadores reais (`[BLOCKER]`) de melhorias opcionais (`[NIT]`).

## 3. Processo
1. **Coleta do Diff e Verificação Base:**
   - Inspecione `git status` e `git diff` contra a branch base.
   - Execute `laravel-verification` (`pest`, `phpstan`, `pint --test`) para garantir que o código já compila e passa nos testes.
2. **Revisão Adversarial em 2 Eixos (Subagentes Paralelos):**
   - **Subagente 1 — Eixo Standards & Laravel/Livewire Security:**
     - Caça N+1 queries Eloquent (falta de `with()` ou `preventLazyLoading`).
     - Verifica se propriedades sensíveis/IDs em componentes `Livewire` possuem `#[Locked]`.
     - Verifica se toda ação mutável chama `$this->authorize()` / `Policy`.
     - Verifica se há lógica de negócio vazando para fora das `Actions` ou ausência de `declare(strict_types=1);`.
     - Verifica comentários desnecessários (`ste100-clean-code`).
   - **Subagente 2 — Eixo Spec & Comportamento:**
     - Compara o `git diff` linha a linha com a Especificação gerada em `/especificar`.
     - Aponta requisitos faltantes, escopo extra não solicitado (*scope creep*) ou casos de borda não cobertos nos testes Pest.
3. **Correção de Bloqueadores:** Se qualquer `[BLOCKER]` for encontrado, corrija-o e rode novamente a verificação antes de prosseguir.
4. **Geração do Briefing de PR (Máximo 40 linhas, padrão ASD-STE100):**
   - **Por que (Why):** 1 a 2 frases explicando o problema resolvido.
   - **O que mudou (What changed):** Bullets curtos focados nas Fronteiras (`Livewire`/HTTP) e Costuras (`Actions`/DTOs).
   - **Porta de Decisão e Raio de Explosão (Blast Radius):** Classifique a mudança como **Porta de 2 Vias** (reversível sem perda de dados) ou **Porta de 1 Via** (ex.: migration destrutiva, alteração de contrato externo) e liste exatamente quais rotas/componentes podem ser afetados.
   - **Prova de Execução (`[measured]`):** Resumo dos resultados do Pest, Larastan e Pint.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Eu mesmo acabei de escrever o código, posso apenas olhar rápido sem seguir os 2 eixos." | **Proibido.** A Revisão Adversarial exige checagem independente de Standards (Segurança/N+1/Livewire) e Spec. |
| "Não há impacto nenhum no Raio de Explosão." | **Proibido.** Toda alteração toca alguma rota, tabela ou componente. Nomeie os pontos afetados explicitamente. |
| "Vou escrever um PR de 200 linhas listando cada arquivo modificado." | **Proibido.** O Git já mostra os arquivos. O briefing de PR deve ter no máximo 40 linhas de alto sinal. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Relatório dos 2 eixos (Standards + Spec) concluído com zero `[BLOCKER]` pendente.
- `[measured]` Tríade final (`./vendor/bin/pest`, `./vendor/bin/phpstan analyse`, `./vendor/bin/pint --test`) executada e verde.
- `[measured]` Briefing de PR com seção de Raio de Explosão entregue ao usuário.
