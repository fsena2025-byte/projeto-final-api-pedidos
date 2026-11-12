# ADR 001 — Persistência por Repository

- **Status:** Aceito
- **Data:** 12/11/2026

## Contexto
O domínio de pedidos precisa salvar e consultar pedidos sem acoplar regras de negócio ao SQLite.

## Decisão
Adotar Repository em `SQLiteOrderRepository`. `OrderService` depende do contrato `save/get`, não conhece SQL e o repositório encapsula conexão e conversão.

## Alternativas
- SQL diretamente no serviço: rejeitado por misturar responsabilidades.
- ORM: rejeitado por adicionar dependências desnecessárias ao escopo.

## Consequências
Facilita testes isolados e eventual troca da persistência. SQLite atende à demonstração local, não a cenários de alta concorrência ou escala distribuída.
