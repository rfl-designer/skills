<?php

declare(strict_types=1);

use App\Livewire\Pedidos\Lista;
use App\Models\Pedido;
use App\Models\User;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;
use Livewire\Livewire;

// Achado 1: a lista do Gerente lê `aprovador` sem with().
it('a lista do Gerente faz o mesmo número de consultas com 2 e com 200 Pedidos', function (): void {
    $gerente = User::factory()->gerente()->create();
    $contar = function () use ($gerente): int {
        DB::flushQueryLog();
        DB::enableQueryLog();
        Livewire::actingAs($gerente)->test(Lista::class);

        return count(DB::getQueryLog());
    };

    Pedido::factory()->count(2)->aprovado()->create(['aprovado_por' => $gerente->id]);
    $com2 = $contar();
    Pedido::factory()->count(198)->aprovado()->create(['aprovado_por' => $gerente->id]);

    expect($contar())->toBe($com2);
});

it('a lista do Gerente não carrega o Aprovador por linha', function (): void {
    $gerente = User::factory()->gerente()->create();
    Pedido::factory()->count(2)->aprovado()->create(['aprovado_por' => $gerente->id]);
    Model::preventLazyLoading();

    try {
        Livewire::actingAs($gerente)->test(Lista::class)->assertOk();
    } finally {
        Model::preventLazyLoading(false);
    }
})->throwsNoExceptions();
