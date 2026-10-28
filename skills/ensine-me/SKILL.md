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
- **Pergunte o destino antes de produzir a Lição:** Ofereça duas opções: arquivo local ou artefato Claude. Não pergunte de novo se o argumento ou a sessão já define o destino.
- **Escreva em ASD-STE100:** Aplique `ste100-clean-code` à Lição e às respostas. Use voz ativa e uma instrução por frase. Limite instruções a 20 palavras e descrições a 25.
- **Use um termo para cada conceito:** Defina o termo novo no primeiro uso e mantenha-o em todas as Lições. Termos de domínio vêm do glossário configurado do projeto.
- **Não ensine da memória:** Apoie cada afirmação técnica numa fonte verificada: documentação oficial da versão instalada, `arquivo:linha` ou commit. Marque com `[inferred]` o que não tem fonte.
- **Ensine uma coisa por Lição:** A Lição cabe em cerca de 10 minutos e entrega um ganho concreto, ligado ao motivo do usuário.
- **Mostre o mecanismo concreto:** Diga o problema que a ideia resolve e como ela funciona. Uma analogia só complementa o mecanismo. Uma lista de funções é referência, não ensino.
- **Monte diagramas em série:** Com 3 ou mais partes, cada figura repete a anterior e acrescenta uma parte. Use até 6 caixas por figura e até 8 palavras por caixa.
- **Não encene:** Não escreva "TL;DR", "o ponto-chave", "esta é a parte difícil" ou "Pausa". Diga o fato.
- **Separe cobertura de aprendizagem:** Uma Lição lida não prova aprendizagem. Registre um aprendizado só com evidência.
- **Proteja dados sensíveis:** Tire da Lição chaves, senhas, tokens, dados de `.env` e dados pessoais. O artefato sai do ambiente local.
- **Não altere o projeto:** Leia o código e escreva só na pasta de ensino. Sem commit, salvo pedido explícito.

## 3. Processo
1. **Alvo e modo:** Identifique o alvo pelo argumento ou pela conversa. Se ele é ambíguo, declare sua interpretação em uma frase e continue. Escolha o modo:
   - **Explicar:** o alvo é código deste repositório (subsistema, mudança, PR ou arquivo). Leia na conversa por que o usuário pergunta: vai alterar, revisar, depurar ou é novo no código. Não o interrogue.
   - **Curso:** o alvo é um tema (tecnologia, conceito ou prática) para aprender em várias sessões. Use a Missão e os Registros.
2. **Destino:** Faça uma pergunta só, com a ferramenta de pergunta estruturada quando ela existe:
   - **Arquivo local:** `docs/ensino/<tema>/licoes/NNNN-<nome>.html`. Uma pasta indicada pelo usuário prevalece.
   - **Artefato Claude:** a ferramenta de artefato do ambiente publica a Lição.
   - Recomende a escolha gravada em `NOTAS.md`. Sem escolha gravada, recomende arquivo local: ele funciona em todos os agentes e fica com o projeto.
   - Sem ferramenta de artefato Claude no ambiente, diga isso na pergunta e recomende arquivo local.
   - Se o usuário recusa as duas opções, ensine na conversa com as mesmas regras.
3. **Pasta de ensino:** Leia `docs/ensino/<tema>/`. No Explicar, `<tema>` é o nome do subsistema ou da mudança. Siga os [formatos](references/formatos.md). Crie cada arquivo só ao gravar o primeiro conteúdo. O destino vale para a Lição; o estado fica nesta pasta quando há sistema de arquivos.
4. **Missão (Curso):** Sem `MISSAO.md`, entreviste o usuário com uma pergunta por vez. Junte a cada pergunta sua hipótese de resposta. Pare quando puder escrever o motivo concreto e o sucesso observável. Confirme a Missão antes de gravar. Se a Missão muda depois, confirme, atualize `MISSAO.md` e grave um Registro.
5. **Foco da Lição:** Atenda o pedido explícito. Sem pedido, leia `REGISTROS.md` e escolha o item mais útil para a Missão. Escolha um passo além do que o usuário já domina. Pule o que ele já sabe.
6. **Conhecimento:**
   - **Código:** Leia o código, os chamadores e os testes. Para o motivo, leia `git log`, `git blame`, PRs, ADRs e a Spec. Sem fonte para um motivo, marque `[inferred]` e liste as hipóteses concorrentes.
   - **Tema:** Detecte a versão instalada no lockfile (`composer.lock`, `package-lock.json`) ou na configuração do projeto. Leia a página oficial dessa versão.
   - **Ordem de autoridade:** documentação oficial, depois blog ou changelog oficial, depois referência de padrão web (MDN). Tutorial, blog pessoal e Stack Overflow não são fonte primária.
   - Registre as fontes novas em `FONTES.md`. Sem acesso às fontes, informe o bloqueio. Não apresente memória como fato verificado.
7. **Lição:** Comece pelo [modelo](assets/licao.html). Mantenha o CSS e o JS do modelo em todas as Lições. Não carregue recurso externo. Escreva estas seções, nesta ordem:
   1. **Pergunta:** a pergunta que a Lição responde e por que ela importa ao usuário, em até 2 frases.
   2. **Definição:** o nome comum da ideia e o que ela é em termos gerais. Depois, onde ela aparece neste projeto.
   3. **Mecanismo:** o problema e o funcionamento, em camadas, com a série de diagramas. Se ajudar, siga o que acontece quando o usuário faz a ação.
   4. **No projeto:** o trecho real com `arquivo:linha`, quando existe.
   5. **Prática:** obrigatória no Curso. No Explicar, só a pedido do usuário. Escreva de 2 a 4 questões com retorno imediato. Prefira recordação de memória a reconhecimento. Intercale um tema de Lição anterior quando existe.
   6. **Leia a seguir:** a fonte primária de maior confiança e a lista de fontes citadas.
   7. **Próximo passo:** links para Lições anteriores e o lembrete para perguntar ao agente.
8. **Questões de múltipla escolha:** Dê às opções o mesmo número de palavras. Varie a posição da opção correta entre questões. No erro, mostre uma pista que leva ao mecanismo, sem a resposta.
9. **Entrega:** Numere a Lição pelo índice de `REGISTROS.md`. Sem índice, comece em `0001`.
   - **Arquivo local:** Grave a Lição em `licoes/NNNN-<nome>.html`. Informe o caminho. Abra o arquivo com `open` ou `xdg-open` quando há interface local.
   - **Artefato Claude:** Siga as regras da ferramenta de artefato do ambiente, como carregar a skill de design exigida. Publique com o título `Lição NNNN: <nome>`. Informe o link.
   - Na conversa, dê a resposta mínima completa em 1 ou 2 frases e o caminho ou o link. Não cole a Lição.
10. **Fechamento:** Pergunte o que ficou confuso e responda. Ofereça aprofundar ou seguir. Depois, atualize só o que tem evidência:
    - `REGISTROS.md`: a Lição no índice e um Registro para cada aprendizado com evidência.
    - `GLOSSARIO.md`: o termo do tema que o usuário já usa corretamente.
    - `FONTES.md`: a fonte nova de alta confiança e a comunidade indicada.
    - `NOTAS.md`: o destino escolhido e as preferências de ensino.
    - Sem sistema de arquivos, como no chat do claude.ai, entregue esses documentos como artefatos. Peça ao usuário para adicioná-los ao conhecimento do projeto.
11. **Comunidade:** Quando a dúvida pede julgamento, não fato, responda e indique uma comunidade de alta reputação. Se o usuário recusa comunidades, registre em `NOTAS.md` e não indique mais.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Conheço bem o Livewire; não preciso abrir a documentação." | **Proibido.** Detecte a versão instalada e cite a página oficial dessa versão. |
| "Vou gerar a Lição agora; o usuário escolhe o destino depois." | **Proibido.** Pergunte o destino antes de produzir a Lição. |
| "Um diagrama completo no fim resume tudo." | **Proibido.** Um diagrama completo é referência. Monte a série, uma parte por figura. |
| "O usuário leu a Lição, então aprendeu." | **Proibido.** Cobertura não é aprendizagem. Registre só com evidência. |
| "A opção certa pode ser a mais detalhada." | **Proibido.** O tamanho revela a resposta. Iguale o número de palavras das opções. |
| "Vou trocar 'Costura' por 'ponto de extensão' para variar o texto." | **Proibido.** Use um termo para cada conceito, o mesmo do glossário. |
| "O commit mudou a validação; o motivo deve ser segurança." | Marque `[inferred]` e liste as hipóteses. Um motivo é fato só com fonte: PR, ADR, issue ou Spec. |
| "A ferramenta de artefato falhou; vou dizer que publiquei." | **Proibido.** Informe a falha e ofereça arquivo local. |
| "Vou fazer commit da Lição para não perder." | **Proibido.** Commit só com pedido explícito. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Destino: resposta do usuário citada, ou destino dado no argumento ou na sessão.
- `[measured]` Caminho da Lição gravada ou link do artefato publicado.
- `[measured]` Fonte para cada afirmação técnica: página oficial com versão, `arquivo:linha` ou commit. O resto marcado `[inferred]`.
- `[measured]` Lição autocontida: busca por `<script src`, `<link rel=` e `@import` sem resultado.
- `[measured]` No Curso, opções de cada questão com o mesmo número de palavras.
- `[measured]` `REGISTROS.md` com a Lição no índice e um Registro com evidência, ou a declaração "nenhum Registro novo".
- `[measured]` Nenhum segredo na Lição: busca por `KEY`, `SECRET`, `PASSWORD` e `TOKEN` sem resultado.
- `[measured]` `git status` sem mudança fora da pasta de ensino.
