<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Foundation\Auth\User as Authenticatable;

final class User extends Authenticatable
{
    protected $fillable = ['name', 'email', 'password', 'papel'];

    public function cliente(): HasOne
    {
        return $this->hasOne(Cliente::class);
    }

    public function isGerente(): bool
    {
        return $this->papel === 'gerente';
    }
}
