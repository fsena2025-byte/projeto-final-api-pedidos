"""Persistência SQLite usando o padrão Repository."""
import json
import sqlite3
from decimal import Decimal
from pathlib import Path
from app.domain import Order, OrderItem

class SQLiteOrderRepository:
    def __init__(self, database_path: str):
        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY, customer TEXT NOT NULL, items TEXT NOT NULL,
                total TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")
    def _connect(self):
        return sqlite3.connect(self.database_path)
    def save(self, order: Order) -> None:
        items = [{"product": i.product, "quantity": i.quantity, "unit_price": str(i.unit_price)} for i in order.items]
        with self._connect() as connection:
            connection.execute("INSERT INTO orders (id, customer, items, total) VALUES (?, ?, ?, ?)",
                               (order.id, order.customer, json.dumps(items), str(order.total)))
    def get(self, order_id: str) -> Order | None:
        with self._connect() as connection:
            row = connection.execute("SELECT id, customer, items FROM orders WHERE id = ?", (order_id,)).fetchone()
        if row is None:
            return None
        items = tuple(OrderItem(i["product"], i["quantity"], Decimal(i["unit_price"])) for i in json.loads(row[2]))
        return Order(row[0], row[1], items)
