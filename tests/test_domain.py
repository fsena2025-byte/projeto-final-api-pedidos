import unittest
from decimal import Decimal
from app.domain import DomainError, Order

class OrderDomainTests(unittest.TestCase):
    def test_calculates_total(self):
        order = Order.create("Ana", [{"product": "Livro", "quantity": 2, "unit_price": 10}])
        self.assertEqual(order.total, Decimal("20.00"))
    def test_rejects_empty_customer(self):
        with self.assertRaises(DomainError): Order.create("", [{"product": "Livro", "quantity": 1, "unit_price": 2}])
    def test_rejects_empty_items(self):
        with self.assertRaises(DomainError): Order.create("Ana", [])
    def test_rejects_invalid_quantity(self):
        with self.assertRaises(DomainError): Order.create("Ana", [{"product": "Livro", "quantity": 0, "unit_price": 2}])
    def test_rejects_invalid_price(self):
        with self.assertRaises(DomainError): Order.create("Ana", [{"product": "Livro", "quantity": 1, "unit_price": -1}])
    def test_rejects_missing_product(self):
        with self.assertRaises(DomainError): Order.create("Ana", [{"product": "", "quantity": 1, "unit_price": 2}])
