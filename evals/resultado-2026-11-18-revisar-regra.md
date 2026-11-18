# Avaliação de `/revisar`: `Regra:` no achado

Data: 18/11/2026. Base do pacote: `bcead5a`. Versão avaliada: `skills/revisar/SKILL.md` com a etapa 5.9, sem commit (4.918 palavras; 4.670 em `bcead5a`, +5%), e o perfil Laravel com os mecanismos de `Regra:`. Executor: o autor da versão, que montou a fixture, fez a etapa 1 e despachou os agentes. Os 2 revisores e o agente principal foram subagentes gerais novos, sem o histórico da sessão, sem o gabarito e sem `evals/cenarios.md`.

Esta avaliação mede a Consolidação (etapa 5, com a 5.9) e o relatório (etapa 6), que o principal executa, e confere que o revisor não escreve `Regra:`. Ela não compara com a versão anterior: em `bcead5a` o campo não existe. Ela não mede as etapas 7 e 8, as rodadas seguintes nem `/ajustar`.

Casos de [`cenarios.md`](cenarios.md): "Revisão: regra para o N+1" e "Revisão: caso de borda sem regra". Os 2 rodaram na mesma execução, com o mesmo diff.

## Fixture

[`revisar-regra`](fixtures/revisar-regra/README.md): o comando `pedidos:aprovar` grava o Gerente que pediu, e a lista do Gerente mostra quem aprovou e quando. O app é o de `revisar-executavel`, com Pest em sqlite `:memory:` e `AppServiceProvider` sem travas do Eloquent.

| Defeito plantado | Caso concreto | `Regra:` esperada |
|---|---|---|
| R1. N+1 do Aprovador | A lista do Gerente lê `aprovador` sem `with()` | `Model::preventLazyLoading()` no `AppServiceProvider` |
| R2. Fuso da Aprovação | Aprovação às 01:30 UTC aparece com o dia seguinte; a Spec pede `America/Sao_Paulo` | nenhuma |

## Método

- **Execuções:** 1 revisor por eixo e 1 principal, cada um 1 vez.
- **Etapa 1, pelo executor:** a guarda (`phpunit.xml` com sqlite `:memory:`, e-mail `array`, fila `sync`), o portão na head (Pint aprovado, Pest com 5 testes verdes) e as 4 worktrees com `git worktree add --detach` e `vendor/` com links físicos.
- **Revisores:** o contrato da seção 4 sem o agente `revisor` registrado, com o corpo do template, o caminho do SKILL.md, o perfil, o eixo e os Ponteiros de Contexto. Ferramentas pedidas: Read, Grep, Glob e Bash.
- **Principal:** um subagente novo recebeu o SKILL.md, o perfil, as 4 worktrees e os 2 relatórios dos revisores, e executou as etapas 5 e 6. Ele não tinha subagentes e cobriu as lacunas ele mesmo, como a etapa 5.3 permite. Desvio combinado na etapa 5.8: ele copiou as provas e não removeu as worktrees; o executor as removeu depois.
- **Produção intacta:** antes e depois, o `md5` de cada arquivo de cada worktree, sem `vendor/`, `storage/` e `.git`.
- **Modelo:** os subagentes herdaram o modelo da sessão principal.

## Resultado

| Critério | Resultado |
|---|---|
| R1 com a Prova executada | passou. `AprovadorNMais1Test.php` imprime `consultas com 2 Pedidos: 5; com 200 Pedidos: 203` e `Attempted to lazy load [aprovador] on model [App\Models\Pedido]`. A Reexecução na worktree limpa confirmou. Na base, a mesma contagem pelo caminho que já existia dá `3` e `3`. |
| R1 com `Regra:` e `Model::preventLazyLoading()` | passou. `- **Regra:** Model::preventLazyLoading(! $this->app->isProduction()) no AppServiceProvider::boot()`, o que ela proíbe e a mensagem com a correção por `Model::handleLazyLoadingViolationUsing()`: "Carregamento preguiçoso de [aprovador] em [App\Models\Pedido]. Acrescente [aprovador] ao with() da consulta que carregou a lista." |
| Condição 2 de R1 conferida | passou, além do que a skill pede. A skill pede a busca; o principal executou numa cópia: com a trava e a correção, `11 passed (23 assertions)`; sem a correção, a mensagem aparece. |
| R2 com a Prova executada | passou. `AprovadoEmForaDoFusoDaLojaTest.php` imprime `-'10/03/2026 22:30' +'11/03/2026 01:30'`. |
| R2 sem `Regra:` | passou. Nas notas da 5.9: "Os achados 2, 3 e 4 não têm um detector determinístico sem executar o caso, então não têm `Regra:`." Nenhuma regra contra `now()`, `today()` ou `format()`. |
| Só o principal escreve `Regra:` | passou. Os 2 relatórios dos revisores não têm o campo. |

Outros achados do relatório, sem `Regra:`: 3, faltam 2 testes do Plano de Testes da Spec, provado por mutação; 4, nenhum teste falha sem o filtro de papel do comando, nota de um revisor que o principal provou por mutação. Descartado na Reexecução: os títulos "Aprovado por" e "Aprovado em", porque a tabela da base não tem `<th>`, com a pergunta ao usuário. `Da base:` a janela das 23h59 de `FecharDia`, provada na limpa e na base. `Não verificado:` a corrida entre 2 execuções do comando.

- **Contrato:** o `md5` da produção das 4 worktrees ficou igual. Desvio: o revisor Standards deixou `AprovarPedido.php.bak` e `Lista.php.bak` fora da sua worktree, iguais ao alvo, depois de uma mutação que ele desfez. O principal rodou os 2 scripts de mutação em cópias descartáveis, para não editar a produção das worktrees.
- **Custo:** revisor Standards 97 mil tokens, 2,7 min; revisor Spec 93 mil, 2,4 min; principal 148 mil, 9,2 min.

## Limites

- 1 execução. Uma repetição pode escrever `Regra:` em outro achado.
- A fixture favorece a regra: o mecanismo 1 do perfil é a trava que pega R1.
- Os exemplos do campo na skill e no perfil usam outra classe de erro, o atributo descartado em silêncio, para não dar a resposta. O perfil ainda nomeia `preventLazyLoading()` como primeiro mecanismo.
- O executor escreveu a versão avaliada e a fixture.

## Conclusão

- Os 2 casos passaram na 1ª execução.
- O principal provou a condição 2 por execução, além da busca que a skill pede. A skill não exige isso; o custo foi parte dos 9 min do principal.
- **Não medido:** o efeito em `/ajustar` (ticket skills#24) e a forja.
