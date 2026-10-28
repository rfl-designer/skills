<?php

declare(strict_types=1);

namespace App\Actions;

use App\Enums\StatusPedido;
use App\Models\Pedido;
use Illuminate\Support\Facades\DB;

final class FecharDia
{
    public function handle(): void
    {
        DB::transaction(function (): void {
            Pedido::query()
                ->where('status', StatusPedido::Aprovado)
                ->whereDate('aprovado_em', today())
                ->with('cliente')
                ->lockForUpdate()
                ->each(function (Pedido $pedido): void {
                    $pedido->cliente->decrement('saldo_centavos', $pedido->total_centavos);
                });
        });
    }
}
