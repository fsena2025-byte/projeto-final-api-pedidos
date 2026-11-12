# API de Pedidos

Projeto acadêmico de engenharia de software: API de domínio único para criação e consulta de pedidos, com persistência SQLite, contrato OpenAPI, testes automatizados, CI e smoke test k6.

## Executar

```bash
cp .env.example .env
docker compose up --build
```

API: http://localhost:8000. Health check: `/health`. Métrica: `/metrics`.

## Testes locais

```bash
pip install -r requirements-dev.txt
ruff check app tests
coverage run -m unittest discover -v
coverage report --fail-under=80
```

A suíte contém 10 testes automatizados; na execução local desta entrega, os 10 passaram e a cobertura medida foi 91% (meta mínima: 80%). O lint e a CI remota ainda precisam ser executados no GitHub Actions. O p95 real deve ser obtido executando `k6 run k6-smoke.js` com a API ativa; não há medição de p95 declarada como concluída.

Documentos: `docs/adr-001-repository.md`, `docs/openapi.yaml`, `docs/desempenho.md`, `CONTRIBUTORS.md`.