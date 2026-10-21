---
name: laravel-deep-modules
description: Disciplina arquitetural de Módulos Profundos para PHP, Laravel e Livewire. Use ao desenhar, planejar, implementar ou revisar Actions, DTOs, Models, Controllers e componentes Livewire.
---

# Módulos Profundos no Laravel e Livewire (`laravel-deep-modules`)

## 1. Objetivo
Garantir que toda regra de negócio viva dentro de Módulos Profundos (`Actions` / `Services` com DTOs tipados), mantendo as Fronteiras do Sistema (`Livewire`, `Controllers`, `FormRequests`) estritamente magras.

## 2. Regras Inegociáveis
- **Declare tipos estritos em todos os arquivos PHP:** Inicie cada arquivo PHP com `declare(strict_types=1);`.
- **Mantenha a Fronteira magra:** Componentes `Livewire` (e `Livewire\Form`) e `Controllers` apenas validam entrada, verificam autorização (`$this->authorize()`), convertem dados para um DTO e delegam para uma `Action`.
- **Proteja o estado público do Livewire:** Adicione o atributo `#[Locked]` em qualquer propriedade pública de componente Livewire que armazene IDs ou estados que o cliente não pode manipular no frontend.
- **Proíba arrays associativos soltos entre camadas:** Transporte dados da fronteira para a `Action` usando uma classe `final readonly` (DTO) ou `enum` nativo do PHP 8.2+.
- **Desenhe a `Action` como Módulo Profundo:** Cada `Action` expõe um único método público `handle()` (a Costura / Seam) e encapsula transações (`DB::transaction`), queries Eloquent e disparos de eventos.

## 3. Padrão de Código Obrigatório (Costura e Fronteira)

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
| "A query Eloquent tem apenas 4 linhas, vou colocá-la direto no método `save()` do componente Livewire." | **Proibido.** Mutações e regras de negócio pertencem a uma `Action` testável na Costura. |
| "Vou passar `$request->validated()` como `array` direto para a Action." | **Proibido.** Crie ou use um DTO `final readonly` para garantir verificação estática no Larastan. |
| "Vou criar uma interface `ApproveOrderActionInterface` mesmo tendo apenas uma implementação." | **Proibido (Anti-Shallow Module).** Não crie interfaces pass-through sem necessidade real de múltiplas implementações. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Todos os arquivos `.php` criados ou editados contêm `declare(strict_types=1);`.
- `[measured]` Zero erros reportados por `./vendor/bin/phpstan analyse`.
