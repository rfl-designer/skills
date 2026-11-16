---
name: tdd-seams
description: Disciplina de Test-Driven Development (TDD) nas Costuras públicas e nas Fronteiras, neutra de linguagem e de framework. Use ao escrever ou revisar testes, e quando duas correções seguidas falham no mesmo teste ou portão.
---

# TDD na Costura (`tdd-seams`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

**Perfil de stack:** Esta skill não assume linguagem nem framework. Use o executor de testes da configuração. Se a configuração ou os manifests mostram Laravel, leia também [references/laravel.md](references/laravel.md): ele traduz cada regra para Pest e Livewire e traz os exemplos em código. Sem perfil para a stack do projeto, aplique cada regra com o mecanismo equivalente da stack.

## 1. Objetivo
Garantir que todo comportamento seja guiado por testes focados nas Costuras públicas e nas Fronteiras, proibindo mocks frágeis de detalhes internos.

## 2. Regras Inegociáveis
- **Teste comportamento, nunca implementação:** Avalie a saída da Costura escolhida, o estado gravado no banco de dados e a resposta da Fronteira.
- **Apague o teste que passa com a Costura vazia:** Imagine a Costura a devolver nulo ou uma coleção vazia, sem gravar nada. Se o teste ainda passa, ele não prova a regra. Reescreva-o para afirmar o valor e o estado que o usuário vê.
- **Não escreva um teste falso:** Às vezes, um teste honesto não é possível: condição de corrida, carga, serviço externo sem fake. Então, não escreva um teste que não prova nada. Registre o motivo e use a prova mais próxima, como a contagem de consultas ou o índice único no schema. Marque essa prova como `parcial`; sem prova, marque `não verificado`. Esta saída não dispensa o RED dos outros comportamentos.
- **Ataque a premissa:** Duas correções com a mesma premissa falharam no mesmo teste ou portão. Pare e reverta as duas. Escreva essa premissa numa frase. Prove ou refute a premissa com uma execução, como um teste ou uma consulta. Não comece a 3ª correção antes dessa prova. Com a premissa refutada, volte às hipóteses.
- **Proíba mocks internos da persistência:** Nunca faça mock do ORM, do construtor de consultas ou de repositórios internos. Use o banco de testes real, com as fábricas ou fixtures do projeto e isolamento por teste.
- **Use mocks apenas em fronteiras externas reais:** Use os fakes da stack só para isolar rede e I/O externo: HTTP de saída, fila, e-mail, armazenamento de arquivos e relógio.
- **Teste a Costura e a Superfície:**
  1. Teste regras pela Costura pública escolhida. CRUD trivial pode ser coberto na Fronteira sem criar uma Costura só para o teste.
  2. Teste autorização, validação e integração na Fronteira usada pelo projeto: teste de componente no servidor ou teste HTTP. Inclua a tentativa de alterar o estado que o cliente controla. Prove interação de UI no navegador quando aplicável.
- **Proteja a arquitetura com testes de arquitetura:** Se a stack tem uma ferramenta de teste de arquitetura, mantenha um teste que codifique as restrições estruturais do projeto. Sem ferramenta, registre a lacuna; não instale uma por rotina.

## 3. Forma do teste

Cada teste tem 3 partes visíveis e afirma um valor concreto.

- **Na Costura:** monte o estado com as fábricas do projeto; chame o ponto de entrada público com o contrato de dados; afirme o valor devolvido e o registro gravado.
- **Na Fronteira:** autentique um usuário sem permissão; dispare a ação pela Fronteira real; afirme a recusa e que nada foi gravado.
- **Na arquitetura:** codifique só as convenções que o projeto adotou. Não force a migração de módulos existentes para satisfazer um exemplo.

O perfil de stack mostra estes testes em código.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou fazer mock do modelo para o teste rodar sem banco." | **Proibido.** Mocks da persistência mentem sobre SQL e relacionamentos. Use fábricas e o banco de testes real. |
| "Vou usar reflexão para testar um método privado da Costura." | **Proibido.** Métodos privados são detalhes de implementação. Teste a interface pública escolhida. |
| "Vou escrever o código primeiro e adicionar o teste depois." | **Proibido.** Siga o ciclo RED → GREEN → REFACTOR. |
| "Afirmar que o retorno não é nulo já cobre a Costura." | **Proibido.** Esse teste passa com quase qualquer retorno. Afirme o status, o valor e o registro gravado. |
| "Não consigo testar a condição de corrida; escrevo um teste que só chama o método." | **Proibido.** Um teste que não pode falhar esconde a lacuna. Registre o motivo e a prova mais próxima, marcada `parcial`. |
| "A 2ª correção também falhou; tento uma 3ª variação." | **Proibido.** Duas falhas com a mesma premissa indicam uma premissa errada. Escreva a premissa e prove-a antes de outra correção. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Teste visto falhando (`RED`) antes da implementação e passando (`GREEN`) depois, com o comando de teste focado da configuração.
- `[measured]` Depois de 2 correções com a mesma premissa sem GREEN: a premissa numa frase e a execução que a prova ou refuta.
