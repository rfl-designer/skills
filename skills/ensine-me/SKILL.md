---
name: ensine-me
description: Ensina um tema ou explica código do repositório em Lições HTML curtas, em português ASD-STE100, com fontes citadas. Pergunta antes se a Lição vai para um arquivo local ou um artefato Claude. Use quando o usuário digitar /ensine-me.
argument-hint: "O que você quer aprender?"
disable-model-invocation: true
---

# Ensinar em Lições Curtas (`/ensine-me`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Fazer o usuário entender e reter um tema ou um trecho do código. A unidade de ensino é a **Lição**: um HTML autocontido que ensina uma coisa só. O resultado é o entendimento do usuário, não uma mudança no código.

## 2. Regras Inegociáveis
- **Pergunte o destino antes de produzir a Lição:** Ofereça duas opções: arquivo local ou artefato Claude. Não pergunte de novo se o argumento ou a sessão já define o destino. `NOTAS.md` só dá a recomendação.
- **Escreva em ASD-STE100:** Aplique `ste100-clean-code` à Lição e às respostas. Use voz ativa e uma instrução por frase. Limite instruções a 20 palavras e descrições a 25.
- **Use um termo para cada conceito:** Defina o termo novo no primeiro uso e mantenha-o em todas as Lições. Termos de domínio vêm do glossário configurado do projeto.
- **Não ensine da memória:** Apoie cada afirmação técnica numa fonte verificada: documentação oficial, código da versão instalada ou commit. Marque com `[inferred]` o que não tem fonte.
- **Ensine uma coisa por Lição:** A Lição cabe em cerca de 10 minutos e entrega um ganho concreto, ligado ao motivo do usuário.
- **Mostre o mecanismo concreto:** Diga o problema que a ideia resolve e como ela funciona. Uma analogia só complementa o mecanismo. Uma lista de funções é referência, não ensino.
- **Monte diagramas em série:** Com 3 ou mais partes, cada figura repete a anterior e acrescenta uma parte. Para antes e depois, use duas figuras lado a lado. Use até 6 caixas por figura e até 4 palavras por caixa.
- **Não encene:** Não escreva "TL;DR", "o ponto-chave", "esta é a parte difícil" ou "Pausa". Diga o fato.
- **Separe cobertura de aprendizagem:** Uma Lição lida não prova aprendizagem. Registre um aprendizado só com evidência.
- **Proteja dados sensíveis:** Tire da Lição chaves, senhas, tokens, dados de `.env` e dados pessoais. O artefato sai do ambiente local.
- **Não altere o projeto:** Leia o código e escreva só na pasta de ensino. Sem commit, salvo pedido explícito.

## 3. Processo
1. **Alvo e modo:** Identifique o alvo pelo argumento ou pela conversa. Se ele é ambíguo, declare sua interpretação em uma frase e continue. Escolha o modo:
   - **Explicar:** uma Lição sobre código deste repositório (subsistema, mudança, PR ou arquivo) ou sobre um conceito pontual. Sem Missão. Leia na conversa por que o usuário pergunta: vai alterar, revisar, depurar ou é novo no código. Não o interrogue. Sem motivo na conversa, escreva para quem vai ler ou alterar o código.
   - **Curso:** o usuário quer aprender um tema em várias sessões, ou a pasta do tema já tem `MISSAO.md`. Use a Missão e os Registros.
2. **Pasta de ensino:** Leia `docs/ensino/<tema>/` antes de perguntar. Escreva `<tema>` e `<nome>` em kebab-case, sem acento. No código, `<tema>` é o nome do subsistema ou da mudança. Siga os [formatos](references/formatos.md). Crie cada arquivo só ao gravar o primeiro conteúdo. Uma pasta indicada pelo usuário substitui `docs/ensino/`.
3. **Destino:** Faça uma pergunta só, com a ferramenta de pergunta estruturada quando ela existe:
   - **Arquivo local:** `docs/ensino/<tema>/licoes/NNNN-<nome>.html`.
   - **Artefato Claude:** a ferramenta de artefato do ambiente publica a Lição.
   - Recomende o destino gravado em `NOTAS.md`. Sem destino gravado, recomende arquivo local: ele funciona em todos os agentes e fica com o projeto.
   - Sem ferramenta de artefato Claude no ambiente, não pergunte. Informe o limite em uma frase e use arquivo local. Não altere o destino gravado em `NOTAS.md`.
   - Se o usuário recusa as duas opções, ensine na conversa com as mesmas regras.
4. **Missão (Curso):** Sem `MISSAO.md`, entreviste o usuário com uma pergunta por vez. Junte a cada pergunta sua hipótese de resposta. Pare quando puder escrever o motivo concreto e o sucesso observável. Confirme a Missão antes de gravar. Se a Missão muda depois, confirme, atualize `MISSAO.md` e grave um Registro.
5. **Foco da Lição:** Atenda o pedido explícito. Sem pedido, leia `REGISTROS.md` e escolha o item mais útil para a Missão. Escolha um passo além do que o usuário já domina. Pule o que ele já sabe. Trate primeiro os Registros com `Status: aberto`.
6. **Conhecimento:**
   - **Código:** Leia o código, os chamadores e os testes. Para o motivo, leia `git log`, `git blame`, PRs, ADRs e a Spec. O commit prova o que mudou e quando. O motivo é fato só quando um texto o declara. Sem esse texto, marque `[inferred]` e liste as hipóteses concorrentes.
   - **Tema:** Detecte a versão instalada no lockfile (`composer.lock`, `package-lock.json`). Leia a página oficial da série instalada, como `12.x`. Confira no changelog se o recurso existe na versão do lockfile.
   - **Ordem de autoridade:** documentação oficial, código em `vendor/` ou `node_modules/` da versão instalada, blog ou changelog oficial e referência de padrão web (MDN). Tutorial, blog pessoal e Stack Overflow não são fonte primária.
   - Registre as fontes em `FONTES.md`. Sem acesso à documentação, use o código instalado e informe o bloqueio. Não apresente memória como fato verificado.
7. **Lição:** Comece pelo [modelo](assets/licao.html). Mantenha o CSS e o JS do modelo em todas as Lições. Não carregue recurso externo. Omita a seção que não se aplica. Escreva estas seções, nesta ordem:
   1. **Pergunta:** a pergunta que a Lição responde e por que ela importa ao usuário, em até 2 frases.
   2. **Definição:** o nome comum da ideia ou do padrão e o que ele é em termos gerais. Depois, onde ele aparece neste projeto.
   3. **Mecanismo:** o problema e o funcionamento, em camadas, com a série de diagramas. Se ajudar, siga o que acontece quando o usuário faz a ação.
   4. **No projeto:** o trecho real com `arquivo:linha`.
   5. **Prática:** obrigatória no Curso. No Explicar, ofereça no fechamento e escreva só a pedido. Escreva de 2 a 4 questões com retorno imediato. Prefira recordação de memória a reconhecimento. Intercale um tema de Lição anterior quando existe.
   6. **Leia a seguir:** a fonte primária de maior confiança e a lista de fontes citadas. No código, a fonte primária é o arquivo ou o teste que melhor mostra o comportamento.
   7. **Próximo passo:** links para Lições anteriores do mesmo tema e o lembrete para perguntar ao agente.
8. **Questões:** Dê às opções de múltipla escolha o mesmo número de palavras. Varie a posição da opção correta. No erro, mostre uma pista que leva ao mecanismo, sem a resposta. Dê a cada questão copiada um `name` novo.
9. **Entrega:** Numere a Lição pelo índice de `REGISTROS.md`. Sem índice, comece em `0001`. Acrescente a Lição ao índice e grave o destino em `NOTAS.md`.
   - **Arquivo local:** Grave a Lição em `licoes/NNNN-<nome>.html`. Informe o caminho. Abra o arquivo com `open` ou `xdg-open` só em máquina local com interface gráfica.
   - **Artefato Claude:** Siga as regras da ferramenta de artefato do ambiente. Elas prevalecem sobre o modelo. Use o nome da Lição como título, em 2 a 4 palavras. Informe o link e grave-o no índice.
   - Na conversa, dê a resposta mínima completa em 1 ou 2 frases e o caminho ou o link. Não cole a Lição.
10. **Fechamento:** Pergunte o que ficou confuso e responda. Ofereça aprofundar ou seguir. Peça o resumo da Prática que a Lição gera. Sem usuário presente, coloque a oferta no fim da resposta e pare. Depois da resposta do usuário, atualize só o que tem evidência:
    - **Evidência:** o resumo da Prática, uma resposta na conversa ou uma declaração do usuário. Escreva a origem no Registro.
    - `REGISTROS.md`: um Registro para cada aprendizado com evidência e para cada erro de entendimento ainda aberto.
    - `GLOSSARIO.md`: o termo do tema que o usuário já usa corretamente.
    - `NOTAS.md`: as preferências de ensino.
    - Sem sistema de arquivos, como no chat do claude.ai, entregue esses documentos como artefatos. Peça ao usuário para adicioná-los ao conhecimento do projeto.
11. **Comunidade:** Quando a dúvida pede julgamento, não fato, responda e indique uma comunidade de alta reputação. Se o usuário recusa comunidades, registre em `NOTAS.md` e não indique mais.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Conheço bem o Livewire; não preciso abrir a documentação." | **Proibido.** Detecte a versão instalada e cite a página oficial da série ou o código instalado. |
| "Vou gerar a Lição agora; o usuário escolhe o destino depois." | **Proibido.** Pergunte o destino antes de produzir a Lição. |
| "O usuário pediu um conceito; vou entrevistá-lo sobre a Missão." | **Proibido.** Um conceito pontual usa o modo Explicar, sem entrevista. |
| "Um diagrama completo no fim resume tudo." | **Proibido.** Um diagrama completo é referência. Monte a série, uma parte por figura. |
| "O usuário leu a Lição, então aprendeu." | **Proibido.** Cobertura não é aprendizagem. Registre só com evidência. |
| "A opção certa pode ser a mais detalhada." | **Proibido.** O tamanho revela a resposta. Iguale o número de palavras das opções. |
| "Vou trocar 'Costura' por 'ponto de extensão' para variar o texto." | **Proibido.** Use um termo para cada conceito, o mesmo do glossário. |
| "O commit diz 'fix: bloqueia aprovação duplicada'; o motivo deve ser concorrência." | Marque `[inferred]` e liste as hipóteses. O commit prova o que mudou, não por quê. |
| "A ferramenta de artefato falhou; vou dizer que publiquei." | **Proibido.** Informe a falha e ofereça arquivo local. |
| "Vou fazer commit da Lição para não perder." | **Proibido.** Commit só com pedido explícito. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Destino: resposta do usuário citada, destino dado no argumento ou na sessão, ou limite do ambiente informado.
- `[measured]` Caminho da Lição gravada ou link do artefato publicado, com a Lição no índice de `REGISTROS.md`.
- `[measured]` Fonte para cada afirmação técnica: página oficial com série, `arquivo:linha` ou commit. O resto marcado `[inferred]`.
- `[measured]` Lição autocontida: busca por `src="http`, `<link rel=`, `url(http` e `@import` sem resultado.
- `[measured]` Questões de múltipla escolha com opções de mesmo número de palavras.
- `[measured]` Nenhum segredo na Lição: busca por `key`, `secret`, `password` e `token`, sem distinção de maiúsculas, com cada resultado revisado.
- `[measured]` `git status` sem mudança nova fora da pasta de ensino.
- `[measured]` Depois do fechamento, cada Registro novo com a origem da evidência, ou a declaração "nenhum Registro novo".
