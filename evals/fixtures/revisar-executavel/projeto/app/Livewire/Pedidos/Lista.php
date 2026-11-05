<?php

declare(strict_types=1);

namespace App\Livewire\Pedidos;

use App\Models\Pedido;
use Illuminate\Contracts\View\View;
use Livewire\Component;

final class Lista extends Component
{
    public function render(): View
    {
        $user = auth()->user();

        $pedidos = $user->isGerente()
            ? Pedido::query()->with('cliente.user')->latest()->get()
            : Pedido::query()->whereBelongsTo($user->cliente)->latest()->get();

        return view('livewire.pedidos.lista', ['pedidos' => $pedidos]);
    }
}
