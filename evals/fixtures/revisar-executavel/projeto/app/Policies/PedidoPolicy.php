<?php

declare(strict_types=1);

namespace App\Policies;

use App\Enums\StatusPedido;
use App\Models\Pedido;
use App\Models\User;

final class PedidoPolicy
{
    public function view(User $user, Pedido $pedido): bool
    {
        return $user->isGerente() || $pedido->cliente->user_id === $user->id;
    }

    public function aprovar(User $user, Pedido $pedido): bool
    {
        return $user->isGerente() && $pedido->status === StatusPedido::Pendente;
    }

    public function cancelar(User $user, Pedido $pedido): bool
    {
        return $pedido->cliente->user_id === $user->id
            && $pedido->status === StatusPedido::Pendente;
    }
}
