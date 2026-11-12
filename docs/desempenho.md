# Desempenho e SLO

## Smoke test
Com a API em execução, rode `k6 run k6-smoke.js`. O script faz 10 iterações com 1 usuário virtual: cria um pedido e consulta o pedido criado, verificando HTTP 201 e HTTP 200.

O threshold é p95 inferior a 1.000 ms e taxa de falhas inferior a 1%. O k6 exibe o p95 no resumo. **O p95 real ainda não foi medido**; execute o teste no ambiente de avaliação e registre aqui o valor observado.

## Métrica
`http_requests_total` em `/metrics`, contador simples de requisições recebidas.

## SLO
Objetivo da demonstração local: 95% das requisições abaixo de 1.000 ms e menos de 1% de falhas. Não representa garantia de produção.
