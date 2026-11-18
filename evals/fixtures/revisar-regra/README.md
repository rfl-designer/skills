# Fixture de `Regra:` em `/revisar`

Uma mudança pequena sobre o app de [`revisar-executavel`](../revisar-executavel/README.md): o comando `pedidos:aprovar` grava o Gerente que pediu a Aprovação, e a lista do Gerente mostra quem aprovou e quando. Ela exercita a etapa 5.9 de `/revisar`: um achado com `Regra:` e um sem.

- `mudanca.patch`: o diff `master...feature/quem-aprovou`.
- `spec-quem-aprovou.md`: a Spec aprovada. O `montar.sh` a grava em `docs/specs/0006-quem-aprovou.md`, no commit da base.
- `mapa-de-fluxos.md`: o Mapa de Fluxos da etapa 2, montado com `rg` no estado da branch.

## Montagem

```bash
evals/fixtures/revisar-regra/montar.sh <pasta> [<pasta com vendor/ pronto>]
```

O script copia `../revisar-executavel/projeto/`, cria o repositório com a base em `master` e o diff em `feature/quem-aprovou`, instala as dependências e roda o Pest. A segunda pasta e os links físicos de `vendor/` seguem as regras de [`revisar-executavel`](../revisar-executavel/README.md#montagem).

Dê ao revisor só a worktree, o diff, o mapa e as skills. Não dê `gabarito/`, `evals/cenarios.md` nem os arquivos de resultado: eles descrevem os defeitos plantados.

## Gabarito

[`gabarito/GabaritoTest.php`](gabarito/GabaritoTest.php) tem uma prova por defeito. Copie-o para `tests/Feature/Gabarito/` e rode `./vendor/bin/pest tests/Feature/Gabarito`.

| Defeito | Caso concreto | Na head | Na base | `Regra:` esperada |
|---|---|---|---|---|
| R1. N+1 do Aprovador | A lista do Gerente lê `aprovador` sem `with()` | `LazyLoadingViolationException`; 23 consultas com 20 Pedidos, 5 com 2 | Não roda: a coluna não existe | `Model::preventLazyLoading()` no `AppServiceProvider` |
| R2. Fuso da Aprovação | Pedido aprovado em `2026-03-10 01:30` UTC | mostra `10/03/2026 01:30`; a Spec pede `09/03/2026 22:30` | Não roda: a coluna não existe | nenhuma |

Condição 2 de R1, medida na montagem: com `with(['cliente.user', 'aprovador'])` e a trava `preventLazyLoading()` com `handleLazyLoadingViolationUsing()` no `AppServiceProvider`, a suíte inteira passa. Sem o `with()`, o teste da base `mostra ao Gerente todos os Pedidos` falha com a mensagem da trava. A trava não pega o `$user->cliente` da lista do Cliente: o Laravel só a aplica a um modelo que veio numa coleção de 2 ou mais.

R2 não tem regra: a classe do erro é o fuso que a regra de negócio pede, e nenhuma ferramenta a detecta sem executar o caso. Uma regra contra `now()`, `today()` ou `format()` daria falso positivo: o comando grava `now()` em UTC, como a Spec pede.
