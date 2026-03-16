/**
 * MentorXHub - JavaScript pour la page d'onboarding mentoré multi-étapes
 * Mentee Onboarding - Multi-step
 */

(function() {
    'use strict';

    const form = document.getElementById('onboardingForm');
    const steps = document.querySelectorAll('.step-content');
    const stepIndicators = document.querySelectorAll('.step-indicator');
    const progressBar = document.getElementById('progressBar');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    let currentStep = 1;
    const totalSteps = steps.length;

    // Initialize
    function init() {
        if (!form) return;
        
        updateProgress();
        setupEventListeners();
        setupCharCounters();
        setupCheckboxes();
        setupInterestSearch();
    }

    // Event Listeners
    function setupEventListeners() {
        if (prevBtn) prevBtn.addEventListener('click', goToPreviousStep);
        if (nextBtn) nextBtn.addEventListener('click', goToNextStep);
        if (form) form.addEventListener('submit', handleSubmit);
                }

    // Navigation
    function goToNextStep() {
        if (validateCurrentStep()) {
            if (currentStep < totalSteps) {
                currentStep++;
                updateStep();
            }
        }
    }

    function goToPreviousStep() {
        if (currentStep > 1) {
            currentStep--;
            updateStep();
        }
    }

    function updateStep() {
        // Hide all steps
        steps.forEach(step => step.classList.remove('active'));
        stepIndicators.forEach(indicator => indicator.classList.remove('active', 'completed'));
    
        // Show current step
        const currentStepEl = document.querySelector(`.step-content[data-step="${currentStep}"]`);
        if (currentStepEl) {
            currentStepEl.classList.add('active');
        }

        // Update indicators
        stepIndicators.forEach((indicator, index) => {
            const stepNum = index + 1;
            if (stepNum < currentStep) {
                indicator.classList.add('completed');
            } else if (stepNum === currentStep) {
                indicator.classList.add('active');
            }
        });

        // Update buttons
        if (prevBtn) prevBtn.style.display = currentStep === 1 ? 'none' : 'inline-block';
        if (nextBtn) nextBtn.style.display = currentStep === totalSteps ? 'none' : 'inline-block';
        if (submitBtn) submitBtn.style.display = currentStep === totalSteps ? 'inline-block' : 'none';

        // Update progress bar
        updateProgress();

        // Load confirmation summary on last step
        if (currentStep === totalSteps) {
            updateConfirmationSummary();
        }
    }

    function updateProgress() {
        if (!progressBar) return;
        const progress = (currentStep / totalSteps) * 100;
        progressBar.setAttribute('data-progress', Math.round(progress));
    }

    // Validation
    function validateCurrentStep() {
        const currentStepEl = document.querySelector(`.step-content[data-step="${currentStep}"]`);
        if (!currentStepEl) return true;
        
        const requiredFields = currentStepEl.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#EF4444';
                setTimeout(() => {
                    field.style.borderColor = '';
                }, 2000);
            }
        });

        return isValid;
    }

    // Character Counters
    function setupCharCounters() {
    const learningGoalsField = document.querySelector('textarea[name="learning_goals"]');
    const charCounter = document.getElementById('learning-goals-counter');
    const charCount = document.getElementById('char-count');
    const maxChars = 500;

    if (learningGoalsField && charCounter && charCount) {
        function updateCharCounter() {
            const currentLength = learningGoalsField.value.length;
            charCount.textContent = currentLength;
            
            charCounter.classList.remove('warning', 'error');
            
            if (currentLength > maxChars) {
                charCounter.classList.add('error');
            } else if (currentLength > maxChars * 0.9) {
                charCounter.classList.add('warning');
            }
        }

        learningGoalsField.addEventListener('input', updateCharCounter);
        learningGoalsField.addEventListener('focus', updateCharCounter);
            updateCharCounter();
        }
    }

    // Checkboxes
    function setupCheckboxes() {
        const checkboxes = document.querySelectorAll('.input-group input[type="checkbox"][name*="interests"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const li = this.closest('li');
                if (li) {
                    if (this.checked) {
                        li.classList.add('checked');
                } else {
                        li.classList.remove('checked');
                    }
                }
            });

            if (checkbox.checked) {
                const li = checkbox.closest('li');
                if (li) {
                    li.classList.add('checked');
                }
            }
        });
    }

    // Confirmation Summary
    function updateConfirmationSummary() {
        const summary = document.getElementById('confirmationSummary');
        if (!summary) return;

        const currentData = {};
        const allInputs = form.querySelectorAll('input, select, textarea');
        
        allInputs.forEach(input => {
            if (input.type === 'checkbox') {
                if (input.checked) {
                    if (!currentData[input.name]) {
                        currentData[input.name] = [];
                    }
                    currentData[input.name].push(input.value);
                }
            } else if (input.type !== 'file' && input.type !== 'submit' && input.type !== 'button') {
                if (input.value) {
                    currentData[input.name] = input.value;
                }
            }
        });

        const labels = {
            'level': 'Niveau',
            'preferred_languages': 'Langues préférées',
            'learning_goals': 'Objectifs d\'apprentissage',
            'github_profile': 'GitHub'
        };

        let html = '';
        Object.keys(currentData).forEach(key => {
            let value = currentData[key];
            if (Array.isArray(value)) {
                value = value.join(', ');
            }
            if (value && labels[key]) {
                html += `
                    <div class="confirmation-item">
                        <span class="confirmation-label">${labels[key]}</span>
                        <span class="confirmation-value">${value}</span>
                    </div>
                `;
        }
        });

        // Handle interests separately
        const interests = form.querySelectorAll('input[name="interests"]:checked');
        if (interests.length > 0) {
            const interestNames = Array.from(interests).map(cb => {
                const label = cb.closest('label') || cb.nextElementSibling;
                return label ? label.textContent.trim() : cb.value;
            }).join(', ');
            html += `
                <div class="confirmation-item">
                    <span class="confirmation-label">Centres d'intérêt</span>
                    <span class="confirmation-value">${interestNames}</span>
                </div>
            `;
    }

        summary.innerHTML = html || '<p style="color: #64748b; text-align: center;">Aucune information à afficher</p>';
    }

    // Interest Search
    function setupInterestSearch() {
        const searchInput = document.getElementById('interestSearch');
        if (!searchInput) return;

        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();
            const interestItems = document.querySelectorAll('.interest-item');

            interestItems.forEach(item => {
                const name = item.getAttribute('data-name') || '';
                const description = item.querySelector('.interest-description')?.textContent.toLowerCase() || '';
                
                if (name.includes(searchTerm) || description.includes(searchTerm) || searchTerm === '') {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        });
    }

    // Form Submission
    function handleSubmit(e) {
        if (!form) return;

        // Show loading state
        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        }
        
        // Form will submit normally
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
