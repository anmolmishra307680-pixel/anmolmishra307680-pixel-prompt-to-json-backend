# Frontend Integration Guide

## Quick Setup

### 1. Authentication Flow
```javascript
// Get JWT token
async function getAuthToken() {
  const response = await fetch('/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'bhiv-secret-key-2024'
    },
    body: JSON.stringify({
      username: 'admin',
      password: 'bhiv2024'
    })
  });
  const data = await response.json();
  return data.access_token;
}
```

### 2. API Client Setup
```javascript
class DesignAPI {
  constructor(baseURL = 'https://prompt-to-json-backend.onrender.com') {
    this.baseURL = baseURL;
    this.apiKey = 'bhiv-secret-key-2024';
    this.token = null;
  }

  async authenticate() {
    this.token = await getAuthToken();
  }

  async generateDesign(prompt) {
    const response = await fetch(`${this.baseURL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({ prompt })
    });
    return response.json();
  }
}
```

### 3. React Hook Example
```javascript
import { useState, useEffect } from 'react';

export function useDesignAPI() {
  const [api] = useState(() => new DesignAPI());
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    api.authenticate().then(() => setIsAuthenticated(true));
  }, []);

  return { api, isAuthenticated };
}
```

## Error Handling
```javascript
async function safeAPICall(apiFunction) {
  try {
    return await apiFunction();
  } catch (error) {
    if (error.status === 401) {
      // Re-authenticate
      await api.authenticate();
      return await apiFunction();
    }
    throw error;
  }
}
```

## Environment Variables
```env
REACT_APP_API_URL=https://prompt-to-json-backend.onrender.com
REACT_APP_API_KEY=bhiv-secret-key-2024
```

## TypeScript Types
```typescript
interface DesignSpec {
  design_type: string;
  materials: string[];
  dimensions: Record<string, number>;
  performance_specs: Record<string, any>;
  components: string[];
  features: string[];
  sustainability: Record<string, any>;
  cost_estimate?: number;
}

interface GenerateRequest {
  prompt: string;
}
```