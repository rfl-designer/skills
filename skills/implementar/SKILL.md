---
name: implementar
description: Implementa uma Especificação ou ticket em Laravel e Livewire usando TDD na Costura (Pest), Larastan e Pint (.php e .blade.php), com commits atômicos. Use quando o usuário digitar /implementar.
disable-model-invocation: true
---

# Implementar Fatia Vertical com TDD (`/implementar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Executar os tickets planejados uma Fatia Vertical por vez, aplicando o ciclo Red-Green-Refactor na Costura pública escolhida e na Fronteira `Livewire`/HTTP, validando com Pest, Larastan e Pint antes de cada commit.

## 2. Regras Inegociáveis
- **Carregue as disciplinas de modelo:** Aplique rigorosamente `laravel-deep-modules`, `laravel-tdd-seams`, `laravel-verification` e `ste100-clean-code`.
- **Siga o ciclo Red-Green-Refactor:** Escreva o teste Pest falhando antes de escrever o código de produção da fatia.
- **Proteja a janela de contexto ao delegar:** Se houver frentes desbloqueadas paralelizáveis e o ambiente suportar subagentes + `git worktree`, passe apenas **Ponteiros de Contexto** (caminho da Spec, número do ticket e arquivos-alvo). Nunca cole o histórico bruto do chat.
- **Faça commits quando autorizados pela sessão:** Cada fatia verde pode gerar um commit atômico (~100 linhas). Se o usuário pedir entrega sem commit, mantenha o diff no working tree e registre o checkpoint.

## 3. Processo (Por Fatia Vertical Desbloqueada)
1. **Seleção da Fatia:** Identifique o próximo ticket desbloqueado no plano ou no destino de Tickets configurado. Siga o vínculo para a Spec, mesmo quando ela estiver em outro sistema. Use os comandos e diretório de execução do escopo afetado, substituindo os exemplos abaixo.
2. **Passo RED (Teste Falhando na Costura e Fronteira):**
   - Crie ou atualize o teste no Pest exercitando a Costura (Action, serviço existente ou Fronteira simples) e/ou a superfície (`Livewire::test()` / rota HTTP).
   - Execute `./vendor/bin/pest --filter=<NomeDoTeste>` e confirme que falha pelo motivo esperado.
3. **Passo GREEN (Implementação Mínima Profunda):**
   - Reutilize a Costura acordada. Crie Enum, DTO ou Action apenas quando justificam a complexidade encapsulada. Preserve validação, autorização e proteção do estado Livewire.
   - Durante as edições, use o ciclo rápido de `laravel-verification`; probes `--agent` são opcionais quando disponíveis.
   - Execute `./vendor/bin/pest --filter=<NomeDoTeste>` até ficar verde.
4. **Passo REFACTOR & PORTÃO DE VERIFICAÇÃO:**
   - Remova código morto e comentários desnecessários (`ste100-clean-code`).
   - Antes do commit ou entrega da fatia, aplique o portão completo de `laravel-verification`: Pint com Blade habilitado → PHPStan → Pest, mais navegador quando necessário. Reutilize resultados que ainda cobrem o estado atual.
5. **Checkpoint da Fatia:** Com o portão aprovado (`[measured]`), faça commit se autorizado; caso contrário, registre a fatia concluída no working tree. Avance para o próximo ticket desbloqueado.
6. **Fechamento:** Ao concluir todos os tickets, instrua o usuário a rodar `/revisar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou implementar os 4 tickets de uma vez e rodar o Pest apenas no final." | **Proibido.** Implemente, teste e verifique uma fatia por vez. Faça commits por fatia quando autorizados. |
| "O teste da Action passou, não preciso testar o componente Livewire." | **Proibido.** Teste regras na Costura escolhida e integração/autorização na Fronteira. CRUD simples pode usar o teste de Fronteira sem Action artificial. |
| "Vou commitar agora e corrigir os erros do Larastan e do Pint no último commit." | **Proibido.** Nenhum commit entra na branch com erro de tipo ou formatação pendente. |

## 5. Prova de Execução (Critério de Saída)
Para cada fatia entregue, apresente evidência medida:
- `[measured]` Saída verde de `./vendor/bin/pest`.
- `[measured]` Saída sem erros de `./vendor/bin/phpstan analyse`.
- `[measured]` Saída limpa do Pint com Blade habilitado; cite o escopo efetivamente verificado.
