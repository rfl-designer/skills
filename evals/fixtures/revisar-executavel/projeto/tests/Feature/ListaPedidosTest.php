<?php

declare(strict_types=1);

use App\Livewire\Pedidos\Lista;
use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\User;
use Livewire\Livewire;

it('mostra ao Cliente só os próprios Pedidos', function (): void {
    $cliente = Cliente::factory()->create();
    $proprio = Pedido::factory()->for($cliente)->create(['total_centavos' => 1_234]);
    Pedido::factory()->create(['total_centavos' => 9_876]);

    Livewire::actingAs($cliente->user)
        ->test(Lista::class)
        ->assertSee('12,34')
        ->assertDontSee('98,76');
});

it('mostra ao Gerente todos os Pedidos', function (): void {
    Pedido::factory()->create(['total_centavos' => 1_234]);
    Pedido::factory()->create(['total_centavos' => 9_876]);

    Livewire::actingAs(User::factory()->gerente()->create())
        ->test(Lista::class)
        ->assertSee('12,34')
        ->assertSee('98,76');
});
