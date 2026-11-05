<?php

declare(strict_types=1);

use App\Actions\AprovarPedido;
use App\Actions\FecharDia;
use App\Enums\StatusPedido;
use App\Livewire\Pedidos\Lista;
use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\User;
use App\Notifications\PedidoAprovado;
use Illuminate\Database\Eloquent\LazyLoadingViolationException;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Notification;
use Illuminate\Support\Facades\Schema;
use Livewire\Livewire;

// D1. Ação sem autorização: o Cliente aprova o próprio Pedido pela lista.
it('D1: o Cliente recebe 403 e o Pedido não muda', function (): void {
    Notification::fake();
    $cliente = Cliente::factory()->create();
    $pedido = Pedido::factory()->for($cliente)->create();

    Livewire::actingAs($cliente->user)
        ->test(Lista::class)
        ->call('aprovar', $pedido->id)
        ->assertForbidden();

    expect($pedido->fresh()->status)->toBe(StatusPedido::Pendente);
});

// D2. Aprovação repetida: 2 chamadas gravam 2 vezes e enviam 2 e-mails.
it('D2: 2 chamadas enviam um só e-mail', function (): void {
    Notification::fake();
    $gerente = User::factory()->gerente()->create();
    $pedido = Pedido::factory()->create();

    app(AprovarPedido::class)->handle($pedido, $gerente);
    app(AprovarPedido::class)->handle($pedido->fresh(), $gerente);

    Notification::assertSentToTimes($pedido->cliente->user, PedidoAprovado::class, 1);
});

// D3. O comando ignora --gerente e grava o primeiro Gerente do banco.
it('D3: o comando grava o Gerente de --gerente', function (): void {
    Notification::fake();
    User::factory()->gerente()->create();
    $segundo = User::factory()->gerente()->create();
    $pedido = Pedido::factory()->create();

    $this->artisan('pedidos:aprovar', ['pedido' => $pedido->id, '--gerente' => $segundo->id]);

    expect($pedido->fresh()->aprovado_por)->toBe($segundo->id);
});

// D4. O comando não recusa mais o Pedido que não está Pendente.
it('D4: o comando recusa o Pedido aprovado ontem e o Saldo não cai 2 vezes', function (): void {
    Notification::fake();
    $gerente = User::factory()->gerente()->create();
    $cliente = Cliente::factory()->create(['saldo_centavos' => 10_000]);
    $pedido = Pedido::factory()->for($cliente)->create([
        'status' => StatusPedido::Aprovado,
        'aprovado_em' => now()->subDay(),
        'total_centavos' => 2_500,
    ]);

    $this->artisan('pedidos:aprovar', ['pedido' => $pedido->id, '--gerente' => $gerente->id])
        ->expectsOutput('O pedido não está pendente.')
        ->assertFailed();
    app(FecharDia::class)->handle();

    expect($cliente->fresh()->saldo_centavos)->toBe(10_000);
});

it('D4: o comando recusa o Pedido Cancelado', function (): void {
    Notification::fake();
    $gerente = User::factory()->gerente()->create();
    $pedido = Pedido::factory()->create(['status' => StatusPedido::Cancelado]);

    $this->artisan('pedidos:aprovar', ['pedido' => $pedido->id, '--gerente' => $gerente->id])
        ->assertFailed();

    expect($pedido->fresh()->status)->toBe(StatusPedido::Cancelado);
});

// D6. N+1 do Aprovador na lista do Gerente.
it('D6: a lista do Gerente não carrega o Aprovador por linha', function (): void {
    Model::preventLazyLoading();
    $gerente = User::factory()->gerente()->create();
    Pedido::factory()->count(2)->aprovado()->create(['aprovado_por' => $gerente->id]);

    Livewire::actingAs($gerente)->test(Lista::class)->assertOk();
})->throwsNoExceptions();

// C1. A migration só acrescenta uma coluna nula: os Pedidos antigos ficam.
it('C1: aprovado_por é nula', function (): void {
    $pedido = Pedido::factory()->create();

    expect(Schema::hasColumn('pedidos', 'aprovado_por'))->toBeTrue()
        ->and($pedido->fresh()->aprovado_por)->toBeNull();
});

// C2. O e-mail sai depois do commit da transação.
it('C2: o e-mail sai depois do commit', function (): void {
    Notification::fake();
    $gerente = User::factory()->gerente()->create();
    $pedido = Pedido::factory()->create();

    app(AprovarPedido::class)->handle($pedido, $gerente);

    expect($pedido->fresh()->status)->toBe(StatusPedido::Aprovado);
    Notification::assertSentToTimes($pedido->cliente->user, PedidoAprovado::class, 1);
});

// Defeito da base: o Pedido aprovado entre 23h59 e 0h nunca é debitado.
it('Base: o Pedido aprovado às 23h59min30s é debitado', function (): void {
    $cliente = Cliente::factory()->create(['saldo_centavos' => 10_000]);
    $pedido = Pedido::factory()->for($cliente)->create(['total_centavos' => 2_500]);

    $this->travelTo(now()->setTime(23, 59, 0));
    app(FecharDia::class)->handle();
    $this->travelTo(now()->setTime(23, 59, 30));
    $pedido->update(['status' => StatusPedido::Aprovado, 'aprovado_em' => now()]);
    $this->travelTo(now()->addDay()->setTime(23, 59, 0));
    app(FecharDia::class)->handle();

    expect($cliente->fresh()->saldo_centavos)->toBe(7_500);
});
