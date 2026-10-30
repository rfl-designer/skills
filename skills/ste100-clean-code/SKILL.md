---
name: ste100-clean-code
description: Disciplina de escrita técnica ASD-STE100 em português, remoção de comentários desnecessários (/no-comments) e eliminação de ruído textual de IA (/unslop). Use em todas as respostas, documentações, commits, PRs e código PHP/Blade.
---

# Escrita Técnica ASD-STE100 e Código Sem Ruído (`ste100-clean-code`)

## 1. Objetivo
Manter toda comunicação, documentação (`SPEC`, `GLOSSARY.md`, PRs) e código-fonte livres de jargão vazio de IA (*slop*) e de comentários redundantes, aplicando o padrão **ASD-STE100** adaptado ao português.

## 2. Regras Inegociáveis de Texto (ASD-STE100 + `/unslop`)
- **Use consistência terminológica (1 termo = 1 conceito):** Chame sempre `Action` de `Action`, `DTO` de `DTO`, `Costura` de `Costura` e `Fatia Vertical` de `Fatia Vertical`.
- **Escreva em voz ativa:** Prefira "A Action atualiza o pedido" em vez de "O pedido é atualizado pela Action".
- **Mantenha frases curtas:** Limite instruções procedimentais a no máximo 20 palavras e explicações descritivas a no máximo 25 palavras.
- **Dê uma instrução por frase:** Separe passos múltiplos em listas numeradas.
- **Corte muletas de IA (`/unslop`):** Proíba expressões vazias como *"Certamente!"*, *"Vamos mergulhar nisso"*, *"É importante notar que"*, *"Robusto e escalável"*, *"Sem mais delongas"*. Vá direto ao fato técnico.
- **Escreva o commit com a prova:** O título diz o que mudou. O corpo diz por que mudou e como você provou. A prova é o comando e o resultado `[measured]`, por exemplo `pest --filter=AprovaPedido: 3 passed`. Sem prova executada, escreva `não verificado` e o motivo.

## 3. Regras Inegociáveis de Código (`/no-comments`)
- **Não narre o que o código já diz:** Remova todo comentário que apenas repete o nome do método ou variável (ex.: `// Busca o usuário pelo ID`).
- **Codifique restrições na estrutura, não em comentários:** Se você sente vontade de escrever um comentário avisando sobre um tipo ou estado, substitua o comentário por um tipo estrito, um `enum`, um DTO `readonly` ou uma asserção.
- **Quando um comentário é permitido:**
  1. Anotações de tipo exigidas pelo Larastan/PHPStan (ex.: `/** @var Collection<int, Order> $orders */`).
  2. Explicação de um *porquê* não-óbvio (workaround de bug externo, link de RFC ou motivo de performance medido).
- **Subtraia antes de adicionar:** Delete código comentado, métodos não chamados e imports órfãos no mesmo commit.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou deixar comentários `// Passo 1`, `// Passo 2` dentro do método `handle()` para ficar didático." | **Proibido.** Se o método precisa de divisórias em comentário, extraia métodos privados com nomes claros. |
| "Vou comentar o código antigo em vez de apagar, caso precisemos dele depois." | **Proibido.** O Git guarda o histórico. Delete código morto imediatamente. |
| "Vou escrever uma introdução longa elogiando a pergunta do usuário." | **Proibido.** Comece a resposta diretamente pela decisão, diagnóstico ou resultado. |
| "O título `fix: corrige aprovação` basta; o diff mostra o resto." | **Proibido.** O diff mostra o quê, não o porquê nem a prova. Escreva os dois no corpo. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Zero código comentado ou comentários narrativos (`// valida dados`, `// salva no banco`) no `git diff`.
- `[measured]` Texto da Spec, ticket ou PR escrito em voz ativa e frases curtas sob o padrão ASD-STE100.
- `[measured]` Corpo de cada commit com o porquê e a prova, ou com `não verificado` e o motivo.
