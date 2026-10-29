# Mapeadores

Um Mapeador é um subagente que mapeia um Domínio. O agente principal coordena: faz o inventário, escreve o README raiz, delega e reconcilia. O Mapeador lê o código do seu Domínio e devolve um resultado curto.

## Regras

- Delegue um Domínio por Mapeador.
- Use até 4 Mapeadores ao mesmo tempo. Com mais Domínios, delegue em ondas.
- Passe ponteiros, não o histórico do chat. O Mapeador lê os arquivos pelos caminhos recebidos.
- O Mapeador não conduz o app, não roda migrations, seeders, filas ou serviços externos e não cria subagentes. Ele usa git só para leitura, como `git log` e `git blame`.
- O Mapeador usa as convenções do README raiz: autenticação, sessões e comando base. Uma convenção que falta volta como dúvida; ele não cria outra.
- No modo Criar, o Mapeador grava só na pasta do seu Domínio. No modo Auditar, ele não grava arquivos.
- O agente principal grava o README raiz, `jornadas.md` e a linha `Base:`. Ele também decide cada correção.

## Contrato no modo Criar

Envie a cada Mapeador:

1. Domínio: nome, descrição e pasta exclusiva, como `docs/features/vendas/`.
2. Inventário: caminhos de `dominios.md`, `ancoras.txt` e `rotas.json`, e as Âncoras deste Domínio.
3. Caminhos de leitura: README raiz já gravado, [formato](formato.md), [exemplo](exemplo/README.md), configuração do projeto, glossário e `ste100-clean-code`.
4. Fronteira com outros Domínios: as Âncoras que pertencem a outro Mapeador.
5. Índice do Domínio: na aplicação grande, grave também `<dominio>/README.md`. Na pequena, devolva só as linhas do índice; o principal as grava no README raiz.
6. Formato de retorno, abaixo.

O Mapeador:

1. Lê rotas, componentes, views, Policies, testes e textos visíveis do Domínio.
2. Grava um Arquivo de Feature por Feature, no formato do contrato.
3. Escreve `Estado: não conduzida em <data>, commit <sha>; receita derivada do código`.
4. Marca com `[inferred]` uma entrada ou um resultado sem prova no código.
5. Descreve o comportamento atual. Lista em `Dúvidas` cada comportamento que parece defeito, com o caso concreto e `arquivo:linha`.
6. Cobre cada Âncora do Domínio com uma Feature, ou a propõe para `Fora do mapa` com o motivo.

## Contrato no modo Auditar

Envie o Domínio, os Arquivos de Feature do Domínio, a Base do mapa, o inventário atual e os mesmos caminhos de leitura. Para cada Feature, o Mapeador compara o arquivo com o código atual. Ele não grava arquivos.

## Retorno

Peça um retorno curto, sem o conteúdo dos arquivos:

```markdown
Domínio: vendas
Arquivos: vendas/README.md, vendas/pedidos.md, vendas/devolucoes.md
Features:
- [Pedidos](pedidos.md): carrinho, checkout, lista, cancelamento e fechamento diário.
Fora do mapa proposto:
- `rota:webhooks.pix`: entrada do gateway, sem tela; motivo.
Âncoras de outro Domínio: `livewire:conta.endereco` (conta).
Jornadas candidatas: checkout com login expirado (conta + vendas).
Pré-condições ausentes no seed: pedido entregue para o cliente de teste.
Deriva (só Auditar): pedidos.md, Sub-feature `pedidos-cancelar`: o botão agora é `Cancelar pedido` (resources/views/livewire/pedidos/tabela.blade.php:42).
Dúvidas: o que o código não responde.
```

Um retorno sem a lista de arquivos, sem cobertura das Âncoras ou com escrita fora da pasta não conclui o Domínio. Retome o mesmo Mapeador com a pendência.

## No Claude Code

Use o agente customizado `mapeador`, com `model: claude-sonnet-5-5` e `effort: medium`. O principal mantém o próprio modelo.

1. Copie o [template](../assets/mapeador.md) para `.claude/agents/mapeador.md` na raiz do projeto consumidor. Se o arquivo já existe, preserve as customizações.
2. Instale `ste100-clean-code` para o Claude Code. O campo `skills` do template pré-carrega essa skill.
3. Delegue com `subagent_type: mapeador`, sem override de modelo. Envie vários Mapeadores na mesma mensagem para rodarem em paralelo.
4. Confira o modelo e o esforço efetivos em `/tasks`. `CLAUDE_CODE_EFFORT_LEVEL` e políticas de modelo podem substituir o template. Se o resultado diverge, informe a causa; não declare Sonnet 5.5 medium sem confirmação.
5. Sem o agente registrado, use o subagente geral com o mesmo contrato. Informe que ele herda o modelo do principal. Criar o primeiro diretório de agentes durante a sessão pode exigir reiniciar o Claude Code.

## Em outros ambientes

Use o mecanismo de subagentes e os modelos autorizados do ambiente. Não traduza IDs da Anthropic para outro provedor. Sem subagentes, mapeie um Domínio por vez no agente principal. Grave o Domínio antes de começar o próximo e informe a limitação.

Fonte: [subagentes do Claude Code](https://code.claude.com/docs/en/sub-agents).
