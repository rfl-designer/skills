# Fixture de correção do humano em `/ajustar`

Uma mudança pequena sobre o app de [`revisar-executavel`](../revisar-executavel/README.md): o Gerente estorna um Pedido Aprovado pela lista, e o componente Livewire grava as 2 escritas com `DB::transaction()`. A revisão não tem achados. O usuário corrige uma classe de erro que a revisão não aponta: o componente Livewire usa o banco direto. Ela exercita a correção do humano de `/ajustar`.

- `base.patch`: a Spec 0007 em `docs/specs/0007-estorno-pela-lista.md`. O `phpunit.xml` da base só tem a suíte `Feature`.
- `base-antiga.patch`: só na variante `antiga`. A base ganha o componente `App\Livewire\Clientes\Saldo`, que soma os Pedidos aprovados com `DB::table()` em `app/Livewire/Clientes/Saldo.php:18`, com a view e um teste.
- `mudanca.patch`: o diff `master...feature/estorno`, a ação `Lista::estornar` com `DB::transaction()` em `app/Livewire/Pedidos/Lista.php:21`.
- `relatorio-revisar.md`: o relatório da rodada 1 de `/revisar`, sem achados, com `Veredito: pode entregar.`

## Montagem

```bash
evals/fixtures/ajustar-feedback/montar.sh <pasta> <sem-antiga|antiga> [<pasta com vendor/ pronto>]
```

O script copia `../revisar-executavel/projeto/`, aplica a base da variante, cria o diff em `feature/estorno`, instala as dependências, copia o relatório e roda o Pest.

Pedido do usuário, igual nas 2 variantes: “/ajustar: não use `DB::` em componente Livewire; a escrita com transação vai numa Action de `App\Actions`, como `FecharDia`. Sem commits.”

Dê ao agente só o projeto, o relatório, o pedido e as skills. Não dê este README, `evals/cenarios.md` nem os arquivos de resultado.

## Gabarito

A regra: `arch('os componentes Livewire não usam o facade DB: a escrita com transação vai numa Action de App\Actions')->expect('App\Livewire')->not->toUse('Illuminate\Support\Facades\DB')`. Medido na montagem, com o teste em `tests/Feature/ArchTest.php` e a escrita movida para `App\Actions\EstornarPedido`:

| Variante | Regra no diff, sem a correção | Com a correção | Esperado |
|---|---|---|---|
| `sem-antiga` | `Expecting 'App\Livewire' not to use 'Illuminate\Support\Facades\DB'.` | `6 passed` | o teste entra no Lote, num diretório de suíte que já roda, com a linha `Regra do achado H1:`; o `phpunit.xml` não muda |
| `antiga` | a mesma saída | `1 failed, 6 passed`: o teste de arquitetura, pelo componente `Saldo` | o teste fica fora do Lote; `Regras propostas:` lista `app/Livewire/Clientes/Saldo.php:18` |

A saída do Pest arch não traz o arquivo nem a linha, e nomeia o namespace, não a classe. O `arquivo:linha` do RED vem do achado `H1`; o da ocorrência antiga vem da busca com `rg`.

Fora do esperado: `tests/Arch/` com a suíte acrescentada ao `phpunit.xml`; `->ignoring('App\Livewire\Clientes\Saldo')`; corrigir o componente `Saldo` nesta rodada; manter o `DB::` com outro caminho, como `$pedido->getConnection()->transaction()`.
