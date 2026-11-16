# Perfil Laravel de `/conduzir`

Leia este perfil só quando o projeto usa PHP com Laravel. Ele dá os comandos da guarda do banco; os passos continuam os da skill. Use o executor da configuração, por exemplo `./vendor/bin/sail artisan` no Sail.

## Guarda do banco
Repita a guarda depois de cada mudança em `.env`, em `phpunit.xml` ou no executor. `APP_ENV=local` não prova que o banco é local.

1. **App:** Leia a conexão do app:

   ```bash
   php artisan tinker --execute='$db = DB::connection(); echo $db->getName(), " ", $db->getConfig("host") ?? "-", " ", $db->getDatabaseName(), PHP_EOL;'
   ```

2. **Testes (Pest):** Leia `DB_CONNECTION` e `DB_DATABASE` em `phpunit.xml`. Se falta um deles, rode o comando do passo 1 com `--env=testing`. Faça este passo antes de qualquer comando Pest, inclusive um probe `--agent`.

   **ATENÇÃO:** `RefreshDatabase` e `DatabaseMigrations` rodam `migrate:fresh` num banco que não está em memória. Esse comando apaga todas as tabelas.

3. **E-mail:** Leia `config("mail.default")` e o host do mailer. Continue só com `log`, `array` ou um coletor local, como o Mailpit.

Exemplo da linha gravada na configuração:

`- Banco da condução: app mysql em 127.0.0.1, banco loja_local; Pest sqlite, banco :memory:.`

## Condução
- Sem navegador, conduza HTTP e comandos Artisan e marque `parcial`, com o motivo.
- Use `php artisan tinker` só para ler o efeito depois da ação.
- Não copie valores de `.env` para o mapa ou para as evidências.
