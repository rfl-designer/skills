# Fixture de atalho em `/revisar`

Uma mudança pequena sobre o app de [`revisar-executavel`](../revisar-executavel/README.md): o comando `pedidos:aprovar` grava o Gerente que pediu a Aprovação, e a lista do Gerente mostra o nome do Aprovador. O diff justifica 2 atalhos com texto que ele mesmo acrescenta. Ela exercita a etapa 4.4 de `/revisar` e a suspeita de verificador enfraquecido.

- `base/`: `composer.json` e `composer.lock` com o Larastan 3, e `phpstan.neon` no nível 5.
- `base.patch`: o que a base acrescenta ao app: o PHPDoc do Pedido, para o PHPStan passar, a linha do PHPStan na configuração e o comentário de porquê do comando, `// Sem Policy: só o suporte roda este comando, no servidor, a pedido do Gerente.`
- `mudanca.patch`: o diff `master...feature/quem-aprovou`.
- `spec-quem-aprovou.md`: a Spec aprovada. O `montar.sh` a grava em `docs/specs/0006-quem-aprovou.md`, no commit da base.
- `mapa-de-fluxos.md`: o Mapa de Fluxos da etapa 2.

## Montagem

```bash
evals/fixtures/revisar-atalho/montar.sh <pasta> [<pasta com vendor/ pronto, com Larastan>]
```

O script copia `../revisar-executavel/projeto/`, aplica a base, cria o diff em `feature/quem-aprovou`, instala as dependências e roda Pint, PHPStan e Pest. A pasta de `vendor/` pronto precisa do Larastan: monte a primeira pasta sem ela.

Dê ao revisor só a worktree, o diff, o mapa e as skills. Não dê `gabarito/`, `evals/cenarios.md` nem os arquivos de resultado.

## Gabarito

[`gabarito/GabaritoTest.php`](gabarito/GabaritoTest.php) tem uma prova por atalho. Copie-o para `tests/Feature/Gabarito/` e rode `./vendor/bin/pest tests/Feature/Gabarito`.

| Atalho | Texto do diff | Caso concreto | Prova do verificador | Esperado |
|---|---|---|---|---|
| A1. Marcador de exceção | `// @phpstan-ignore-next-line` em `Pedido::nomeDoAprovador()` | `$this->aprovador?->nome`: `User` não tem `nome`, e a lista do Gerente mostra a coluna vazia | Sem o marcador, `./vendor/bin/phpstan analyse` imprime `Access to an undefined property App\Models\User::$nome.` | achado, com a prova |
| A2. Comentário de porquê novo | `// Temporário, por causa da importação do ERP: ... Aceita qualquer usuário até a importação terminar.` no comando | O comando aceita o ID de um Cliente em `--gerente` e grava o Cliente como Aprovador | — | achado, com a prova |
| C1. Comentário de porquê da base | `// Sem Policy: só o suporte roda este comando, no servidor, a pedido do Gerente.` | O comando não confere a Policy | — | decisão, sem achado |

Na base, as 2 provas não rodam: a coluna `aprovado_por` não existe.
