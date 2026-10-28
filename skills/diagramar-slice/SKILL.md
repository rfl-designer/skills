---
name: diagramar-slice
description: Gera um diagrama HTML de vertical slice a partir do diff de uma branch contra a base. Mostra os arquivos alterados por camada técnica e abre o diff de cada arquivo num modal. Com git, grava um HTML descartável fora do repositório; sem git, gera um artefato Claude a partir do diff colado. No fim, pergunta se o usuário já revisou e apaga o HTML. Use quando o usuário digitar /diagramar-slice.
argument-hint: "[base] [alvo] [--contexto <glob>] [--camadas <arquivo>]"
disable-model-invocation: true
---

# Diagramar a Slice de uma Branch (`/diagramar-slice`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

As regras de camada do projeto ficam em `docs/agents/camadas-slice.txt`. A configuração pode apontar outro arquivo.

## 1. Objetivo
Mostrar a **slice** de uma branch num diagrama. A slice é o conjunto de arquivos que a branch adicionou, alterou, removeu ou renomeou. O diagrama agrupa os arquivos por camada técnica. O clique num arquivo abre o diff dele num modal. O HTML é descartável: ele não entra no repositório.

## 2. Termos
- **Base:** a branch de comparação. Padrão: `main`; sem `main`, `master`.
- **Alvo:** a branch que a slice mostra. Padrão: a branch atual.
- **Camada:** uma linha do diagrama, como Interface ou Dados.
- **Regra de camada:** uma expressão regular que liga um caminho a uma camada. Siga as [regras de camada](references/camadas.md).
- **Arquivo de contexto:** um arquivo sem mudança que o usuário pede para ver. Ele aparece em cinza, sem status.

## 3. Regras Inegociáveis
- **Compare com o merge-base:** Use `base...alvo`, com três pontos. Assim, o diagrama mostra os mesmos arquivos que o PR. As mudanças que entraram na base depois da criação da branch não aparecem.
- **Use o script e o modelo:** Gere o HTML com `python3 <pasta-desta-skill>/scripts/gerar-slice.py`. O [modelo](assets/slice.html) lê o diff, classifica os arquivos e desenha o diagrama nos dois modos. Não escreva outro layout.
- **Mantenha o HTML fora do repositório:** O script grava na pasta temporária do sistema e recusa um caminho dentro do repositório. Não copie o HTML para o repositório. Não faça commit dele.
- **Não altere o repositório:** Só leia. A exceção é `git fetch` da base, que atualiza só as refs remotas. Sem checkout, stash, commit ou push.
- **Fique no escopo:** Não comente no PR, não publique o HTML do modo git e não revise o código. Para revisão, ofereça `/revisar`.
- **Pergunte antes de apagar:** A última pergunta é "Já revisou o diagrama? Se sim, apago o HTML.". Apague só depois de um "sim".

## 4. Entradas
- **Base:** o primeiro argumento ou `--base`. O script prefere `origin/<base>` quando esta ref existe, porque o PR compara com a base remota. Sem `main` e sem `master`, o script para e lista as branches. Pergunte ao usuário qual é a base.
- **Alvo:** o segundo argumento ou `--alvo`. Com HEAD destacado, o nome da slice é o hash curto do commit.
- **Regras de camada:** `--camadas <arquivo>`. Sem a opção, o script usa `docs/agents/camadas-slice.txt` quando este arquivo existe. Senão, usa as regras padrão.
- **Contexto (opcional):** `--contexto '<glob>'`, repetível. O glob aceita `**` (cruza pastas), `*` e `?`. Um caminho sem `*` e `?` mostra a pasta inteira. Só o modo git aceita contexto.

## 5. Escolher o modo
- **Modo git:** o agente tem um shell num repositório git que tem a base e o alvo. O resultado é um arquivo HTML local.
- **Modo artefato:** o agente não tem acesso ao repositório, como no chat do claude.ai. O resultado é um artefato HTML Claude.

Os dois modos usam o mesmo modelo. Assim, o diagrama, o modal e o comportamento são iguais para o mesmo diff.

## 6. Processo no modo git
1. **Estado:** Execute `git status --short` e `git branch --show-current`. Guarde a saída para a prova final.
2. **Base remota:** Se o remoto `origin` existe, execute `git fetch --quiet origin <base>`. Sem base informada, use `main`; se o remoto não tem `main`, use `master`. Se o fetch falha, continue com as refs locais e informe a falha.
3. **Gerar:** Execute o script na raiz do repositório:
   ```bash
   python3 <pasta-desta-skill>/scripts/gerar-slice.py --base main --alvo minha-branch
   ```
   Passe só as opções que o usuário informou. O script imprime o caminho do HTML, o intervalo, o total por status e a fonte das regras.
4. **Saída do script:**
   - **Código 0:** Continue.
   - **Código 3 (diff vazio):** Informe que não há diferenças entre `base...alvo`. Pare. Sem HTML, não há pergunta final.
   - **Código 2 com "Ref inexistente":** Mostre a ref e as branches da mensagem. Pare.
   - **Código 2 com "Nenhuma base padrão":** Pergunte qual é a base. Use as branches da mensagem como opções. Execute o script de novo.
   - **Outro erro:** Mostre a mensagem e pare.
5. **Entrega:** Informe o caminho do HTML, o intervalo e o total de arquivos por status. Repita cada linha `Aviso:` do script. Abra o arquivo com `open` ou `xdg-open` só numa máquina local com interface gráfica. Não cole o HTML na conversa.
6. **Pergunta final:** Siga a seção 8.

## 7. Processo no modo artefato
1. **Diff:** Se o usuário já colou um diff na conversa, use este diff. Senão, peça a saída do comando abaixo, com os nomes reais da base e do alvo. Diga que o comando roda na raiz do repositório. As opções dão a mesma saída com qualquer configuração local do git.
   ```bash
   git diff -M --no-color --no-ext-diff --src-prefix=a/ --dst-prefix=b/ main...minha-branch
   ```
2. **Nomes:** O cabeçalho mostra a base e o alvo. Sem nomes na conversa, use `main` e `alvo`. Diga ao usuário que os campos do artefato aceitam outros nomes.
3. **Limites:** Se o diff não tem nenhuma linha `diff --git`, informe que não há diferenças e pare. Se o usuário pede contexto, diga que o modo artefato só conhece o diff e continue sem contexto.
4. **Gerar:** Grave o diff num arquivo temporário fora do repositório. Execute:
   ```bash
   python3 <pasta-desta-skill>/scripts/gerar-slice.py --diff /tmp/slice.diff --base main --alvo minha-branch
   ```
   Para regras do usuário, grave-as num arquivo e passe `--camadas`. O script grava um fragmento HTML sem `<!doctype>`, como a ferramenta de artefato pede.
5. **Sem Python:** Copie o [modelo](assets/slice.html). Troque `__TITULO__` pelo alvo, com escape HTML. Troque `__DADOS__` por um JSON com `modo` (`"artefato"`), `nome`, `base`, `alvo`, `diff`, `contexto` (`[]`), `camadas` (texto das regras ou `""`) e `fonteCamadas`. No JSON, escreva `<` como `<`, `>` como `>` e `&` como `&`. Assim, um `</script>` no diff não fecha o bloco.
6. **Publicar:** Publique o HTML como artefato, com as regras da ferramenta de artefato do ambiente. O título é `Slice <alvo>`. O artefato tem uma caixa de texto e o botão "Gerar slice" para outro diff. O hash `#file=` abre o arquivo dentro da página. Diga que o link compartilhado do artefato pode perder o hash.
7. **Pergunta final:** Siga a seção 8. Ela cobre os arquivos temporários (diff e HTML) e, se a ferramenta permite, o artefato publicado.

## 8. Pergunta final
1. Faça uma pergunta só, com a ferramenta de pergunta estruturada quando ela existe: "Já revisou o diagrama? Se sim, apago o HTML." Opções: "Sim, apague o HTML" e "Ainda não".
2. **Sim:** Apague só os arquivos que esta execução criou: `rm -f -- '<caminho>'`. Confirme com `test ! -e '<caminho>'`. Informe o caminho apagado. No modo artefato, apague também o artefato quando a ferramenta tem a ação de apagar. No chat do claude.ai, diga que o artefato fica só na conversa.
3. **Ainda não:** Não apague. Informe o caminho e diga que o usuário pode pedir "apague o HTML da slice" depois.
4. **Sem resposta:** Sem usuário presente, termine a resposta com a pergunta e pare. Não apague.

## 9. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Dois pontos (`base..alvo`) mostram tudo que mudou; é mais completo." | **Proibido.** Use três pontos. Dois pontos mostram também as mudanças da base depois da branch. |
| "A `main` local basta; o fetch é lento." | Prefira `origin/<base>` atualizada. O PR compara com a base remota. Sem rede, informe a falha. |
| "Vou gravar o HTML em `docs/` para o usuário achar fácil." | **Proibido.** O HTML fica fora do repositório. O script recusa outro destino. |
| "O script falhou; vou desenhar o diagrama com outro layout." | **Proibido.** Use o modelo. Sem Python, preencha o modelo como na seção 7. |
| "No artefato, `git diff main...x` basta; as opções poluem o comando." | **Proibido.** Mostre o comando completo. As opções dão a mesma saída com qualquer configuração do git. |
| "O usuário pediu contexto no artefato; vou montar o conteúdo pelo diff." | **Proibido.** O modo artefato só conhece o diff. Informe o limite. |
| "Vi um risco no diff; vou comentar no PR." | **Proibido.** Fora do escopo. Ofereça `/revisar`. |
| "O usuário não respondeu; vou apagar o HTML para limpar." | **Proibido.** Apague só com "sim". |

## 10. Prova de Execução (Critério de Saída)
- `[measured]` Comando do script e o resumo que ele imprimiu: intervalo, total por status e fonte das regras.
- `[measured]` Caminho do HTML fora do repositório, ou o link do artefato.
- `[measured]` `git status --short` igual ao do início.
- `[measured]` Diff vazio ou ref inexistente: a mensagem do script, sem HTML.
- `[measured]` Resposta do usuário à pergunta final. Com "sim", a saída de `test ! -e '<caminho>'`.
