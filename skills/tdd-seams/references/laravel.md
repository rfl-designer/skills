# Perfil Laravel de `tdd-seams`

Leia este perfil só quando o projeto usa PHP com Laravel e Pest. Ele traduz as regras da skill; não acrescenta regra nova. Os comandos da configuração do projeto prevalecem sobre os exemplos.

## Tradução das regras

| Regra da skill | Em Pest, Laravel e Livewire |
|---|---|
| Executor de testes | `./vendor/bin/pest`; teste focado com `./vendor/bin/pest --filter=<NomeDoTeste>`. Respeite o executor do projeto, como o Sail. |
| Costura | Action, ou o serviço ou Model que o projeto já usa. |
| Fronteira | `Livewire::test()` para componentes Livewire, inclusive a tentativa de `set()` numa propriedade `#[Locked]`. Teste HTTP para Controllers. |
| Mocks internos da persistência | Nunca faça mock de `Builder`, `Model` ou repositórios internos. Use `RefreshDatabase` (ou `lazilyRefreshDatabase`) com Factories reais. |
| Fronteiras externas reais | `Http::fake()`, `Bus::fake()`, `Queue::fake()`, `Mail::fake()` ou `Storage::fake()`. |
| Testes de arquitetura | Pest Arch Tests em `tests/ArchTest.php`. |

**ATENÇÃO:** `RefreshDatabase` roda `migrate:fresh` num banco que não está em memória. Esse comando apaga todas as tabelas. Confira o banco de testes em `phpunit.xml` antes da primeira execução.

## Padrão de testes (Pest)

```php
<?php

declare(strict_types=1);

use App\Actions\Orders\ApproveOrderAction;
use App\Data\ApproveOrderData;
use App\Enums\OrderStatus;
use App\Livewire\Orders\ApproveOrderModal;
use App\Models\Order;
use App\Models\User;
use Livewire\Livewire;

it('aprova um pedido na costura da Action', function (): void {
    $approver = User::factory()->create();
    $order = Order::factory()->pending()->create();

    $action = app(ApproveOrderAction::class);
    $updated = $action->handle(new ApproveOrderData(
        orderId: $order->id,
        approverId: $approver->id,
        status: OrderStatus::Approved,
    ));

    expect($updated->status)->toBe(OrderStatus::Approved)
        ->and($updated->approved_by)->toBe($approver->id);
});

it('bloqueia usuário sem permissão na fronteira do Livewire', function (): void {
    $unauthorizedUser = User::factory()->create();
    $order = Order::factory()->pending()->create();

    Livewire::actingAs($unauthorizedUser)
        ->test(ApproveOrderModal::class, ['orderId' => $order->id])
        ->call('approve')
        ->assertForbidden();
});
```

## Exemplo de Pest Architecture Test (`tests/ArchTest.php`)
Aplique as convenções aos módulos adotados pelo projeto; não force migração de DTOs existentes só para satisfazer este exemplo.

```php
<?php

declare(strict_types=1);

arch('arquivos PHP usam strict_types')
    ->expect('App')
    ->toUseStrictTypes();

arch('DTOs são final e readonly')
    ->expect('App\Data')
    ->toBeFinal()
    ->toBeReadonly();

arch('código de produção não contém helpers de debug')
    ->expect(['dd', 'dump', 'ray'])
    ->not->toBeUsed();
```

## Racionalizações neste perfil
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou usar `Mockery::mock(Order::class)` para o teste rodar sem banco." | **Proibido.** Mocks de Eloquent mentem sobre SQL e relacionamentos. Use Factories + `RefreshDatabase`. |
| "Vou usar `ReflectionClass` para testar um método `private` da Action." | **Proibido.** Teste a interface pública escolhida. |
| "`expect($pedido)->not->toBeNull()` já cobre a Action." | **Proibido.** Afirme o status, o valor e o registro gravado. |
