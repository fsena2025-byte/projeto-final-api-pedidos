import json
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from app.main import create_server

class OrdersApiIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.server = create_server("127.0.0.1", 0, self.temp.name + "/test.db")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=2); self.temp.cleanup()
    def test_create_then_retrieve_order(self):
        payload = {"customer": "Maria", "items": [{"product": "Caderno", "quantity": 3, "unit_price": 4.5}]}
        request = Request(self.base + "/orders", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(request) as response:
            self.assertEqual(response.status, 201); created = json.loads(response.read())
        with urlopen(self.base + "/orders/" + created["id"]) as response:
            retrieved = json.loads(response.read())
        self.assertEqual(retrieved["id"], created["id"]); self.assertEqual(retrieved["total"], "13.50")
    def test_health_and_metrics_endpoints(self):
        with urlopen(self.base + "/health") as response: self.assertEqual(json.loads(response.read())["status"], "ok")
        with urlopen(self.base + "/metrics") as response: metrics = response.read().decode()
        self.assertIn("http_requests_total", metrics)
    def test_unknown_order_returns_404(self):
        with self.assertRaises(HTTPError) as error: urlopen(self.base + "/orders/nao-existe")
        self.assertEqual(error.exception.code, 404)
    def test_invalid_order_returns_400(self):
        request = Request(self.base + "/orders", data=b'{"customer":"","items":[]}', headers={"Content-Type": "application/json"}, method="POST")
        with self.assertRaises(HTTPError) as error: urlopen(request)
        self.assertEqual(error.exception.code, 400)
