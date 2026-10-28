# Formatos da pasta de ensino

A pasta `docs/ensino/<tema>/` guarda o estado de um tema. Uma pasta serve a um tema só. Crie cada arquivo só ao gravar o primeiro conteúdo.

```
docs/ensino/<tema>/
├── MISSAO.md
├── REGISTROS.md
├── FONTES.md
├── GLOSSARIO.md
├── NOTAS.md
└── licoes/0001-<nome>.html
```

## `MISSAO.md` (só no Curso)

```md
# Missão: {Tema}

## Por quê
{1 a 3 frases. O objetivo concreto. O que muda no trabalho do usuário quando ele domina o tema.}

## Sucesso
- {Uma ação observável que o usuário vai fazer}

## Limites
- {Tempo, preferências e restrições}

## Fora do escopo
- {Temas vizinhos que o usuário não quer agora}
```

- **Prefira o concreto:** "Revisar PRs com Livewire sem ajuda" é melhor que "aprender Livewire".
- **Questione o vago:** Sem um motivo concreto, continue a entrevista. Uma Missão ruim é pior que nenhuma.
- **Mantenha curta:** A Missão cabe numa tela.
- **Atualize quando muda:** Confirme com o usuário e grave um Registro sobre a mudança.

## `REGISTROS.md`

```md
# Registros: {Tema}

## Lições
| # | Lição | Destino | Conteúdo |
|---|---|---|---|
| 0001 | Eager loading no Eloquent | licoes/0001-eager-loading.html | `with()`, consultas N+1 |
| 0002 | Ciclo de vida do Livewire | {link do artefato} | `mount()`, `hydrate()` |

## Registros

### RA-0001: Identifica consultas N+1 no log
O usuário achou o N+1 no log de consultas sem ajuda. A próxima Lição pode usar `with()` sem explicar o problema de novo.
Evidência: acertou de memória a questão 2 da Lição 0001.
```

- **O índice registra a cobertura:** Cada Lição entregue entra na tabela, com o caminho ou o link.
- **O Registro registra a aprendizagem:** Numere `RA-NNNN` a partir do maior número existente. Escreva de 1 a 3 frases: o que o usuário sabe agora e o que isso muda nas próximas Lições.
- **Grave um Registro quando:**
  1. O usuário mostra que usa um conceito não trivial corretamente.
  2. O usuário declara conhecimento prévio. Registre também a profundidade declarada.
  3. Um erro de entendimento foi corrigido. Este Registro prevê dificuldades em temas vizinhos.
  4. A Missão mudou.
- **Não grave Registro para:** conteúdo só apresentado, termo já definido em `GLOSSARIO.md` ou diário de sessão.
- **Não apague Registros:** Quando um Registro novo contradiz um antigo, acrescente ao antigo `Status: substituído por RA-NNNN`.

## `FONTES.md`

```md
# Fontes: {Tema}

## Conhecimento
- [Laravel 12.x: Eager Loading](https://laravel.com/docs/12.x/eloquent-relationships#eager-loading)
  Versão: 12.x, de `composer.lock`. Use para: carregar relações sem N+1.

## Comunidades
- {Nome e link da comunidade}
  Use para: {dúvidas de julgamento que ela responde bem}

## Lacunas
- {Área da Missão sem fonte boa}
```

- **Só fonte de alta confiança:** Documentação oficial primeiro. Retire o material de marketing.
- **Anote cada fonte:** Uma linha com a versão e o uso. Um link sem anotação perde o valor.
- **Retire a fonte errada ou rasa:** Cinco fontes boas valem mais que trinta medianas.
- **Registre a recusa:** Se o usuário não quer comunidades, escreva isso em `NOTAS.md`.

## `GLOSSARIO.md`

```md
# Glossário: {Tema}

**Eager loading**:
Carga das relações de um conjunto de Models numa consulta adicional, antes do uso.
_Evite_: pré-carga, carregamento ansioso
```

- **Acrescente o termo só quando o usuário o usa corretamente.** O glossário registra conhecimento comprimido. Não é material de leitura.
- **Escolha um termo:** Liste os sinônimos em `_Evite_`.
- **Defina em 1 ou 2 frases:** Diga o que o termo é, não como usá-lo.
- **Não duplique o domínio:** Termos de negócio ficam no glossário configurado do projeto.

## `NOTAS.md`

Texto livre, curto. Comece pelo destino:

```md
Destino: arquivo local
- Prefere exemplos do próprio código a exemplos genéricos.
- Não quer indicação de comunidades.
```
