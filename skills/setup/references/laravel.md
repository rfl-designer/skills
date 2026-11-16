# Perfil Laravel de `/setup`

Leia este perfil só quando a detecção mostra PHP com Laravel. Ele lista os pontos de detecção dessa stack. Não instale nem atualize nada.

- **Manifests:** `composer.json`, `composer.lock`, `package.json`, `tests/Pest.php` e `phpunit.xml`.
- **Executor:** local, Herd, Sail ou outro. No Sail, os comandos começam com `./vendor/bin/sail`.
- **Teste focado e suíte:** `./vendor/bin/pest --filter=<Teste>` e `./vendor/bin/pest`.
- **Análise estática:** `./vendor/bin/phpstan analyse`, com Larastan quando instalado.
- **Formatação:** `./vendor/bin/pint --test`. Registre como o Blade é habilitado: `"Pint/laravel_blade": true` em `rules` do `pint.json`, ou `--blade`.
- **Driver de cobertura:** `php -m` mostra `pcov` ou `xdebug`.
- **Mutação:** `--mutate` no help do Pest (`pest --mutate --path=<arquivos>`), ou `infection/infection` no `composer.lock` (`--git-diff-filter=AM`).
- **Relatório Clover para CRAP:** `pest --coverage-clover=<arquivo fora do repositório>`. O `<source>` do `phpunit.xml` define os arquivos medidos.
- **Capacidades condicionais:** Pest Agent (`--agent` no help do Pest), plugin Browser e Blade no Pint.
- **Linha `Perfis de stack`:** `laravel`.
