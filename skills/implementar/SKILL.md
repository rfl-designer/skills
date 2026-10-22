---
name: implementar
description: Orquestra a implementação de uma Especificação ou ticket em Laravel e Livewire com subagentes por fatia, TDD na Costura (Pest), Larastan e Pint (.php e .blade.php). Use quando o usuário digitar /implementar.
disable-model-invocation: true
---

# Implementar Fatia Vertical com TDD (`/implementar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
O agente principal coordena os tickets planejados e delega cada Fatia Vertical completa a um implementador. Cada implementador aplica Red-Green-Refactor na Costura pública escolhida e na Fronteira `Livewire`/HTTP. O principal confere e integra as entregas, validando o estado integrado antes de commit ou entrega.

## 2. Regras Inegociáveis
- **Carregue as disciplinas de modelo:** Aplique rigorosamente `laravel-deep-modules`, `laravel-tdd-seams`, `laravel-verification` e `ste100-clean-code`.
- **Siga o ciclo Red-Green-Refactor:** Escreva o teste Pest falhando antes de escrever o código de produção da fatia.
- **Delegue a fatia inteira:** O mesmo implementador escreve o teste, confirma RED, implementa GREEN e refatora. Não separe teste e produção entre agentes. O principal mantém a coordenação; não configure esta skill inteira com `context: fork`.
- **Proteja a janela de contexto ao delegar:** Passe ponteiros e um contrato curto de execução, sem o histórico bruto do chat. Cada agente precisa carregar as disciplinas de modelo; não presuma que herdou as skills do principal.
- **Limite a concorrência:** Use até dois implementadores simultâneos, apenas em fatias independentes e worktrees separados. Arquivos compartilhados ou dependências exigem sequência. Sem isolamento, use um implementador por vez e não edite o mesmo escopo enquanto ele trabalha.
- **Faça commits quando autorizados pela sessão:** Cada fatia verde pode gerar um commit atômico (~100 linhas). Se o usuário pedir entrega sem commit, mantenha o diff no working tree e registre o checkpoint.

## 3. Preparar e delegar (agente principal)

1. Leia a Spec, os tickets e suas dependências. Confira o estado inicial do repositório e preserve alterações existentes. Selecione uma fatia desbloqueada; selecione duas apenas quando não compartilham arquivos, contratos em mudança ou recursos de verificação incompatíveis.
2. No Claude Code, siga [references/claude-code.md](references/claude-code.md): use o agente `implementador` com **Sonnet 5.5 / medium**, mantendo o modelo do principal. Em outros ambientes, use o mecanismo e os modelos autorizados disponíveis; não traduza IDs da Anthropic para outro provedor. Se não houver subagentes, execute o ciclo diretamente e informe essa limitação.
3. Defina a base e o diretório de cada implementador. Worktrees devem partir do estado de integração escolhido, incluindo dependências já integradas; não presuma que o isolamento automático usa o HEAD atual. Se mudanças locais forem necessárias, prepare uma transferência revisável para a área isolada ou execute sequencialmente no checkout atual, sem commit implícito.
4. Envie este contrato, com caminhos válidos no diretório do agente e URLs acessíveis quando os documentos forem externos:
   - Spec, ticket, critérios de aceite e decisões da sessão ainda não registradas.
   - Configuração do projeto, instruções locais e caminhos das quatro disciplinas de modelo.
   - Base de integração, diretório de execução, arquivos/módulos sob sua responsabilidade e limites de escopo.
   - Comandos e recursos de verificação: se banco, portas ou app local forem compartilhados, isole-os ou serialize as verificações. Um worktree sozinho não isola esses recursos.
   - Autorização de commits e formato de retorno descrito abaixo.

Avise cada implementador que há outros agentes no repositório: não reverta mudanças alheias e ajuste sua implementação às alterações já integradas. Mudança necessária fora do escopo volta ao principal para replanejar. O implementador não delega novamente.

## 4. Processo (implementador, por Fatia Vertical)
1. **Confirmar a Fatia Atribuída:** Leia o ticket recebido e siga seu vínculo para a Spec, mesmo quando ela estiver em outro sistema. Confira critérios, escopo e dependências indicados pelo principal. Use os comandos e diretório de execução do escopo afetado, substituindo os exemplos abaixo. Não selecione outro ticket.
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
5. **Retorno ao principal:** Entregue ticket, critérios atendidos, arquivos alterados, diretório/worktree e diff ou commits autorizados. Inclua comandos, evidência RED e GREEN, portão completo, estado coberto e bloqueios. Distinga teste focado de suíte completa. Preserve mudanças e artefatos até a integração; não avance para outro ticket por conta própria.

## 5. Integrar e avançar (agente principal)

1. Aguarde o retorno e confira o diff contra a Spec, os critérios de aceite e o escopo atribuído. Um retorno parcial, sem RED esperado ou com verificação bloqueada não conclui a fatia. Retome o mesmo agente com a pendência e preserve o trabalho válido.
2. Integre uma fatia por vez, por diff ou commits quando autorizados. Resolva conflitos sem descartar trabalho alheio. Se a resolução alterar comportamento, retorne ao ciclo de teste da fatia afetada.
3. Execute o portão completo de `laravel-verification` sobre o estado integrado antes de commit ou entrega. Evidência de worktrees isolados não prova a combinação. Reutilize resultados apenas quando ainda cobrem exatamente o código, configuração e dependências relevantes; mudanças posteriores invalidam a cobertura afetada.
4. Com o portão aprovado (`[measured]`), faça commit atômico se autorizado; caso contrário, registre o checkpoint no working tree. Atualize dependências e selecione a próxima fatia desbloqueada. Limpe apenas worktrees criados por este fluxo, depois de preservar integração e evidências.
5. Ao concluir todos os tickets, apresente as provas do estado integrado e instrua o usuário a rodar `/revisar`.

## 6. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou implementar os 4 tickets de uma vez e rodar o Pest apenas no final." | **Proibido.** Cada implementador testa e verifica sua fatia completa antes de retornar; o principal verifica a integração. Faça commits por fatia quando autorizados. |
| "O teste da Action passou, não preciso testar o componente Livewire." | **Proibido.** Teste regras na Costura escolhida e integração/autorização na Fronteira. CRUD simples pode usar o teste de Fronteira sem Action artificial. |
| "Vou commitar agora e corrigir os erros do Larastan e do Pint no último commit." | **Proibido.** Nenhum commit entra na branch com erro de tipo ou formatação pendente. |
| "Os dois agentes passaram nos testes, então a integração está verde." | **Proibido.** Verifique o estado integrado antes de commit ou entrega. |

## 7. Prova de Execução (Critério de Saída)
Para cada fatia entregue e para o estado integrado, apresente evidência medida, com comando, diretório e estado coberto:
- `[measured]` Saída verde de `./vendor/bin/pest`.
- `[measured]` Saída sem erros de `./vendor/bin/phpstan analyse`.
- `[measured]` Saída limpa do Pint com Blade habilitado; cite o escopo efetivamente verificado.
