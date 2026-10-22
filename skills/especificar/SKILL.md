---
name: especificar
description: Sintetiza o alinhamento em uma Especificação (Spec) com fronteiras Livewire/HTTP e contratos nas Costuras existentes ou propostas, usando o destino configurado e perguntando apenas se faltar. Use quando o usuário digitar /especificar.
disable-model-invocation: true
---

# Especificar Funcionalidade e Fronteiras (`/especificar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Congelar as decisões de produto e os contratos técnicos (Fronteira Livewire/HTTP, dados de entrada e Costura pública) em uma Especificação concisa antes de planejar os tickets.

## 2. Regras Inegociáveis
- **Carregue a disciplina `laravel-deep-modules`:** Descreva o módulo, a Costura e os dados que ela recebe e devolve. Não escreva a implementação interna.
- **Não ponha caminhos de arquivo nem código na Spec:** Caminhos e trechos de código ficam desatualizados rápido. Descreva contratos em prosa e listas. Exceção: um formato de tipo, Enum ou máquina de estados que veio de um protótipo e é mais preciso que prosa. Marque a origem.
- **Confirme as Costuras com o usuário:** Prefira Costuras que já existem. Proponha a Costura mais alta possível e o menor número de Costuras.
- **Use os termos do glossário configurado (`GLOSSARY.md` como fallback):** Nomes de classes, métodos, tabelas e propriedades devem refletir o glossário do projeto.
- **Use o destino acordado:** Leia o destino de Specs da configuração ou da sessão. Pergunte apenas se faltar ou houver conflito. Não troque de destino por falha de acesso; registre o bloqueio.
- **Declare o que fica fora de escopo:** Toda Spec deve listar explicitamente o que não será feito nesta entrega.

## 3. Processo
1. **Revisão de Contexto:** Releia as decisões tomadas em `/alinhar` e os arquivos-alvo do projeto.
2. **Redação da Spec (Padrão ASD-STE100):** Monte a estrutura contendo:
   - **1. Problema e Comportamento Observável** (máximo 4 frases).
   - **2. Vocabulário de Domínio** (Enums PHP 8.2+ e termos do glossário configurado).
   - **3. Fronteira do Sistema (Livewire / HTTP):** Componente `Livewire` / `Livewire\Form` (incluindo propriedades `#[Locked]`), ou `Controller` + `FormRequest`, e regra de `Policy` (`$this->authorize()`).
   - **4. Módulo Profundo e Costura (Seam):** Costura pública existente ou proposta, dados de entrada, retorno e invariantes. Justifique Action/DTO novos ou o uso de CRUD simples na Fronteira. Escreva em lista, não em PHP.
   - **5. Plano de Testes na Costura (Pest):** Cenários testados na Costura escolhida e na Fronteira Livewire/HTTP; navegador quando houver comportamento de UI.
   - **6. Fora de Escopo:** Itens excluídos desta entrega.
3. **Resolver o Destino:** Use a configuração de Specs sem repetir a pergunta. Se não houver escolha registrada, apresente a prévia e pergunte:
   - **Opção 1:** Salvar em arquivo Markdown no repositório (ex.: `docs/specs/NNNN-slug.md`).
   - **Opção 2:** Publicar como Issue no GitHub (`gh issue create`) ou GitLab (`glab issue create`).
   - **Opção 3:** Salvar em outro destino ou formato específico.
4. **Gravação e Fechamento:** Grave a Spec no destino escolhido, informe o caminho ou link gerado e oriente o usuário a executar `/planejar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou escrever todo o código Eloquent e o template Blade dentro da Spec." | **Proibido.** A Spec define apenas contratos, fronteiras, tipos e comportamento esperado. |
| "Vou colar a classe `final readonly` do DTO e o caminho `app/Actions/...` para ficar preciso." | **Proibido.** Liste os campos e nomeie a Costura. O código e os caminhos nascem em `/implementar`. |
| "Vou salvar direto em `docs/specs/` sem perguntar ao usuário." | Use o destino de Specs já acordado na configuração ou sessão. Pergunte apenas quando ele não estiver definido. |
| "Não preciso especificar propriedades `#[Locked]` do Livewire agora." | **Proibido.** Fronteiras de segurança do Livewire e Policies fazem parte do contrato da Spec. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Costura, dados de entrada e Fronteira Livewire/HTTP nomeados sem ambiguidade e confirmados pelo usuário.
- `[measured]` Zero caminhos de arquivo e zero trechos de código na Spec, exceto formatos de protótipo marcados.
- `[measured]` Destino confirmado na configuração ou sessão e Spec gravada com sucesso (caminho do arquivo ou URL da Issue exibido).
