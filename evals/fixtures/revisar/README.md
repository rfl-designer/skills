# Fixtures de `/revisar`

Uma mudança sobre o app de [`leitura-independente`](../leitura-independente/README.md): o Gerente aprova o Pedido pela lista. O app não roda.

- `mudanca.patch`: o diff `master...feature/aprovar-pela-lista`.
- `spec-aprovar-pela-lista.md`: a Spec aprovada da mudança.
- `mapa-de-fluxos.md`: o Mapa de Fluxos da etapa 2, montado com `rg` no estado da branch.

Para uma execução, monte uma pasta fora do repositório:

1. Copie `../leitura-independente/projeto/` para `<pasta>/projeto/` e aplique o patch: `git apply mudanca.patch`.
2. Copie a Spec para `<pasta>/projeto/docs/specs/0005-aprovar-pela-lista.md`.
3. Copie o patch para `<pasta>/diff.patch` e o mapa para `<pasta>/mapa-de-fluxos.md`.
4. Copie `skills/revisar/` e as 3 disciplinas do revisor para `<pasta>/skills/`.

Dê ao revisor só essa pasta. Não dê esta pasta de fixtures, `evals/cenarios.md` nem os arquivos de resultado: eles descrevem os defeitos plantados.
