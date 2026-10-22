# Implementadores no Claude Code

O principal executa `/implementar` e coordena as fatias. Use o agente customizado
`implementador`, com `model: claude-sonnet-5-5` e `effort: medium`. Não altere o
modelo da conversa principal nem use um fork que herda o modelo e o histórico.

## Registrar uma vez no projeto consumidor

O [template](../assets/implementador.md) pertence à skill. Instalar a skill com
`npx skills add` não registra esse arquivo como agente do Claude Code.

Copie o template para `.claude/agents/implementador.md` na raiz do **projeto
consumidor**, não na pasta de instalação da skill. Crie o diretório se necessário.
Se já existir um agente com esse nome, leia-o e preserve customizações; ajuste
somente o necessário para o fluxo acordado. Não altere configurações globais.

Instale também `laravel-deep-modules`, `laravel-tdd-seams`, `laravel-verification`
e `ste100-clean-code` para o Claude Code. O campo `skills` pré-carrega essas
disciplinas; confira sua disponibilidade e forneça os caminhos resolvidos no
contrato de delegação. `/implementar` não deve entrar nessa lista, pois coordena
o fluxo e tem invocação explícita.

## Iniciar e conferir

- Delegue usando `subagent_type: implementador`. Não passe um override de modelo
  que substitua o definido no arquivo. Cada chamada recebe uma fatia completa e
  o contrato da skill, sem histórico bruto.
- Confira o modelo e o esforço efetivos em `/tasks` durante a execução.
  `CLAUDE_CODE_EFFORT_LEVEL` prevalece sobre o esforço do arquivo, e uma política
  ou configuração forçada de modelo pode substituir o modelo solicitado. Se o
  resultado divergir, informe a causa e resolva a configuração com o usuário;
  não declare Sonnet 5.5 medium sem confirmação nem troque de modelo em silêncio.
- Se o agente não aparecer, confirme seu registro. Criar o primeiro diretório
  de agentes durante a sessão pode exigir reiniciar o Claude Code. Preserve o
  checkpoint e informe o passo necessário; não finja que houve delegação.
- Se a versão, conta ou provedor não aceitar o modelo ou o esforço, reporte o
  erro e peça apenas a escolha necessária para continuar. Não instale ou
  atualize o runtime automaticamente.

## Isolamento e integração

O template não fixa `isolation: worktree`: o principal precisa escolher a base
correta por fatia. Ao usar isolamento nativo ou worktrees preparados pelo
principal, confira o commit-base e as dependências antes de implementar. O
isolamento nativo pode partir da branch padrão em vez do HEAD da sessão.

Para duas fatias simultâneas, use worktrees separados e recursos de teste
isolados, ou serialize o uso desses recursos. Não lance dois agentes escrevendo
no mesmo checkout. Sem worktree disponível, delegue sequencialmente no checkout
atual e preserve alterações existentes. Em ambos os modos, o principal examina
o retorno e valida a integração antes de concluir a fatia.

Fonte: [subagentes do Claude Code](https://code.claude.com/docs/en/sub-agents),
incluindo modelo, esforço, pré-carregamento de skills e isolamento.
