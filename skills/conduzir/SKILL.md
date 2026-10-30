---
name: conduzir
description: Conduz as receitas do Mapa de Features no app local, atualiza a linha Estado e separa Deriva, lacuna de condução e defeito do produto. Antes da primeira condução, prova que o app e o Pest usam o banco permitido. Use quando o usuário digitar /conduzir.
argument-hint: "[tudo | Domínio | Feature]"
disable-model-invocation: true
---

# Conduzir o Mapa de Features (`/conduzir`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

O mapa vem da linha `Mapa de Features` na tabela de destinos. Sem mapa, pare e ofereça `/mapear`. O banco permitido vem da linha `Banco da condução`, na seção `Execução e verificação`. A guarda do banco diz como gravá-la.

## 1. Objetivo
Provar no app o comportamento que o Mapa de Features descreve. `/mapear` escreve cada receita a partir do código, com `Estado: não conduzida`. Esta skill executa as receitas, corrige o mapa errado, reporta os defeitos do produto e atualiza a linha `Estado:`.

## 2. Termos
- **Condução:** operação do app pela tela, pelo comando ou pela rota que o usuário usa, com o resultado observado.
- **Receita:** os itens da seção `Como conduzir` de um Arquivo de Feature.
- **Diagnóstico:** os comandos do README do mapa que provam que a instância merece condução.
- **Banco permitido:** o banco que o usuário autorizou para a condução. A configuração o registra sem credenciais.
- **Deriva:** o app está certo e o mapa está errado.
- **Lacuna de condução:** o app funciona, mas a receita não o conduz.
- **Defeito do produto:** o app está errado.

## 3. Regras Inegociáveis
- **Conduza só no banco permitido:** Faça a guarda do banco antes da primeira condução. `APP_ENV=local` não prova que o banco é local.
- **Não declare condução sem condução:** A linha `Estado:` diz o que você conduziu, em que data e em que commit.
- **Conduza em série:** Só o agente principal conduz. App, banco e sessão locais são compartilhados.
- **Não altere o produto:** Escreva só no mapa, na pasta de evidências e na linha `Banco da condução`. Reporte cada defeito; não ajuste o mapa para escondê-lo.
- **Não enfraqueça a condução para passar:** Se o seed não cria um estado necessário, a condução falha. Registre a falta em `Armadilhas`.
- **Proteja dados:** Não copie segredos, senhas ou valores de `.env` para o mapa ou para as evidências.
- **Faça commit só com autorização da sessão.**

## 4. Guarda do banco
Faça a guarda antes da primeira condução. Repita-a depois de cada mudança em `.env`, em `phpunit.xml` ou no executor.

1. **App:** Leia a conexão do app com o executor da configuração:

   ```bash
   php artisan tinker --execute='$db = DB::connection(); echo $db->getName(), " ", $db->getConfig("host") ?? "-", " ", $db->getDatabaseName(), PHP_EOL;'
   ```

2. **Pest:** Leia `DB_CONNECTION` e `DB_DATABASE` em `phpunit.xml`. Se falta um deles, rode o comando do passo 1 com `--env=testing`. Faça este passo antes de qualquer comando Pest, inclusive um probe `--agent`.

   **ATENÇÃO:** `RefreshDatabase` e `DatabaseMigrations` rodam `migrate:fresh` num banco que não está em memória. Esse comando apaga todas as tabelas.

3. **E-mail:** Leia `config("mail.default")` e o host do mailer. Continue só com `log`, `array` ou um coletor local, como o Mailpit.
4. **Comparar:** Continue só quando cada conexão lida é igual à linha `Banco da condução`. Sem a linha, mostre ao usuário a conexão, o host e o banco de cada leitura. Pergunte se são bancos locais ou de teste. Depois da confirmação, grave a linha, por exemplo:

   `- Banco da condução: app mysql em 127.0.0.1, banco loja_local; Pest sqlite, banco :memory:.`

   O nome do host, o nome do banco e `APP_ENV` não autorizam uma conexão. Só a confirmação do usuário autoriza.
5. **Parar:** Se uma leitura diverge, pare antes de qualquer condução ou comando Pest. Não mude a linha `Estado:`. Informe a conexão lida, sem usuário nem senha, e o que falta.

## 5. Escolher o alcance
- `tudo`: a ordem da `Varredura completa` do README do mapa, com as jornadas no fim.
- Um Domínio ou uma Feature: só esse alcance.
- Sem argumento: as Features com `Estado:` diferente de `conduzida`. Se todas estão `conduzida`, pergunte o alcance.

## 6. Conduzir
1. **Preparar:** Leia o README raiz do mapa: pré-condições base, convenções, `Prova e lacunas` e o contrato. Faça a guarda do banco. Depois, faça o Diagnóstico.
2. **Executar:** Para cada Feature do alcance, em série:
   - Leia o Arquivo de Feature e prepare as pré-condições.
   - Execute cada item de `Como conduzir` com o comando base e a ferramenta do README.
   - Registre a ação, o comando, o resultado e o caminho da evidência. Siga as regras de evidência de `laravel-verification`: o nome do artefato é estável, e a condução nova substitui o arquivo da mesma Sub-feature.
   - Depois de cada falha, faça o Diagnóstico de novo.
   - Sem navegador, conduza HTTP e Artisan e marque `parcial`, com o motivo.
   - Se o app não inicia, informe o bloqueio exato e mantenha `não conduzida`.
3. **Triagem:** Classifique cada falha:
   - **Deriva:** corrija o Arquivo de Feature.
   - **Lacuna de condução:** corrija a receita, ou marque o caminho como manual, com o motivo.
   - **Defeito do produto:** reporte com o caso concreto e ofereça `/bug`. Não altere o mapa nem o código.

   Uma diferença sem commit, Spec ou pedido que a explique é defeito do produto. Rode cada receita corrigida de novo, a partir do arquivo. Uma Âncora nova ou removida, uma Feature nova ou uma Feature removida vai para `/mapear`.
4. **Limpar:** Remova os dados que a condução criou. Desative as flags que ela ativou. Preserve as evidências.
5. **Registrar:** Atualize a linha `Estado:` de cada Feature conduzida:

   `Estado: <valor> em AAAA-MM-DD, commit <sha>[; detalhe]`

   | Valor | Quando |
   | --- | --- |
   | `conduzida` | Você conduziu cada entrada listada nesse commit e viu o resultado descrito. |
   | `parcial` | Você conduziu parte das entradas. O detalhe lista as outras e o motivo. |
   | `bloqueada` | Você tentou e uma pré-condição impediu. O detalhe diz qual. |

   Um defeito do produto não muda o Estado. O mapa continua com o comportamento esperado.
6. **Conferir:** Rode o conferidor da skill `mapear`: `php <pasta-da-skill-mapear>/scripts/conferir-mapa.php <destino> --evidencias=<pasta de Evidências>`. Omita `--evidencias` quando a pasta não existe. Sem a skill `mapear`, registre `conferidor: não executado`.
   - Mova cada artefato que o conferidor aponta numa pasta errada.
   - Mostre ao usuário os artefatos sem Sub-feature. Apague-os só depois da confirmação. Um nome antigo, com data, também aparece nessa lista.
7. **Resultado:** Declare um destes resultados:
   - `em dia`: cada Feature do alcance conduzida e nada para corrigir.
   - `corrigido`: um conjunto de correções provadas. Releia cada arquivo alterado.
   - `bloqueado`: a condução não terminou. Diga o que bloqueou.

## 7. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "`APP_ENV` é `local`; então o banco é local." | **Proibido.** Faça a guarda do banco. Só a confirmação do usuário autoriza uma conexão. |
| "É só um probe `--agent`; ele não grava no banco." | **Proibido.** O probe usa o banco do Pest e pode aplicar `RefreshDatabase`. Faça a guarda do Pest antes. |
| "Li o componente Livewire; a receita está certa." | **Proibido.** A receita fica `não conduzida` até uma condução real. |
| "O botão sumiu da tela; vou tirar a Sub-feature do mapa." | **Proibido.** Classifique primeiro. Sem commit, Spec ou pedido que explique a remoção, é defeito do produto. Reporte-o. |
| "Posso conduzir as Features em paralelo com subagentes." | **Proibido.** O agente principal conduz em série. App, banco e sessão locais são compartilhados. |
| "O seed não tem pedido entregue; vou pular esse passo." | **Proibido.** Registre a falta em `Armadilhas` e marque `parcial` ou `bloqueada`. |

## 8. Prova de Execução (Critério de Saída)
- `[measured]` Guarda do banco: a conexão do app e a do Pest, sem credenciais, e a linha `Banco da condução`.
- `[measured]` Saída do Diagnóstico antes da primeira condução.
- `[measured]` Por condução: ação, comando, resultado e caminho da evidência.
- `[measured]` Por Feature do alcance, uma linha `Estado:` coerente com o que rodou.
- `[measured]` Saída `OK` do conferidor, com `--evidencias` quando a pasta existe, ou `não executado` com o motivo.
- `[measured]` `git status` sem mudança fora do mapa, das evidências e da linha `Banco da condução`.
- `[measured]` O resultado, as Derivas e lacunas corrigidas e os defeitos reportados.
