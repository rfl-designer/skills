---
name: revisar
description: Executa Revisão Adversarial em contexto limpo (Standards + Spec + Segurança Livewire/Laravel) e gera o resumo de PR com Raio de Explosão. Use quando o usuário digitar /revisar.
disable-model-invocation: true
---

# Revisão Adversarial e Briefing de Entrega (`/revisar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Submeter o `git diff` da entrega a uma Revisão Adversarial em dois eixos isolados (Padrões Laravel/Livewire vs. Especificação) e gerar um briefing de Pull Request conciso com análise de Raio de Explosão.

## 2. Regras Inegociáveis
- **Use subagentes com contexto limpo:** Sempre que a ferramenta suportar subagentes, dispare 2 revisores paralelos isolados passando apenas Ponteiros de Contexto (`git diff`, caminho da Spec, glossário e configuração do projeto). O agente que escreveu o código tem viés de confirmação.
- **Reporte, não corrija:** `/revisar` não edita código. O usuário decide quais achados corrigir. A correção acontece depois, em `/implementar` ou `/bug`.
- **Passe o pente-fino anti-ruído:** Aponte comentários óbvios, código morto e imports não utilizados segundo `ste100-clean-code`.
- **Mantenha os eixos separados:** Apresente Standards e Spec em seções próprias. Não junte nem reordene achados entre eixos. Um eixo aprovado não compensa o outro reprovado.
- **Classifique os achados por severidade dentro de cada eixo:** Separe bloqueadores reais (`[BLOCKER]`) de melhorias opcionais (`[NIT]`).

## 3. Processo
1. **Coleta do Diff e Verificação Base:**
   - Inspecione `git status` e `git diff` contra a branch base.
   - Aplique o portão completo de `laravel-verification` ou reutilize evidência ainda válida para o mesmo estado. Não repita a suíte apenas por entrar na revisão.
2. **Revisão Adversarial em 2 Eixos (Subagentes Paralelos):**
   - **Subagente 1 — Eixo Standards & Laravel/Livewire Security:**
     - Caça N+1 queries Eloquent (falta de `with()` ou `preventLazyLoading`).
     - Verifica se propriedades sensíveis/IDs em componentes `Livewire` possuem `#[Locked]`.
     - Verifica se toda ação mutável chama `$this->authorize()` / `Policy`.
     - Verifica regras e coordenação sem encapsulamento, abstrações sem benefício e ausência de `declare(strict_types=1);`. Aceita CRUD simples e Costuras existentes conforme `laravel-deep-modules`.
     - Verifica comentários desnecessários (`ste100-clean-code`).
   - **Subagente 2 — Eixo Spec & Comportamento:**
     - Compara o `git diff` linha a linha com a Especificação gerada em `/especificar`.
     - Aponta requisitos faltantes, escopo extra não solicitado (*scope creep*) ou casos de borda não cobertos nos testes Pest.
3. **Relatório por Eixo:** Apresente os achados sob `## Standards` e `## Spec`, cada um com seus `[BLOCKER]` e `[NIT]`. Termine com 1 linha: total por eixo e o pior achado de cada eixo. Se houver `[BLOCKER]`, pare aqui e pergunte ao usuário como seguir.
4. **Prova do Fato de Segurança:** Identifique o único fato que torna a mudança segura (ex.: "a migration só adiciona coluna nullable"). Prove esse fato com um teste Pest ou um script que executa o código real. Se não conseguir provar, escreva `não provado`.
5. **Geração do Briefing de PR (Máximo 40 linhas, padrão ASD-STE100):**
   - **Por que (Why):** 1 a 2 frases explicando o problema resolvido.
   - **O que mudou (What changed):** Bullets curtos focados nas Fronteiras (`Livewire`/HTTP) e Costuras (`Actions`/DTOs).
   - **Porta de Decisão e Raio de Explosão (Blast Radius):** Classifique a mudança como **Porta de 2 Vias** (reversível sem perda de dados) ou **Porta de 1 Via** (ex.: migration destrutiva, alteração de contrato externo) e liste exatamente quais rotas/componentes podem ser afetados. Inclua o fato de segurança da etapa 4 com a prova ou o rótulo `não provado`.
   - **Prova de Execução (`[measured]`):** Resumo dos resultados do Pest, Larastan e Pint.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Eu mesmo acabei de escrever o código, posso apenas olhar rápido sem seguir os 2 eixos." | **Proibido.** A Revisão Adversarial exige checagem independente de Standards (Segurança/N+1/Livewire) e Spec. |
| "Não há impacto nenhum no Raio de Explosão." | **Proibido.** Toda alteração toca alguma rota, tabela ou componente. Nomeie os pontos afetados explicitamente. |
| "Vou escrever um PR de 200 linhas listando cada arquivo modificado." | **Proibido.** O Git já mostra os arquivos. O briefing de PR deve ter no máximo 40 linhas de alto sinal. |
| "O `[BLOCKER]` é simples, eu mesmo corrijo durante a revisão." | **Proibido.** A revisão só reporta. Corrigir no meio mistura autor e revisor e esconde a decisão do usuário. |
| "Vou juntar os achados dos 2 eixos numa lista única por prioridade." | **Proibido.** Reordenar entre eixos deixa um eixo mascarar o outro. |
| "O raio de explosão está bem descrito, não preciso rodar nada." | **Proibido.** Texto convincente não prova nada. Execute código que prove o fato de segurança. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Relatório dos 2 eixos (Standards + Spec) entregue em seções separadas, sem edição de código.
- `[measured]` Fato de segurança provado por execução, ou rotulado `não provado`.
- `[measured]` Portão completo de `laravel-verification` aprovado para o estado revisado, com comandos, escopos e resultados citados.
- `[measured]` Briefing de PR com seção de Raio de Explosão entregue ao usuário.
