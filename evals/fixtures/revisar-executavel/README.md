# Fixture executável de `/revisar`

A mesma mudança de [`revisar`](../revisar/README.md), num app Laravel que roda: o Gerente aprova o Pedido pela lista. Com ela, um revisor pode provar cada achado com o Pest.

## Diferenças da fixture de leitura

O app de [`leitura-independente`](../leitura-independente/README.md) não roda. Para rodar, esta cópia acrescenta só o necessário:

- `composer.json` e `composer.lock` (Laravel 12, Livewire 3, Pest 3, Pint), `artisan`, `bootstrap/`, `phpunit.xml` e `.env.testing`, com sqlite `:memory:` e e-mail no mailer `array`.
- A migration de `users`, as factories, `HasFactory` nos Models e `Notifiable` no `User`, como no esqueleto do Laravel. Sem eles, o teste do próprio diff falha, e o autor não entregaria a mudança.
- `->name('fechar-dia')` no agendamento de `routes/console.php`. Sem o nome, o Laravel 12 recusa `onOneServer()`, e nenhum comando `artisan` roda.
- 2 testes da base: o Fechamento do Dia e a lista de pedidos.
- A Spec entra no commit da base, em `docs/specs/0005-aprovar-pela-lista.md`.

O diff é o mesmo: [`mudanca.patch`](mudanca.patch) difere do patch da fixture de leitura só no contexto de `Pedido.php`. O [Mapa de Fluxos](mapa-de-fluxos.md) difere só na linha da relação `aprovador()`. Na base, o diff tem o Pest verde e o Pint aprovado.

Consequência: o defeito não plantado do `User` sem `Notifiable`, que a avaliação de 30/10 achou, não existe aqui.

## Montagem

```bash
evals/fixtures/revisar-executavel/montar.sh <pasta>
```

O script copia `projeto/`, cria o repositório com a base em `master` e o diff em `feature/aprovar-pela-lista`, instala as dependências e roda o Pest. Para várias pastas, instale uma vez e passe a pasta pronta como segundo argumento: o script copia `vendor/` com links físicos. Não rode `composer` numa pasta com links físicos, porque ele reescreve arquivos que as outras pastas compartilham.

Depois, copie `skills/revisar/` e as 3 disciplinas do revisor para `<pasta>/skills/`. Dê ao revisor só essa pasta. Não dê `gabarito/`, `evals/cenarios.md` nem os arquivos de resultado: eles descrevem os defeitos plantados.

## Gabarito

[`gabarito/GabaritoTest.php`](gabarito/GabaritoTest.php) tem uma prova por defeito. Para executá-la, copie o arquivo para `tests/Feature/Gabarito/` e rode `./vendor/bin/pest tests/Feature/Gabarito`. [`gabarito/mutacao-d5.sh`](gabarito/mutacao-d5.sh) `<pasta do projeto>` prova D5 por mutação.

| Defeito | Prova | Na head | Na base |
|---|---|---|---|
| D1. Ação sem autorização | O Cliente chama `aprovar` no próprio Pedido | 200 no lugar de 403 | Não roda: a ação não existe |
| D2. Aprovação repetida | 2 chamadas à Action | 2 e-mails no lugar de 1 | Não roda: a Action não existe |
| D3. Gerente errado no comando | `--gerente` com o 2º Gerente | grava o 1º | Não roda: a opção não existe |
| D4. Comando sem a recusa do status | Pedido aprovado ontem, e Pedido Cancelado | sai com sucesso; o Fechamento do Dia debita de novo | Não roda: a opção não existe; sem ela, a base recusa |
| D5. Teste que não prova | A Action deixa de gravar | o teste do diff continua verde | — |
| D6. N+1 do Aprovador | Lista do Gerente com 2 Pedidos e `preventLazyLoading()` | `LazyLoadingViolationException` | Não roda: a coluna não existe |
| Janela das 23h59, da base | Pedido aprovado às 23h59min30s | nunca é debitado | a mesma falha |

Os controles C1 (coluna nula) e C2 (e-mail depois do commit) passam na head. C3 (lista sem paginação) é escolha da Spec.
