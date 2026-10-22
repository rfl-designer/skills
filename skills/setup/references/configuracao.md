# Estrutura da configuração do projeto

Use este formato em `docs/agents/projeto.md` ou no destino existente. Os marcadores `{{...}}` são instruções de preenchimento, não valores finais. Omita campos que não se aplicam; pendências reais levam `não confirmado` e uma ação concreta.

```markdown
# Configuração do projeto

## Escopo
- Raiz dos caminhos: raiz do repositório.
- Aplicação: {{nome e diretório relativo; ponto para a raiz}}.
- Instruções locais: {{arquivos já usados}}.

## Tecnologias
| Tecnologia | Versão resolvida/declarada | Fonte e estado da instalação | Planejado ou pendente |
| --- | --- | --- | --- |
| {{tecnologia do projeto}} | {{versão ou restrição declarada}} | {{lockfile/manifest; instalação confirmada ou não}} | {{decisão do usuário, se houver}} |

## Execução e verificação
- Diretório de execução: {{caminho relativo à raiz}}.
- Executor: {{local, Herd, Sail ou outro}}.
- URL local: {{URL existente, ou não aplicável}}.

| Operação | Comando ou ferramenta | Estado da prova |
| --- | --- | --- |
| Teste focado | {{comando; use <Teste> como parâmetro quando necessário}} | {{encontrado, executado ou pendente}} |
| Suíte completa | {{comando}} | {{estado}} |
| Análise estática | {{comando ou ausente}} | {{estado}} |
| Formatação PHP/Blade | {{comando e como Blade é habilitado}} | {{estado}} |
| Build | {{comando ou não aplicável}} | {{estado}} |
| Navegador | {{comando ou ferramenta disponível}} | {{estado}} |

- Capacidades condicionais: {{Pest Agent, Browser, Blade no Pint; detectadas ou não disponíveis}}.
- Ordem do portão: formatação → análise estática → testes; acrescente build/navegador quando necessários.

## Destinos
| Artefato | Tipo | Destino exato | Convenção |
| --- | --- | --- | --- |
| Specs | {{local, GitHub, GitLab ou outro}} | {{pasta ou host/projeto}} | {{nome ou título; como localizar a Spec}} |
| Tickets | {{escolha independente}} | {{pasta ou host/projeto}} | {{nome/título, relação com Spec e dependências}} |
| Glossário | local | {{caminho do arquivo}} | {{termos de domínio}} |
| ADRs | local | {{pasta}} | {{convenção existente ou NNNN-slug.md}} |
| Protocolos | local | {{pasta}} | {{por feature}} |
| Evidências | local | {{pasta durável}} | {{não gravar segredos; política de versionamento}} |

## Acesso ao tracker
- Ferramenta: {{conector ou CLI real disponível; omita se tudo for local}}.
- Alvo: {{host e projeto/repositório exatos}}.
- Localizar, criar e atualizar: {{operações disponíveis e campos/convenções}}.
- Bloqueios de acesso: {{nenhum observado ou pendência; nunca credenciais}}.

## Organização do código
- {{pastas existentes por responsabilidade; não criar camadas por obrigação}}.

## Decisões e pendências
- {{escolhas confirmadas pelo usuário e o que ainda falta confirmar ou executar}}.
```

Se houver vários apps, repita as seções de tecnologias, execução e destinos dentro de cada escopo identificado por caminho. Declare destinos compartilhados uma vez e registre exceções por app. Um caminho de artefato continua relativo à raiz, mesmo quando o comando roda numa subpasta.

Exemplo de bloco nas instruções do projeto (substitua o caminho se necessário):

```markdown
<!-- skills:config:start -->
## Configuração das skills
Antes de usar o fluxo de skills, leia `docs/agents/projeto.md`.
Use o escopo da aplicação afetada e seus comandos e destinos.
Instruções explícitas da sessão prevalecem; não regrave preferências sem pedido.
<!-- skills:config:end -->
```

Uma escolha de destino da Spec nunca determina automaticamente o destino dos tickets. Configurar GitHub/GitLab não cria issues. Se faltarem informações de acesso, registre-as como pendentes e peça apenas quando a publicação fizer parte da tarefa.
