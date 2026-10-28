# Regras de camada

Uma regra liga uma camada a uma expressão regular. O diagrama aplica a expressão ao caminho do arquivo. Numa renomeação, o diagrama usa o caminho novo.

## Formato

- Uma regra por linha: `Camada: expressão regular`.
- O primeiro `:` separa o nome da expressão. O nome não pode ter `:`.
- A expressão usa a sintaxe de `RegExp` do JavaScript, sem barras e sem flags. A diferença entre maiúsculas e minúsculas conta.
- A ordem das linhas é a prioridade. A primeira regra que combina define a camada.
- Linhas vazias e linhas que começam com `#` não contam.
- Um arquivo sem regra vai para a camada `Outros`.
- Uma linha inválida não para o diagrama. O diagrama ignora a linha e mostra um alerta com o número da linha.

## Regras padrão

O modelo [slice.html](../assets/slice.html) guarda estas regras no bloco `camadas-padrao`. Um teste do pacote confere que os dois textos são iguais.

```text
# Regras padrão. A primeira regra que combina com o caminho define a camada.
Testes: (^|/)(tests?|__tests__|spec|e2e|cypress)/|[._-](test|spec)\.[A-Za-z0-9]+$|(^|/)test_[^/]+\.py$|Test\.php$
Interface: (^|/)(resources/(views|js|css|sass|scss)|app/(Livewire|View)|lang|components|pages|views|layouts|public|assets|styles?)/|\.(blade\.php|vue|svelte|jsx|tsx|css|scss|sass|less|html?)$
API: (^|/)(routes|app/Http|app/Console|api|[Cc]ontrollers?|graphql)/|\.(graphql|proto)$|(^|/)openapi\.(ya?ml|json)$
Domínio: (^|/)(app/(Models|Actions|Services|Domain|Domains|Policies|Events|Listeners|Jobs|Mail|Notifications|Rules|Enums|Data|DTOs?|Observers|Exceptions|Support)|domain|services|models|entities)/
Dados: (^|/)(database|migrations?|seeders?|factories|db|prisma)/|\.(sql|sqlite)$
```

Exemplos com as regras padrão:

| Caminho | Camada |
|---|---|
| `tests/Feature/PedidoTest.php` | Testes |
| `resources/js/carrinho.spec.ts` | Testes |
| `app/Livewire/Carrinho.php` | Interface |
| `resources/views/pedidos/index.blade.php` | Interface |
| `routes/web.php` | API |
| `app/Http/Requests/SalvarPedido.php` | API |
| `app/Actions/AprovarPedido.php` | Domínio |
| `app/Models/Pedido.php` | Domínio |
| `database/migrations/2026_01_01_create_pedidos.php` | Dados |
| `config/app.php` | Outros |
| `composer.lock` | Outros |

## Regras do projeto

Grave as regras do projeto em `docs/agents/camadas-slice.txt`. O script lê este arquivo quando ele existe. Para usar outro arquivo, passe `--camadas <arquivo>`. O arquivo do projeto troca todas as regras padrão. Copie o bloco acima e altere só o necessário.

Exemplo com uma camada nova:

```text
Testes: ^tests/
Interface: ^(resources|app/Livewire)/
API: ^(routes|app/Http)/
Infra: ^(docker|\.github|deploy)/|(^|/)Dockerfile$
Domínio: ^app/
Dados: ^database/
```

## Ordem no diagrama

O diagrama mostra as camadas nesta ordem: Interface, API, Domínio, Dados, Testes. Depois vêm as camadas novas, na ordem do arquivo, e por fim `Outros`. Uma camada das regras aparece também sem arquivos. `Outros` só aparece com arquivos.

A ordem de exibição não muda a prioridade. No exemplo acima, `Infra` vem antes de `Domínio` na prioridade, mas aparece depois de `Testes` no diagrama.
