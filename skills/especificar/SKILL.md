---
name: especificar
description: Sintetiza o alinhamento em uma Especificação (Spec) com Fronteiras e contratos nas Costuras existentes ou propostas, usando o destino configurado e perguntando apenas se faltar. Antes de gravar, um Leitor novo lê o rascunho. Use quando o usuário digitar /especificar.
disable-model-invocation: true
---

# Especificar Funcionalidade e Fronteiras (`/especificar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Congelar as decisões de produto e os contratos técnicos (Fronteira, dados de entrada e Costura pública) em uma Especificação concisa antes de planejar os tickets.

## 2. Regras Inegociáveis
- **Carregue a disciplina `deep-modules`:** Descreva o módulo, a Costura e os dados que ela recebe e devolve. Não escreva a implementação interna.
- **Não ponha caminhos de arquivo nem código na Spec:** Caminhos e trechos de código ficam desatualizados rápido. Descreva contratos em prosa e listas. Exceção: um formato de tipo, Enum ou máquina de estados que veio de um protótipo e é mais preciso que prosa. Marque a origem.
- **Confirme as Costuras com o usuário:** Prefira Costuras que já existem. Proponha a Costura mais alta possível e o menor número de Costuras.
- **Use os termos do glossário configurado (`GLOSSARY.md` como fallback):** Nomes de classes, métodos, tabelas e propriedades devem refletir o glossário do projeto.
- **Use o destino acordado:** Leia o destino de Specs da configuração ou da sessão. Pergunte apenas se faltar ou houver conflito. Não troque de destino por falha de acesso; registre o bloqueio.
- **Declare o que fica fora de escopo:** Toda Spec deve listar explicitamente o que não será feito nesta entrega.
- **Passe o rascunho por um Leitor novo antes de gravar:** O implementador lê a Spec sem o histórico do chat. Aplique `leitura-independente` no modo Spec: um subagente novo lê o rascunho nas mesmas condições.

## 3. Processo
1. **Revisão de Contexto:** Releia as decisões tomadas em `/alinhar` e os arquivos-alvo do projeto.
2. **Redação da Spec (Padrão ASD-STE100):** Monte a estrutura contendo:
   - **1. Problema e Comportamento Observável** (máximo 4 frases).
   - **2. Vocabulário de Domínio** (enumerações e termos do glossário configurado).
   - **3. Fronteira do Sistema:** O ponto de entrada (handler HTTP, componente de UI, comando ou job), a validação da entrada, cada valor que o cliente controla e não pode alterar, e a regra de autorização.
   - **4. Módulo Profundo e Costura (Seam):** Costura pública existente ou proposta, dados de entrada, retorno e invariantes. Justifique Costura ou contrato de dados novos, ou o uso de CRUD simples na Fronteira. Escreva em lista, não em código.
   - **5. Plano de Testes na Costura:** Cenários testados na Costura escolhida e na Fronteira; navegador quando houver comportamento de UI.
   - **6. Fora de Escopo:** Itens excluídos desta entrega.
3. **Leitura Independente:** Aplique `leitura-independente` no modo Spec. Grave o rascunho num arquivo temporário fora do repositório e delegue a leitura a um Leitor novo. Mostre a Paráfrase e os achados ao usuário. Continue só depois da resposta dele.
4. **Resolver o Destino:** Use a configuração de Specs sem repetir a pergunta. Se não houver escolha registrada, apresente a prévia e pergunte:
   - **Opção 1:** Salvar em arquivo Markdown no repositório (ex.: `docs/specs/NNNN-slug.md`).
   - **Opção 2:** Publicar como Issue no GitHub (`gh issue create`) ou GitLab (`glab issue create`).
   - **Opção 3:** Salvar em outro destino ou formato específico.
5. **Gravação e Fechamento:** Grave a Spec no destino escolhido e apague o rascunho temporário. Informe o caminho ou link gerado e a linha `Leitura Independente:`. Envie os achados `mover para tickets` com a orientação de executar `/planejar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou escrever todo o código de persistência e o template dentro da Spec." | **Proibido.** A Spec define apenas contratos, fronteiras, tipos e comportamento esperado. |
| "Vou colar a classe `final readonly` do DTO e o caminho `app/Actions/...` para ficar preciso." | **Proibido.** Liste os campos e nomeie a Costura. O código e os caminhos nascem em `/implementar`. |
| "Vou salvar direto em `docs/specs/` sem perguntar ao usuário." | Use o destino de Specs já acordado na configuração ou sessão. Pergunte apenas quando ele não estiver definido. |
| "Não preciso especificar agora os valores que o cliente não pode alterar." | **Proibido.** A trava desses valores e a regra de autorização fazem parte do contrato da Spec. |
| "A Spec está clara para mim; gravo sem a Leitura Independente." | **Proibido.** O autor lê o que quis dizer, não o que escreveu. Um Leitor novo lê o que o implementador vai ler. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Costura, dados de entrada e Fronteira nomeados sem ambiguidade e confirmados pelo usuário.
- `[measured]` Zero caminhos de arquivo e zero trechos de código na Spec, exceto formatos de protótipo marcados.
- `[measured]` Paráfrase do Leitor mostrada ao usuário antes da gravação, e linha `Leitura Independente:` no fechamento.
- `[measured]` Destino confirmado na configuração ou sessão e Spec gravada com sucesso (caminho do arquivo ou URL da Issue exibido).
