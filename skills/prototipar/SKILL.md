---
name: prototipar
description: Constrói um protótipo descartável para responder uma pergunta de design (modelo de estado ou layout de tela) antes da Especificação, em projetos Laravel e Livewire. Use quando o usuário digitar /prototipar.
disable-model-invocation: true
---

# Protótipo Descartável (`/prototipar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Responder uma pergunta de design com o menor custo possível, antes de `/especificar`. O protótipo é um instrumento descartável. O resultado é a decisão, não o código.

## 2. Regras Inegociáveis
- **Declare a pergunta primeiro:** Escreva em uma frase qual decisão o protótipo responde. Sem pergunta, não há protótipo: volte para `/alinhar` ou `/especificar`.
- **Escolha um ramo pela pergunta:**
  - **Lógica** ("Este modelo de estado está certo?"): um arquivo HTML único, sem build e sem servidor, que o usuário abre com clique duplo.
  - **Tela** ("Como esta tela deve ficar?"): variantes na rota que já existe, trocadas por `?variant=`.
  - Se a pergunta é ambígua e o usuário não responde, escolha pelo código vizinho (Action ou Model → Lógica; página ou componente Livewire → Tela) e escreva a suposição no topo do protótipo.
- **Marque o código como protótipo:** Coloque `prototype` no nome do arquivo, da classe ou da view. Um leitor casual identifica o protótipo sem abrir o arquivo.
- **Corte o polimento:** Sem testes Pest, sem tratamento de erro além do necessário para rodar, sem abstrações. As disciplinas `laravel-tdd-seams` e `laravel-verification` não se aplicam ao protótipo.
- **Mantenha o estado em memória:** Sem migrations e sem gravação no banco. Se a pergunta é sobre persistência, use um SQLite descartável com `prototype` no nome.
- **Mostre o estado:** Depois de cada ação (Lógica) ou de cada troca de variante (Tela), mostre o estado relevante completo.
- **Não commite:** O protótipo fica no working tree até o usuário decidir. Commit numa branch descartável só com pedido explícito.

## 3. Processo
1. **Pergunta:** Declare a pergunta e o ramo ao usuário em até 3 linhas.
2. **Construção, ramo Lógica:**
   - Escreva a regra num módulo puro (reducer `(estado, acao) => estado`, máquina de estados ou funções puras), num único `<script>`, sem acesso ao DOM.
   - Na página, mostre de cima para baixo: título e pergunta, painel do estado atual com rótulos legíveis, um botão por ação e abas com cenários guiados (caminho feliz, caso de borda, ação que deve ser ilegal). Cada cenário começa do mesmo estado inicial.
   - Escreva rótulos e botões na linguagem do domínio (glossário configurado), não nos nomes do código.
3. **Construção, ramo Tela:**
   - Crie de 3 a 5 variantes como views Blade ou componentes Livewire (`VariantA`, `VariantB`, ...) na página real, com os dados reais da página.
   - Faça variantes estruturalmente diferentes: layout, hierarquia de informação e ação principal. Variantes que só mudam cor ou texto não contam.
   - Adicione uma barra flutuante com seta anterior, rótulo da variante e seta seguinte. As setas atualizam `?variant=`. As teclas `←` e `→` também trocam, exceto com foco em `input`, `textarea` ou `[contenteditable]`.
   - Mostre a barra só em ambiente local (`@env('local')`). Ligue mutações a um stub, não a uma `Action` real.
4. **Observação:** Para Tela, capture uma screenshot de cada variante no navegador. Para Lógica, execute cada cenário e registre o estado final.
5. **Entrega:** Mostre ao usuário as variantes ou cenários, a evidência, as vantagens e desvantagens de cada um e sua recomendação. Informe o caminho ou a URL do protótipo.
6. **Captura da decisão:** Depois que o usuário escolher:
   - Grave a decisão e a pergunta que ela respondeu no lugar que o usuário indicar (ticket, ADR via `/alinhar` ou nota da Spec).
   - Converta cada cenário validado do ramo Lógica num caso de teste para a Costura pública escolhida. Esses casos entram na Especificação.
   - Remova do código de produção as variantes perdedoras, a barra e as rotas de protótipo. A variante vencedora é reescrita do zero em `/implementar`, com TDD.
   - Instrua o usuário a rodar `/especificar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou escrever testes Pest para o protótipo ficar confiável." | **Proibido.** Teste no protótipo custa tempo e não responde a pergunta. Os testes vêm em `/implementar`. |
| "A variante B ficou boa, vou só mover para produção." | **Proibido.** O protótipo não tem testes nem autorização. Reescreva a variante em `/implementar`. |
| "Três variantes com o mesmo grid de cards e cores diferentes bastam." | **Proibido.** Variantes precisam discordar na estrutura. Refaça a variante parecida com outro layout. |
| "Vou criar uma migration para o protótipo usar dados reais." | **Proibido.** O estado fica em memória. Persistência só entra se ela for a pergunta. |
| "Vou prototipar para ver o que surge." | **Proibido.** Sem pergunta declarada, o protótipo não tem critério de parada. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` A pergunta declarada e o ramo escolhido.
- `[measured]` Screenshot de cada variante (Tela) ou estado final de cada cenário (Lógica).
- `[measured]` A decisão do usuário, gravada no local indicado, com o caminho citado.
- `[measured]` `git status` sem arquivos de protótipo no código de produção, ou a declaração do usuário de que eles ficam.
