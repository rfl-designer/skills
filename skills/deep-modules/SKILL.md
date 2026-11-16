---
name: deep-modules
description: Disciplina arquitetural de Módulos Profundos, neutra de linguagem e de framework. Use ao desenhar, planejar, implementar ou revisar Costuras, Fronteiras, contratos de dados e módulos de regra de negócio.
---

# Módulos Profundos (`deep-modules`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

**Perfil de stack:** Esta skill não assume linguagem nem framework. Se a configuração ou os manifests mostram Laravel, leia também [references/laravel.md](references/laravel.md): ele traduz cada regra para PHP, Laravel e Livewire. Sem perfil para a stack do projeto, aplique cada regra com o mecanismo equivalente da stack e diga qual mecanismo você usou.

## 1. Objetivo
Encapsular regras de negócio atrás de interfaces pequenas e testáveis. Prefira as Costuras existentes e mantenha validação e autorização explícitas na Fronteira.

- **Costura:** a interface pública de um módulo de regra de negócio. O teste e o resto do sistema chamam o módulo por ela.
- **Fronteira:** o ponto em que a entrada externa entra no sistema: handler HTTP, componente de UI com estado no servidor, comando, job ou consumidor de fila.

## 2. Regras Inegociáveis
- **Use o modo mais estrito da linguagem:** Ative a checagem estrita de tipos que a linguagem e o analisador do projeto oferecem. Não baixe o nível de rigor já configurado.
- **Preserve a arquitetura existente:** Antes de criar um módulo, identifique a Costura pública e a complexidade que ela esconde. Não converta código vizinho só para impor este padrão.
- **Mantenha a Fronteira magra:** Valide entrada e autorização na Fronteira. Extraia regras, transações e coordenação quando houver complexidade a encapsular. CRUD trivial pode continuar na Fronteira se seguir a arquitetura do projeto e permanecer testável.
- **Não confie no estado que o cliente controla:** Um ID ou um estado que passa pelo cliente pode voltar alterado: campo oculto, estado de componente, parâmetro de URL ou corpo da requisição. Trave esse valor com o mecanismo da stack, ou leia-o de novo no servidor e autorize a operação sobre ele.
- **Escolha dados pelo contrato:** Prefira um contrato de dados imutável e tipado quando vários campos, invariantes ou consumidores pedirem um contrato explícito. Reutilize tipos existentes; valores escalares ou dados validados locais bastam para operações simples. Não crie um tipo que apenas repassa campos sem benefício.
- **Desenhe interfaces pequenas:** Para uma Costura nova, prefira um só ponto de entrada público e encapsule o fluxo relevante. Preserve assinaturas públicas já estabelecidas. Justifique a escolha ou exceção no ticket/Spec em uma frase; não crie ADR só por isso.
- **Torne o estado inválido impossível de escrever:** Use enumerações, tipos imutáveis e tipos estritos para que o analisador recuse o valor inválido. Não silencie o analisador com um comentário de supressão nem com uma entrada nova no baseline.
- **Valide uma vez, na entrada:** A Fronteira valida e converte a entrada em tipos ou no contrato de dados. Dentro da Costura, confie no dado. Não repita a validação nem espalhe checagens defensivas de nulo.
- **Torne a operação repetível:** Nova tentativa de job, webhook, tarefa agendada e duplo clique executam a mesma operação de novo. Executar 2 vezes, ou de novo depois de uma falha no meio, deixa o mesmo estado final. Use índice único com upsert, chave de idempotência, trava de job único ou a conferência do estado dentro da transação.
- **Dê um só escritor ao estado compartilhado:** Se dois processos não precisam do mesmo registro mutável, dê a cada um o seu. Se precisam, garanta um só escritor na estrutura: trava de linha na transação, incremento atômico ou job sem sobreposição.

## 3. Exemplo de Costura com contrato tipado

A Costura `AprovarPedido` tem um só ponto de entrada.

- **Entrada:** `DadosDaAprovacao`, imutável: `pedidoId` (inteiro), `aprovadorId` (inteiro), `estado` (enumeração `EstadoDoPedido`).
- **Retorno:** o `Pedido` gravado.
- **Invariantes:** a operação lê o pedido com trava de linha, dentro de uma transação. Ela grava o estado e o aprovador juntos. A 2ª execução com os mesmos dados deixa o mesmo estado.
- **Fronteira:** valida a entrada, autoriza o aprovador e monta `DadosDaAprovacao`. Ela não contém a regra.

O perfil de stack mostra este exemplo em código.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "A consulta tem apenas 4 linhas, vou colocá-la direto no handler da Fronteira." | Avalie o comportamento: CRUD trivial pode ficar na Fronteira; regras, transações e coordenação pedem uma Costura própria. O número de linhas não decide sozinho. |
| "Vou passar o mapa de dados validados direto para a Costura." | Prefira um contrato tipado quando ele estabiliza um contrato entre módulos. Não adicione um tipo apenas para repassar dados validados locais. |
| "Vou criar uma interface para a Costura mesmo tendo apenas uma implementação." | **Proibido (Anti-Shallow Module).** Não crie interfaces pass-through sem necessidade real de múltiplas implementações. |
| "O job tem 3 tentativas; se falhar, ele roda de novo e pronto." | **Proibido.** A nova tentativa repete as escritas que já aconteceram. Prove que a 2ª execução deixa o mesmo estado. |
| "O analisador reclama do tipo; ponho um comentário de supressão e sigo." | **Proibido.** O erro aponta um estado inválido possível. Corrija o tipo ou a origem do dado. |
| "O ID vem de um campo oculto do meu próprio formulário; ele é confiável." | **Proibido.** O cliente pode alterar esse valor. Trave-o ou autorize a operação sobre o valor recebido. |

## 5. Prova de Execução (Critério de Saída)
Quando houver alteração de código, aplique o alcance de `verification`. Em desenho ou documentação, registre a decisão sem executar ferramentas só por carregar esta disciplina.
- `[measured]` Costura escolhida e complexidade encapsulada identificadas; exceção ao padrão explicada quando aplicável.
- `[measured]` Zero erros na análise estática da configuração, sem supressão nova nem entrada nova no baseline. Sem analisador no projeto, registre `não verificado`.
- `[measured]` Para cada operação repetível do diff (job, webhook, tarefa agendada ou ação de UI que grava): um teste que a executa 2 vezes e confere o mesmo estado final.
- `[measured]` Para cada valor sensível que passa pelo cliente no diff: o mecanismo que o trava, ou a autorização feita sobre o valor recebido.
