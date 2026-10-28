<?php

declare(strict_types=1);

use App\Livewire\Pedidos\Lista;
use Illuminate\Support\Facades\Route;

Route::middleware('auth')->group(function (): void {
    Route::get('/pedidos', Lista::class)->name('pedidos.lista');
});
