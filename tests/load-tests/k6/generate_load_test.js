import http from "k6/http";
import { sleep, check } from "k6";

export let options = {
  vus: __ENV.VUS ? Number(__ENV.VUS) : 50,
  duration: __ENV.DURATION || "3m",
  thresholds: {
    http_req_duration: ["p(95)<2000"], // 95% of requests must complete below 2s
    http_req_failed: ["rate<0.1"],     // Error rate must be below 10%
  },
};

export default function () {
  const baseUrl = __ENV.TARGET_URL || "http://localhost:8000";
  const apiKey = __ENV.API_KEY || "bhiv-secret-key-2024";
  const token = __ENV.JWT_TOKEN || "";
  
  // Test different endpoints
  const endpoints = [
    {
      url: `${baseUrl}/generate`,
      payload: JSON.stringify({ prompt: "Design a small concrete bridge for pedestrians" }),
      method: "POST"
    },
    {
      url: `${baseUrl}/health`,
      payload: null,
      method: "GET"
    },
    {
      url: `${baseUrl}/basic-metrics`,
      payload: null,
      method: "GET"
    }
  ];
  
  // Randomly select an endpoint to test
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  
  const headers = {
    "Content-Type": "application/json",
    "X-API-Key": apiKey
  };
  
  // Add JWT token if available and endpoint requires auth
  if (token && endpoint.url.includes("/generate")) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  
  const params = { headers: headers };
  
  let res;
  if (endpoint.method === "POST") {
    res = http.post(endpoint.url, endpoint.payload, params);
  } else {
    res = http.get(endpoint.url, params);
  }
  
  // Check response status
  const isHealthOrMetrics = endpoint.url.includes("/health") || endpoint.url.includes("/metrics");
  const expectedStatus = isHealthOrMetrics ? 200 : (token ? 200 : 401);
  
  check(res, {
    [`status is ${expectedStatus}`]: (r) => r.status === expectedStatus,
    "response time < 2000ms": (r) => r.timings.duration < 2000,
    "response has body": (r) => r.body.length > 0,
  });
  
  sleep(1);
}