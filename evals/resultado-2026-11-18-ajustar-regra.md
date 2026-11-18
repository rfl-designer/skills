# Avaliação de `/ajustar`: a regra entra no Lote ou vai para `Regras propostas:`

Data: 18/11/2026. Base do pacote: `bcead5a`. Versão avaliada, sem commit:
- `skills/ajustar/SKILL.md` com as regras "Escreva e prove a regra" e "Leve a correção do humano à regra", o passo 5.6 "Regra no repositório", a linha `Regra do achado N:` e a seção `Regras propostas:` no retorno e no relatório (3.817 palavras; 2.811 em `bcead5a`, com skills#22 no meio).
- `skills/ajustar/assets/ajustador.md` com o parágrafo da regra (668 palavras; 499 em `bcead5a`).
- `skills/ajustar/references/laravel.md`, novo: a configuração dos verificadores, os marcadores de exceção e onde cada regra mora.

Executor: o autor da versão, que montou as fixtures e, nos casos 1 e 2, fez o papel do principal. Os Ajustadores dos casos 1 e 2 e os principais dos casos 3 e 4 foram subagentes gerais novos, sem o histórico da sessão, sem o gabarito e sem `evals/cenarios.md`. Cada um leu só a sua pasta de execução, com as skills copiadas para `skills/`.

Casos de [`cenarios.md`](cenarios.md): "Ajuste: regra que entra no Lote", "Ajuste: regra com ocorrências antigas" e "Ajuste: correção do humano vira regra", nas 2 variantes. Não há comparação com `bcead5a`: lá a regra não existe.

## Fixtures

- [`ajustar-regra`](fixtures/ajustar-regra/README.md): a mudança de `revisar-regra`. O relatório traz só o achado 1, o N+1 do Aprovador, com `Regra:` `Model::preventLazyLoading()`. Na variante `antigos`, a base tem 3 N+1 em outras relações, cada um com um teste de 2 registros.
- [`ajustar-feedback`](fixtures/ajustar-feedback/README.md): o estorno pela lista com `DB::transaction()` no componente Livewire; o relatório tem `Veredito: pode entregar.`; o `phpunit.xml` só tem a suíte `Feature`. Na variante `antiga`, a base tem `App\Livewire\Clientes\Saldo`, que lê com `DB::table()`.

## Método

- **Casos 1 e 2 (`ajustar-regra`, `limpa` e `antigos`):** o executor fez a seleção (achado 1), conferiu a branch e o trecho, formou o Lote A e mandou o contrato da seção 4, com o achado e o campo `Regra:` copiados do relatório. O Ajustador: subagente geral novo com o modelo `sonnet`, o corpo do template, o caminho do SKILL.md, do perfil e das 4 disciplinas, sem o agente registrado. O caso mede o retorno do Ajustador (passo 5.8), não o relatório do principal.
- **Casos 3 e 4 (`ajustar-feedback`, `sem-antiga` e `antiga`):** o principal foi um subagente geral novo, com o modelo da sessão, que recebeu só o pedido do usuário, o SKILL.md e a pasta. Sem ferramenta de subagente, ele corrigiu o Lote no próprio contexto, como a seção 4.5 manda. O caso mede o registro do achado `H1`, as 3 condições, a correção e o relatório da seção 6.7.
- **Pedido dos casos 3 e 4:** “/ajustar: não use `DB::` em componente Livewire; a escrita com transação vai numa Action de `App\Actions`, como `FecharDia`. Sem commits.”
- **Conferência do executor:** `git status`, o diff, o Pest completo e a busca de marcadores em cada pasta depois do retorno.
- **Desvio do contrato:** os 4 prompts diziam que o projeto não tem `docs/agents/projeto.md`, mas o app de `revisar-executavel` o tem. Os principais dos casos 3 e 4 o leram e registraram a divergência. Os comandos do arquivo são os do prompt.

## Resultado

### Caso 1: regra que entra no Lote (`limpa`)

| Critério | Resultado |
|---|---|
| Corrige com `with()` | passou. `app/Livewire/Pedidos/Lista.php:18` com `with(['cliente.user', 'aprovador'])`. |
| Escreve a trava com a mensagem da correção | passou. `Model::preventLazyLoading(! $this->app->isProduction())` e `handleLazyLoadingViolationUsing()`, que lança `LogicException` com a mensagem do campo. |
| RED da trava no código com o defeito, com o alvo proibido e o `arquivo:linha` do achado | passou. 3 testes falharam com `Carregamento preguiçoso de [aprovador] em [App\Models\Pedido]. Acrescente [aprovador] ao with() da consulta que carregou a lista.`, "(lista.blade.php:9, Lista.php:18, do achado)". |
| GREEN e suíte completa verde com a trava | passou. Conferido pelo executor: `9 passed (14 assertions)`; `phpunit.xml` sem alteração. |
| Linha `Regra do achado 1:` | passou. `Regra do achado 1: app/Providers/AppServiceProvider.php (...). RED: ... GREEN: passou depois da correção. Repositório: verde (...)`. |
| Nada em `Regras propostas:` | passou. `Regras propostas: nenhuma.` |

- Além do pedido: o Ajustador escreveu `tests/Feature/CarregamentoPreguicosoTest.php`, que exige a exceção com a mensagem exata, e rodou a mutação no provider.
- Achado novo: o `cliente.user` do `with()` não tem leitor na view. Ele não o corrigiu.
- **Custo:** 101 mil tokens, 2,2 min.

### Caso 2: regra com ocorrências antigas (`antigos`)

| Critério | Resultado |
|---|---|
| Corrige o achado 1 com RED e GREEN | passou. RED `Failed asserting that 203 is identical to 5.` e `Attempted to lazy load [aprovador]`; GREEN nos 2 testes da prova. |
| A trava deixa a suíte vermelha nos 3 testes antigos, e o Ajustador a retira | passou. "Com a correção do achado aplicada, a suíte completa fica com 3 testes vermelhos [...]. Eu a escrevi em app/Providers/AppServiceProvider.php e a desfiz com `git checkout`." O executor conferiu o provider igual à base. |
| Não corrige os 3 N+1 antigos nem acrescenta exceção | passou. O diff só tem `Lista.php:18` e a prova; nenhum `->ignoring(` nem `@phpstan-ignore`. |
| `Regras propostas:` com o esboço, a mensagem e as 3 ocorrências com `arquivo:linha` | passou. `Motivo: ocorrências antigas`; a mensagem; `app/Actions/ExportarPedidos.php:24`, `app/Console/Commands/ResumoClientes.php:19` e `app/Actions/SaldosBaixos.php:22`, com a relação e o teste que quebra; o esboço em PHP. |
| Sem linha `Regra do achado 1:` | passou. "Regra do achado 1: NÃO entrou no Lote." A linha existe, mas diz que a regra está em `Regras propostas:`; o formato da seção 5 não prevê esse uso. |

- O Ajustador usou `git stash` na pasta da fixture para refazer o RED sem a correção. A skill não proíbe.
- **Custo:** 98 mil tokens, 1,3 min.

### Caso 3: correção do humano, sem ocorrência antiga (`sem-antiga`)

| Critério | Resultado |
|---|---|
| Registra a correção como achado `H1` e confere as 3 condições | passou. A seleção mostra `H1`, o caso concreto, os locais `Lista.php:10` e `:21-24` e as 3 condições, uma a uma. |
| Move a escrita para uma Action | passou. `App\Actions\EstornarPedido`, com teste na Costura; `Lista::estornar` mantém a assinatura e o `abort_unless`. |
| RED do teste no código do diff, com `Illuminate\Support\Facades\DB` na saída, e GREEN | passou. `Expecting 'App\Livewire' not to use 'Illuminate\Support\Facades\DB'.`, "O local é `app/Livewire/Pedidos/Lista.php:10,21`, do achado". |
| O teste entra num diretório de suíte que já roda, sem alterar o `phpunit.xml` | passou. `tests/Feature/ArchTest.php`, "porque o `phpunit.xml` só tem a suíte Feature". Conferido: `phpunit.xml` igual; `7 passed (12 assertions)`. |
| Linha `Regra do achado H1:` no relatório | passou. `Regra do achado H1: tests/Feature/ArchTest.php`, com RED, GREEN e "Repositório: verde". |

- Achado novo `[inferred]`: o estorno em dobro com 2 requisições ao mesmo tempo, sem `lockForUpdate()`. O principal ofereceu `/depurar` e não o corrigiu.
- **Custo:** 109 mil tokens, 3,4 min.

### Caso 4: correção do humano, com ocorrência antiga (`antiga`)

| Critério | Resultado |
|---|---|
| `H1` com as 3 condições e a escrita movida para uma Action | passou. Condição 2: "`Saldo.php` fica fora do diff e conta como ocorrência antiga." |
| RED do teste no código do diff | passou. A mesma saída, com `Lista.php:21` do achado. |
| O teste fica fora do Lote | passou. "Nenhuma regra entrou no Lote." O executor conferiu: sem `ArchTest.php`; `8 passed (16 assertions)`. |
| `Regras propostas:` lista o componente com `arquivo:linha` | passou. `app/Livewire/Clientes/Saldo.php:9` e `:18`, com o motivo, a mensagem, o esboço e o lugar (`tests/Feature/ArchTest.php`, sem `phpunit.xml`). |
| Nenhum `->ignoring(` e o componente antigo sem correção | passou. `Saldo.php` sem alteração. |

- O principal notou que `Saldo` lê com `DB::` e não grava, e sugeriu outra mensagem para a regra. Ele fez a pergunta A/B/C sobre a regra proposta.
- **Custo:** 113 mil tokens, 3,8 min.

## Decisão de texto: `tests/Arch/` só com a suíte

A Spec rfl-designer/forja#19 põe o teste Pest arch em `tests/Arch/`. Um arquivo nesse diretório só roda se o `phpunit.xml` tem a suíte, e alterar o `phpunit.xml` mexe na configuração dos verificadores. O perfil Laravel de `/ajustar` manda pôr o teste em `tests/Arch/` só com a suíte já presente; senão, no diretório de uma suíte que já roda, como `tests/Unit/ArchTest.php` ou `tests/Feature/ArchTest.php`; sem esse diretório, a regra vai para `Regras propostas:`. Os casos 3 e 4 exercitaram o 2º caminho.

## Limites

- 1 execução por caso, sem comparação com `bcead5a`.
- Nos casos 1 e 2, o executor fez o papel do principal: o relatório da seção 6.7 não foi medido ali. Nos casos 3 e 4, o principal fez o Lote sem subagente; o contrato do template não foi medido ali.
- A prova do achado em `ajustar-regra/provas/` termina com `->throwsNoExceptions()` e sai como "risky". Os 2 Ajustadores acrescentaram uma asserção ao copiá-la.
- As fixtures favorecem o caminho certo: a trava pega o N+1 do achado, e o teste de arquitetura pega o `DB::`. Nenhum caso mede a opção do Larastan, que vai sempre para `Regras propostas:`.
- O executor escreveu a versão avaliada e as fixtures.

## Conclusão

- Os 4 casos passaram na 1ª execução.
- **Ajuste de texto depois da execução:** no caso 2, o Ajustador escreveu "Regra do achado 1: NÃO entrou no Lote". Um leitor que procura a linha `Regra do achado N:` pode tomá-la como a regra no Lote. A seção 6.7 e o template agora dizem que só a regra no Lote tem essa linha. O caso 2 não rodou de novo com esse texto.
- **Não medido:** a forja (forja#22), a opção do Larastan e o relatório do principal com um Ajustador delegado.
