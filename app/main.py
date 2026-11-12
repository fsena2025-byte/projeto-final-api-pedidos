"""Servidor HTTP da API de Pedidos."""
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from app.domain import DomainError
from app.repository import SQLiteOrderRepository
from app.service import OrderService
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='{"level":"%(levelname)s","message":"%(message)s"}')
logger = logging.getLogger("orders-api")
REQUEST_COUNT = 0

def serialize(order):
    return {"id": order.id, "customer": order.customer,
            "items": [{"product": i.product, "quantity": i.quantity, "unit_price": str(i.unit_price), "subtotal": str(i.subtotal)} for i in order.items],
            "total": str(order.total)}

class Handler(BaseHTTPRequestHandler):
    service = None
    def _send(self, status, payload, content_type="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        global REQUEST_COUNT
        REQUEST_COUNT += 1
        if self.path == "/health": return self._send(200, {"status": "ok"})
        if self.path == "/metrics":
            body = f"# HELP http_requests_total Total de requisições HTTP\\n# TYPE http_requests_total counter\\nhttp_requests_total {REQUEST_COUNT}\\n".encode()
            return self._send(200, body, "text/plain; version=0.0.4")
        if self.path.startswith("/orders/"):
            order = self.service.get_order(self.path.removeprefix("/orders/"))
            if order is None: return self._send(404, {"error": "pedido não encontrado"})
            return self._send(200, serialize(order))
        return self._send(404, {"error": "rota não encontrada"})
    def do_POST(self):
        global REQUEST_COUNT
        REQUEST_COUNT += 1
        if self.path != "/orders": return self._send(404, {"error": "rota não encontrada"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1000000: return self._send(400, {"error": "corpo da requisição inválido"})
            payload = json.loads(self.rfile.read(length))
            order = self.service.create_order(payload.get("customer"), payload.get("items"))
            logger.info("pedido_criado id=%s total=%s", order.id, order.total)
            return self._send(201, serialize(order))
        except (json.JSONDecodeError, AttributeError, TypeError):
            return self._send(400, {"error": "JSON inválido ou campos ausentes"})
        except DomainError as error:
            return self._send(400, {"error": str(error)})
    def log_message(self, fmt, *args):
        logger.info("http client=%s message=%s", self.client_address[0], fmt % args)

def create_server(host="0.0.0.0", port=8000, database_path=None):
    path = database_path or os.getenv("DATABASE_PATH", "/data/orders.db")
    Handler.service = OrderService(SQLiteOrderRepository(path))
    return ThreadingHTTPServer((host, port), Handler)

if __name__ == "__main__":
    server = create_server(port=int(os.getenv("PORT", "8000")))
    logger.info("api_iniciada port=%s", server.server_port)
    server.serve_forever()
