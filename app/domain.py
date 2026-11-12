"""Regras do domínio de pedidos."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from uuid import uuid4

class DomainError(ValueError):
    """Erro de validação das regras do domínio."""

@dataclass(frozen=True)
class OrderItem:
    product: str
    quantity: int
    unit_price: Decimal
    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity

@dataclass(frozen=True)
class Order:
    id: str
    customer: str
    items: tuple[OrderItem, ...]
    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0.00"))
    @classmethod
    def create(cls, customer: str, raw_items: list[dict]) -> "Order":
        if not isinstance(customer, str) or not customer.strip():
            raise DomainError("customer é obrigatório")
        if not isinstance(raw_items, list) or not raw_items:
            raise DomainError("o pedido deve possuir ao menos um item")
        items = []
        for raw in raw_items:
            if not isinstance(raw, dict):
                raise DomainError("cada item deve ser um objeto")
            product, quantity, price = raw.get("product"), raw.get("quantity"), raw.get("unit_price")
            if not isinstance(product, str) or not product.strip():
                raise DomainError("product é obrigatório")
            if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
                raise DomainError("quantity deve ser um inteiro positivo")
            try:
                unit_price = Decimal(str(price))
            except (InvalidOperation, TypeError):
                raise DomainError("unit_price deve ser um número válido") from None
            if not unit_price.is_finite() or unit_price <= 0:
                raise DomainError("unit_price deve ser maior que zero")
            items.append(OrderItem(product.strip(), quantity, unit_price.quantize(Decimal("0.01"))))
        return cls(str(uuid4()), customer.strip(), tuple(items))
