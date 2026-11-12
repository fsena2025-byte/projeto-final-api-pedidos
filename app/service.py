"""Caso de uso: criação e consulta de pedidos."""
from typing import Protocol
from app.domain import Order

class OrderRepository(Protocol):
    """Contrato de persistência requerido pelo serviço."""
    def save(self, order: Order) -> None: ...
    def get(self, order_id: str) -> Order | None: ...

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    def create_order(self, customer: str, items: list[dict]) -> Order:
        order = Order.create(customer, items)
        self.repository.save(order)
        return order
    def get_order(self, order_id: str) -> Order | None:
        return self.repository.get(order_id)
