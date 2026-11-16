# Perfil Laravel de `/revisar`

Leia este perfil só quando o projeto usa PHP com Laravel. Ele traduz as etapas da skill; não acrescenta etapa nova. Os comandos da configuração do projeto prevalecem sobre os exemplos.

## Guarda do ambiente de teste
Leia `DB_CONNECTION`, `DB_DATABASE`, `MAIL_MAILER` e `QUEUE_CONNECTION` em `phpunit.xml`. Se falta um deles, leia o valor com `php artisan tinker --env=testing`. Continue só com banco `:memory:` ou com um banco de teste que o usuário confirmou, e com e-mail `array` ou `log`.

**ATENÇÃO:** `RefreshDatabase` roda `migrate:fresh` num banco que não está em memória. Esse comando apaga todas as tabelas. Com um banco que não está em memória, cada worktree precisa de um banco próprio, confirmado pelo usuário.

Não use o `.env` do usuário.

## Worktrees
- Copie `vendor/` para cada worktree, ou rode `composer install`.
- Uma cópia com links físicos (`cp -al`) é rápida, mas não rode `composer` nessa worktree: ele reescreve arquivos que as outras compartilham.
- Não use link simbólico para `vendor/`: o autoload segue o caminho real e carrega o código da outra pasta.
- Confirme que `./vendor/bin/pest` roda em cada worktree.
- **Pasta de provas:** `tests/Feature/Revisao/`.
- O revisor executa só o Pest e scripts `php` com a configuração de teste.

## Suspeitas do eixo Standards
- **Carga esperada:** procure também Horizon, Octane e o scheduler.
- **Segurança:** propriedade sensível ou ID em componente Livewire sem `#[Locked]`. Ação mutável sem `$this->authorize()` ou Policy.
- **Perda de dados:** erro engolido em `try/catch`. Várias escritas sem `DB::transaction()`. Job ou evento antes do commit sem `afterCommit()`. Job com `$tries`, webhook, comando agendado ou duplo clique que grava em dobro.
- **Escala:** N+1 por falta de `with()` ou de `preventLazyLoading`. `firstOrCreate` sem índice único; falta de `lockForUpdate()` ou `increment()`. Falta de `onOneServer()`, `withoutOverlapping()` ou `ShouldBeUnique`. `->get()` em tabela grande no lugar de `chunkById()` ou `lazy()`. Propriedade estática no Octane.

## Formas de prova

| Suspeita | Prova |
|---|---|
| Ação sem `authorize()` ou sem Policy | Teste Livewire ou HTTP com um usuário sem permissão: a ação passa e grava |
| Propriedade sem `#[Locked]` | Teste Livewire que altera a propriedade com `set()` e chama a ação |
| Operação executada 2 vezes | 2 chamadas em sequência; conte gravações e envios com `Mail::fake()`, `Notification::fake()` ou `Queue::fake()` |
| N+1 | Teste com 2 ou mais registros e `Model::preventLazyLoading()`, ou contagem com `DB::enableQueryLog()` |

Exemplo da linha **Prova** de um achado: `./vendor/bin/pest tests/Feature/Revisao/PedidoDiaErradoTest.php` imprime `Failed asserting that '2026-03-11' is identical to '2026-03-10'`.
