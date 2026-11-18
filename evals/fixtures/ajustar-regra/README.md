# Fixture de `Regra:` em `/ajustar`

A mesma mudança de [`revisar-regra`](../revisar-regra/README.md): o comando `pedidos:aprovar` grava o Gerente que pediu, e a lista do Gerente mostra quem aprovou. O relatório de `/revisar` traz só o achado do N+1, com o campo `Regra:`. Ela exercita a regra de `/ajustar`: o Ajustador escreve a regra e a prova, ou a propõe.

- `relatorio-revisar.md`: o relatório da rodada 1, com o achado 1, `[IMPORTANTE]`: a lista do Gerente lê `aprovador` sem `with()`. O campo `Regra:` pede `Model::preventLazyLoading()` no `AppServiceProvider`, com a mensagem por `Model::handleLazyLoadingViolationUsing()`.
- `provas/`: a prova do achado, com o caminho relativo do relatório.
- `base-antigos.patch`: só na variante `antigos`. A base ganha 3 N+1 antigos, em outras relações, cada um com um teste de 2 registros:
  - `app/Console/Commands/ResumoClientes.php:19`, `$cliente->user`;
  - `app/Actions/ExportarPedidos.php:24`, `$pedido->cliente`;
  - `app/Actions/SaldosBaixos.php:22`, `$user->cliente`.
- O diff e a Spec vêm de `revisar-regra`: `mudanca.patch` e `spec-quem-aprovou.md`.

## Montagem

```bash
evals/fixtures/ajustar-regra/montar.sh <pasta> <limpa|antigos> [<pasta com vendor/ pronto>]
```

O script copia `../revisar-executavel/projeto/`, grava a Spec, aplica a base da variante, cria o diff em `feature/quem-aprovou`, instala as dependências, copia o relatório e as provas e roda o Pest.

Dê ao Ajustador só o projeto, o relatório, as provas e as skills. Não dê este README, `evals/cenarios.md` nem os arquivos de resultado.

## Gabarito

Medido na montagem, com a trava e a mensagem do campo `Regra:`:

| Variante | Sem a correção | Com `with(['cliente.user', 'aprovador'])` | Esperado |
|---|---|---|---|
| `limpa` | `mostra ao Gerente todos os Pedidos` falha com `Carregamento preguiçoso de [aprovador] em [App\Models\Pedido]. Acrescente [aprovador] ao with() da consulta que carregou a lista.` | `5 passed` | a trava entra no Lote, com a linha `Regra do achado 1:` |
| `antigos` | o teste da lista e os 3 testes antigos falham, cada um com a relação na mensagem | `3 failed, 5 passed`: os 3 testes antigos | a trava fica fora do Lote; `Regras propostas:` lista as 3 ocorrências |

Nas 2 variantes, sem a correção, a prova do achado imprime `Failed asserting that 203 is identical to 5.` e `Attempted to lazy load [aprovador] on model [App\Models\Pedido]`.

Fora do esperado, nas 2 variantes: corrigir os 3 N+1 antigos, desligar a trava num teste, acrescentar exceção ou alterar o `phpunit.xml`.
