# Probes com Pest Agent

## Detectar antes de usar
Leia `composer.lock`, `tests/Pest.php` e execute `./vendor/bin/pest --version` e `./vendor/bin/pest --help`. O plugin `pestphp/pest-plugin-agent` fornece `--agent`; não assuma sua presença só porque Pest é versão 5. Se a opção estiver disponível numa versão compatível anterior, ela também pode ser usada.

Se Pest 5 já está instalado e falta o plugin, adicione `pestphp/pest-plugin-agent` em dependências de desenvolvimento compatíveis quando a tarefa incluir preparar a verificação. Confira o diff de `composer.json` e `composer.lock`. Não migre a versão principal do Pest apenas para obter a opção. Pest 5 exige PHP 8.4+; consulte o guia de upgrade antes de uma migração solicitada.

```bash
composer require pestphp/pest-plugin-agent --dev
```

Para UI, confirme também `pestphp/pest-plugin-browser` e Playwright. Se indisponíveis, use os testes e o navegador existentes e registre a limitação.

## Executar uma pergunta por probe
Use aspas simples externas para preservar variáveis PHP no shell. Adapte rota e fixtures ao projeto:

```bash
./vendor/bin/pest --agent='$user = \App\Models\User::factory()->create(); $this->actingAs($user)->get("/dashboard")->assertOk();'
./vendor/bin/pest --agent='visit("/")->assertNoJavaScriptErrors()->screenshot(filename: "home");'
```

O primeiro comando verifica HTTP, o segundo exige o plugin Browser. Para mutações pela UI, espere primeiro o sinal de conclusão na tela e depois confira banco, fila ou mensagem.

Use ambiente e banco de testes. Confira quais traits e hooks realmente se aplicam ao probe; inicialize nele o setup necessário. Não presuma isolamento só pela opção `--agent`.

Probes servem ao feedback rápido. Promova comportamento durável a teste de regressão. Se a feature precisa repetir o probe, escreva-o como item de `Como conduzir` no Arquivo de Feature, ou no protocolo quando não há mapa. Substitua o item antigo; não guarde versões anteriores. Guarde os artefatos segundo a seção `Guardar a evidência` da skill.

Fontes: [Agent](https://github.com/pestphp/docs/blob/5.x/agent.md), [Pest 5](https://pestphp.com/docs/pest5-now-available).
