<?php

declare(strict_types=1);

use App\Enums\StatusPedido;
use App\Livewire\Pedidos\Lista;
use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\User;
use Livewire\Livewire;

it('estorno com falha na devolução do Saldo não deixa o Pedido Cancelado', function (): void {
    $cliente = Cliente::factory()->create(['saldo_centavos' => 1_000]);
    $pedido = Pedido::factory()->for($cliente)->aprovado()->create(['total_centavos' => 2_500]);
    Cliente::updating(function (): void {
        throw new RuntimeException('falha forçada na devolução do Saldo');
    });

    try {
        Livewire::actingAs(User::factory()->gerente()->create())
            ->test(Lista::class)
            ->call('estornar', $pedido->id);
    } catch (RuntimeException) {
    }

    expect($pedido->fresh()->status)->toBe(StatusPedido::Aprovado)
        ->and($cliente->fresh()->saldo_centavos)->toBe(1_000);
});
