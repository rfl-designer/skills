# Execução de `/mapear` num app real

Data: 28/10/2026. Candidato: a skill `mapear` no working tree desta sessão. Executor: o próprio autor da skill, no papel de agente principal. Por isso, esta execução não é uma avaliação independente; ela prova que as instruções rodam, não que outro agente as segue sem ajuda.

## Fixture

App Laravel 13.39 com Livewire 3.8 e SQLite, criado só para o teste e não versionado neste pacote. Três Domínios:

- `conta`: login Livewire com bloqueio por tentativas e logout.
- `estoque`: catálogo com busca, cadastro de produto com Policy e comando agendado de alerta por e-mail.
- `vendas`: compra por rota POST, lista Livewire com filtro e cancelamento com `wire:confirm`, comando agendado de fechamento diário.

A configuração do projeto não tinha a linha do Mapa de Features. O esqueleto tinha um Form object Livewire e o comando `inspire`.

## Execução

| Passo | Resultado |
|---|---|
| Inventário | Os comandos de `references/inventario.md` rodaram como escritos e geraram 20 Âncoras. O Form object ficou fora. `/up` não aparece com `--except-vendor`. |
| Tamanho | 3 Domínios e 6 Features: aplicação pequena pelo critério. A delegação veio de um pedido da sessão, para testar o caminho dos Mapeadores. |
| Mapeadores | 3 subagentes gerais com modelo Sonnet, em paralelo, com o texto do template e o contrato. O agente `mapeador` não estava registrado. Cada um levou de 7 a 9 minutos e de 150 a 180 mil tokens. Os três gravaram só a própria pasta e devolveram o formato pedido. |
| Reconciliação | O conferidor com `--ancoras` só acusou a falta da linha `Base:`. O principal unificou a variável da senha e gravou índice, `Fora do mapa` e `jornadas.md`. |
| Condução | Playwright conduziu Acesso, Catálogo e Pedidos por inteiro: 30 itens (11, 5 e 14). 28 deram o resultado escrito. |
| Registro | `Base:`, linha de destino na configuração e conferidor final: `OK: 6 Arquivos de Feature, 38 Sub-features, 19 Âncoras; inventário: 20 itens cobertos`. `git status` mostrou só o mapa, a configuração e as evidências. |

## Falhas encontradas pela condução

- **Lacuna de condução:** em Pedidos, o texto pedia "compre de novo", mas o comando não comprava. Sem pedido pendente, o clique esperava até o tempo limite.
- **Deriva:** o Mapeador inferiu `419` para a compra com sessão apagada. O app respondeu `302` para o login, porque o Laravel 13 aceita a origem do próprio site sem token CSRF.

As duas receitas corrigidas rodaram de novo a partir do arquivo antes da linha `Estado: conduzida`. As outras três Features ficaram `não conduzida`.

## Mudanças na skill depois da execução

- O principal define no README raiz, antes de delegar, a autenticação na condução e o comando base. Dois Mapeadores usaram `LOJA_SENHA` e um usou `SENHA_SEED`.
- O formato pede um comando base. Cada item de Pedidos repetia o mesmo código Playwright.
- Os Mapeadores podem usar git só para leitura. Os três rodaram `git log` apesar da proibição.
- O principal reporta ao usuário os comportamentos suspeitos dos retornos. Os Mapeadores acharam casos plausíveis de defeito: slug repetido sem validação, estoque negativo sem mensagem e bloqueio de login só por e-mail.
- `references/inventario.md` ganhou os comandos de comandos Artisan e de notificações. O exemplo deixou de listar rotas que `--except-vendor` omite.

Não houve execução dos modos Atualizar e Auditar, nem de uma aplicação grande pelo critério real.
