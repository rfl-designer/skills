# Protocolo reutilizável de verificação

Use quando a feature precisar ser conduzida novamente por outro agente. Atualize o runbook ou teste existente. Com Mapa de Features configurado, registre o protocolo no Arquivo de Feature: pré-condições e condução em `Como conduzir`, limpeza em `Armadilhas`. Senão, use a pasta de Protocolos configurada (`docs/verification/<feature>.md` como fallback). Guarde provas na pasta de Evidências configurada. Reutilize o destino acordado na sessão.

Registre somente o necessário:

1. **Ambiente:** versões e capacidades detectadas, comando de início, URL, health check e configuração de testes. Nunca grave credenciais.
2. **Estado inicial:** factories/seeders e autenticação de teste, isolamento do banco e setup necessário ao probe.
3. **Ação e oráculo:** comandos exatos ou teste permanente, ação do usuário, sinal visível de conclusão e efeito esperado no servidor.
4. **Evidência:** saída, screenshots/logs, estado verificado e caminho dos artefatos. Diferencie probe, teste HTTP e navegador real. Use o nome estável e a validade da seção `Guardar a evidência` da skill.
5. **Limpeza:** remova apenas dados/processos criados para a prova. Preserve evidências fora de diretórios temporários limpos pelo runner.

Execute o protocolo pelo menos uma vez antes de apresentá-lo como validado. Registre qualquer etapa bloqueada. Para Pest Agent, guarde snippets reproduzíveis; não gere outra skill quando um teste ou runbook já atende.
