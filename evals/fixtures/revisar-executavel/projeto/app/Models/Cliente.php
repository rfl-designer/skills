<?php

declare(strict_types=1);

namespace App\Models;

use Database\Factories\ClienteFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

final class Cliente extends Model
{
    /** @use HasFactory<ClienteFactory> */
    use HasFactory;

    protected $fillable = ['user_id', 'saldo_centavos'];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function pedidos(): HasMany
    {
        return $this->hasMany(Pedido::class);
    }
}
