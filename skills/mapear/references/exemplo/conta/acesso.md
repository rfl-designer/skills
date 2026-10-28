# Acesso

O cliente entra com e-mail e senha, sai da conta e recupera a senha por e-mail. Depois de cinco tentativas erradas, o login fica bloqueado por um minuto.

Âncoras: `rota:login`, `rota:logout`, `rota:password.*`, `livewire:auth.login`, `notificacao:ResetPassword`
Estado: não conduzida em 2026-10-28, commit 3f9c2ab; receita derivada do código

## Sub-features

- `acesso-login`: entra com e-mail e senha e abre `Meus pedidos`.
- `acesso-logout`: sai da conta e volta para a página inicial.
- `acesso-recuperar-senha`: envia o link de nova senha e aceita a senha nova.
- `acesso-bloqueio`: bloqueia o login por um minuto depois de cinco erros.

## Como chegar (visão do usuário)

- Escolha `Entrar` no topo da página, ou abra `/login`.
- Escolha `Sair` no menu da conta.
- Escolha `Esqueci minha senha` na tela de login.

## Como conduzir

Pré-condições:

- Banco local com seed recente.
- Nenhuma sessão aberta no navegador.

- **Entrar.** Ação: preencha `E-mail` e `Senha` e escolha `Entrar`. Conduza no navegador configurado, com a senha do seed. Resultado: a página mostra `Meus pedidos`.
- **Sair.** Ação: escolha `Sair` no menu da conta. Resultado: o topo mostra `Entrar` de novo.
- **Recuperar senha.** Ação: escolha `Esqueci minha senha` e envie `cliente@loja.test`. Resultado: a tela mostra `Enviamos o link`, e o Mailpit mostra o e-mail. Abra o link, defina a senha nova e entre com ela.
- **Bloqueio.** Ação: envie uma senha errada cinco vezes. Resultado: a sexta tentativa mostra `Tente de novo em 60 segundos`.

## Armadilhas

- O bloqueio usa o cache. Rode `php artisan cache:clear` depois do item Bloqueio, ou a próxima condução falha.
- O link de nova senha expira em 60 minutos. Gere um novo link a cada condução.
