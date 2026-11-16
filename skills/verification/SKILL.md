---
name: verification
description: Verifica mudanças de código com feedback rápido durante a edição e portão completo antes de commit, PR ou entrega, em qualquer linguagem ou framework. Inclui formatação, análise estática, testes, mutação e CRAP no escopo alterado e prova no navegador. Use também ao registrar evidências para uma pausa.
---

# Verificação Proporcional (`verification`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

**Perfil de stack:** Esta skill não assume linguagem nem framework. Os comandos vêm da tabela `Execução e verificação` da configuração. Se a configuração ou os manifests mostram Laravel, leia também [references/laravel.md](references/laravel.md): ele traz os comandos padrão de Pint, PHPStan e Pest. Sem perfil para a stack do projeto, use só os comandos da configuração e dos scripts do projeto.

## 1. Preparar o projeto
Leia os manifests, lockfiles, testes e scripts existentes no escopo escolhido. Não invente arquivo ou ferramenta ausente. Respeite o executor existente, como um contêiner ou um wrapper do projeto. Confira o `--help` de cada ferramenta antes de usar uma opção condicional.

O formatador e o analisador cobrem todos os tipos de arquivo do diff, inclusive templates. Se uma ferramenta não cobre um tipo de arquivo, use a ferramenta que o projeto já tem para esse tipo, ou registre o bloqueio. Não declare cobertura inexistente. Não atualize dependências incompatíveis como parte de uma verificação.

## 2. Escolher o alcance
- **Durante a edição:** rode o teste da Costura ou Fronteira afetada. Rode o formatador em modo de conferência só nos arquivos alterados. Rode análise estática focada conforme os scripts do projeto; amplie se mudar contratos compartilhados.
- **Antes de commit, PR ou entrega de código:** execute o portão completo abaixo. Uma fatia pode ter várias edições sem repetir toda a suíte entre elas.
- **Só documentação:** valide links, exemplos e regras do pacote; marque as ferramentas de código como `não aplicável`. Se a mudança afeta configuração executável, rode também os verificadores afetados.
- **Ao pausar:** registre o último resultado, seu escopo e o estado verificado. Reutilize evidência se os arquivos e dependências cobertos não mudaram. Caso contrário, marque `desatualizado` e deixe o comando pendente na retomada. Não rode a suíte completa apenas para pausar.

## 3. Portão completo
Esta seção é a única fonte da ordem do portão. As outras skills apontam para ela.

Use os comandos completos da configuração para o app afetado, no diretório de execução registrado. Respeite wrappers e scripts existentes também no ciclo RED/GREEN; não os some novamente aos comandos já completos. A ordem é:

1. Formatação, em modo de conferência.
2. Análise estática.
3. Testes, com a suíte completa.
4. Qualidade dos testes.
5. Navegador, quando a seção 4 o exige.

Se a configuração não tem o comando de uma etapa, procure-o nos scripts do projeto e no perfil de stack. Se o projeto não tem a ferramenta, registre a etapa como `não verificado`, com o motivo. Não instale uma ferramenta para completar o portão.

Se a formatação falhar, formate o escopo alterado e repita os checks que a edição invalidou. A análise e os testes que já passaram continuam válidos enquanto seu código, configuração e dependências relevantes permanecem iguais. Não repita checks apenas para mudar de etapa.

Nunca enfraqueça testes, tipos ou configuração para obter verde. Se uma ferramenta não pode executar, registre o comando, o erro e a cobertura ausente. Não declare o portão completo como aprovado.

### Qualidade dos testes
Um teste verde prova só que ele passa. A mutação prova que o teste falha quando a regra quebra. Execute esta etapa depois dos testes verdes, só nos arquivos de produção do diff. As duas medidas exigem a medição de cobertura da stack. Sem cobertura ou sem ferramenta, registre `não verificado` com o motivo. Essa ausência não bloqueia o commit; ela aparece na evidência e no PR. Não instale dependências para esta etapa.

1. **Mutação:** Use o comando da linha `Mutação` da configuração, limitado aos arquivos do diff. Sem configuração, procure a ferramenta de mutação da stack nos manifests e confira o help dela.

   Trate cada mutante que sobrevive e cada linha sem cobertura:
   - Escreva o teste que mata o mutante.
   - Ou apague o código que nenhum comportamento usa.
   - Ou registre o mutante como equivalente, com o motivo. Um mutante equivalente não muda nenhum resultado observável.
2. **CRAP:** Gere o relatório Clover fora do repositório, com o comando da configuração. Depois, execute `python3 <pasta-desta-skill>/scripts/crap.py <arquivo> <arquivos do diff>`. O limite é 10. O script sai com 1 quando um método fica com CRAP 10 ou mais.
   - CRAP = CC² × (1 − cobertura)³ + CC. CC é a complexidade ciclomática. Com cobertura total, CRAP = CC.
   - O script exige Python 3 e um relatório Clover com linhas `type="method"` e o atributo `complexity`. Ele usa o atributo `crap` do relatório. Sem esse atributo, ele calcula o CRAP com a cobertura das linhas do método.
   - Se a stack não gera esse relatório, use a ferramenta dela que mede complexidade e cobertura por função, com o mesmo limite. Sem ferramenta, registre `não verificado`.
   - Primeiro, teste os ramos sem cobertura. Se o CRAP continua alto, separe o método por responsabilidade.
   - Uma seleção de casos com braços simples pode ficar acima do limite. Registre o motivo.
   - A linha `fora do relatório:` mostra um arquivo do diff sem medida. Confira os arquivos de origem na configuração de cobertura. Um arquivo com lógica e sem medida fica `não verificado`.

Não baixe o mínimo de mutação, não aumente `--limite` e não exclua arquivos para obter verde.

## 4. Provar comportamento real
Quando o diff toca a interface que o usuário vê (templates, componentes de UI, CSS ou JavaScript), prove o caminho real no navegador e o efeito esperado. Um teste de componente no servidor comprova a Fronteira; ele não executa o navegador.

- **Probe:** um comando curto que exercita o app para responder uma pergunta. Use a ferramenta de probe da configuração para exploração, screenshots e verificações pontuais.
- **Regressão permanente:** use os testes da suíte do projeto. Um probe não substitui o teste de regressão nem a suíte final. Confirme que a suíte completa inclui os testes de navegador; se não, execute-os separadamente.
- **Sem teste de navegador:** conduza o app com a ferramenta de navegador disponível, registre ação, resultado, console e efeito persistido.
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
| Probe | comando de probe | teste de regressão, ou item de `Como conduzir` no Arquivo de Feature | até a promoção; depois, não guarde o comando solto |
| Artefato | screenshot, log, saída do console | pasta de Evidências da configuração | até a próxima condução da mesma Sub-feature, que substitui o arquivo |

- Não grave a prova de estado como arquivo no repositório.
- Dê ao artefato um nome estável, sem data: `<domínio>/<feature>/<id-da-sub-feature>.<extensão>`. Para mais de um arquivo, use `<id-da-sub-feature>.<detalhe>.<extensão>`. A linha `Estado:` guarda a data e o commit.
- Sem Mapa de Features, use `<feature>/<caso>.<extensão>`. Guarde a prova de uma jornada na pasta da primeira Feature, com o ID da Sub-feature inicial.
- Se a ferramenta grava o screenshot na pasta dela, mova o arquivo de prova para a pasta de Evidências, com o nome estável.
- Siga a política de versionamento da linha `Evidências` na configuração. Sem política, não faça `git add` de artefatos binários e ofereça `/setup`.
- Quando uma Sub-feature sai do mapa, apague seus artefatos na mesma mudança. Com Mapa de Features, confira a pasta com o conferidor de `/mapear` e a opção `--evidencias`.
- Não grave segredos, senhas ou valores de arquivos de ambiente em artefatos.
- Guarde os artefatos fora de diretórios temporários que o executor de testes limpa.
