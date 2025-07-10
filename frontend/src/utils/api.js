const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
    
  static getCSRFTokenFromCookie() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

static async getCSRFToken() {
    // Try to get from cookie first
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    if (match) return match[1];

    // If not found, fetch from API and try again
    await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include',
    });
    const newMatch = document.cookie.match(/csrftoken=([^;]+)/);
    return newMatch ? newMatch[1] : '';
}

  static async getAuthHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    // Get auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Get CSRF token
    const csrfToken = await this.getCSRFToken();
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
    
    return headers;
  }

  // Journey Templates
  static async getJourneyTemplates(params = {}) {
    const queryParams = new URLSearchParams(params).toString();
    return this.request(`/boarding/templates/?${queryParams}`);
  }

  static async createJourneyTemplate(data) {
    return this.request('/boarding/templates/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Get a specific journey template by ID
  static async getJourneyTemplate(templateId) {
    try {
      const response = await this.request(`/boarding/templates/${templateId}/`, {
        method: 'GET',
      });
      return response;
    } catch (error) {
      console.error('Failed to fetch journey template:', error);
      throw error;
    }
  }

  // Update a journey template
  static async updateJourneyTemplate(templateId, data) {
    try {
      const response = await this.request(`/boarding/templates/${templateId}/`, {
        method: 'PUT',
        body: JSON.stringify(data),
      });
      return response;
    } catch (error) {
      console.error('Failed to update journey template:', error);
      throw error;
    }
  }

  // Delete a journey template
  static async deleteJourneyTemplate(templateId) {
    try {
      const response = await this.request(`/boarding/templates/${templateId}/`, {
        method: 'DELETE',
      });
      return response;
    } catch (error) {
      console.error('Failed to delete journey template:', error);
      throw error;
    }
  }

  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = await this.getAuthHeaders();
    
    const config = {
      credentials: 'include',
      headers: {
        ...headers,
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (response.status === 401) {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
        return;
      }
      
      if (!response.ok) {
        const errorText = await response.text();
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { detail: errorText };
        }
        console.error(`API Error ${response.status}:`, errorData);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail || errorText}`);
      }
      
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      
      return await response.text();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Accounts
  static async getAccounts() {
    return this.request('/accounts/');
  }

  // Departments and Business Units
  static async getDepartments() {
    return this.request('/boarding/templates/departments/');
  }

  static async getBusinessUnits() {
    return this.request('/boarding/templates/business_units/');
  }

  static async getUserData() {
    return this.request('/users/userdata/');
  }

  // Authentication
  static async login(credentials) {
    return this.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  static async logout() {
    return this.request('/auth/logout/', {
      method: 'POST',
    });
  }
}

export default ApiService;
