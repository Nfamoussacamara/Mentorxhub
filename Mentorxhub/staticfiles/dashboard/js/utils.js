/**
 * Utilitaires JavaScript pour le dashboard
 * Toast, Modal, Helpers
 */

/**
 * Système de Toast universel
 */
const Toast = {
    /**
     * Affiche un toast
     */
    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icon = this.getIcon(type);
        toast.innerHTML = `
            <i class="${icon}"></i>
            <span>${this.escapeHtml(message)}</span>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Ajouter au DOM
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.style.cssText = `
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 1rem;
            `;
            document.body.appendChild(toastContainer);
        }
        
        toastContainer.appendChild(toast);
        
        // Animation d'entrée
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        }, 10);
        
        // Auto-suppression
        if (duration > 0) {
            setTimeout(() => {
                this.hide(toast);
            }, duration);
        }
        
        return toast;
    },
    
    /**
     * Cache un toast
     */
    hide(toast) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 300);
    },
    
    /**
     * Récupère l'icône selon le type
     */
    getIcon(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle',
        };
        return icons[type] || icons.info;
    },
    
    /**
     * Échappe le HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    /**
     * Méthodes de raccourci
     */
    success(message, duration) {
        return this.show(message, 'success', duration);
    },
    
    error(message, duration) {
        return this.show(message, 'error', duration);
    },
    
    warning(message, duration) {
        return this.show(message, 'warning', duration);
    },
    
    info(message, duration) {
        return this.show(message, 'info', duration);
    },
};

/**
 * Système de Modal universel
 */
const Modal = {
    /**
     * Affiche un modal
     */
    show(title, content, options = {}) {
        const {
            size = 'medium',
            closable = true,
            onClose = null,
            buttons = [],
        } = options;
        
        // Créer l'overlay
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.id = 'modal-overlay';
        
        // Créer le contenu du modal
        const modal = document.createElement('div');
        modal.className = `modal-content modal-${size}`;
        
        modal.innerHTML = `
            <div class="modal-header">
                <h2>${this.escapeHtml(title)}</h2>
                ${closable ? '<button class="modal-close" onclick="Modal.close()"><i class="fas fa-times"></i></button>' : ''}
            </div>
            <div class="modal-body">
                ${typeof content === 'string' ? content : content.outerHTML}
            </div>
            ${buttons.length > 0 ? `
                <div class="modal-footer">
                    ${buttons.map(btn => `
                        <button class="neu-button ${btn.class || ''}" onclick="${btn.onClick || ''}">
                            ${btn.label}
                        </button>
                    `).join('')}
                </div>
            ` : ''}
        `;
        
        overlay.appendChild(modal);
        document.body.appendChild(overlay);
        
        // Fermer en cliquant sur l'overlay
        if (closable) {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    this.close();
                }
            });
        }
        
        // Sauvegarder le callback
        overlay.dataset.onClose = onClose ? onClose.toString() : '';
        
        // Animation
        setTimeout(() => {
            overlay.style.opacity = '1';
            modal.style.transform = 'scale(1)';
        }, 10);
        
        return overlay;
    },
    
    /**
     * Ferme le modal
     */
    close() {
        const overlay = document.getElementById('modal-overlay');
        if (overlay) {
            overlay.style.opacity = '0';
            const modal = overlay.querySelector('.modal-content');
            if (modal) {
                modal.style.transform = 'scale(0.9)';
            }
            
            setTimeout(() => {
                if (overlay.dataset.onClose) {
                    try {
                        const callback = eval(overlay.dataset.onClose);
                        if (typeof callback === 'function') {
                            callback();
                        }
                    } catch (e) {
                        console.error('Error executing onClose callback:', e);
                    }
                }
                overlay.remove();
            }, 300);
        }
    },
    
    /**
     * Échappe le HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
};

/**
 * Helpers utilitaires
 */
const Helpers = {
    /**
     * Formate une date
     */
    formatDate(date, format = 'fr-FR') {
        if (!date) return '';
        const d = new Date(date);
        return d.toLocaleDateString(format, {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    },
    
    /**
     * Formate un montant
     */
    formatCurrency(amount, currency = 'EUR') {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: currency,
        }).format(amount);
    },
    
    /**
     * Échappe le HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    /**
     * Débounce une fonction
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    /**
     * Throttle une fonction
     */
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    /**
     * Copie du texte dans le presse-papiers
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            Toast.success('Copié dans le presse-papiers');
            return true;
        } catch (err) {
            console.error('Failed to copy:', err);
            Toast.error('Erreur lors de la copie');
            return false;
        }
    },
};

// Exposer globalement pour compatibilité
window.showToast = (message, type, duration) => Toast.show(message, type, duration);
window.Modal = Modal;
window.Helpers = Helpers;

