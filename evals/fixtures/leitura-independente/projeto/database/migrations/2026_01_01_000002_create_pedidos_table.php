<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('pedidos', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('cliente_id')->constrained();
            $table->unsignedBigInteger('total_centavos');
            $table->string('status')->default('pendente');
            $table->timestamp('aprovado_em')->nullable();
            $table->timestamps();
        });
    }
};
