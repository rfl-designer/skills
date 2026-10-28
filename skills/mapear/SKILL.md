---
name: mapear
description: Cria e mantém o Mapa de Features da aplicação, um índice e um arquivo por Feature com entradas do usuário, condução, prova e armadilhas. Em aplicações com vários Domínios, delega cada Domínio a um subagente Mapeador. Atualiza o mapa depois de mudanças e o audita contra o app real. Use quando o usuário digitar /mapear.
argument-hint: "[auditar] [Domínio ou Feature]"
disable-model-invocation: true
---

# Mapear Features da Aplicação (`/mapear`)

## Configuração do projeto
Leia a configuração apontada nas instruções do projeto; sem ponteiro, procure `docs/agents/projeto.md` na raiz do repositório. Reutilize-a enquanto não mudar. Use seus caminhos, comandos e escopo; os exemplos abaixo são fallback. A sessão prevalece. Sem configuração, pergunte só pelas escolhas necessárias ausentes e ofereça `/setup` uma vez, sem bloquear a tarefa.

O destino do mapa vem da linha `Mapa de Features` na tabela de destinos. Sem essa linha, recomende `docs/features/` e confirme antes de gravar. Depois, acrescente a linha à configuração existente e preserve o resto.

## 1. Objetivo
Manter na aplicação um inventário de comportamento, do ponto de vista do usuário: o **Mapa de Features**. Um agente lê só o Arquivo de Feature da mudança, conduz cada entrada listada e sabe que prova vale. Uma pessoa usa o mapa como checklist de regressão. Esta skill cria o mapa, o atualiza depois de mudanças e o audita contra o app real.

## 2. Termos
- **Domínio:** área de negócio que o usuário reconhece, como Vendas. Cada Domínio tem uma pasta no mapa.
- **Feature:** capacidade que o usuário nomeia, como Pedidos.
- **Arquivo de Feature:** o Markdown de uma Feature, na pasta do seu Domínio.
- **Sub-feature:** um comportamento da Feature, com um ID único no mapa.
- **Condução:** operação do app real pela tela, pelo comando ou pela rota que o usuário usa, com o resultado observado.
- **Âncora:** identificador estável do código que liga um diff à Feature: rota, componente Livewire, comando, agenda, notificação ou flag.
- **Mapeador:** subagente que mapeia um Domínio.
- **Deriva:** diferença entre o mapa e o comportamento real do app.

## 3. Regras Inegociáveis
- **Siga o contrato:** Use o [formato](references/formato.md) em cada arquivo do mapa. Antes de entregar, rode o conferidor: `php <pasta-desta-skill>/scripts/conferir-mapa.php <destino> --ancoras="$INV/ancoras.txt"`.
- **Descreva comportamento, não implementação:** Nomeie telas, botões, URLs, comandos e resultados visíveis. Caminhos de arquivo e classes internas ficam fora; as exceções são as Âncoras e os testes de regressão.
- **Cubra cada entrada:** Cada Âncora do inventário pertence a uma Feature ou à seção `Fora do mapa`, com o motivo. Não omita uma entrada em silêncio.
- **Não declare condução sem condução:** A linha `Estado:` diz o que um agente conduziu, em que data e em que commit. Uma receita lida só no código fica `não conduzida`.
- **Não altere o produto:** Escreva só no mapa e na linha de destino da configuração. Se o app contradiz o mapa, classifique a diferença: mapa errado é Deriva; app errado é defeito. Reporte o defeito; não ajuste o mapa para escondê-lo.
- **Não enfraqueça a condução para passar:** Se o seed não cria um estado necessário, a condução falha. Registre a falta em `Armadilhas`.
- **Proteja dados:** Não copie segredos, senhas ou valores de `.env`. Conduza só em ambiente local ou de teste.
- **Use o glossário:** Nomeie Domínios e Features com os termos configurados. Use um termo para cada conceito.
- **Faça commit só com autorização da sessão.**

## 4. Escolher o modo e o tamanho
Escolha o modo:

- **Criar:** o destino não tem `README.md`. Um README sem a linha `Base:` indica um Criar interrompido; retome no passo que falta.
- **Atualizar:** o mapa existe e o argumento não começa com `auditar`. O alcance é o alvo do usuário (diff, branch ou PR). Sem alvo, o alcance são as mudanças desde a linha `Base:` e o working tree.
- **Auditar:** o argumento começa com `auditar`. Um Domínio ou uma Feature no argumento limita o alcance.

Depois do inventário, escolha o tamanho:

- **Aplicação grande:** 3 ou mais Domínios e mais de 12 Features estimadas. O principal delega um Domínio por Mapeador, segundo [mapeadores](references/mapeadores.md).
- **Aplicação pequena:** os outros casos. O agente principal mapeia tudo.

Um pedido da sessão para delegar, ou para não delegar, prevalece sobre o tamanho.

Em monorepo, crie um mapa por app, no destino do escopo desse app.

## 5. Criar
1. **Inventário:** Siga o [inventário](references/inventario.md). Grave `ancoras.txt` e `dominios.md` fora do repositório.
2. **Confirmação:** Mostre os Domínios, as Features estimadas, o tamanho e o destino. Na aplicação grande, mostre também o número de Mapeadores e de ondas e aguarde a confirmação. Na pequena, continue sem esperar, exceto quando falta o destino.
3. **README raiz:** Grave as seções comuns: pré-condições base com Diagnóstico, convenções, prova e lacunas, contrato e manutenção. Use os comandos, a URL e a ferramenta de navegador da configuração. Defina aqui o que todos os Arquivos de Feature repetem: a autenticação na condução, as sessões gravadas e o comando base da ferramenta. Os Mapeadores leem este arquivo e não inventam outra convenção.
4. **Mapear:** Na aplicação pequena, grave cada Arquivo de Feature. Na grande, delegue os Domínios com o contrato do modo Criar. Aguarde cada onda antes da próxima.
5. **Reconciliar:**
   - Confira cada retorno: arquivos gravados, cobertura das Âncoras e escrita só na pasta do Domínio. Prove a pasta com `git status`.
   - Resolva Âncoras repetidas ou sem dono. Decida cada proposta de `Fora do mapa`.
   - Unifique convenções divergentes entre Domínios, como nomes de variáveis e arquivos de sessão.
   - Reúna as dúvidas dos retornos. Reporte ao usuário cada comportamento suspeito como possível defeito, com o caso concreto.
   - Grave o índice, a seção `Fora do mapa` e `jornadas.md` com as jornadas candidatas.
   - Rode o conferidor com `--ancoras`. Corrija até passar.
6. **Conduzir:** Faça o Diagnóstico do README. Conduza ao vivo pelo menos uma Feature por Domínio: a mais usada, com sucesso, erro e persistência. Corrija cada receita que falhou por Deriva ou lacuna de condução e rode-a de novo a partir do arquivo. Atualize `Estado:` só nas Features conduzidas.
   - Siga as regras de evidência de `laravel-verification`.
   - Sem navegador, conduza HTTP e Artisan e marque `parcial`, com o motivo.
   - Se o app não inicia, informe o bloqueio exato e mantenha `não conduzida`.
7. **Registrar:** Grave `Base: commit <HEAD> em <data>` no README. Grave a linha de destino na configuração. Rode o conferidor de novo.

## 6. Atualizar
1. **Alcance:** Use o alvo do usuário. Sem alvo, use `git diff <Base>..HEAD` e o working tree. Se o commit da Base não está no histórico, use `git log --since=<data da Base>`.
2. **Features afetadas:** Traduza cada arquivo alterado em Âncoras: a rota, o componente, o comando ou o componente que renderiza a view. Busque cada Âncora no mapa com `rg`. Gere o inventário atual e rode o conferidor com `--ancoras` para achar Âncoras novas e removidas.
3. **Editar:** Atualize Sub-features, entradas, condução e armadilhas das Features afetadas. Uma Feature nova recebe um arquivo e uma linha no índice. Uma Feature removida perde os dois e sai de `jornadas.md`.
4. **Conduzir:** Conduza as entradas alteradas e atualize `Estado:`. Se a receita mudou e você não a conduziu, marque `não conduzida`.
5. **Registrar:** Mova a `Base:` para o HEAD só depois de reconciliar todo o alcance. Rode o conferidor.

Se o alcance toca 3 ou mais Domínios, delegue um Mapeador por Domínio afetado, como no Criar.

## 7. Auditar
1. **Índice:** Rode o conferidor com o inventário atual. Corrija links, arquivos fora do índice e Âncoras sem dono.
2. **Leitura:** Na aplicação grande, envie um Mapeador por Domínio, no modo Auditar. Na pequena, compare cada Feature com o código.
3. **Reconciliar:** Confira por amostra cada Deriva citada com `arquivo:linha`. Procure no histórico recente entradas novas sem Feature. Exija um caminho concreto antes de declarar uma falta.
4. **Conduzir:** Conduza cada Feature do alcance pelo menos uma vez, também quando a leitura não acha Deriva. O agente principal conduz tudo, em série. Faça o Diagnóstico antes da primeira condução e depois de cada falha. Limpe os dados que a condução criou; preserve as evidências.
5. **Triagem:**
   - **Deriva do mapa:** o app está certo e o mapa está errado. Corrija o mapa.
   - **Lacuna de condução:** o app funciona, mas a receita não o conduz. Corrija a receita, ou marque o caminho como manual com o motivo.
   - **Defeito do produto:** o app está errado. Reporte com o caso concreto e ofereça `/bug`. Não altere o mapa nem o código.
6. **Resultado:** Declare um destes resultados:
   - `em dia`: cobertura completa e nada para corrigir.
   - `corrigido`: um conjunto de correções provadas. Releia cada arquivo alterado.
   - `bloqueado`: a cobertura não terminou. Diga o que bloqueou.

## 8. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Li o componente Livewire; a receita está certa." | **Proibido.** A receita fica `não conduzida` até uma condução real. |
| "O app é grande; vou mapear só os menus principais." | **Proibido.** Cada Âncora vai para uma Feature ou para `Fora do mapa`, com o motivo. |
| "O botão sumiu da tela; vou tirar a Sub-feature do mapa." | **Proibido.** Classifique primeiro. Sem commit, Spec ou pedido que explique a remoção, é defeito do produto. Reporte-o. |
| "Os Mapeadores podem conduzir o app em paralelo." | **Proibido.** O agente principal conduz em série. App, banco e sessão locais são compartilhados. |
| "Vou pedir aos Mapeadores o conteúdo dos arquivos para revisar tudo." | **Proibido.** Peça o retorno curto. Leia por amostra e rode o conferidor. |
| "O seed não tem pedido entregue; vou pular esse passo." | **Proibido.** Registre a falta em `Armadilhas` e marque `parcial` ou `bloqueada`. |
| "Mudei uma rota; atualizo o mapa num PR depois." | **Proibido.** Atualize o Arquivo de Feature no mesmo diff. |
| "O conferidor passou; o mapa está certo." | **Proibido.** O conferidor prova forma e cobertura. Só a condução prova comportamento. |

## 9. Prova de Execução (Critério de Saída)
- `[measured]` Saída `OK` do conferidor com `--ancoras` sobre o inventário atual.
- `[measured]` Por Feature, uma linha `Estado:` coerente com o que rodou. No Criar, pelo menos uma Feature `conduzida` por Domínio, ou o bloqueio exato.
- `[measured]` Por condução: ação, comando, resultado e caminho da evidência.
- `[measured]` Na aplicação grande, um retorno por Mapeador, com Domínio, arquivos e cobertura.
- `[measured]` `git status` sem mudança fora do mapa e da linha de destino na configuração.
- `[measured]` No Auditar: o resultado, as Features conduzidas, as Derivas corrigidas e os defeitos reportados.
