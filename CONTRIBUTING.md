# Como contribuir

## Branches (git flow)

| Branch | Para quê | Sai de | Volta para |
|---|---|---|---|
| `main` | Versão publicada | n/a | n/a |
| `develop` | Integração do que está pronto | `main` | `main` (via release) |
| `feature/<descricao>` | Uma tarefa ou funcionalidade | `develop` | `develop` |
| `release/<versao>` | Preparar uma versão | `develop` | `main` e `develop` |
| `hotfix/<descricao>` | Correção urgente em produção | `main` | `main` e `develop` |

Nomes em minúsculas, com hífen: `feature/t2-coletor`, `hotfix/parser-linha-vazia`.

Toda mudança entra por pull request, com o CI verde. Features vão para `develop`;
só `release/*` e `hotfix/*` vão para `main`.

## Commits (Conventional Commits)

```
<tipo>(<escopo opcional>): <resumo no imperativo, em português>
```

Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`.
Escopos comuns: `coletor`, `parser`, `pipeline`, `web`, `calculo`, `ci`.

Exemplos:

```
feat(coletor): baixar o boletim diário de proventos
fix(parser): herdar o ISIN da linha anterior quando vier em branco
ci: rodar o build do web no CI
```

O título do PR segue o mesmo formato.
