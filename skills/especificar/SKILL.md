---
name: especificar
description: Sintetiza o alinhamento em uma Especificação (Spec) com fronteiras Livewire/HTTP, DTOs readonly e Costuras de Action, perguntando onde salvar. Use quando o usuário digitar /especificar.
disable-model-invocation: true
---

# Especificar Funcionalidade e Fronteiras (`/especificar`)

## 1. Objetivo
Congelar as decisões de produto e as assinaturas técnicas (Fronteira Livewire/HTTP, DTO `readonly` e Costura da `Action`) em uma Especificação concisa antes de planejar os tickets.

## 2. Regras Inegociáveis
- **Carregue a disciplina `laravel-deep-modules`:** Defina a assinatura pública do DTO e da `Action` sem escrever a implementação interna das queries.
- **Use os termos exatos do `GLOSSARY.md`:** Nomes de classes, métodos, tabelas e propriedades devem refletir o glossário do projeto.
- **Pergunte o destino de gravação:** Nunca assuma onde salvar a Spec sem confirmar com o usuário (a menos que já esteja definido na sessão).
- **Declare o que fica fora de escopo:** Toda Spec deve listar explicitamente o que não será feito nesta entrega.

## 3. Processo
1. **Revisão de Contexto:** Releia as decisões tomadas em `/alinhar` e os arquivos-alvo do projeto.
2. **Redação da Spec (Padrão ASD-STE100):** Monte a estrutura contendo:
   - **1. Problema e Comportamento Observável** (máximo 4 frases).
   - **2. Vocabulário de Domínio** (Enums PHP 8.2+ e termos do `GLOSSARY.md`).
   - **3. Fronteira do Sistema (Livewire / HTTP):** Componente `Livewire` / `Livewire\Form` (incluindo propriedades `#[Locked]`), ou `Controller` + `FormRequest`, e regra de `Policy` (`$this->authorize()`).
   - **4. Módulo Profundo e Costura (Seam):** Assinatura exata de `final readonly class <Nome>Data` e `<Nome>Action::handle(<Nome>Data $data): <Retorno>`.
   - **5. Plano de Testes na Costura (Pest):** Cenários que serão testados na `Action` e em `Livewire::test()`.
   - **6. Fora de Escopo:** Itens excluídos desta entrega.
3. **Pergunta de Destino:** Apresente uma prévia enxuta da Spec e pergunte ao usuário:
   - **Opção 1:** Salvar em arquivo Markdown no repositório (ex.: `docs/specs/NNNN-slug.md`).
   - **Opção 2:** Publicar como Issue no GitHub (`gh issue create`) ou GitLab (`glab issue create`).
   - **Opção 3:** Salvar em outro destino ou formato específico.
4. **Gravação e Fechamento:** Grave a Spec no destino escolhido, informe o caminho ou link gerado e oriente o usuário a executar `/planejar`.

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou escrever todo o código Eloquent e o template Blade dentro da Spec." | **Proibido.** A Spec define apenas contratos, fronteiras, tipos e comportamento esperado. |
| "Vou salvar direto em `docs/specs/` sem perguntar ao usuário." | **Proibido.** Pergunte sempre se o destino é Markdown local, GitHub/GitLab ou outro. |
| "Não preciso especificar propriedades `#[Locked]` do Livewire agora." | **Proibido.** Fronteiras de segurança do Livewire e Policies fazem parte do contrato da Spec. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Assinaturas do DTO `readonly`, da `Action` e da Fronteira Livewire/HTTP definidas sem ambiguidade.
- `[measured]` Destino de armazenamento confirmado pelo usuário e Spec gravada com sucesso (caminho do arquivo ou URL da Issue exibido).
