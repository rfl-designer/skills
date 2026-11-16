# Inventário da aplicação

O inventário lista as entradas que o usuário alcança e as agrupa em Domínios. O agente principal faz o inventário uma vez e passa os arquivos aos Mapeadores. Use só comandos de leitura. Confira cada comando com `--help` na versão instalada; não invente opção ausente.

Este arquivo não assume linguagem nem framework. Em Laravel, o [inventário Laravel](inventario-laravel.md) dá o comando de cada fonte. Em outra stack, use o comando de listagem do framework quando ele existe; sem comando, leia o código.

## Pasta do inventário

Grave o inventário numa pasta temporária fora do repositório:

```bash
INV="$(mktemp -d)"
```

Arquivos esperados:

- `rotas.json`: a saída bruta da listagem de rotas, quando o framework tem esse comando.
- `ancoras.txt`: uma Âncora por linha, para o conferidor.
- `dominios.md`: proposta de Domínios, com as Âncoras e as Features estimadas de cada um.

Não copie arquivos de ambiente nem segredos para o inventário. Registre só nomes de variáveis.

## Fontes, em ordem

Use o executor e o diretório de execução da configuração.

1. **Rotas.** Liste as rotas da aplicação: páginas, API e webhooks. Grave `rota:<nome>`; sem nome, `rota:<MÉTODO> /<uri>`. Omita as rotas do framework e dos pacotes, como o health check; elas não precisam de Feature.
2. **Componentes de UI.** Liste os componentes com estado e ações próprias que o usuário alcança dentro de uma página. Grave `componente:<nome estável do componente>`. Um componente só de apresentação fica fora.
3. **Comandos.** Liste os comandos de linha de comando da aplicação. Grave `comando:<nome>`, sem argumentos.
4. **Agenda.** Liste as tarefas agendadas. Grave `agenda:<comando ou classe>`.
5. **Notificações e e-mails.** Liste cada mensagem que a aplicação envia. Grave `notificacao:<Nome>`. Acrescente à mão uma notificação do framework que a aplicação usa, como a de troca de senha.
6. **Flags.** Procure as definições do sistema de flags do projeto. Grave `flag:<nome>`.
7. **Visão do usuário.** Leia os menus, a navegação, os textos de tradução e o README. Eles dão os nomes que o usuário vê e a ordem das telas.
8. **Permissões.** Leia as regras de autorização. Elas definem o papel do usuário em cada pré-condição.
9. **Testes.** Leia os nomes dos testes de comportamento e de navegador. Eles mostram comportamentos e casos de borda que já têm prova.
10. **Glossário e ADRs.** Use os termos do glossário configurado para nomear Domínios e Features.

Uma entrada que não cabe nesses prefixos recebe `outro:<descrição curta>`.

Remova itens repetidos de `ancoras.txt` com `sort -u -o "$INV/ancoras.txt" "$INV/ancoras.txt"`. Sem dependências instaladas ou sem app executável, leia as rotas e classes direto do código e registre a limitação.

## Agrupar em Domínios

Um Domínio é uma área de negócio que o usuário reconhece, como Vendas, Estoque ou Financeiro. Uma camada técnica, como handlers ou jobs, não é Domínio.

Use estes sinais, nesta ordem:

1. Áreas do glossário e das ADRs.
2. Seções do menu e grupos de navegação.
3. Prefixos de nome e de URI das rotas.
4. Módulos e pastas de domínio do código, e os modelos com suas regras de autorização.
5. Pastas de testes.

Divida um Domínio com mais de 15 Features estimadas em Domínios menores. Coloque autenticação, perfil e preferências num Domínio `conta`. Coloque usuários, papéis e auditoria num Domínio `administracao`, quando existem.

## Estimar Features

Uma Feature é uma capacidade que o usuário nomeia: "Pedidos", "Relatório de vendas", "Login". Listar, criar, editar e excluir uma mesma entidade formam uma Feature. Um fluxo longo, como o checkout, pode ser outra.

Para cada Domínio, grave em `dominios.md`:

- o nome e uma linha de descrição;
- as Âncoras do Domínio, com `*` quando o prefixo é exclusivo;
- as Features estimadas, uma linha cada;
- as Âncoras sem dono claro e as candidatas a `Fora do mapa`.

O número de Domínios e de Features define o tamanho da aplicação e o modo de mapeamento.
