import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up to 10 users
    { duration: '1m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 100 }, // Ramp up to 100 users
    { duration: '1m', target: 100 },  // Stay at 100 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    http_req_failed: ['rate<0.1'],    // Error rate under 10%
  },
};

const BASE_URL = 'https://prompt-to-json-backend.onrender.com';
const API_KEY = 'bhiv-secret-key-2024';

export default function() {
  // Test health endpoint
  let healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health check status is 200': (r) => r.status === 200,
  });

  // Test generate endpoint
  let generateRes = http.post(`${BASE_URL}/generate`, 
    JSON.stringify({ prompt: 'Modern office building' }),
    {
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
    }
  );
  
  check(generateRes, {
    'generate status is 200': (r) => r.status === 200,
    'generate has spec': (r) => JSON.parse(r.body).spec !== undefined,
  });

  sleep(1);
}