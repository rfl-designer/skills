---
name: laravel-verification
description: Portão obrigatório de Prova de Execução para PHP, Laravel e Livewire (Pest, Larastan/PHPStan e Laravel Pint em .php e .blade.php). Use antes de qualquer commit, PR ou encerramento de tarefa.
---

# Portão de Prova de Execução Laravel (`laravel-verification`)

## 1. Objetivo
Impedir que qualquer código seja considerado pronto sem evidência real medida no terminal através da tríade obrigatória: **Pest**, **Larastan/PHPStan** e **Laravel Pint** (para `.php` e `.blade.php`).

## 2. Regras Inegociáveis
- **Zero confiança em inspeção visual:** "Parece correto" ou "deve passar" nunca é aceito. Execute os comandos reais no terminal.
- **Rotule cada evidência honestamente:** Use `[measured]` apenas para comandos executados nesta sessão após a última edição de arquivo. Se um comando não pôde rodar, rotule como `[inferred]` ou `[guess]` e explique o bloqueio.
- **Proíba sabotagem de verificadores (Floor Guard):** Nunca adicione `@phpstan-ignore`, `phpstan-baseline` falso, `pint.json` permissivo ou `->skip()` em testes para forçar o painel a ficar verde.

## 3. Os 3 Comandos Obrigatórios do Portão
Execute sempre nesta ordem após qualquer alteração de código:

1. **Formatação Estrita (`.php` e `.blade.php`):**
   ```bash
   ./vendor/bin/pint --test
   ```
   *(Se falhar, execute `./vendor/bin/pint` para corrigir arquivos `.php` e templates `.blade.php`, e rode `--test` novamente).*

2. **Análise Estática de Tipos e Domínio:**
   ```bash
   ./vendor/bin/phpstan analyse --memory-limit=2G
   ```

3. **Suíte de Testes Comportamentais e Arquiteturais:**
   ```bash
   ./vendor/bin/pest
   ```

## 4. Racionalizações Proibidas (Anti-Atalho)
| Desculpa do Agente | Regra Correta |
|---|---|
| "Alterei apenas um template `.blade.php`, não preciso rodar o Pint nem o Pest." | **Proibido.** O Pint formata `.blade.php` e mudanças no Blade podem quebrar componentes Livewire no Pest. |
| "Rodei os testes há 5 minutos e só mudei uma linha depois disso." | **Proibido.** Qualquer edição invalida a medição anterior. Rode a tríade novamente. |
| "Vou colocar `@phpstan-ignore-next-line` porque o relacionamento Eloquent deu aviso." | **Proibido.** Declare os generics/PHPDocs corretos no Model ou use tipos explícitos. |

## 5. Prova de Execução (Critério de Saída)
Reporte no resumo final da tarefa:
- `[measured]` `./vendor/bin/pint --test` → PASS (arquivos `.php` e `.blade.php`).
- `[measured]` `./vendor/bin/phpstan analyse` → 0 erros.
- `[measured]` `./vendor/bin/pest` → Todos os testes verdes.
