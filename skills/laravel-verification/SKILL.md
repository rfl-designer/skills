---
name: laravel-verification
description: Verifica mudanças Laravel com feedback rápido durante a edição e portão completo antes de commit, PR ou entrega. Inclui Blade no Pint, mutação e CRAP no escopo alterado, navegador e probes Pest --agent quando disponíveis. Use também ao registrar evidências para uma pausa.
---

# Verificação Proporcional Laravel (`laravel-verification`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

## 1. Preparar o projeto
Leia os manifests, lockfiles, testes e scripts existentes no escopo escolhido. `composer.lock`, `tests/Pest.php` e `phpunit.xml` são referências para projetos PHP; não invente arquivo ou ferramenta ausente. Respeite o executor existente (por exemplo, Sail). Confira `./vendor/bin/pint --help` e `./vendor/bin/pest --help` antes de usar opções condicionais.

Para habilitar Blade, mescle esta linha no objeto `rules` do `pint.json` do projeto, preservando as demais regras:

```json
{
    "rules": {
        "Pint/laravel_blade": true
    }
}
```

Essa configuração exige Pint com suporte a Blade e suas dependências Node/Prettier. Use `--blade` em uma execução isolada como alternativa. Se a versão não suporta Blade, use o formatador Blade já configurado ou registre o bloqueio; não declare cobertura inexistente. Não atualize dependências incompatíveis como parte de uma verificação.

## 2. Escolher o alcance
- **Durante a edição:** rode o teste da Costura ou Fronteira afetada. Em PHP/Blade, use `./vendor/bin/pint --dirty --test` com Blade habilitado. Rode análise estática focada conforme os scripts do projeto; amplie se mudar contratos compartilhados.
- **Antes de commit, PR ou entrega de código:** execute o portão completo abaixo. Uma fatia pode ter várias edições sem repetir toda a suíte entre elas.
- **Só documentação:** valide links, exemplos e regras do pacote; marque ferramentas PHP como `não aplicável`. Se a mudança afeta configuração executável, rode também os verificadores afetados.
- **Ao pausar:** registre o último resultado, seu escopo e o estado verificado. Reutilize evidência se os arquivos e dependências cobertos não mudaram. Caso contrário, marque `desatualizado` e deixe o comando pendente na retomada. Não rode a suíte completa apenas para pausar.

## 3. Portão completo
Esta seção é a única fonte da ordem do portão. As outras skills apontam para ela.

Use os comandos completos da configuração para o app afetado, no diretório de execução registrado. Respeite wrappers e scripts existentes também no ciclo RED/GREEN; não os some novamente aos comandos já completos. Se faltarem, use os padrões abaixo. Com Blade habilitado, a ordem é formatação → análise estática → testes → qualidade dos testes → navegador, quando a seção 4 o exige:

```bash
./vendor/bin/pint --test
./vendor/bin/phpstan analyse --memory-limit=2G
./vendor/bin/pest
```

Se Pint falhar, formate o escopo alterado e repita os checks que a edição invalidou. PHPStan/Pest que já passaram continuam válidos enquanto seu código, configuração e dependências relevantes permanecem iguais. Não repita checks apenas para mudar de etapa.

Nunca enfraqueça testes, tipos ou configuração para obter verde. Se uma ferramenta não pode executar, registre o comando, o erro e a cobertura ausente. Não declare o portão completo como aprovado.

### Qualidade dos testes
Um teste verde prova só que ele passa. A mutação prova que o teste falha quando a regra quebra. Execute esta etapa depois dos testes verdes, só nos arquivos PHP de produção do diff. As duas medidas exigem driver de cobertura (PCOV ou Xdebug). Sem driver ou sem ferramenta, registre `não verificado` com o motivo. Essa ausência não bloqueia o commit; ela aparece na evidência e no PR. Não instale dependências para esta etapa.

1. **Mutação:** Use o comando da configuração. Sem configuração, confira o help:
   - Pest com `--mutate` no help: `./vendor/bin/pest --mutate --path=<arquivos do diff, separados por vírgula>`.
   - Infection instalado: `./vendor/bin/infection --git-diff-filter=AM --git-diff-base=<base>`.

   Trate cada mutante que sobrevive e cada linha sem cobertura:
   - Escreva o teste que mata o mutante.
   - Ou apague o código que nenhum comportamento usa.
   - Ou registre o mutante como equivalente, com o motivo. Um mutante equivalente não muda nenhum resultado observável.
2. **CRAP:** Gere o relatório Clover fora do repositório: `./vendor/bin/pest --coverage-clover=<arquivo>`. Depois, execute `php <pasta-desta-skill>/scripts/crap.php <arquivo> <arquivos do diff>`. O limite é 10. O script sai com 1 quando um método fica com CRAP 10 ou mais.
   - CRAP = CC² × (1 − cobertura)³ + CC. CC é a complexidade ciclomática. Com cobertura total, CRAP = CC.
   - Primeiro, teste os ramos sem cobertura. Se o CRAP continua alto, separe o método por responsabilidade.
   - Um `match` ou `switch` com braços simples pode ficar acima do limite. Registre o motivo.
   - A linha `fora do relatório:` mostra um arquivo do diff sem medida. Confira o `<source>` do `phpunit.xml`. Um arquivo com lógica e sem medida fica `não verificado`.

Não baixe `--min`, não aumente `--limite` e não exclua arquivos para obter verde.

## 4. Provar comportamento real
Quando o diff toca Blade, Livewire, Alpine, CSS ou JavaScript, prove o caminho real no navegador e o efeito esperado. `Livewire::test()` comprova a fronteira no servidor; não executa o navegador.

- **Probe Pest Agent:** leia [references/pest-agent.md](references/pest-agent.md) se `--agent` aparece no help. Use para exploração, screenshots e verificações pontuais.
- **Regressão permanente:** use testes em `tests/Feature` ou `tests/Browser`. Um probe não substitui o teste de regressão nem a suíte final. Confirme que a configuração do Pest inclui os testes de navegador; se não, execute-os separadamente.
- **Sem plugin de navegador:** conduza o app com a ferramenta de navegador disponível, registre ação, resultado, console e efeito persistido.
- **Sem navegador:** registre a superfície como `não verificada` e explique o bloqueio. Não converta evidência de servidor em evidência de UI.

Se a configuração registra um Mapa de Features, leia o Arquivo de Feature afetado antes de provar. Exercite as entradas e os caminhos que a mudança afeta. Se o comportamento visível mudou, atualize o arquivo no mesmo diff, segundo a seção `Manutenção` do índice do mapa. Sem mapa, `/mapear` cria um.

Se a feature exigir verificação recorrente, leia [references/protocolo-do-app.md](references/protocolo-do-app.md) para registrar um protocolo reutilizável no projeto.

## 5. Evidência de saída
Reporte comando, alcance, resultado, estado verificado (commit ou arquivos/diff) e caminho dos artefatos.

- `[measured]`: executado sobre o estado coberto; pode ser reutilizado enquanto esse estado não mudou.
- `[inferred]` ou `[guess]`: conclusão sem execução; explique sua base e limite.
- `desatualizado`, `não verificado` e `não aplicável`: use explicitamente quando corresponderem ao caso.

Diga se o resultado veio de teste focado, probe ou suíte completa. Para UI, cite o fluxo exercitado e a prova de efeito. Para a qualidade dos testes, cite os mutantes mortos, sobreviventes, sem cobertura e equivalentes, com o motivo de cada equivalente. Cite também os métodos com CRAP 10 ou mais e o motivo de cada exceção.

### Guardar a evidência
Cada tipo de evidência tem um destino e uma validade. Não acumule arquivos por execução.

| Tipo | Exemplo | Destino | Validade |
|---|---|---|---|
| Prova de estado | saída do portão, RED e GREEN | retorno ao principal, nota de pausa, descrição do PR ou CI | até a próxima mudança do estado coberto; depois, `desatualizado` |
| Probe | snippet `--agent` | teste de regressão, ou item de `Como conduzir` no Arquivo de Feature | até a promoção; depois, não guarde o snippet solto |
| Artefato | screenshot, log, saída do console | pasta de Evidências da configuração | até a próxima condução da mesma Sub-feature, que substitui o arquivo |

- Não grave a prova de estado como arquivo no repositório.
- Dê ao artefato um nome estável, sem data: `<domínio>/<feature>/<id-da-sub-feature>.<extensão>`. Para mais de um arquivo, use `<id-da-sub-feature>.<detalhe>.<extensão>`. A linha `Estado:` guarda a data e o commit.
- Sem Mapa de Features, use `<feature>/<caso>.<extensão>`. Guarde a prova de uma jornada na pasta da primeira Feature, com o ID da Sub-feature inicial.
- O `screenshot()` do plugin Browser grava na pasta do plugin. Mova o arquivo de prova para a pasta de Evidências, com o nome estável.
- Siga a política de versionamento da linha `Evidências` na configuração. Sem política, não faça `git add` de artefatos binários e ofereça `/setup`.
- Quando uma Sub-feature sai do mapa, apague seus artefatos na mesma mudança. Com Mapa de Features, confira a pasta com o conferidor de `/mapear` e a opção `--evidencias`.
- Não grave segredos, senhas ou valores de `.env` em artefatos.
- Guarde os artefatos fora de diretórios temporários que o runner limpa.
