---
name: planejar
description: Decompõe uma Especificação (Spec) aprovada em um grafo de Fatias Verticais com Throughput Checkpoint, usando o destino de tickets configurado e perguntando apenas se faltar. Use quando o usuário digitar /planejar.
disable-model-invocation: true
---

# Planejar Grafo de Fatias Verticais (`/planejar`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Transformar uma Especificação (Spec) aprovada em tickets pequenos de Fatias Verticais (*Tracer Bullets*) com relações de bloqueio explícitas e um *Throughput Checkpoint* antes da execução.

## 2. Regras Inegociáveis
- **Proíba fatiamento horizontal:** Nunca separe tarefas por camada técnica isolada (ex.: "Ticket 1: Criar todas as migrations", "Ticket 2: Criar todas as Actions"). Cada ticket deve entregar uma fatia vertical verificável de ponta a ponta.
- **Use expand–contract para refactor amplo:** Uma mudança mecânica que quebra muitos pontos de chamada de uma vez (renomear coluna, mudar o tipo de um Enum ou DTO compartilhado) não cabe numa fatia vertical. Sequencie em 3 etapas:
  1. **Expand:** Adicione a forma nova ao lado da antiga. Nada quebra.
  2. **Migrate:** Migre os pontos de chamada em lotes (por módulo ou diretório). Cada lote é um ticket bloqueado pelo Expand e fica verde sozinho.
  3. **Contract:** Remova a forma antiga num ticket bloqueado por todos os lotes.
- **Escreva o Throughput Checkpoint antes dos tickets:** Separe passos bloqueantes de frentes paralelizáveis e identifique arquivos com estado compartilhado.
- **Declare arestas de bloqueio:** Todo ticket deve conter `Bloqueado por: Nenhum` ou `Bloqueado por: Ticket #N`.
- **Use o destino de Tickets:** Leia sua escolha própria na configuração ou sessão. O destino da Spec não determina o dos tickets. Pergunte somente se a escolha estiver ausente ou conflitante.

## 3. Processo
1. **Leitura da Spec:** Leia a Spec indicada; sem indicação, localize-a no destino de Specs configurado. Se houver candidatas ambíguas, peça apenas a identificação. Inspecione os arquivos afetados.
2. **Throughput Checkpoint (4 itens obrigatórios):**
   - **1. Fundação Bloqueante:** O que precisa existir antes de qualquer paralelismo (ex.: contrato compartilhado ou migration, somente quando necessários).
   - **2. Frentes Paralelizáveis:** Quais fatias verticais não disputam os mesmos arquivos e podem ser delegadas em paralelo.
   - **3. Estado Mutável Compartilhado:** Arquivos que múltiplos tickets poderiam tocar (ex.: `routes/web.php`, componente Livewire pai) e como serializar a edição.
   - **4. Menor Decomposição Segura:** Quantidade mínima de tickets/commits verificáveis (~100 linhas por fatia).
3. **Estrutura de Cada Ticket (Fatia Vertical):**
   - **Título e Objetivo Observável** (1 frase em voz ativa).
   - **Bloqueado por:** `#ID` ou `Nenhum`.
   - **Ponteiros de Contexto:** Caminhos exatos dos arquivos a criar ou modificar.
   - **Critério de Aceite no Pest:** Qual teste da Costura escolhida e da Fronteira (`Livewire::test()` ou HTTP) comprovará a fatia.
4. **Destino e Gravação:** Use o destino de Tickets registrado, mantendo o vínculo com a Spec mesmo em sistemas diferentes. Só quando faltar escolha, pergunte entre:
   - **Opção 1:** Markdown local (ex.: `docs/tickets/<spec>/NN-slug.md`).
   - **Opção 2:** Issues no GitHub (`gh issue create`) ou GitLab (`glab issue create`) com links de bloqueio.
   - **Opção 3:** Outro destino informado.
5. **Fechamento:** Exiba o resumo do grafo e oriente o usuário a executar `/implementar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou criar um ticket separado no final apenas para escrever os testes no Pest." | **Proibido.** Cada Fatia Vertical inclui seu próprio teste Pest executado via TDD. |
| "Vou colar o código inteiro dos arquivos dentro da descrição do ticket." | **Proibido.** Use apenas Ponteiros de Contexto (caminho do arquivo e linhas) e assinaturas de tipos. |
| "Vou renomear a coluna e corrigir os 200 usos num ticket só." | **Proibido.** Use expand–contract. Cada lote de migração fica verde sozinho. |
| "Não preciso mapear arquivos compartilhados entre tickets." | **Proibido.** Sem mapear o Estado Mutável Compartilhado, subagentes paralelos gerarão conflitos de merge. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` *Throughput Checkpoint* de 4 itens presente no plano.
- `[measured]` Zero tickets horizontais ou tickets exclusivos de teste, exceto lotes de expand–contract.
- `[measured]` Tickets gravados no destino escolhido pelo usuário.
