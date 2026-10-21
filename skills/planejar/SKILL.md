---
name: planejar
description: Decompõe uma Especificação (Spec) aprovada em um grafo de Fatias Verticais com Throughput Checkpoint, perguntando onde salvar os tickets. Use quando o usuário digitar /planejar.
disable-model-invocation: true
---

# Planejar Grafo de Fatias Verticais (`/planejar`)

## 1. Objetivo
Transformar uma Especificação (Spec) aprovada em tickets pequenos de Fatias Verticais (*Tracer Bullets*) com relações de bloqueio explícitas e um *Throughput Checkpoint* antes da execução.

## 2. Regras Inegociáveis
- **Proíba fatiamento horizontal:** Nunca separe tarefas por camada técnica isolada (ex.: "Ticket 1: Criar todas as migrations", "Ticket 2: Criar todas as Actions"). Cada ticket deve entregar uma fatia vertical verificável de ponta a ponta.
- **Escreva o Throughput Checkpoint antes dos tickets:** Separe passos bloqueantes de frentes paralelizáveis e identifique arquivos com estado compartilhado.
- **Declare arestas de bloqueio:** Todo ticket deve conter `Bloqueado por: Nenhum` ou `Bloqueado por: Ticket #N`.
- **Pergunte o destino de gravação:** Pergunte ao usuário onde salvar os tickets (Markdown local, Issues no GitHub/GitLab ou outro destino), a menos que o destino já tenha sido definido em `/especificar`.

## 3. Processo
1. **Leitura da Spec:** Leia a Especificação gerada por `/especificar` e inspecione os arquivos que serão tocados.
2. **Throughput Checkpoint (4 itens obrigatórios):**
   - **1. Fundação Bloqueante:** O que precisa existir antes de qualquer paralelismo (ex.: Migration base + Enum + DTO `readonly` + assinatura da Costura da `Action`).
   - **2. Frentes Paralelizáveis:** Quais fatias verticais não disputam os mesmos arquivos e podem ser delegadas em paralelo.
   - **3. Estado Mutável Compartilhado:** Arquivos que múltiplos tickets poderiam tocar (ex.: `routes/web.php`, componente Livewire pai) e como serializar a edição.
   - **4. Menor Decomposição Segura:** Quantidade mínima de tickets/commits verificáveis (~100 linhas por fatia).
3. **Estrutura de Cada Ticket (Fatia Vertical):**
   - **Título e Objetivo Observável** (1 frase em voz ativa).
   - **Bloqueado por:** `#ID` ou `Nenhum`.
   - **Ponteiros de Contexto:** Caminhos exatos dos arquivos a criar ou modificar.
   - **Critério de Aceite no Pest:** Qual teste de Costura (`Action`) e de Fronteira (`Livewire::test()` ou HTTP) comprovará a fatia.
4. **Pergunta de Destino e Gravação:** Confirme com o usuário se os tickets devem ser salvos em:
   - **Opção 1:** Arquivo Markdown no repositório (ex.: `docs/specs/NNNN-slug-tickets.md`).
   - **Opção 2:** Issues no GitHub (`gh issue create`) ou GitLab (`glab issue create`) com links de bloqueio.
   - **Opção 3:** Outro destino informado.
5. **Fechamento:** Exiba o resumo do grafo e oriente o usuário a executar `/implementar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou criar um ticket separado no final apenas para escrever os testes no Pest." | **Proibido.** Cada Fatia Vertical inclui seu próprio teste Pest executado via TDD. |
| "Vou colar o código inteiro dos arquivos dentro da descrição do ticket." | **Proibido.** Use apenas Ponteiros de Contexto (caminho do arquivo e linhas) e assinaturas de tipos. |
| "Não preciso mapear arquivos compartilhados entre tickets." | **Proibido.** Sem mapear o Estado Mutável Compartilhado, subagentes paralelos gerarão conflitos de merge. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` *Throughput Checkpoint* de 4 itens presente no plano.
- `[measured]` Zero tickets horizontais ou tickets exclusivos de teste.
- `[measured]` Tickets gravados no destino escolhido pelo usuário.
