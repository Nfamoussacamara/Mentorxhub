/**
 * State Manager - Gestion de l'état global de l'application
 * Évite les appels API redondants et synchronise l'UI
 */

class StateManager {
    constructor() {
        this.state = {
            user: null,
            unreadMessages: 0,
            notifications: [],
            theme: localStorage.getItem('theme') || 'light',
            sidebarCollapsed: false,
            currentPage: 'home',
        };
        this.subscribers = {};
        this.init();
    }

    init() {
        // Charger l'état depuis localStorage
        this.loadFromStorage();
        
        // Écouter les changements de thème
        this.subscribe('theme', (theme) => {
            localStorage.setItem('theme', theme);
        });
    }

    setState(key, value) {
        const oldValue = this.state[key];
        this.state[key] = value;

        // Notifier les abonnés
        if (this.subscribers[key]) {
            this.subscribers[key].forEach(callback => {
                callback(value, oldValue);
            });
        }

        // Sauvegarder dans localStorage si nécessaire
        if (['theme', 'sidebarCollapsed'].includes(key)) {
            localStorage.setItem(key, JSON.stringify(value));
        }
    }

    getState(key) {
        return this.state[key];
    }

    subscribe(key, callback) {
        if (!this.subscribers[key]) {
            this.subscribers[key] = [];
        }
        this.subscribers[key].push(callback);

        // Retourner une fonction pour se désabonner
        return () => {
            this.subscribers[key] = this.subscribers[key].filter(cb => cb !== callback);
        };
    }

    loadFromStorage() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            this.state.theme = savedTheme;
        }

        const savedSidebarState = localStorage.getItem('sidebarCollapsed');
        if (savedSidebarState) {
            this.state.sidebarCollapsed = JSON.parse(savedSidebarState);
        }
    }

    clearState() {
        this.state = {
            user: null,
            unreadMessages: 0,
            notifications: [],
            theme: 'light',
            sidebarCollapsed: false,
            currentPage: 'home',
        };
        localStorage.removeItem('theme');
        localStorage.removeItem('sidebarCollapsed');
    }

    // Méthodes utilitaires
    updateUser(userData) {
        this.setState('user', userData);
    }

    updateUnreadMessages(count) {
        this.setState('unreadMessages', count);
    }

    addNotification(notification) {
        const notifications = [...this.state.notifications, notification];
        this.setState('notifications', notifications);
    }

    removeNotification(id) {
        const notifications = this.state.notifications.filter(n => n.id !== id);
        this.setState('notifications', notifications);
    }

    markNotificationAsRead(id) {
        const notifications = this.state.notifications.map(n => 
            n.id === id ? { ...n, read: true } : n
        );
        this.setState('notifications', notifications);
    }
}

// Instance globale
window.stateManager = new StateManager();

