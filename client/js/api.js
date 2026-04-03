/** 
 * API Service for NutriCore 2.0
 * Handles all network requests with central JWT token management
 */

const API_BASE_URL = 'http://localhost:5000/api';

const api = {
  /**
   * Internal request wrapper
   */
  async _request(endpoint, options = {}) {
    // Inject JWT token if available
    const token = sessionStorage.getItem('access_token');
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle token expiration specifically
        if (response.status === 401 && token) {
          console.warn('Session expired. Redirecting to login.');
          sessionStorage.removeItem('access_token');
          window.location.href = '/pages/login.html';
        }
        throw new Error(data.msg || 'API Request failed');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error.message);
      throw error;
    }
  },

  // Auth Endpoints
  async login(email, password) {
    const data = await this._request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    
    if (data.access_token) {
      sessionStorage.setItem('access_token', data.access_token);
      sessionStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  async register(userData) {
    return await this._request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  },

  async getProfile() {
    return await this._request('/auth/profile');
  },

  // Risk Endpoints
  async getRiskScores() {
    return await this._request('/risk/scores');
  },

  // Meal Endpoints
  async logMeal(mealData) {
    return await this._request('/meals', {
      method: 'POST',
      body: JSON.stringify(mealData)
    });
  }
};

// Export for use in other scripts
// Using window.api for simplicity in vanilla JS without build tools
window.api = api;
