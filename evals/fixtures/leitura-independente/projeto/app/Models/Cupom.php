<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

final class Cupom extends Model
{
    protected $table = 'cupons';

    protected $fillable = ['codigo', 'percentual', 'valido_ate', 'ativo'];

    protected function casts(): array
    {
        return [
            'valido_ate' => 'date',
            'ativo' => 'boolean',
        ];
    }
}
