# Matriz de referências

Consultada em 21/10/2026. As fontes abaixo descrevem correspondências no conteúdo, não autoria histórica comprovada nem eficácia medida. Os links apontam à branch corrente; registre uma revisão fixa ao repetir a pesquisa.

| Prática local | Matt Pocock | Addy Osmani | pstack | Interpretação |
|---|---|---|---|---|
| Configuração persistente por projeto | [setup-matt-pocock-skills](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md) | — | [setup-pstack](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md) | Matt configura tracker e documentação; pstack configura modelos. Stack, pastas e destinos independentes em `/setup` são adaptação local |
| Entrevista antes do código | [grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) | [interview-me](https://github.com/addyosmani/agent-skills/blob/main/skills/interview-me/SKILL.md) | — | Prática compartilhada; perguntas Laravel são adaptação local |
| Glossário e ADRs | [domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md) | [documentation-and-adrs](https://github.com/addyosmani/agent-skills/blob/main/skills/documentation-and-adrs/SKILL.md) | — | Há sobreposição em decisões documentadas; glossário integrado se aproxima de Matt |
| Protótipo para responder uma pergunta | [prototype](https://github.com/mattpocock/skills/blob/main/skills/engineering/prototype/SKILL.md) | — | [prototype playbook](https://github.com/cursor/plugins/tree/main/pstack/skills/poteto-mode) | Correspondência; preservação e descarte seguem política local |
| Spec sem caminhos e código | [to-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md) | — | — | Correspondência específica com Matt, sem presumir consenso |
| Fatias verticais e dependências | [to-tickets](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md) | [planning-and-task-breakdown](https://github.com/addyosmani/agent-skills/blob/main/skills/planning-and-task-breakdown/SKILL.md) | — | Prática compartilhada; ponteiros de arquivos são escolha local |
| TDD pela interface pública | [tdd](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd) | [test-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md) | [tdd](https://github.com/cursor/plugins/tree/main/pstack/skills/tdd) | Princípio comum; Pest e fakes Laravel são aplicação local |
| Standards e Spec separados | [code-review](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md) | — | — | Correspondência específica; revisão multi-modelo do pstack tem outra organização |
| Provar o fato de segurança por execução | — | — | [blast-radius](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md) | Correspondência específica com pstack |
| Portão proporcional e proteção contra enfraquecimento | — | [constraint-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md) | — | Adaptação; não implementa todo o sistema de constraints do Addy |
| Protocolo reproduzível do app | — | — | [create-verification-skill](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) | Inspiração; aqui preferimos teste/runbook existente a gerar outra skill |
| Action/DTO opcionais, Policies e estado Livewire | [codebase-design](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md) | — | [architect](https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md) | Os princípios se relacionam; a convenção Laravel é escolha local |

`—` significa que esta matriz não estabelece correspondência, não que o autor rejeita ou nunca trata a prática. Não exigimos dois autores para justificar uma regra útil.

Fontes de ferramentas: [Pint e Blade](https://laravel.com/framework/docs/pint), [Pest Agent](https://github.com/pestphp/docs/blob/5.x/agent.md), [Pest 5](https://pestphp.com/docs/pest5-now-available). Versões e opções devem ser detectadas no projeto consumidor.
