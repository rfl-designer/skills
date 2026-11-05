<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Enums\StatusPedido;
use App\Models\Pedido;
use Illuminate\Console\Command;

final class AprovarPedido extends Command
{
    protected $signature = 'pedidos:aprovar {pedido}';

    protected $description = 'Aprova um Pedido pendente. O suporte usa este comando a pedido do Gerente.';

    public function handle(): int
    {
        $pedido = Pedido::findOrFail($this->argument('pedido'));

        if ($pedido->status !== StatusPedido::Pendente) {
            $this->error('O pedido não está pendente.');

            return self::FAILURE;
        }

        $pedido->update(['status' => StatusPedido::Aprovado, 'aprovado_em' => now()]);

        return self::SUCCESS;
    }
}
