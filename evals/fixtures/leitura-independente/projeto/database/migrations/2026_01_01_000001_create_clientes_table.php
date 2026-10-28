<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('clientes', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('user_id')->constrained();
            $table->bigInteger('saldo_centavos')->default(0);
            $table->timestamps();
        });
    }
};
