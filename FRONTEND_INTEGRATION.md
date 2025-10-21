# Frontend Integration Guide - Firebase Auth with FastAPI

This document explains how to integrate your React/Astro frontend with the FastAPI backend using Firebase Authentication.

## Overview

The authentication flow works as follows:
1. User logs in via Firebase on your main web app
2. Frontend obtains Firebase ID token from authenticated user
3. Frontend sends token in `Authorization` header with each API request
4. FastAPI backend validates token and grants access to environmental metrics data

## Prerequisites

Ensure your React/Astro app already has:
- Firebase initialized and configured
- User authentication working (sign-in/sign-up)
- Firebase user object available after login

## Implementation Steps

### 1. Getting the Firebase ID Token

After a user is authenticated, you need to retrieve their ID token:

```javascript
import { getAuth } from 'firebase/auth';

// Get the current authenticated user
const auth = getAuth();
const user = auth.currentUser;

if (user) {
  // Get the ID token
  const idToken = await user.getIdToken();
  console.log('Token:', idToken);
} else {
  console.log('No user is signed in');
}
```

**Important Notes:**
- ID tokens are short-lived (typically 1 hour)
- Firebase automatically refreshes them
- Use `getIdToken()` to always get a fresh token (it returns cached valid token or fetches new one)
- Use `getIdToken(true)` to force refresh the token

### 2. Making API Requests with the Token

#### Option A: Using Fetch API

```javascript
const fetchMetrics = async () => {
  const auth = getAuth();
  const user = auth.currentUser;

  if (!user) {
    throw new Error('User not authenticated');
  }

  // Get fresh token
  const token = await user.getIdToken();

  // Make API request
  const response = await fetch('https://your-api-url.com/api/metrics', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  const data = await response.json();
  return data;
};
```

#### Option B: Using Axios

```javascript
import axios from 'axios';
import { getAuth } from 'firebase/auth';

const fetchMetrics = async () => {
  const auth = getAuth();
  const user = auth.currentUser;

  if (!user) {
    throw new Error('User not authenticated');
  }

  const token = await user.getIdToken();

  const response = await axios.get('https://your-api-url.com/api/metrics', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  return response.data;
};
```

### 3. Creating an API Client (Recommended Approach)

Create a reusable API client to avoid repeating token logic:

```javascript
// src/services/apiClient.js
import { getAuth } from 'firebase/auth';

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  async getAuthToken() {
    const auth = getAuth();
    const user = auth.currentUser;

    if (!user) {
      throw new Error('User not authenticated');
    }

    return await user.getIdToken();
  }

  async request(endpoint, options = {}) {
    const token = await this.getAuthToken();

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API error: ${response.status}`);
    }

    return await response.json();
  }

  // Convenience methods
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
}

export const apiClient = new ApiClient();
```

**Usage:**

```javascript
import { apiClient } from './services/apiClient';

// In your React component
const AirQualityDashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        setLoading(true);
        const data = await apiClient.get('/api/air-quality');
        setMetrics(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadMetrics();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return <div>{/* Display metrics */}</div>;
};
```

### 4. Handling Authentication State

Use Firebase's auth state observer to track when users log in/out:

```javascript
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { useEffect, useState } from 'react';

const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const auth = getAuth();
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  return { user, loading };
};

// Usage in components
const MyComponent = () => {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>Please log in</div>;

  // User is authenticated, safe to make API calls
  return <div>Welcome {user.email}</div>;
};
```

### 5. Error Handling

Handle common authentication errors:

```javascript
const handleApiCall = async () => {
  try {
    const data = await apiClient.get('/api/metrics');
    return data;
  } catch (error) {
    if (error.message.includes('not authenticated')) {
      // Redirect to login
      window.location.href = '/login';
    } else if (error.message.includes('401')) {
      // Token expired or invalid - try refreshing
      const auth = getAuth();
      const user = auth.currentUser;
      if (user) {
        await user.getIdToken(true); // Force refresh
        // Retry request
      }
    } else {
      // Other errors
      console.error('API error:', error);
    }
  }
};
```

### 6. Axios Interceptor Approach (Alternative)

For larger applications using Axios, set up interceptors:

```javascript
// src/services/axios.js
import axios from 'axios';
import { getAuth } from 'firebase/auth';

const axiosInstance = axios.create({
  baseURL: import.meta.env.PUBLIC_API_URL || 'http://localhost:8000'
});

// Request interceptor to add token
axiosInstance.interceptors.request.use(
  async (config) => {
    const auth = getAuth();
    const user = auth.currentUser;

    if (user) {
      const token = await user.getIdToken();
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try to refresh
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        try {
          await user.getIdToken(true); // Force refresh
          // Retry the original request
          error.config.headers.Authorization = `Bearer ${await user.getIdToken()}`;
          return axiosInstance.request(error.config);
        } catch (refreshError) {
          // Redirect to login
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
```

**Usage:**

```javascript
import axiosInstance from './services/axios';

// Token is automatically added
const data = await axiosInstance.get('/api/air-quality');
```

## Testing the Integration

### 1. Check Token in Browser Console

```javascript
// In browser console after logging in
const auth = getAuth();
const user = auth.currentUser;
user.getIdToken().then(token => console.log(token));
```

### 2. Manual API Test with cURL

```bash
# Copy token from console, then test:
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     http://localhost:8000/api/metrics
```

### 3. Verify Token Expiration Handling

Tokens expire after 1 hour. Test that your app:
- Automatically refreshes tokens
- Handles 401 errors gracefully
- Doesn't require user to log in again

## Environment Variables

Set up environment variables for API URL:

```bash
# .env.local (for local development)
PUBLIC_API_URL=http://localhost:8000

# .env.production (for production)
PUBLIC_API_URL=https://api.yourapp.com
```

## Security Checklist

- ✅ Never store tokens in localStorage (use Firebase SDK methods only)
- ✅ Always use HTTPS in production
- ✅ Send tokens only in `Authorization` header
- ✅ Handle token expiration gracefully
- ✅ Check auth state before making API calls
- ✅ Don't expose tokens in URLs or logs
- ✅ Set up CORS properly on backend

## Common Issues

### Issue: "User not authenticated" error
**Solution:** Ensure Firebase auth is initialized and user is logged in before making API calls

### Issue: 401 Unauthorized from API
**Solution:**
- Verify token is being sent correctly
- Check backend Firebase configuration matches frontend
- Force refresh token: `user.getIdToken(true)`

### Issue: CORS errors
**Solution:** Backend needs to allow requests from your frontend domain

### Issue: Token in wrong format
**Solution:** Ensure you're sending `Bearer ${token}`, not just `${token}`

## Next Steps

Once backend is ready:
1. Replace `API_BASE_URL` with actual backend URL
2. Implement the API client service
3. Test with a simple endpoint first
4. Add error handling and loading states
5. Implement retry logic for failed requests

## Questions?

If you encounter issues during implementation, check:
1. Firebase Console - ensure app is configured correctly
2. Network tab - verify token is in request headers
3. Backend logs - check what error FastAPI is returning
