# Perfil Laravel de `verification`

Leia este perfil só quando o projeto usa PHP com Laravel. Ele dá os comandos padrão de cada etapa do portão; a ordem continua a da skill. Os comandos da configuração do projeto prevalecem sobre estes.

## Preparar o projeto
`composer.lock`, `tests/Pest.php` e `phpunit.xml` são as referências. Respeite o executor existente, por exemplo o Sail. Confira `./vendor/bin/pint --help` e `./vendor/bin/pest --help` antes de usar opções condicionais.

Para o Pint cobrir Blade, mescle esta linha no objeto `rules` do `pint.json` do projeto, preservando as demais regras:

```json
{
    "rules": {
        "Pint/laravel_blade": true
    }
}
```

Essa configuração exige Pint com suporte a Blade e suas dependências Node/Prettier. Use `--blade` em uma execução isolada como alternativa. Se a versão não suporta Blade, use o formatador Blade já configurado ou registre o bloqueio.

## Comandos padrão do portão

Durante a edição, use `./vendor/bin/pint --dirty --test` com Blade habilitado e o teste focado: `./vendor/bin/pest --filter=<NomeDoTeste>`.

Antes de commit, PR ou entrega:

```bash
./vendor/bin/pint --test
./vendor/bin/phpstan analyse --memory-limit=2G
./vendor/bin/pest
```

Se Pint falhar, formate o escopo alterado e repita os checks que a edição invalidou.

## Qualidade dos testes
As duas medidas exigem driver de cobertura (PCOV ou Xdebug): `php -m` mostra o driver.

- **Mutação:**
  - Pest com `--mutate` no help: `./vendor/bin/pest --mutate --path=<arquivos do diff, separados por vírgula>`.
  - Infection instalado: `./vendor/bin/infection --git-diff-filter=AM --git-diff-base=<base>`.
  - Não baixe `--min` para obter verde.
- **CRAP:** `./vendor/bin/pest --coverage-clover=<arquivo fora do repositório>`. Depois, execute o `scripts/crap.py` da skill sobre esse arquivo. O relatório do PHPUnit já traz o atributo `crap`.
  - Um `match` ou `switch` com braços simples pode ficar acima do limite. Registre o motivo.
  - Para um arquivo `fora do relatório:`, confira o `<source>` do `phpunit.xml`.

## Navegador
A interface inclui Blade, Livewire, Alpine, CSS e JavaScript. `Livewire::test()` comprova a Fronteira no servidor; não executa o navegador.

- **Probe Pest Agent:** leia [pest-agent.md](pest-agent.md) se `--agent` aparece no help do Pest.
- **Regressão permanente:** use testes em `tests/Feature` ou `tests/Browser`. Confirme que a configuração do Pest inclui os testes de navegador.
- O `screenshot()` do plugin Browser grava na pasta do plugin. Mova o arquivo de prova para a pasta de Evidências, com o nome estável.
- Não grave valores de `.env` em artefatos.

## Requisitos e opcionais
- Pest, Larastan ou PHPStan e Laravel Pint.
- Opcional: `pestphp/pest-plugin-agent`, detectado por `pest --help`. Pest 5 exige PHP 8.4+; estas skills não o atualizam.
- Recomendado: `pestphp/pest-plugin-browser`, numa versão compatível com o Pest instalado, e Playwright.
