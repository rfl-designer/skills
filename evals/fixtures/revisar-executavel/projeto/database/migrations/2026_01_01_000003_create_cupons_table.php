<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('cupons', function (Blueprint $table): void {
            $table->id();
            $table->string('codigo', 20)->unique();
            $table->unsignedTinyInteger('percentual');
            $table->date('valido_ate');
            $table->boolean('ativo')->default(true);
            $table->timestamps();
        });
    }
};
