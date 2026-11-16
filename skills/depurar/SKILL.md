---
name: depurar
description: Diagnostica e corrige bugs por método científico, em qualquer linguagem ou framework (reproduzir num teste, localizar por busca binária, corrigir na causa raiz e validar). Use quando o usuário digitar /depurar.
disable-model-invocation: true
---

# Diagnóstico Científico e Correção de Bugs (`/depurar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Localizar a causa raiz de um defeito através de hipóteses verificáveis e provar a correção com um teste de regressão que falha antes do fix e passa depois.

## 2. Regras Inegociáveis
- **Pare a linha (Regra Stop-the-Line):** Nunca aplique um "chute" ou correção cosmética sem antes reproduzir o defeito de forma confiável.
- **Reproduza antes de corrigir:** Escreva um teste, na Costura ou na Fronteira, que reproduza exatamente o bug e falhe (`RED`).
- **Corrija a causa raiz, não o sintoma:** Se um dado inválido chegou à Costura, corrija a validação na Fronteira e a tipagem no contrato de dados, em vez de espalhar checagens defensivas de nulo pelo código.
- **Separe a reprodução da correção:** Verifique que o teste de regressão falha sem a correção e passa com ela.
- **Ataque a premissa:** Depois de 2 correções com a mesma premissa sem GREEN, aplique a regra "Ataque a premissa" de `tdd-seams`. Sem essa skill, pare, reverta as duas correções, escreva a premissa numa frase e prove-a por execução antes da 3ª correção.

## 3. Processo (Loop de 5 Etapas)
1. **Reproduzir (Loop Vermelho):**
   - Use os comandos e o diretório de execução configurados; os comandos abaixo são exemplos de fallback.
   - Colete o stack trace, log da aplicação ou comportamento incorreto relatado.
   - Crie um teste mínimo que reproduza a falha. Execute o teste focado, com o comando da configuração, e meça a falha (`[measured]`).
2. **Localizar e Minimizar (Busca Binária):**
   - Trace o fluxo da Fronteira até a Costura, o modelo e o banco.
   - Formule de 3 a 5 hipóteses falsificáveis, ordenadas por probabilidade. Cada hipótese declara sua previsão: "Se X é a causa, mudar Y faz o bug sumir."
   - Mostre a lista ao usuário antes de testar. Não espere a resposta para começar.
   - Elimine hipóteses com logs temporários, `dump()` em teste ou leitura de queries (`DB::enableQueryLog()`) até confirmar a linha exata que corrompe o estado.
   - Quando a evidência refuta uma hipótese, reverta toda alteração que ela motivou.
3. **Corrigir na Causa Raiz:**
   - Aplique a menor alteração estrutural que elimina a causa raiz respeitando `deep-modules`.
   - Remova qualquer instrumentação temporária (`dd`, `dump`, `Log::debug`).
4. **Proteger (Guard & Verification):**
   - Durante o diagnóstico, execute o teste de regressão focado; use probes se disponíveis. Antes de entregar, aplique o portão completo de `verification`.
   - Se o usuário pedir commits, grave o teste de regressão em um commit antes do commit da correção. O histórico mostra o vermelho e depois o verde.
5. **Relatório Curto de Causa Raiz:**
   - Explique em 3 bullets: (1) Qual era a causa raiz, (2) Qual teste agora impede a regressão, (3) Qual foi o resultado medido da verificação.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Já sei qual é o erro olhando o código, vou alterar direto sem criar o teste antes." | **Proibido.** Sem ver o teste falhar antes da alteração, você não provou que o teste realmente captura o bug. |
| "O primeiro fix não funcionou, vou adicionar mais um try/catch por cima." | **Proibido.** Releia o erro, reverta a tentativa falha e formule uma hipótese baseada em evidência medida. |
| "Dois fixes da mesma hipótese falharam; tento uma terceira variação." | **Proibido.** Escreva a premissa comum numa frase e prove-a ou refute-a por execução antes da 3ª correção. |
| "Vou colocar `@` ou `optional()` para silenciar o erro de propriedade nula." | **Proibido.** Silenciar exceção oculta corrupção de estado. Corrija a origem do dado nulo. |
| "A primeira hipótese parece certa, não preciso listar outras." | **Proibido.** Uma hipótese única prende a busca na primeira ideia plausível. Liste de 3 a 5. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Teste de regressão visto falhando (`RED`) antes do fix.
- `[measured]` Mesmo teste visto passando (`GREEN`) após o fix.
- `[measured]` Depois de 2 correções sem GREEN: a premissa comum numa frase e a execução que a prova ou refuta.
- `[measured]` Portão completo de `verification` aprovado para o estado corrigido; regressão preservada em teste permanente.
