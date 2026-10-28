# Inventário da aplicação

O inventário lista as entradas que o usuário alcança e as agrupa em Domínios. O agente principal faz o inventário uma vez e passa os arquivos aos Mapeadores. Confira cada comando com `--help` na versão instalada; não invente opção ausente.

## Pasta do inventário

Grave o inventário numa pasta temporária fora do repositório:

```bash
INV="$(mktemp -d)"
```

Arquivos esperados:

- `rotas.json`: saída de `route:list`.
- `ancoras.txt`: uma Âncora por linha, para o conferidor.
- `dominios.md`: proposta de Domínios, com as Âncoras e as Features estimadas de cada um.

Não copie `.env` nem segredos para o inventário. Registre só nomes de variáveis.

## Fontes, em ordem

Use o executor e o diretório de execução da configuração, por exemplo `./vendor/bin/sail artisan` no Sail.

1. **Rotas.** Execute `php artisan route:list --json --except-vendor > "$INV/rotas.json"`. Gere as Âncoras:

   ```bash
   php -r '$rotas = json_decode(file_get_contents($argv[1]), true); foreach ($rotas as $r) { echo "rota:", $r["name"] ?: strtok($r["method"], "|") . " /" . ltrim($r["uri"], "/"), PHP_EOL; }' "$INV/rotas.json" >> "$INV/ancoras.txt"
   ```

   As rotas cobrem páginas Livewire de página inteira, recursos Filament, páginas Inertia, API e webhooks. A opção `--except-vendor` omite as rotas do framework e dos pacotes, como `/up` e `sanctum.csrf-cookie`; elas não precisam de Feature.
2. **Componentes Livewire.** Liste as classes que estendem `Component` em `app/Livewire/`. Exclua Form objects e classes abstratas. O nome do componente é o caminho em `kebab-case`, com pontos:

   ```bash
   grep -rlE 'extends\s+Component\b' app/Livewire | sort | php -r 'require "vendor/autoload.php"; while (($f = fgets(STDIN)) !== false) { $p = substr(trim($f), strlen("app/Livewire/"), -4); echo "livewire:", implode(".", array_map([Illuminate\Support\Str::class, "kebab"], explode("/", $p))), PHP_EOL; }' >> "$INV/ancoras.txt"
   ```

   Com Volt ou componentes de arquivo único, leia os caminhos registrados no provider e na documentação da versão instalada.
3. **Comandos Artisan.** Leia a assinatura em `app/Console/Commands/` e os comandos de `routes/console.php`:

   ```bash
   grep -rhoE "signature\s*=\s*['\"][^ '\"]+" app/Console/Commands | sed -E "s/.*['\"]/comando:/" >> "$INV/ancoras.txt"
   grep -hoE "Artisan::command\(\s*['\"][^ '\"]+" routes/console.php | sed -E "s/.*['\"]/comando:/" >> "$INV/ancoras.txt"
   ```

   Um comando com o atributo `#[AsCommand]` declara o nome nesse atributo.
4. **Agenda.** Execute `php artisan schedule:list`. Grave `agenda:<comando ou classe>` para cada item.
5. **Notificações e e-mails.** Liste as classes em `app/Notifications/` e `app/Mail/`:

   ```bash
   for f in app/Notifications/*.php app/Mail/*.php; do [ -f "$f" ] && echo "notificacao:$(basename "$f" .php)"; done >> "$INV/ancoras.txt"
   ```

   Acrescente à mão uma notificação do framework que a aplicação usa, como `ResetPassword`.
6. **Flags.** Procure `Feature::define(` e as classes de `app/Features/` do Laravel Pennant, ou outro sistema de flags do projeto. Grave `flag:<nome>`.
7. **Visão do usuário.** Leia os menus nos layouts Blade, a navegação do Filament, os textos em `lang/` e o README. Eles dão os nomes que o usuário vê e a ordem das telas.
8. **Permissões.** Leia `app/Policies/` e os Gates. Eles definem o papel do usuário em cada pré-condição.
9. **Testes.** Leia os nomes em `tests/Feature/` e `tests/Browser/`. Eles mostram comportamentos e casos de borda que já têm prova.
10. **Glossário e ADRs.** Use os termos do glossário configurado para nomear Domínios e Features.

Remova itens repetidos de `ancoras.txt` com `sort -u -o "$INV/ancoras.txt" "$INV/ancoras.txt"`. Sem `vendor/` ou sem app executável, leia as rotas e classes direto do código e registre a limitação.

## Agrupar em Domínios

Um Domínio é uma área de negócio que o usuário reconhece, como Vendas, Estoque ou Financeiro. Uma camada técnica, como Controllers ou Jobs, não é Domínio.

Use estes sinais, nesta ordem:

1. Áreas do glossário e das ADRs.
2. Seções do menu e grupos de navegação do Filament.
3. Prefixos de nome e de URI das rotas.
4. Módulos e pastas de domínio em `app/`, e os Models com suas Policies.
5. Pastas de testes.

Divida um Domínio com mais de 15 Features estimadas em Domínios menores. Coloque autenticação, perfil e preferências num Domínio `conta`. Coloque usuários, papéis e auditoria num Domínio `administracao`, quando existem.

## Estimar Features

Uma Feature é uma capacidade que o usuário nomeia: "Pedidos", "Relatório de vendas", "Login". Listar, criar, editar e excluir uma mesma entidade formam uma Feature. Um fluxo longo, como o checkout, pode ser outra.

Para cada Domínio, grave em `dominios.md`:

- o nome e uma linha de descrição;
- as Âncoras do Domínio, com `*` quando o prefixo é exclusivo;
- as Features estimadas, uma linha cada;
- as Âncoras sem dono claro e as candidatas a `Fora do mapa`.

O número de Domínios e de Features define o tamanho da aplicação e o modo de mapeamento.
