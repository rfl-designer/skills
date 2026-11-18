# Perfil Laravel de `/ajustar`

Leia este perfil só quando o projeto usa PHP com Laravel. Ele traduz as regras da skill; não acrescenta etapa nova. Os comandos da configuração do projeto prevalecem sobre os exemplos.

## Configuração dos verificadores
`phpunit.xml`, `phpstan.neon`, `phpstan-baseline.neon` e `pint.json`. Uma regra que só roda com uma mudança num deles vai para `Regras propostas:`.

## Marcadores de exceção
`->ignoring(` num teste Pest arch, `@pest-arch-ignore`, `@phpstan-ignore` e `@phpstan-ignore-next-line`. Nenhum deles serve para obter verde, nem para deixar uma regra nova verde sobre as ocorrências antigas.

## Onde cada regra mora
O campo `Regra:` nomeia o mecanismo. Os mecanismos, em ordem de preferência:

1. **Trava do Eloquent** em `AppServiceProvider::boot()`: `Model::preventLazyLoading()`, `Model::preventSilentlyDiscardingAttributes()` ou `Model::preventAccessingMissingAttributes()`. Pode entrar no Lote.
   - Desligue a trava em produção: `Model::preventLazyLoading(! $this->app->isProduction())`.
   - A mensagem com a correção vem do handler: `Model::handleLazyLoadingViolationUsing()`, `Model::handleDiscardedAttributeViolationUsing()` ou `Model::handleMissingAttributeViolationUsing()`. O handler substitui a exceção padrão: ele lança uma exceção com a mensagem. Um handler que só grava log deixa a suíte verde com o defeito.
   - `preventLazyLoading()` só age no modelo que veio numa coleção de 2 ou mais. O RED precisa de um teste com 2 registros ou mais que passe pelo `arquivo:linha` do achado; o arquivo de prova do achado serve.
   - A trava vale para a aplicação inteira: o repositório inteiro é a suíte completa. Cada teste que falha com a mensagem da trava aponta uma ocorrência. A relação na mensagem e o stack trace dão o `arquivo:linha`.
2. **Teste Pest arch.** Pode entrar no Lote.
   - O arquivo vai para `tests/Arch/` só se o `phpunit.xml` já tem uma suíte com esse diretório. Senão, ponha-o no diretório de uma suíte que já roda, como `tests/Unit/ArchTest.php` ou `tests/Feature/ArchTest.php`. Não acrescente a suíte ao `phpunit.xml`. Sem uma suíte que rode o arquivo, a regra vai para `Regras propostas:`, e o esboço traz a suíte `Arch`.
   - O Pest arch não aceita mensagem de falha customizada: a correção vai na descrição, `arch('<proibição>: <correção>')`.
   - `not->toUse` falha sem arquivo e linha, e a saída nomeia o namespace e o alvo proibido: `Expecting 'App\Livewire' not to use 'Illuminate\Support\Facades\DB'.` O `arquivo:linha` do RED vem do achado. As ocorrências antigas vêm de uma busca com `rg` pelo alvo proibido no namespace da regra.
3. **Opção do Larastan ou regra PHPStan customizada**, com a correção em `tip()`. Sempre vai para `Regras propostas:`: a opção mora em `phpstan.neon`, e a regra do projeto precisa de `includes` em `phpstan.neon`, porque o `phpstan/extension-installer` não lê o `extra.phpstan` do projeto raiz. O esboço traz a classe da regra e a linha de `phpstan.neon`.

Exemplo da linha do relatório: `Regra do achado 3: app/Providers/AppServiceProvider.php. RED: com o defeito, tests/Feature/PerfilTest.php falhou com "Acrescente [apelido] a $fillable de [App\Models\Cliente]" (app/Livewire/Perfil.php:27, do achado). GREEN: passou depois da correção. Repositório: verde.`
