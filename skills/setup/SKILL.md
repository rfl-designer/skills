---
name: setup
description: Configura este pacote de skills por projeto; detecta tecnologias, combina pastas e comandos e registra onde specs, tickets e documentos de domínio serão gravados. Use ao preparar o projeto, mudar essas convenções ou executar /setup; não instala o pacote nem cria uma aplicação.
---

# Configurar o Projeto (`/setup`)

Prepare uma configuração persistente que as outras skills leem. Configure o projeto consumidor, não a pasta de instalação das skills.

## 1. Descobrir o estado existente

- Leia as instruções do projeto (`AGENTS.md`, `CLAUDE.md` ou arquivo nativo já usado). Siga o ponteiro de configuração existente; o destino padrão é `docs/agents/projeto.md`.
- Inspecione manifests, lockfiles, scripts, configuração de testes e estrutura de código/documentação. Detecte tecnologias e versões sem presumir que Laravel, Livewire ou Pest estejam instalados.
- Separe versão resolvida no lockfile, instalação confirmada, restrição declarada e tecnologia planejada. Sem prova da instalação/runtime, registre `não confirmado`; o lockfile sozinho não prova instalação.
- Detecte executor (local, Herd, Sail ou outro), comandos de teste, análise estática, formatação, build e navegador. Reutilize scripts existentes e a URL local já definida. Não inicie servidor quando o ambiente já serve o app.
- Inspecione remotes para sugerir tracker, sem publicar nada. Detecte diretórios existentes de specs, tickets, glossário, ADRs, verificação e Mapa de Features antes de sugerir novos.
- Se houver mais de um app, identifique o escopo afetado. Guarde uma seção por escopo no mesmo arquivo; não aplique comandos de um app aos demais.

Não leia nem copie credenciais para a configuração. Para capacidades condicionais, como Blade no Pint ou `--agent` no Pest, use lockfiles/help quando disponíveis; ausência da ferramenta é uma pendência, não autorização para instalá-la.

Para a qualidade dos testes de `laravel-verification`, detecte também:
- O driver de cobertura: `php -m` mostra `pcov` ou `xdebug`.
- A mutação: `--mutate` no help do Pest, ou `infection/infection` no `composer.lock`.
- O `<source>` do `phpunit.xml`, que define os arquivos medidos.

## 2. Completar as escolhas

Apresente o que encontrou e a recomendação. Pergunte uma categoria por vez, apenas quando a sessão ou a configuração existente não resolver:

1. **Tecnologias e execução:** confirme as tecnologias planejadas ou divergências relevantes. Registre comandos completos, diretório de execução e URL; não proponha trocar uma stack existente por padrão.
2. **Specs:** Markdown local, GitHub, GitLab ou outro destino descrito pelo usuário. Prefira a convenção existente; sem convenção, sugira `docs/specs/`.
3. **Tickets:** escolha independente da Spec. Para Markdown, sugira `docs/tickets/<spec>/`; para tracker, registre host e projeto/repositório exatos. Inclua convenção de nomes, vínculo com a Spec e representação das dependências.
4. **Documentação e pastas:** proponha um único conjunto para glossário, ADRs, protocolos, evidências e Mapa de Features. Reutilize a organização do domínio e do código; pastas novas de Actions/DTOs não são obrigatórias. Para Evidências, pergunte também a política de versionamento da [configuração](references/configuracao.md#política-de-evidências) e recomende `Fora do Git`.

As escolhas já feitas dispensam nova confirmação. Para destinos externos, prefira o conector/CLI disponível e registre a capacidade de acesso sem confundir configuração com publicação. Se o usuário escolher outro tracker, documente a operação real disponível; não invente comandos.

## 3. Gravar e conectar

Use [references/configuracao.md](references/configuracao.md) como estrutura. Preencha só o que se aplica; não deixe marcadores de template na configuração final.

- Por padrão, grave `docs/agents/projeto.md`, com caminhos relativos à raiz do repositório e diretório de execução explícito por app. Preserve outro destino já acordado.
- Crie os diretórios locais confirmados para artefatos. Com a política `Fora do Git`, acrescente a pasta de Evidências ao `.gitignore` do projeto. Não trate URLs como pastas nem mova documentos existentes. Para convenções com `<spec>`, crie só a pasta base; a subpasta nasce com a Spec correspondente. Pastas vazias podem não entrar no Git; as skills as recriam ao gravar o primeiro conteúdo.
- Registre verificadores ausentes como pendências. Este setup não instala dependências, atualiza versões principais ou altera o ambiente global. Instalação solicitada separadamente exige executar e validar a mudança real, além de atualizar o registro.
- Acrescente um bloco pequeno `Configuração das skills` no arquivo de instruções já utilizado, apontando para a configuração. Se nenhum existir, crie `AGENTS.md` mínimo. Se mais de um já existir, mantenha o mesmo ponteiro nos arquivos usados pelos agentes do projeto.
- Delimite o bloco com `<!-- skills:config:start -->` e `<!-- skills:config:end -->`. Atualize o bloco existente; preserve todas as instruções fora dele. Se já houver um ponteiro sem esses marcadores, atualize-o sem criar outro concorrente.

O bloco instrui a ler a configuração antes do fluxo, usar o escopo correto e respeitar instruções explícitas da sessão. Guarde detalhes no arquivo de configuração; não duplique tecnologias ou destinos no bloco.

## 4. Reexecução e prova

Reexecutar `/setup` atualiza somente escolhas alteradas ou evidência invalidada. Não peça novamente destinos válidos, não sobrescreva notas manuais e não migre artefatos antigos implicitamente. Se houver conflito entre registros ou entre o combinado e o ambiente, mostre a diferença e resolva apenas a escolha necessária.

Antes de encerrar:

- Releia a configuração e os ponteiros. Confira caminhos locais e escopos; campos externos devem conter o host/projeto escolhido.
- Distinga comandos encontrados, executados e ainda não verificados. Só marque como testado o que rodou no ambiente configurado.
- Confirme que `/especificar` e `/planejar` conseguem determinar os destinos sem nova pergunta. Se um acesso externo falhou, mantenha a preferência e registre o bloqueio; não troque silenciosamente para arquivos locais.
- Informe o arquivo gravado, tecnologias detectadas, destinos escolhidos e pendências. Não abra issues nem faça commit só para provar o setup.
