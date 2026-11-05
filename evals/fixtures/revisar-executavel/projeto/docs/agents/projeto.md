# Configuração do projeto

- Stack: Laravel 12, Livewire 3, Pest 3, PHP 8.3.
- Specs: `docs/specs/NNNN-slug.md`.
- Tickets: `docs/tickets/<spec>/NN-slug.md`.
- Glossário: `GLOSSARY.md`.
- ADRs: `docs/adr/`.
- Comandos: `./vendor/bin/pint --test`, `./vendor/bin/pest`.

## Execução e verificação

- Pest: `phpunit.xml` e `.env.testing` usam sqlite, banco `:memory:`, e-mail no mailer `array` e fila `sync`.
- O app não tem `.env`. Não há banco de desenvolvimento.
