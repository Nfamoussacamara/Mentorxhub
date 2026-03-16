/**
 * JavaScript pour le module Paramètres
 */

(function() {
    'use strict';

    // Charger une section de paramètres
    async function loadSettingsSection(url) {
        const content = document.getElementById('settings-content');
        if (!content) return;

        content.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();
            
            if (data.html) {
                content.innerHTML = data.html;
                initFormHandlers();
            }
        } catch (error) {
            console.error('Error loading settings section:', error);
            content.innerHTML = '<p>Erreur lors du chargement</p>';
        }
    }

    // Initialiser les handlers de formulaires
    function initFormHandlers() {
        // Formulaire général
        const generalForm = document.getElementById('general-settings-form');
        if (generalForm) {
            generalForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await submitForm(generalForm, '/dashboard/settings/general/');
            });
        }

        // Formulaire sécurité
        const securityForm = document.getElementById('security-settings-form');
        if (securityForm) {
            securityForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await submitForm(securityForm, '/dashboard/settings/security/');
            });
        }

        // Formulaire notifications
        const notificationsForm = document.getElementById('notifications-settings-form');
        if (notificationsForm) {
            notificationsForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await submitForm(notificationsForm, '/dashboard/settings/notifications/');
            });
        }
    }

    // Soumettre un formulaire
    async function submitForm(form, url) {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enregistrement...';

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });
            const data = await response.json();
            
            if (data.success) {
                showToast('Paramètres mis à jour avec succès', 'success');
            } else {
                showToast(data.message || 'Erreur lors de la mise à jour', 'error');
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            showToast('Erreur lors de la mise à jour', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }

    // Afficher un toast
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Initialisation
    document.addEventListener('DOMContentLoaded', function() {
        // Navigation entre sections
        document.querySelectorAll('.settings-nav-item').forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Mettre à jour l'état actif
                document.querySelectorAll('.settings-nav-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
                
                // Charger la section
                loadSettingsSection(this.getAttribute('href'));
            });
        });

        // Charger la première section par défaut
        const firstSection = document.querySelector('.settings-nav-item.active');
        if (firstSection) {
            loadSettingsSection(firstSection.getAttribute('href'));
        }
    });
})();

