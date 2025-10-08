/**
 * React Native Expo wrapper for BHIV Backend
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

class BHIVMobileClient {
  constructor(baseUrl = 'https://prompt-to-json-backend.onrender.com') {
    this.baseUrl = baseUrl;
    this.apiKey = 'bhiv-secret-key-2024';
    this.token = null;
  }

  async login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'X-API-Key': this.apiKey,
      },
      body: formData,
    });

    const data = await response.json();
    this.token = data.access_token;
    await AsyncStorage.setItem('bhiv_token', this.token);
    return data;
  }

  async generate(prompt, context = {}) {
    const response = await fetch(`${this.baseUrl}/api/v1/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        'Authorization': `Bearer ${this.token}`,
      },
      body: JSON.stringify({
        prompt,
        context: {
          ...context,
          mobile_optimized: true,
          low_poly: true,
        },
      }),
    });

    return await response.json();
  }

  async switch(specId, targetObjectId, material, properties = {}) {
    const response = await fetch(`${this.baseUrl}/api/v1/switch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        'Authorization': `Bearer ${this.token}`,
      },
      body: JSON.stringify({
        spec_id: specId,
        target: { object_id: targetObjectId },
        update: { material, properties },
        note: `Mobile switch: ${material}`,
      }),
    });

    return await response.json();
  }

  async getPreview(specId) {
    const response = await fetch(`${this.baseUrl}/api/v1/vr/preview?spec_id=${specId}`, {
      headers: {
        'X-API-Key': this.apiKey,
        'Authorization': `Bearer ${this.token}`,
      },
    });

    return await response.json();
  }
}

export default BHIVMobileClient;