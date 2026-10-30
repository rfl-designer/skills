---
name: laravel-tdd-seams
description: Disciplina de Test-Driven Development (TDD) com Pest focada em Costuras de Actions, componentes Livewire e Architecture Tests. Use ao escrever ou revisar testes em projetos Laravel, e quando duas correções seguidas falham no mesmo teste ou portão.
---

# TDD na Costura com Pest (`laravel-tdd-seams`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Objetivo
Garantir que todo comportamento seja guiado por testes no Pest focados nas Costuras públicas (`Actions` e Fronteiras `Livewire`/HTTP), proibindo mocks frágeis de detalhes internos.

## 2. Regras Inegociáveis
- **Teste comportamento, nunca implementação:** Avalie a saída da Costura escolhida, o estado gravado no banco de dados e a resposta do componente `Livewire`.
- **Apague o teste que passa com a Costura vazia:** Imagine a Costura a devolver `null` ou uma coleção vazia, sem gravar nada. Se o teste ainda passa, ele não prova a regra. Reescreva-o para afirmar o valor e o estado que o usuário vê.
- **Não escreva um teste falso:** Às vezes, um teste honesto não é possível: condição de corrida, carga, serviço externo sem fake. Então, não escreva um teste que não prova nada. Registre o motivo e use a prova mais próxima, como a contagem de queries ou o índice único no schema. Marque essa prova como `parcial`; sem prova, marque `não verificado`. Esta saída não dispensa o RED dos outros comportamentos.
- **Ataque a premissa:** Duas correções com a mesma premissa falharam no mesmo teste ou portão. Pare e reverta as duas. Escreva essa premissa numa frase. Prove ou refute a premissa com uma execução, como um teste ou uma query. Não comece a 3ª correção antes dessa prova. Com a premissa refutada, volte às hipóteses.
- **Proíba mocks internos do Eloquent:** Nunca faça mock de `Builder`, `Model` ou repositórios internos. Use `RefreshDatabase` (ou `lazilyRefreshDatabase`) com Factories reais do Laravel.
- **Use mocks apenas em fronteiras externas reais:** Use `Http::fake()`, `Bus::fake()`, `Queue::fake()`, `Mail::fake()` ou `Storage::fake()` apenas para isolar rede e I/O externo.
- **Teste a Costura e a Superfície:**
  1. Teste regras pela Costura pública escolhida (Action ou módulo existente). CRUD trivial pode ser coberto na Fronteira sem criar Action/DTO só para o teste.
  2. Teste autorização, validação e integração na Fronteira usada pelo projeto: `Livewire::test()` para Livewire (incluindo `#[Locked]`) ou teste HTTP para Controllers. Prove interação de UI no navegador quando aplicável.
- **Proteja a arquitetura com Pest Arch Tests:** Mantenha um teste de arquitetura em `tests/ArchTest.php` que codifique as restrições estruturais do projeto.

## 3. Padrão de Testes Obrigatório (Pest)

```php
<?php

declare(strict_types=1);

use App\Actions\Orders\ApproveOrderAction;
use App\Data\ApproveOrderData;
use App\Enums\OrderStatus;
use App\Livewire\Orders\ApproveOrderModal;
use App\Models\Order;
use App\Models\User;
use Livewire\Livewire;

it('aprova um pedido na costura da Action', function (): void {
    $approver = User::factory()->create();
    $order = Order::factory()->pending()->create();

    $action = app(ApproveOrderAction::class);
    $updated = $action->handle(new ApproveOrderData(
        orderId: $order->id,
        approverId: $approver->id,
        status: OrderStatus::Approved,
    ));

    expect($updated->status)->toBe(OrderStatus::Approved)
        ->and($updated->approved_by)->toBe($approver->id);
});

it('bloqueia usuário sem permissão na fronteira do Livewire', function (): void {
    $unauthorizedUser = User::factory()->create();
    $order = Order::factory()->pending()->create();

    Livewire::actingAs($unauthorizedUser)
        ->test(ApproveOrderModal::class, ['orderId' => $order->id])
        ->call('approve')
        ->assertForbidden();
});
```

### Exemplo de Pest Architecture Test (`tests/ArchTest.php`)
Aplique as convenções aos módulos adotados pelo projeto; não force migração de DTOs existentes só para satisfazer este exemplo.
```php
<?php

declare(strict_types=1);

arch('arquivos PHP usam strict_types')
    ->expect('App')
    ->toUseStrictTypes();

arch('DTOs são final e readonly')
    ->expect('App\Data')
    ->toBeFinal()
    ->toBeReadonly();

arch(' código de produção não contém helpers de debug')
    ->expect(['dd', 'dump', 'ray'])
    ->not->toBeUsed();
```

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Vou usar `Mockery::mock(Order::class)` para o teste rodar sem banco." | **Proibido.** Mocks de Eloquent mentem sobre SQL e relacionamentos. Use Factories + `RefreshDatabase`. |
| "Vou usar `ReflectionClass` para testar um método `private` da Action." | **Proibido.** Métodos privados são detalhes de implementação. Teste a interface pública escolhida. |
| "Vou escrever o código primeiro e adicionar o teste depois." | **Proibido.** Siga o ciclo RED → GREEN → REFACTOR. |
| "`expect($pedido)->not->toBeNull()` já cobre a Action." | **Proibido.** Esse teste passa com quase qualquer retorno. Afirme o status, o valor e o registro gravado. |
| "Não consigo testar a condição de corrida; escrevo um teste que só chama o método." | **Proibido.** Um teste que não pode falhar esconde a lacuna. Registre o motivo e a prova mais próxima, marcada `parcial`. |
| "A 2ª correção também falhou; tento uma 3ª variação." | **Proibido.** Duas falhas com a mesma premissa indicam uma premissa errada. Escreva a premissa e prove-a antes de outra correção. |

## 5. Prova de Execução (Critério de Saída)
- `[measured]` Teste visto falhando (`RED`) antes da implementação e passando (`GREEN`) depois via `./vendor/bin/pest`.
- `[measured]` Depois de 2 correções com a mesma premissa sem GREEN: a premissa numa frase e a execução que a prova ou refuta.
