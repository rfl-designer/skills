<?php

declare(strict_types=1);

use App\Livewire\Pedidos\Lista;
use App\Models\Pedido;
use App\Models\User;
use Illuminate\Database\Eloquent\LazyLoadingViolationException;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;
use Livewire\Livewire;

// R1. N+1 do Aprovador: a lista do Gerente lê `aprovador` sem `with()`.
it('R1: a lista do Gerente não carrega o Aprovador por linha', function (): void {
    $gerente = User::factory()->gerente()->create();
    Pedido::factory()->count(2)->aprovado()->create(['aprovado_por' => $gerente->id]);
    Model::preventLazyLoading();

    try {
        Livewire::actingAs($gerente)->test(Lista::class)->assertOk();
    } finally {
        Model::preventLazyLoading(false);
    }
})->throwsNoExceptions();

it('R1: a lista do Gerente faz o mesmo número de consultas com 2 e com 20 Pedidos', function (): void {
    $gerente = User::factory()->gerente()->create();
    $contar = function () use ($gerente): int {
        DB::flushQueryLog();
        DB::enableQueryLog();
        Livewire::actingAs($gerente)->test(Lista::class);

        return count(DB::getQueryLog());
    };

    Pedido::factory()->count(2)->aprovado()->create(['aprovado_por' => User::factory()->gerente()]);
    $com2 = $contar();
    Pedido::factory()->count(18)->aprovado()->create(['aprovado_por' => User::factory()->gerente()]);

    expect($contar())->toBe($com2);
});

// R2. Fuso: a Spec pede a data e a hora no fuso da loja, America/Sao_Paulo.
it('R2: mostra a aprovação no fuso da loja', function (): void {
    $gerente = User::factory()->gerente()->create();
    Pedido::factory()->aprovado()->create([
        'aprovado_por' => $gerente->id,
        'aprovado_em' => '2026-03-10 01:30:00',
    ]);

    Livewire::actingAs($gerente)
        ->test(Lista::class)
        ->assertSee('09/03/2026 22:30');
});
