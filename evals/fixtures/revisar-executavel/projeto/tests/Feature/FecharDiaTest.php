<?php

declare(strict_types=1);

use App\Actions\FecharDia;
use App\Enums\StatusPedido;
use App\Models\Cliente;
use App\Models\Pedido;

it('debita do Saldo os Pedidos aprovados no dia', function (): void {
    $cliente = Cliente::factory()->create(['saldo_centavos' => 10_000]);
    Pedido::factory()->for($cliente)->aprovado()->create(['total_centavos' => 2_500]);
    Pedido::factory()->for($cliente)->create(['total_centavos' => 500]);
    Pedido::factory()->for($cliente)->create([
        'status' => StatusPedido::Aprovado,
        'aprovado_em' => now()->subDay(),
        'total_centavos' => 1_000,
    ]);

    app(FecharDia::class)->handle();

    expect($cliente->fresh()->saldo_centavos)->toBe(7_500);
});
