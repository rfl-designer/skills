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

Revise como o desenvolvedor que recebe o alerta quando a mudança quebra. Dentro de cada eixo, priorize nesta ordem: correto, seguro, aguenta a carga esperada, testado, rápido, enxuto.

## 2. Regras Inegociáveis
- **Use subagentes com contexto limpo:** Sempre que a ferramenta suportar subagentes, dispare 2 revisores paralelos isolados passando apenas Ponteiros de Contexto (referência do diff da etapa 1, caminho da Spec, glossário e configuração do projeto). O agente que escreveu o código tem viés de confirmação.
- **Reporte, não corrija:** `/revisar` não edita código. O usuário decide quais achados corrigir. A correção acontece depois, em `/implementar` ou `/bug`.
- **Leia o código conectado, não só o diff:** Leia os chamadores das funções alteradas, as funções chamadas, os testes e o README. Quando uma assinatura, um retorno ou um comportamento muda, busque todos os chamadores com `rg`.
- **Passe o pente-fino anti-ruído:** Aponte comentários óbvios, código morto e imports não utilizados segundo `ste100-clean-code`.
- **Mantenha os eixos separados:** Apresente Standards e Spec em seções próprias. Não junte nem reordene achados entre eixos. Um eixo aprovado não compensa o outro reprovado.
- **Classifique os achados por severidade dentro de cada eixo:**
  - `[BLOCKER]`: bug, falha de segurança, perda de dados ou quebra com a carga esperada.
  - `[IMPORTANTE]`: lógica de risco sem teste, lentidão real, duplicação, função com várias responsabilidades ou código que não devia existir.
  - `[NIT]`: ganho pequeno de velocidade ou forma mais curta.
- **Exija um caso concreto:** Todo achado descreve uma entrada ou situação e o resultado errado que ela produz. Sem caso concreto, não há achado.

## 3. Processo
1. **Coleta do Diff e Verificação Base:**
   - Use o alvo que o usuário indicar: mudanças locais, staged, branch, PR ou arquivos. Sem alvo, use o diff contra a branch base, com as mudanças locais. Sem diferença, use o último commit.
   - Inspecione `git status` e o diff do alvo. Registre a referência exata (ex.: `main...HEAD`) e passe a mesma referência aos dois subagentes.
   - Aplique o portão completo de `laravel-verification` ou reutilize evidência ainda válida para o mesmo estado. Não repita a suíte apenas por entrar na revisão.
2. **Revisão Adversarial em 2 Eixos (Subagentes Paralelos):** Cada subagente lê o código conectado e ordena seus achados pela prioridade da seção 1.
   - **Subagente 1 — Eixo Standards & Laravel/Livewire Security:**
     - **Carga esperada:** Procura a carga no repositório (README, filas, Horizon, Octane, scheduler, deploy). Declara a carga presumida.
     - **Segurança:** Verifica se propriedades sensíveis/IDs em componentes `Livewire` possuem `#[Locked]`. Verifica se toda ação mutável chama `$this->authorize()` / `Policy`.
     - **Perda de dados:** Caça erro engolido em `try/catch`, várias escritas sem `DB::transaction()` e job ou evento disparado antes do commit sem `afterCommit()`.
     - **Escala:**
       - N+1 queries Eloquent (falta de `with()` ou `preventLazyLoading`).
       - Condição de corrida entre leitura e escrita: `firstOrCreate` sem índice único, falta de `lockForUpdate()` ou `increment()`.
       - Tarefa repetida em cada processo: falta de `onOneServer()`, `withoutOverlapping()` ou `ShouldBeUnique`.
       - Memória que só cresce: `->get()` em tabela grande no lugar de `chunkById()` ou `lazy()`.
       - Algoritmo O(n²) sobre entrada grande.
       - Estado local do processo que devia ser compartilhado: propriedade estática no Octane, disco local com vários servidores.
     - **Velocidade:** Reporta lentidão real como `[IMPORTANTE]`. Reporta ganho pequeno, como trabalho repetido num laço quente, como `[NIT]`.
     - **Estrutura:** Verifica regras e coordenação sem encapsulamento, abstrações sem benefício e ausência de `declare(strict_types=1);`. Aceita CRUD simples e Costuras existentes conforme `laravel-deep-modules`.
     - **Enxuto:**
       - Apagar: código morto, opções sem uso, funcionalidade especulativa, comentários desnecessários (`ste100-clean-code`).
       - Reutilizar: o repositório já tem o helper, a Action ou o Scope. Cite o caminho.
       - Nativo: o Laravel ou o PHP já resolve (`Collection`, `Str`, `Arr`, regras de validação). Uma dependência nova para poucas linhas também entra aqui.
       - YAGNI: Interface com uma só implementação, configuração que ninguém altera.
       - Juntar: quase-cópias que precisam mudar juntas.
       - Separar: função com várias responsabilidades, difícil de ler ou testar. Separe por responsabilidade, nunca por número de linhas.
   - **Subagente 2 — Eixo Spec & Comportamento:**
     - Compara o diff linha a linha com a Especificação gerada em `/especificar`.
     - Aponta requisitos faltantes e escopo extra não solicitado (*scope creep*).
     - **Bug:** Caça resultado errado e erro em casos de borda (vazio, zero, último item, arredondamento, fuso horário). Caça chamador quebrado pela mudança. Caça correção feita num só chamador, com a função compartilhada ainda errada.
     - **Teste ausente:** Aponta lógica de risco sem um teste Pest que falhe quando ela quebra: ramo, parser, dinheiro, segurança, escrita de dados ou correção de bug. Pede um teste bom, não cobertura.
3. **Confirmação dos Achados:** Antes de reportar, cada subagente:
   1. Escreve o caso concreto de cada achado.
   2. Relê as linhas e confirma o fato: o chamador existe, o valor pode ser vazio, o código não tem uso.
   3. Trata como decisão, não como achado, o atalho com limite documentado em ADR, Spec ou comentário de porquê. Reporta o atalho só se a carga esperada já passa desse limite.
   4. Propõe a menor correção que funciona. Prefere a correção que apaga código. Não adiciona camadas, pacotes ou configuração que o problema não exige.
   5. Descarta gosto de estilo, "considere..." e preocupação vaga.
4. **Relatório por Eixo:**
   - Comece com `O que a mudança faz:` em 2 ou 3 frases.
   - Apresente os achados sob `## Standards` e `## Spec`, cada um com seus `[BLOCKER]`, `[IMPORTANTE]` e `[NIT]`. Omita o nível sem achados.
   - Numere os achados em sequência contínua de um eixo para o outro, sem reordenar. Assim, o usuário pode responder "corrija 2 e 5".
   - Explique cada termo técnico na primeira vez que ele aparecer. O leitor pode não conhecer o código.
   - Escreva cada achado neste formato, com 1 ou 2 frases curtas por parte:
     ```markdown
     2. [BLOCKER] **Pedido entra no dia errado** (`app/Actions/FecharDia.php:40-52`)
        - **O que é:** À meia-noite, esta Action fecha o dia e fatura os pedidos desse dia.
        - **Problema:** A Action usa `now()` no fuso UTC da aplicação. Um pedido feito às 22h em São Paulo já é 01h do dia seguinte em UTC.
        - **Correção:** Calcule o dia uma vez no fuso da loja: `now('America/Sao_Paulo')->toDateString()`. Nada mais muda.
        - **Se não corrigir:** Pedidos da noite saem com a data errada, e o financeiro corrige à mão.
     ```
   - Termine com:
     - 1 linha por eixo: total por nível e o pior achado.
     - `Carga presumida:` a carga usada no eixo Standards.
     - Sem `[BLOCKER]` nem `[IMPORTANTE]`: `Veredito: pode entregar.` Caso contrário: `Veredito: corrija 1 e 3 antes.`, com os números desses achados.
     - `Enxuto: -N linhas possíveis.` quando houver achado de Enxuto.
     - `Não verificado:` em 1 linha, quando algo importante não pôde ser verificado.
   - Sem achados nos dois eixos: escreva `O que a mudança faz:`, depois `Sem achados. Pode entregar.` e 1 linha com o que foi verificado.
   - Se houver `[BLOCKER]`, pare aqui e pergunte ao usuário como seguir.
5. **Prova do Fato de Segurança:** Identifique o único fato que torna a mudança segura (ex.: "a migration só adiciona coluna nullable"). Prove esse fato com um teste Pest ou um script que executa o código real. Se não conseguir provar, escreva `não provado`.
6. **Geração do Briefing de PR (Máximo 40 linhas, padrão ASD-STE100):**
   - **Por que (Why):** 1 a 2 frases explicando o problema resolvido.
   - **O que mudou (What changed):** Bullets curtos focados nas Fronteiras (`Livewire`/HTTP) e Costuras (`Actions`/DTOs).
   - **Porta de Decisão e Raio de Explosão (Blast Radius):** Classifique a mudança como **Porta de 2 Vias** (reversível sem perda de dados) ou **Porta de 1 Via** (ex.: migration destrutiva, alteração de contrato externo) e liste exatamente quais rotas/componentes podem ser afetados. Inclua o fato de segurança da etapa 5 com a prova ou o rótulo `não provado`.
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
| "O diff está correto; o resto do código não mudou." | **Proibido.** Uma mudança de assinatura, retorno ou comportamento quebra chamadores fora do diff. Busque todos os chamadores. |
| "Não tenho um caso concreto, mas vou anotar 'considere...' por precaução." | **Proibido.** Sem caso concreto, não há achado. A preocupação vaga vira ruído e esconde os achados reais. |
| "A correção certa é criar um Service, uma Interface e uma configuração nova." | **Proibido.** Proponha a menor correção que funciona. Prefira a correção que apaga código. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Relatório dos 2 eixos (Standards + Spec) entregue em seções separadas, sem edição de código.
- `[measured]` Cada achado com caso concreto, `arquivo:linha` e as 4 partes (O que é, Problema, Correção, Se não corrigir).
- `[measured]` Busca de chamadores citada para cada assinatura, retorno ou comportamento alterado.
- `[measured]` Carga presumida declarada no relatório.
- `[measured]` Fato de segurança provado por execução, ou rotulado `não provado`.
- `[measured]` Portão completo de `laravel-verification` aprovado para o estado revisado, com comandos, escopos e resultados citados.
- `[measured]` Briefing de PR com seção de Raio de Explosão entregue ao usuário.
