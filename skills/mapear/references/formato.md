# Formato do Mapa de Features

O [exemplo](exemplo/README.md) mostra uma aplicação pequena com dois Domínios. Os nomes e comandos do exemplo são fictícios; copie a forma, não os valores.

## Estrutura de pastas

```text
docs/features/                 # destino configurado do Mapa de Features
  README.md                    # índice, pré-condições base, convenções, prova, manutenção
  jornadas.md                  # jornadas que passam por várias Features
  <dominio>/
    README.md                  # só em aplicação grande: índice do Domínio
    <feature>.md               # um Arquivo de Feature por área de comportamento
```

- Dê a cada Domínio uma pasta, também na aplicação pequena. Assim, cada Mapeador grava numa pasta exclusiva.
- Use nomes `kebab-case` em português, com os termos do glossário: `vendas/pedidos.md`, não `sales/OrderController.md`.
- Na aplicação pequena, o README raiz lista cada Feature. Na aplicação grande, ele lista cada Domínio com um link para `<dominio>/README.md`, e esse arquivo lista as Features do Domínio.

## README raiz

Comece com o título `# Mapa de Features de <App>` e um parágrafo sobre o uso do mapa. Antes da primeira H2, escreva a linha `Base: commit <sha> em AAAA-MM-DD`. A Base é o último commit que `/mapear` reconciliou por inteiro com o código.

Depois, use estas H2. O conferidor exige todas:

1. `Pré-condições base`: como iniciar o app, URL, dados de seed, autenticação na condução, e-mail, fila e isolamento. Inclua o **Diagnóstico**: os comandos que provam que a instância merece condução. Por exemplo, health check, migrations em dia, assets atualizados e commit sob prova.
2. `Convenções de condução`: o comando base da ferramenta, seletores preferidos, espera pelo estado final, uso de `tinker` só para ler efeitos, ambiente permitido e flags.
3. `Prova e lacunas`: o padrão de prova e como registrar um caminho inalcançável.
4. `Varredura completa`: a ordem de uma regressão ampla. Termine com o link para `jornadas.md`.
5. `Domínios`: uma H3 por Domínio com uma linha por Feature, ou uma linha por Domínio na aplicação grande.
6. `Fora do mapa`: cada Âncora do inventário que não pertence a uma Feature, com o motivo. Por exemplo, health check, rota de infraestrutura ou comando interno.
7. `Contrato dos Arquivos de Feature`: o contrato abaixo, em poucas linhas, para o agente que não tem esta skill.
8. `Manutenção`: as regras de atualização no mesmo diff, de `Estado:` e de `Base:`.

Escreva as pré-condições comuns uma vez, no README raiz. Um Arquivo de Feature repete só o que muda.

- **Autenticação na condução:** nomeie a variável de ambiente que guarda a senha de teste, ou o arquivo de sessão gravada. A senha nunca vai para o mapa.
- **Comando base:** se a ferramenta repete código em cada item, como abrir o navegador e carregar a sessão, defina esse código uma vez. Pode ser um comando no README ou um script curto na pasta do mapa, com o uso documentado. Cada item usa só a parte que muda.

## README de Domínio (aplicação grande)

Comece com `# <Domínio>` e um parágrafo sobre a área de negócio. Depois, use `## Pré-condições do Domínio` para o que vale em todas as suas Features, como papel do usuário ou flag. Termine com `## Features`, uma linha por Feature: `- [Nome](arquivo.md): o que o usuário faz.`

## Arquivo de Feature

```markdown
# <Feature>

<Um parágrafo: o comportamento visível, na voz do usuário.>

Âncoras: `rota:pedidos.*`, `livewire:pedidos.tabela`, `comando:pedidos:fechar-dia`
Estado: não conduzida em 2026-10-28, commit 3f9c2ab; receita derivada do código

## Sub-features

- `pedidos-cancelar`: cancela um pedido pendente depois de uma confirmação.

## Como chegar (visão do usuário)

- Escolha `Cancelar` na linha de um pedido pendente em `Meus pedidos`.

## Como conduzir

Pré-condições:

- <estado necessário além das pré-condições base>

- **<Rótulo>.** Ação: <o que o usuário faz>. Conduza: `<comando exato>`. Resultado: <estado observável>.

## Armadilhas

- <o que invalida ou atrasa uma condução>
```

- **Sub-features:** cada item começa com um ID `kebab-case` entre crases, com o nome da Feature como prefixo. O ID é único no mapa inteiro.
- **Como chegar:** liste cada entrada do usuário: menu, botão, URL, atalho, comando Artisan, endpoint de API, link de e-mail e agenda. Uma entrada ausente aqui fica sem prova.
- **Como conduzir:** comece com `Pré-condições:`. Cada item tem um rótulo e liga ação, comando e resultado. Use a ferramenta de navegador registrada na configuração. Inclua o caminho de sucesso, cancelamento, erro, vazio e persistência que existir. Termine com **Regressão** (testes Pest existentes) e **Prova** (o que capturar).
- **Armadilhas:** estado que o seed não cria, espera assíncrona, fuso horário, cache, fila, flag e caminho que exige ação manual.
- **Divida** a Feature quando uma parte exige pré-condições próprias ou quando passa de 10 Sub-features.
- **Junte** comportamentos pequenos e sem pré-condição própria num arquivo `outros.md` do Domínio.

Não escreva caminho de arquivo de produção, nome de classe interna ou passo a passo do código. A exceção são as Âncoras e os testes de regressão.

## Âncoras

Uma Âncora liga a Feature a um identificador estável do código. Com ela, um agente encontra a Feature de um diff: `rg 'livewire:pedidos.tabela' docs/features`. Cada Âncora pertence a uma só Feature ou à seção `Fora do mapa`.

| Prefixo | Identificador | Fonte no inventário |
| --- | --- | --- |
| `rota:` | nome da rota; sem nome, `MÉTODO /uri` | `php artisan route:list` |
| `livewire:` | nome do componente, como `pedidos.tabela` | componentes Livewire e Volt |
| `comando:` | nome do comando Artisan, sem argumentos | comandos da aplicação |
| `agenda:` | comando ou classe agendada | `php artisan schedule:list` |
| `notificacao:` | nome curto da classe de Notification ou Mailable | notificações e e-mails |
| `flag:` | nome da flag | definições de flag, como Laravel Pennant |
| `outro:` | descrição curta de outra entrada | registro manual; o conferidor não cruza com o inventário |

- Um `*` no fim cobre todos os identificadores com o mesmo início: `rota:pedidos.*`.
- Use o `*` só quando a Feature tem todas essas rotas. Uma rota de outra Feature com o mesmo início exige Âncoras exatas.

## Linha Estado

`Estado: <valor> em AAAA-MM-DD, commit <sha>[; detalhe]`

| Valor | Significado |
| --- | --- |
| `conduzida` | Um agente conduziu cada entrada listada nesse commit e viu o resultado descrito. |
| `parcial` | Um agente conduziu parte das entradas. O detalhe lista as não conduzidas. |
| `não conduzida` | A receita vem só da leitura do código. |
| `bloqueada` | Um agente tentou e uma pré-condição impediu. O detalhe diz qual. |

Um defeito do produto não muda o Estado. O agente o reporta ao usuário. O mapa continua com o comportamento esperado.

## jornadas.md

Comece com `# Jornadas entre Features` e um link para o README raiz. Use uma H2 por jornada. Cada jornada lista as Features envolvidas, os passos e o resultado observável. Inclua isolamento entre sessões ou usuários, efeitos que passam por fila ou e-mail e atalhos globais. Sem jornada, grave só o título, o link e a frase `Nenhuma jornada mapeada.`

## Conferidor

Rode o conferidor sobre a pasta do mapa. Ele exige PHP 8.1 ou mais novo:

```bash
php <pasta-desta-skill>/scripts/conferir-mapa.php docs/features
php <pasta-desta-skill>/scripts/conferir-mapa.php docs/features --ancoras=<inventario>.txt
```

Ele confere links e arquivos fora do índice, as H2 e sua ordem, as linhas `Base:`, `Âncoras:` e `Estado:`, IDs únicos e Âncoras repetidas. Com `--ancoras`, ele também confere a cobertura do inventário e as Âncoras que não existem mais no código. O inventário tem uma Âncora por linha; linhas vazias e linhas com `#` no início ficam fora.
