# WINDS

Dashboard com os proventos do dia a partir dos avisos de proventos publicados pela B3,
calculando quanto você receberia pela quantidade de ações que tem (50 por padrão).

Arquitetura estática e sem servidor: um robô agendado no GitHub Actions coleta e
interpreta os avisos, publica JSON em `data/`, e um site estático no GitHub Pages
faz a conta no navegador.

## Estrutura

```
coletor/            Python: download dos avisos da B3
parser/             Python: texto bruto → eventos; fixtures de avisos reais
pipeline/           Python: gera data/dias/*.json e data/index.json
web/                Vite + React + TypeScript
  src/calculo/      motor de cálculo puro, sem UI
data/               saída publicada (JSON) e config de alíquotas
raw/                avisos brutos por ano/mês
.github/workflows/  ci.yml (e, depois, coleta.yml e deploy.yml)
```

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

O CI roda tudo isso em cada pull request.
