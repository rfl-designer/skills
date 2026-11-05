<?php

declare(strict_types=1);

namespace Database\Factories;

use App\Enums\StatusPedido;
use App\Models\Cliente;
use App\Models\Pedido;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Pedido>
 */
final class PedidoFactory extends Factory
{
    protected $model = Pedido::class;

    /**
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'cliente_id' => Cliente::factory(),
            'total_centavos' => fake()->numberBetween(1_000, 50_000),
            'status' => StatusPedido::Pendente,
            'aprovado_em' => null,
        ];
    }

    public function aprovado(): self
    {
        return $this->state([
            'status' => StatusPedido::Aprovado,
            'aprovado_em' => now(),
        ]);
    }
}
