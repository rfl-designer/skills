---
name: laravel-deep-modules
description: Disciplina arquitetural de Módulos Profundos para PHP, Laravel e Livewire. Use ao desenhar, planejar, implementar ou revisar Actions, DTOs, Models, Controllers e componentes Livewire.
---

# Módulos Profundos no Laravel e Livewire (`laravel-deep-modules`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Encapsular regras de negócio atrás de interfaces pequenas e testáveis. Prefira as Costuras existentes e mantenha validação e autorização explícitas na Fronteira.

## 2. Regras Inegociáveis
- **Declare tipos estritos em código PHP:** Inicie arquivos de código PHP com `declare(strict_types=1);`. Templates `.blade.php` ficam fora desta regra.
- **Preserve a arquitetura existente:** Antes de criar classes, identifique a Costura pública e a complexidade que ela esconde. Não converta código vizinho só para impor este padrão.
- **Mantenha a Fronteira magra:** Valide entrada e autorização na Fronteira. Extraia regras, transações e coordenação quando houver complexidade a encapsular. CRUD trivial pode continuar no Controller/Livewire se seguir a arquitetura do projeto e permanecer testável.
- **Proteja o estado público do Livewire:** Adicione o atributo `#[Locked]` em qualquer propriedade pública de componente Livewire que armazene IDs ou estados que o cliente não pode manipular no frontend.
- **Escolha dados pelo contrato:** Prefira DTO `final readonly` quando vários campos, invariantes ou consumidores pedirem um contrato explícito. Reutilize tipos existentes; valores escalares ou dados validados locais bastam para operações simples. Não crie DTO que apenas repassa campos sem benefício.
- **Desenhe interfaces pequenas:** Para uma nova Action, prefira `handle()` e encapsule o fluxo relevante. Preserve assinaturas públicas já estabelecidas. Justifique a escolha ou exceção no ticket/Spec em uma frase; não crie ADR só por isso.
- **Torne o estado inválido impossível de escrever:** Use `enum`, DTO `readonly` e tipos estritos para que o PHPStan recuse o valor inválido. Não silencie o PHPStan com `@phpstan-ignore` nem com uma entrada nova no baseline.
- **Valide uma vez, na entrada:** O `FormRequest` ou o `Livewire\Form` valida e converte a entrada em tipos ou DTO. Dentro da Costura, confie no dado. Não repita a validação nem espalhe `if ($x !== null)` defensivos.
- **Torne a operação repetível:** Job com retry, webhook, comando agendado e duplo clique no Livewire executam a mesma operação de novo. Executar 2 vezes, ou de novo depois de uma falha no meio, deixa o mesmo estado final. Use índice único com `upsert`, chave de idempotência, `ShouldBeUnique` ou a conferência do estado dentro da transação.
- **Dê um só escritor ao estado compartilhado:** Se dois processos não precisam do mesmo registro mutável, dê a cada um o seu. Se precisam, garanta um só escritor na estrutura: `lockForUpdate()` na transação, `increment()` atômico ou job com `WithoutOverlapping`.

## 3. Exemplo de Action com contrato tipado

```php
<?php

declare(strict_types=1);

namespace App\Data;

use App\Enums\OrderStatus;

final readonly class ApproveOrderData
{
    public function __construct(
        public int $orderId,
        public int $approverId,
        public OrderStatus $status,
    ) {}
}
```

```php
<?php

declare(strict_types=1);

namespace App\Actions\Orders;

use App\Data\ApproveOrderData;
use App\Models\Order;
use Illuminate\Support\Facades\DB;

final readonly class ApproveOrderAction
{
    public function handle(ApproveOrderData $data): Order
    {
        return DB::transaction(function () use ($data): Order {
            $order = Order::query()->lockForUpdate()->findOrFail($data->orderId);
            $order->update([
                'status' => $data->status,
                'approved_by' => $data->approverId,
            ]);

            return $order;
        });
    }
}
```

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "A query Eloquent tem apenas 4 linhas, vou colocá-la direto no método `save()` do componente Livewire." | Avalie o comportamento: CRUD trivial pode ficar na Fronteira; regras, transações e coordenação pedem uma Costura própria. O número de linhas não decide sozinho. |
| "Vou passar `$request->validated()` como `array` direto para a Action." | Prefira DTO quando estabiliza um contrato entre módulos. Não adicione uma classe apenas para repassar dados validados locais. |
| "Vou criar uma interface `ApproveOrderActionInterface` mesmo tendo apenas uma implementação." | **Proibido (Anti-Shallow Module).** Não crie interfaces pass-through sem necessidade real de múltiplas implementações. |
| "O job tem `$tries = 3`; se falhar, ele roda de novo e pronto." | **Proibido.** A nova tentativa repete as escritas que já aconteceram. Prove que a 2ª execução deixa o mesmo estado. |
| "O PHPStan reclama do tipo; ponho `@phpstan-ignore` e sigo." | **Proibido.** O erro aponta um estado inválido possível. Corrija o tipo ou a origem do dado. |

## 5. Prova de Execução (Critério de Saída)
Quando houver alteração PHP, aplique o alcance de `laravel-verification`. Em desenho ou documentação, registre a decisão sem executar ferramentas PHP só por carregar esta disciplina.
- `[measured]` Arquivos de código PHP criados ou editados (exceto templates `.blade.php`) contêm `declare(strict_types=1);`.
- `[measured]` Costura escolhida e complexidade encapsulada identificadas; exceção ao padrão explicada quando aplicável.
- `[measured]` Zero erros reportados por `./vendor/bin/phpstan analyse`, sem `@phpstan-ignore` nem entrada nova no baseline.
- `[measured]` Para cada operação repetível do diff (job, webhook, comando agendado ou ação Livewire que grava): um teste que a executa 2 vezes e confere o mesmo estado final.
