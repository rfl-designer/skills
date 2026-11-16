# Perfil Laravel de `deep-modules`

Leia este perfil só quando o projeto usa PHP com Laravel. Ele traduz as regras da skill; não acrescenta regra nova. Os comandos da configuração do projeto prevalecem sobre os exemplos.

## Tradução das regras

| Regra da skill | Em PHP, Laravel e Livewire |
|---|---|
| Modo mais estrito da linguagem | Inicie cada arquivo de código PHP com `declare(strict_types=1);`. Templates `.blade.php` ficam fora desta regra. |
| Fronteira | Controller com `FormRequest`, componente Livewire com `Livewire\Form`, comando Artisan, job ou listener. |
| Costura | Action com `handle()`, ou o serviço ou Model que o projeto já usa. CRUD trivial pode ficar no Controller ou no componente Livewire. |
| Estado que o cliente controla | Adicione `#[Locked]` em cada propriedade pública de componente Livewire que guarda um ID ou um estado que o cliente não pode alterar. Autorize a ação com `$this->authorize()` ou Policy. |
| Contrato de dados | DTO `final readonly`. `$request->validated()` como `array` basta para uma operação local simples. |
| Estado inválido impossível | `enum`, DTO `readonly` e tipos estritos, conferidos pelo PHPStan ou Larastan. Não use `@phpstan-ignore` nem uma entrada nova no baseline. |
| Validação na entrada | O `FormRequest` ou o `Livewire\Form` valida e converte. Não espalhe `if ($x !== null)` dentro da Costura. |
| Operação repetível | Job com `$tries`, webhook, comando agendado e duplo clique no Livewire. Use índice único com `upsert`, chave de idempotência, `ShouldBeUnique` ou a conferência do estado dentro de `DB::transaction()`. |
| Um só escritor | `lockForUpdate()` na transação, `increment()` atômico ou job com `WithoutOverlapping`. |

## Exemplo de Action com contrato tipado

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

## Prova de execução neste perfil
- `[measured]` Arquivos de código PHP criados ou editados, exceto templates `.blade.php`, contêm `declare(strict_types=1);`.
- `[measured]` Zero erros em `./vendor/bin/phpstan analyse`, ou no comando de análise da configuração, sem `@phpstan-ignore` nem entrada nova no baseline.
