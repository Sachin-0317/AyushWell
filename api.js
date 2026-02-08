const API_BASE_URL = 'http://localhost:5000/api';
let authToken = localStorage.getItem('authToken');

const api = {
    async call(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };

        if (authToken) {
            options.headers['Authorization'] = authToken;
        }

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'API request failed');
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async register(userData) {
        return this.call('/register', 'POST', userData);
    },

    async login(credentials) {
        const response = await this.call('/login', 'POST', credentials);
        authToken = response.token;
        localStorage.setItem('authToken', authToken);
        return response;
    },

    async logout() {
        await this.call('/logout', 'POST');
        authToken = null;
        localStorage.removeItem('authToken');
    },

    async submitAssessment(answers) {
        return this.call('/assessment', 'POST', { answers });
    },

    async getAssessment() {
        return this.call('/assessment/current');
    },

    async getProgress(days = 7) {
        return this.call(`/progress?days=${days}`);
    },

    async addProgress(progressData) {
        return this.call('/progress', 'POST', progressData);
    },

    async sendMessage(message) {
        return this.call('/chatbot', 'POST', { message });
    }
};