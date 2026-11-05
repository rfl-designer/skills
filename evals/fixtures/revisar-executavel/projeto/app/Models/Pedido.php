<?php

declare(strict_types=1);

namespace App\Models;

use App\Enums\StatusPedido;
use Database\Factories\PedidoFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

final class Pedido extends Model
{
    /** @use HasFactory<PedidoFactory> */
    use HasFactory;

    protected $fillable = ['cliente_id', 'total_centavos', 'status', 'aprovado_em'];

    protected function casts(): array
    {
        return [
            'status' => StatusPedido::class,
            'aprovado_em' => 'datetime',
        ];
    }

    public function cliente(): BelongsTo
    {
        return $this->belongsTo(Cliente::class);
    }
}
