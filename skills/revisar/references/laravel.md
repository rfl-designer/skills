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
- **Verificador enfraquecido:** uma linha que o diff acrescenta com `->ignoring(` num teste Pest arch, `@pest-arch-ignore`, `@phpstan-ignore` ou `@phpstan-ignore-next-line`.

## Formas de prova

| Suspeita | Prova |
|---|---|
| Ação sem `authorize()` ou sem Policy | Teste Livewire ou HTTP com um usuário sem permissão: a ação passa e grava |
| Propriedade sem `#[Locked]` | Teste Livewire que altera a propriedade com `set()` e chama a ação |
| Operação executada 2 vezes | 2 chamadas em sequência; conte gravações e envios com `Mail::fake()`, `Notification::fake()` ou `Queue::fake()` |
| N+1 | Teste com 2 ou mais registros e `Model::preventLazyLoading()`, ou contagem com `DB::enableQueryLog()` |
| Marcador de exceção novo | Script que apaga o marcador, roda `./vendor/bin/phpstan analyse` ou `./vendor/bin/pest tests/Arch`, mostra o erro e restaura o arquivo |

Exemplo da linha **Prova** de um achado: `./vendor/bin/pest tests/Feature/Revisao/PedidoDiaErradoTest.php` imprime `Failed asserting that '2026-03-11' is identical to '2026-03-10'`.

## Mecanismos de `Regra:`
Escolha o primeiro mecanismo que detecta a classe do erro:

1. **Trava do Eloquent** em `AppServiceProvider::boot()`: `Model::preventLazyLoading()`, `Model::preventSilentlyDiscardingAttributes()` e `Model::preventAccessingMissingAttributes()`. Desligue a trava em produção, como em `Model::preventLazyLoading(! $this->app->isProduction())`. A mensagem padrão só proíbe: dê a correção com `Model::handleLazyLoadingViolationUsing()`, `Model::handleDiscardedAttributeViolationUsing()` ou `Model::handleMissingAttributeViolationUsing()`.
2. **Teste Pest arch** em `tests/Arch/`. O Pest arch não aceita mensagem de falha customizada: a correção vai na descrição, `arch('<proibição>: <correção>')`.
3. **Opção do Larastan ou regra PHPStan customizada**, com a correção em `tip()`.

Exemplo do campo: `- **Regra:** Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction()) no AppServiceProvider, proíbe atribuir em massa um atributo fora de $fillable, mensagem "Acrescente [<atributo>] a $fillable de [<Model>]" por handleDiscardedAttributeViolationUsing().`
