<?php

declare(strict_types=1);

use App\Actions\FecharDia;
use Illuminate\Support\Facades\Schedule;

Schedule::call(fn () => app(FecharDia::class)->handle())
    ->name('fechar-dia')
    ->dailyAt('23:59')
    ->onOneServer();
