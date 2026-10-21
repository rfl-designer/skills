---
name: alinhar
description: Conduz entrevista pré-código (1 pergunta por vez) e atualiza o vocabulário de domínio (GLOSSARY.md) em projetos PHP, Laravel e Livewire. Use quando o usuário digitar /alinhar.
disable-model-invocation: true
---

# Alinhar Requisitos e Domínio (`/alinhar`)

## 1. Objetivo
Extrair os requisitos reais da funcionalidade através de uma entrevista estruturada (uma pergunta por vez) e alinhar os termos de negócio no `GLOSSARY.md` antes de escrever código.

## 2. Regras Inegociáveis
- **Leia o código antes de perguntar:** Se uma migration, Model, Action ou componente Livewire já responder à dúvida, inspecione os arquivos em silêncio. Nunca pergunte ao humano o que o repositório já informa.
- **Faça apenas uma pergunta por mensagem:** Percorra a árvore de decisão um ramo por vez.
- **Ofereça sempre uma recomendação:** Em cada pergunta, apresente a opção recomendada segundo as convenções do Laravel e da arquitetura `laravel-deep-modules`.
- **Sincronize o vocabulário:** Sempre que surgir um conceito novo ou ambíguo, defina o termo canônico em `GLOSSARY.md` (ou proponha sua criação).

## 3. Processo
1. **Inspeção Silenciosa:** Busque as migrations, Models, Enums, Actions e componentes Livewire relacionados ao pedido usando buscas rápidas.
2. **Mapeamento de Lacunas:** Liste mentalmente os pontos cegos nos 5 eixos do Laravel:
   - **Domínio e Estado:** Quais Enums, transições de estado ou invariantes existem?
   - **Fronteira (Livewire / HTTP):** Quais propriedades precisam de `#[Locked]`? Qual `FormRequest` ou `Livewire\Form` valida os dados?
   - **Autorização:** Qual `Policy` ou Gate controla o acesso (`$this->authorize()`)?
   - **Costura (`Action`):** Qual método público receberá o DTO `readonly` e quais transações de banco ocorrerão?
   - **Efeitos Colaterais:** Há disparo de Jobs, Events, notificações ou chamadas externas?
3. **Ciclo de Entrevista (1 por vez):** Faça a pergunta de maior impacto primeiro, incluindo sua recomendação técnica.
4. **Atualização de Glossário:** Atualize `GLOSSARY.md` com os termos de domínio acordados.
5. **Fechamento:** Ao atingir 95% de clareza em todos os ramos, resuma os pontos decididos em até 10 linhas e instrua o usuário a rodar `/especificar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou fazer 5 perguntas de uma vez para economizar tempo." | **Proibido.** Faça apenas 1 pergunta por vez para não sobrecarregar a decisão. |
| "O requisito parece óbvio, já vou gerar a migration e o componente Livewire." | **Proibido.** `/alinhar` não escreve código de produção. Conclua a entrevista primeiro. |
| "Vou perguntar ao usuário quais colunas existem na tabela `users`." | **Proibido.** Leia `database/migrations` e `app/Models/User.php` diretamente. |

## 5. Prova de Execução (Critério de Saída)
Antes de encerrar `/alinhar`, confirme com rótulo explícito:
- `[measured]` Arquivos de domínio existentes (Models/Migrations afetados) lidos e citados por caminho.
- `[measured]` Termos novos adicionados ou verificados em `GLOSSARY.md` (se aplicável).
- `[measured]` Todos os ramos críticos (Autorização, Fronteira Livewire/HTTP, Costura da Action e Efeitos Colaterais) respondidos pelo usuário.
