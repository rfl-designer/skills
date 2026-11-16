# Inventário Laravel

Leia este perfil só quando o projeto usa PHP com Laravel. Ele dá o comando de cada fonte do [inventário](inventario.md). A pasta do inventário, os Domínios e as Features seguem esse arquivo. Confira cada comando com `--help` na versão instalada; não invente opção ausente.

## Fontes, em ordem

Use o executor e o diretório de execução da configuração, por exemplo `./vendor/bin/sail artisan` no Sail.

1. **Rotas.** Execute `php artisan route:list --json --except-vendor > "$INV/rotas.json"`. Gere as Âncoras:

   ```bash
   php -r '$rotas = json_decode(file_get_contents($argv[1]), true); foreach ($rotas as $r) { echo "rota:", $r["name"] ?: strtok($r["method"], "|") . " /" . ltrim($r["uri"], "/"), PHP_EOL; }' "$INV/rotas.json" >> "$INV/ancoras.txt"
   ```

   As rotas cobrem páginas Livewire de página inteira, recursos Filament, páginas Inertia, API e webhooks. A opção `--except-vendor` omite as rotas do framework e dos pacotes, como `/up` e `sanctum.csrf-cookie`; elas não precisam de Feature.
2. **Componentes Livewire.** Liste as classes que estendem `Component` em `app/Livewire/`. Exclua Form objects e classes abstratas. O nome do componente é o caminho em `kebab-case`, com pontos. A Âncora usa o prefixo `componente:`. O conferidor ainda aceita o prefixo antigo `livewire:`; num mapa que já o usa, mantenha um só prefixo:

   ```bash
   grep -rlE 'extends\s+Component\b' app/Livewire | sort | php -r 'require "vendor/autoload.php"; while (($f = fgets(STDIN)) !== false) { $p = substr(trim($f), strlen("app/Livewire/"), -4); echo "componente:", implode(".", array_map([Illuminate\Support\Str::class, "kebab"], explode("/", $p))), PHP_EOL; }' >> "$INV/ancoras.txt"
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

Sem `vendor/` ou sem app executável, leia as rotas e classes direto do código e registre a limitação.

## Agrupar em Domínios

Nos sinais do [inventário](inventario.md), use também os grupos de navegação do Filament, as pastas de domínio em `app/` e os Models com suas Policies.
