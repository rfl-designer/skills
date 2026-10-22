---
name: implmentar-em-par
description: Implementa uma Fatia Vertical Laravel ou Livewire em par com o usuário. Confirma e explica RED antes da produção; implementa um componente por etapa e aguarda revisão. Use quando o usuário pedir /implmentar-em-par ou implementação em par com essas pausas.
---

# Implementar em par (`/implmentar-em-par`)

## 1. Objetivo e disciplinas

Use a disciplina técnica de `/implementar` com revisão humana entre etapas. Conduza uma Fatia Vertical por vez na conversa principal.
Não invoque `/implementar` como orquestrador nem delegue a implementação completa. Isso eliminaria as pausas combinadas.

Carregue `laravel-deep-modules`, `laravel-tdd-seams`, `laravel-verification` e `ste100-clean-code` antes de implementar.
Localize essas skills no ambiente; se alguma faltar, informe a dependência ausente antes do trabalho dependente.

Leia a configuração indicada nas instruções do projeto. Sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório.
Use os caminhos, executor, comandos e convenções configurados. A sessão prevalece.
Sem configuração, pergunte apenas pelas escolhas necessárias ausentes. Ofereça `/setup` uma vez, sem bloquear o trabalho independente.

## 2. Planejar a Fatia Vertical

1. Leia a Spec, o ticket vinculado, seus critérios de aceite e dependências.
2. Confira o estado do repositório e preserve alterações existentes.
3. Selecione uma Fatia Vertical desbloqueada. Registre o comportamento esperado e a Costura ou Fronteira que o teste exercitará.
4. Identifique os componentes existentes e aqueles que precisam mudar. Ordene as etapas pelas dependências de implementação.
5. Apresente o plano antes de escrever o teste. Informe o escopo de cada etapa e o resultado esperado da fatia.

Neste fluxo, **componente** é a unidade de pausa: Form Request, Policy, Model, Controller, Action, Blade ou outro elemento necessário.
Um componente pode envolver vários arquivos diretamente relacionados. Não agrupe componentes distintos para evitar revisões.

A ordem da implementação pode diferir do percurso da requisição. Service Providers, middlewares e rotas só entram quando exigem alteração.
Não imponha uma sequência fixa nem crie Action, Service ou DTO sem necessidade.
Se o projeto não usa migrations, siga seu mecanismo de schema e banco de testes. Não introduza migrations por rotina.
Para Livewire, respeite sua validação, autorização e Fronteira; não crie Controller ou Form Request artificial.

## 3. Escrever, executar e explicar RED

Escreva primeiro um teste Pest do comportamento escolhido. Use a Costura pública ou a Fronteira HTTP/Livewire conforme `laravel-tdd-seams`.
Teste resultados observáveis; não exija um teste isolado para cada componente.

Execute o teste com o comando configurado antes de escrever produção. Confirme uma falha causada pelo comportamento ausente.
Erros de ambiente, banco indisponível ou configuração inválida não comprovam RED. Resolva o impedimento ou registre o bloqueio.
Uma classe ou rota ausente pode comprovar RED quando representa o contrato escolhido e o teste alcança essa ausência.
Se o teste passar, investigue a cobertura e o comportamento existente antes de implementar.

Depois de confirmar RED, explique:

- **Comportamento:** qual critério o teste verifica.
- **Preparação:** quais dados, usuário e permissões o teste utiliza.
- **Execução:** qual operação o teste chama e por qual Costura ou Fronteira.
- **Verificações:** quais respostas, efeitos ou dados persistidos ele confere.
- **Resultado:** comando, diretório, falha observada e por que ela era esperada.
- **Próxima etapa:** qual componente será implementado primeiro e sua responsabilidade.

**Pare aqui e aguarde a revisão do usuário antes de escrever produção.**

## 4. Implementar um componente por etapa

Após a revisão, implemente somente o próximo componente acordado. Preserve os contratos, a autorização e as convenções do projeto.
Faça as verificações focadas úteis para a etapa, conforme `laravel-verification`.
Execute o teste da fatia quando a alteração permitir observar seu avanço. Registre quando ele ainda não foi executado novamente.

O teste pode continuar vermelho enquanto faltam componentes. Confira a causa observada; diferencie incompletude prevista de regressão ou falha inesperada.
Não adicione stubs de sucesso, mocks internos ou retornos artificiais para esconder a incompletude.
Se surgir outro comportamento necessário, escreva seu teste e confirme RED antes da produção correspondente.
Explique esse novo teste e pause para revisão, como no primeiro RED.

Depois da etapa, apresente este resumo em português:

- **Implementado:** componente e arquivos alterados, com links quando disponíveis.
- **Responsabilidade:** o que ele faz no fluxo da Fatia Vertical.
- **Decisão:** por que adotou essa solução e como ela se conecta aos outros componentes.
- **Verificação:** comando, diretório, resultado e escopo verificado; informe o que continua vermelho ou não verificado.
- **Próxima etapa:** componente seguinte e o que falta para cumprir o comportamento.

Use os princípios de `ste100-clean-code`: voz ativa, termos consistentes e uma ideia por frase.
Limite instruções a 20 palavras e explicações a 25 palavras por frase. Explique termos técnicos novos quando necessários.
Explique o motivo das decisões sem narrar cada linha de código ou adicionar comentários didáticos redundantes.

**Pare após cada componente. Não implemente o seguinte no mesmo turno.**
Uma resposta como “continue” libera a próxima etapa. Uma dúvida ou pedido de ajuste mantém o componente atual em revisão.
Responda à dúvida ou ajuste o componente e apresente novas evidências antes de avançar.
Se o usuário alterar explicitamente o ritmo das pausas, siga a nova combinação e registre seu alcance.

## 5. Confirmar GREEN, refatorar e concluir

Quando os componentes necessários estiverem conectados, execute os testes da fatia e confirme GREEN.
Se o teste passar antes do previsto, reavalie as etapas restantes. Não crie componentes desnecessários para completar o plano inicial.
GREEN comprova apenas o comportamento coberto; confira os demais critérios de aceite e a Fronteira usada pelo projeto.

Explique o resultado e apresente os ajustes de refatoração necessários. Aguarde revisão antes de executar esses ajustes.
Se não houver ajustes, informe isso e siga com a verificação final.
Refatorações que envolvam vários componentes devem ser divididas em etapas revisáveis, preservando o comportamento.
Repita os testes afetados após refatorar.

Antes de concluir a fatia ou fazer commit autorizado, aplique o portão completo de `laravel-verification` no estado atual.
Inclua navegador quando o fluxo exigir. Reutilize evidências apenas enquanto elas ainda cobrirem o estado atual.
Uma pausa intermediária pode manter testes vermelhos. Ela não conclui a fatia nem exige a suíte completa apenas para pausar.
Não faça commit de etapa vermelha. Faça commits somente quando autorizados pela sessão e com o portão aprovado.

Na entrega, relacione critérios atendidos, componentes alterados, provas RED/GREEN, verificações finais e pendências.
Use `[measured]` somente para execução real. Diferencie teste focado, suíte completa e prova de navegador.
Se houver bloqueio, preserve o trabalho e informe a cobertura ausente. Não declare a fatia concluída.
Após a entrega, aguarde revisão antes de iniciar outra fatia ou ticket. Ao concluir o escopo, indique `/revisar`.

## 6. Continuidade entre pausas

Em cada pausa, deixe claros: ticket, fatia, etapa atual, arquivos alterados, última evidência e próximo passo.
Se o usuário pedir `/pausar`, use o fluxo de handoff existente para registrar esses dados.
Na retomada, confira o diff e as mudanças posteriores. Atualize o plano e marque evidências afetadas como desatualizadas.
Não presuma que a ausência de resposta autoriza avançar.
