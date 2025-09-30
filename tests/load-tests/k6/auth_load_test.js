import http from "k6/http";
import { sleep, check } from "k6";

export let options = {
  vus: __ENV.VUS ? Number(__ENV.VUS) : 10,
  duration: __ENV.DURATION || "2m",
  thresholds: {
    http_req_duration: ["p(95)<3000"],
    http_req_failed: ["rate<0.05"],
  },
};

export default function () {
  const baseUrl = __ENV.TARGET_URL || "http://localhost:8000";
  const apiKey = __ENV.API_KEY || "bhiv-secret-key-2024";
  
  // Step 1: Get JWT token
  const tokenPayload = JSON.stringify({
    username: "admin",
    password: "bhiv2024"
  });
  
  const tokenRes = http.post(`${baseUrl}/token`, tokenPayload, {
    headers: { "Content-Type": "application/json" }
  });
  
  check(tokenRes, {
    "token request successful": (r) => r.status === 200,
    "token response has access_token": (r) => JSON.parse(r.body).access_token !== undefined,
  });
  
  if (tokenRes.status !== 200) {
    console.log("Failed to get token, skipping authenticated requests");
    return;
  }
  
  const token = JSON.parse(tokenRes.body).access_token;
  
  // Step 2: Use token for authenticated requests
  const generatePayload = JSON.stringify({
    prompt: "Design a modern office building with sustainable features"
  });
  
  const authHeaders = {
    "Content-Type": "application/json",
    "X-API-Key": apiKey,
    "Authorization": `Bearer ${token}`
  };
  
  const generateRes = http.post(`${baseUrl}/generate`, generatePayload, {
    headers: authHeaders
  });
  
  check(generateRes, {
    "generate request successful": (r) => r.status === 200,
    "generate response has spec": (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.spec !== undefined;
      } catch (e) {
        return false;
      }
    },
    "generate response time < 3000ms": (r) => r.timings.duration < 3000,
  });
  
  sleep(2);
}