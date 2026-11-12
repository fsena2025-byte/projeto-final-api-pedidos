import http from 'k6/http';
import { check } from 'k6';
export const options = { vus: 1, iterations: 10, thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<1000'] } };
export default function () {
  const base = __ENV.BASE_URL || 'http://localhost:8000';
  const payload = JSON.stringify({ customer: 'Smoke Test', items: [{ product: 'Caneta', quantity: 2, unit_price: 3.25 }] });
  const response = http.post(`${base}/orders`, payload, { headers: { 'Content-Type': 'application/json' } });
  check(response, { 'pedido criado (201)': (r) => r.status === 201 });
  if (response.status === 201) {
    const id = response.json('id');
    const lookup = http.get(`${base}/orders/${id}`);
    check(lookup, { 'pedido consultado (200)': (r) => r.status === 200 && r.json('id') === id });
  }
}
