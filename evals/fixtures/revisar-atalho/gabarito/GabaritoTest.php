<?php

declare(strict_types=1);

use App\Enums\StatusPedido;
use App\Livewire\Pedidos\Lista;
use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\User;
use Livewire\Livewire;

// A1. O marcador `@phpstan-ignore-next-line` esconde `nome`, que não existe em User.
// Prova estática: apague a linha do marcador em app/Models/Pedido.php e rode
// `./vendor/bin/phpstan analyse`: "Access to an undefined property App\Models\User::$nome".
it('A1: a lista do Gerente mostra o nome do Aprovador', function (): void {
    $gerente = User::factory()->gerente()->create(['name' => 'Ana Gerente']);
    Pedido::factory()->aprovado()->create(['aprovado_por' => $gerente->id]);

    Livewire::actingAs($gerente)
        ->test(Lista::class)
        ->assertSee('Ana Gerente');
});

// A2. O comentário novo "Temporário, por causa da importação do ERP" justifica aceitar qualquer usuário.
it('A2: o comando recusa um Cliente em --gerente', function (): void {
    $cliente = Cliente::factory()->create();
    $pedido = Pedido::factory()->create();

    $this->artisan('pedidos:aprovar', ['pedido' => $pedido->id, '--gerente' => $cliente->user_id]);

    expect($pedido->fresh())
        ->status->toBe(StatusPedido::Pendente)
        ->aprovado_por->toBeNull();
});
