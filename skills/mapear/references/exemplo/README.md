# Mapa de Features da Loja

Inventário de comportamento da Loja, uma aplicação fictícia em Laravel e Livewire. Os agentes usam este mapa para escolher o que conduzir e que prova vale. As pessoas o usam como checklist de regressão.

Base: commit 3f9c2ab em 2026-10-28

## Pré-condições base

- Inicie o app com `composer run dev`. A URL local é `http://loja.test`.
- Faça o diagnóstico antes da primeira condução e depois de cada falha:
  - `php artisan tinker --execute='echo DB::connection()->getDatabaseName();'` mostra `loja_local`, o banco da linha `Banco da condução` na configuração.
  - `curl -fsS http://loja.test/up` responde com sucesso.
  - `php artisan migrate:status` não mostra migration pendente.
  - `public/hot` existe, ou `npm run build` rodou depois da última mudança em `resources/`.
  - `git rev-parse --short HEAD` mostra o commit sob prova.
- Prepare os dados com `php artisan migrate:fresh --seed`, só depois do diagnóstico do banco. O comando apaga todas as tabelas. O seed cria o usuário `cliente@loja.test` e três produtos.
- Nos probes Pest, autentique com `actingAs()`. A senha do seed fica no `DatabaseSeeder`; não a copie para o mapa.
- O Mailpit local recebe os e-mails em `http://localhost:8025`.
- No app local, rode `php artisan queue:work --once` depois de uma ação que enfileira trabalho.

## Convenções de condução

- Prefira papel ARIA e nome acessível. Depois, use o atributo `dusk`. Use classe CSS só como último recurso.
- Depois de uma ação Livewire, espere o estado final visível. Não use espera fixa.
- Conduza pela tela, pelo comando ou pela rota que o usuário usa. Use `php artisan tinker` só para ler o efeito depois da ação.
- Conduza só no banco da linha `Banco da condução`. `APP_ENV=local` não prova que o banco é local.
- Para uma variante com flag, ative a flag antes e desative-a no fim.

## Prova e lacunas

- O Arquivo de Feature define o conjunto de cobertura da mudança. Para uma mudança entre Features, leia também as [jornadas](jornadas.md).
- Exercite cada entrada, modo e flag ativa que a mudança afeta. Inclua sucesso, cancelamento, erro, vazio e persistência.
- Registre a ação e o estado final observável na mesma prova.
- Confira o efeito, não só a tela: linha no banco, e-mail no Mailpit, arquivo em `storage/` ou recarga da página.
- Um fake vale só na fronteira de um serviço externo, por exemplo `Http::fake()` para o gateway de pagamento.
- Para um caminho inalcançável, diga o caminho e o bloqueio: conta, permissão, serviço externo ou sistema operacional. Conduza o caminho real mais próximo.
- Guarde as provas em `docs/verification/evidencias/`, sem segredos.

## Varredura completa

Para uma regressão ampla, siga os Domínios de cima para baixo. Termine com as [jornadas entre Features](jornadas.md).

## Domínios

### Conta

- [Acesso](conta/acesso.md): login, logout, recuperação de senha e bloqueio por tentativas.

### Vendas

- [Pedidos](vendas/pedidos.md): carrinho, checkout, lista de pedidos, cancelamento e fechamento diário.

## Fora do mapa

- `rota:POST /webhooks/gateway`: entrada do gateway de pagamento, sem tela; os testes de webhook a cobrem.
- `comando:inspire`: comando de exemplo do esqueleto Laravel.
- `comando:loja:limpar-miniaturas`: manutenção interna, sem efeito visível.

## Contrato dos Arquivos de Feature

Cada Arquivo de Feature começa com um título H1 e um parágrafo sobre o comportamento visível. Depois vêm a linha `Âncoras:` e a linha `Estado:`. Depois vêm exatamente estas H2, nesta ordem:

1. `Sub-features`: um ID `kebab-case` e uma linha por comportamento.
2. `Como chegar (visão do usuário)`: cada entrada do usuário.
3. `Como conduzir`: começa com `Pré-condições:`. Cada item liga uma ação a um comando exato e a um resultado observável.
4. `Armadilhas`: o que invalida ou atrasa uma condução.

Não descreva implementação. Nomeie só caminhos do usuário, identificadores estáveis, estado necessário, comandos e prova observável.

## Manutenção

- Atualize o Arquivo de Feature no mesmo diff da mudança de comportamento visível.
- Uma Feature nova recebe um arquivo e uma linha neste índice. Uma Feature removida perde os dois.
- Uma Âncora nova vai para uma Feature ou para `Fora do mapa`.
- Depois de conduzir, atualize a linha `Estado:` com a data e o commit. `/conduzir` conduz uma Feature, um Domínio ou o mapa inteiro.
- Só `/mapear` atualiza a linha `Base:`, depois de reconciliar todo o código até esse commit.
- Antes de entregar, rode o `scripts/conferir-mapa.php` da skill `mapear` sobre esta pasta.
