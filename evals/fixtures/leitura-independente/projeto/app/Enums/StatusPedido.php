<?php

declare(strict_types=1);

namespace App\Enums;

enum StatusPedido: string
{
    case Pendente = 'pendente';
    case Aprovado = 'aprovado';
    case Cancelado = 'cancelado';
}
