# WINDS

Dashboard com os proventos do dia a partir do boletim diário de proventos publicado pela
B3, calculando quanto você receberia pela quantidade de ações que tem (50 por padrão).

Arquitetura estática e sem servidor: um robô agendado coleta e interpreta o boletim,
publica JSON no branch `dados`, e um site estático no GitHub Pages faz a conta no
navegador.

## Estrutura

Branches de código (`main`, `develop` e os de trabalho):

```
coletor/            Python: listagem e download do boletim
parser/             Python: texto bruto → proventos; fixtures de boletins reais
pipeline/           Python: gera os arquivos publicados
web/                Vite + React + TypeScript
  src/calculo/      motor de cálculo puro, sem UI
config/             aliquotas.json e o JSON Schema do contrato
docs/               fonte-b3.md e decisões
.github/workflows/  ci.yml (e, depois, coleta.yml, deploy.yml e revisao.yml)
```

`data/` (JSON publicado) e `raw/` (boletins brutos) ficam no branch órfão `dados`,
escrito só pelo robô.

## Desenvolvimento

Python (requer [uv](https://docs.astral.sh/uv/)):

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Web:

```bash
cd web
npm ci
npm run lint && npm run typecheck && npm test && npm run build
```

O CI roda tudo isso em cada pull request. Fluxo de branches e padrão de commits: [CONTRIBUTING.md](CONTRIBUTING.md).
