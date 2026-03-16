/**
 * API Client - Centralisation des appels API
 * Gère les headers, erreurs, et retry automatique
 */

class ApiClient {
    constructor() {
        this.baseURL = '';
        this.timeout = 30000; // 30 secondes
        this.retryCount = 3;
        this.pendingRequests = new Map();
    }

    async request(url, options = {}) {
        const requestKey = `${options.method || 'GET'}_${url}`;
        
        // Annuler la requête précédente si elle existe
        if (this.pendingRequests.has(requestKey)) {
            this.pendingRequests.get(requestKey).abort();
        }

        const controller = new AbortController();
        this.pendingRequests.set(requestKey, controller);

        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin',
            signal: controller.signal,
        };

        // Ajouter le token CSRF
        const csrfToken = this.getCsrfToken();
        if (csrfToken) {
            defaultOptions.headers['X-CSRFToken'] = csrfToken;
        }

        const config = { ...defaultOptions, ...options };
        config.headers = { ...defaultOptions.headers, ...(options.headers || {}) };

        try {
            const response = await this.fetchWithTimeout(url, config);
            
            // Nettoyer la requête
            this.pendingRequests.delete(requestKey);

            if (!response.ok) {
                await this.handleError(response);
            }

            return response;
        } catch (error) {
            this.pendingRequests.delete(requestKey);
            
            if (error.name === 'AbortError') {
                throw new Error('Requête annulée');
            }
            
            throw error;
        }
    }

    async fetchWithTimeout(url, config) {
        const timeoutId = setTimeout(() => {
            if (config.signal) {
                config.signal.abort();
            }
        }, this.timeout);

        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    async handleError(response) {
        let errorMessage = 'Une erreur est survenue';

        try {
            const data = await response.json();
            errorMessage = data.message || data.error || errorMessage;
        } catch (e) {
            // Si la réponse n'est pas du JSON, utiliser le texte
            const text = await response.text();
            if (text) {
                errorMessage = text;
            }
        }

        // Afficher un toast d'erreur
        if (window.showToast) {
            window.showToast(errorMessage, 'error');
        }

        throw new Error(errorMessage);
    }

    getCsrfToken() {
        // Récupérer le token CSRF depuis les cookies
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

    // Méthodes HTTP
    async get(url, options = {}) {
        return this.request(url, { ...options, method: 'GET' });
    }

    async post(url, data = {}, options = {}) {
        return this.request(url, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async put(url, data = {}, options = {}) {
        return this.request(url, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async delete(url, options = {}) {
        return this.request(url, { ...options, method: 'DELETE' });
    }

    // Méthode pour les formulaires (FormData)
    async postForm(url, formData, options = {}) {
        const config = {
            ...options,
            method: 'POST',
            body: formData,
        };
        
        // Ne pas définir Content-Type pour FormData (le navigateur le fait)
        if (config.headers) {
            delete config.headers['Content-Type'];
        }
        
        return this.request(url, config);
    }
}

// Instance globale
window.apiClient = new ApiClient();
