(function() {
    'use strict';

    const form = document.getElementById('completeProfileForm');
    const steps = document.querySelectorAll('.step-content');
    const stepIndicators = document.querySelectorAll('.step-indicator');
    const progressBar = document.getElementById('progressBar');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    let currentStep = 1;
    const totalSteps = steps.length;
    const formData = {};

    function init() {
        if (!form) return;
        
        updateProgress();
        setupEventListeners();
        setupCharCounters();
        setupFilePreviews();
        setupInterestSearch();
        loadSavedData();
    }

    function setupEventListeners() {
        if (prevBtn) prevBtn.addEventListener('click', goToPreviousStep);
        if (nextBtn) nextBtn.addEventListener('click', goToNextStep);
        if (form) {
            form.addEventListener('submit', handleSubmit);
            form.addEventListener('input', saveFormData);
            form.addEventListener('change', saveFormData);
        }
        
    }
    

    function goToNextStep() {
        if (validateCurrentStep()) {
            if (currentStep < totalSteps) {
                saveStepData();
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
        steps.forEach(step => step.classList.remove('active'));
        stepIndicators.forEach(indicator => indicator.classList.remove('active', 'completed'));

        const currentStepEl = document.querySelector(`.step-content[data-step="${currentStep}"]`);
        if (currentStepEl) {
            currentStepEl.classList.add('active');
        }

        stepIndicators.forEach((indicator, index) => {
            const stepNum = index + 1;
            if (stepNum < currentStep) {
                indicator.classList.add('completed');
            } else if (stepNum === currentStep) {
                indicator.classList.add('active');
            }
        });

        if (prevBtn) prevBtn.style.display = currentStep === 1 ? 'none' : 'inline-block';
        if (nextBtn) nextBtn.style.display = currentStep === totalSteps ? 'none' : 'inline-block';
        if (submitBtn) submitBtn.style.display = currentStep === totalSteps ? 'inline-block' : 'none';

        updateProgress();

        if (currentStep === totalSteps) {
            updateConfirmationSummary();
        }
    }

    function updateProgress() {
        if (!progressBar) return;
        const progress = (currentStep / totalSteps) * 100;
        progressBar.setAttribute('data-progress', Math.round(progress));
    }

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

    function saveStepData() {
        const currentStepEl = document.querySelector(`.step-content[data-step="${currentStep}"]`);
        if (!currentStepEl) return;
        
        const inputs = currentStepEl.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                if (input.checked) {
                    if (!formData[input.name]) {
                        formData[input.name] = [];
                    }
                    if (!formData[input.name].includes(input.value)) {
                        formData[input.name].push(input.value);
                    }
                }
            } else if (input.type !== 'file') {
                formData[input.name] = input.value;
            }
        });
    }

    function saveFormData() {
        saveStepData();
        localStorage.setItem('completeProfileData', JSON.stringify(formData));
    }

    function loadSavedData() {
        const saved = localStorage.getItem('completeProfileData');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                Object.keys(data).forEach(name => {
                    const field = form.querySelector(`[name="${name}"]`);
                    if (field) {
                        if (field.type === 'checkbox') {
                            if (Array.isArray(data[name]) && data[name].includes(field.value)) {
                                field.checked = true;
                            }
                        } else {
                            field.value = data[name];
                        }
                    }
                });
                Object.assign(formData, data);
            } catch (e) {
                console.error('Error loading saved data:', e);
            }
        }
    }

    function setupCharCounters() {
        const bioField = document.getElementById('bio');
        const goalsField = document.getElementById('learning_goals');
        const bioCount = document.getElementById('bioCount');
        const goalsCount = document.getElementById('goalsCount');

        if (bioField && bioCount) {
            updateCharCount(bioField, bioCount, 500);
            bioField.addEventListener('input', () => updateCharCount(bioField, bioCount, 500));
        }

        if (goalsField && goalsCount) {
            updateCharCount(goalsField, goalsCount, 500);
            goalsField.addEventListener('input', () => updateCharCount(goalsField, goalsCount, 500));
        }
    }

    function updateCharCount(field, counter, max) {
        const count = field.value.length;
        counter.textContent = count;
        if (count > max * 0.9) {
            counter.style.color = '#F59E0B';
        } else {
            counter.style.color = '';
        }
    }

    function setupFilePreviews() {
        const profileInput = document.getElementById('profile_picture');
        const bannerInput = document.getElementById('banner_image');
        const profilePreview = document.getElementById('profilePreview');
        const bannerPreview = document.getElementById('bannerPreview');

        if (profileInput && profilePreview) {
            profileInput.addEventListener('change', (e) => {
                handleFilePreview(e.target.files[0], profilePreview);
            });
        }

        if (bannerInput && bannerPreview) {
            bannerInput.addEventListener('change', (e) => {
                handleFilePreview(e.target.files[0], bannerPreview);
            });
        }
    }

    function handleFilePreview(file, previewContainer) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                previewContainer.classList.add('active');
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.classList.remove('active');
        }
    }

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
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'bio': 'Biographie',
            'expertise': 'Expertise',
            'years_of_experience': 'Années d\'expérience',
            'hourly_rate': 'Tarif horaire',
            'languages': 'Langues',
            'certifications': 'Certifications',
            'level': 'Niveau',
            'learning_goals': 'Objectifs d\'apprentissage',
            'preferred_languages': 'Langues préférées',
            'linkedin_profile': 'LinkedIn',
            'github_profile': 'GitHub',
            'website': 'Site web'
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

        const interests = form.querySelectorAll('input[name="interests"]:checked');
        if (interests.length > 0) {
            const interestNames = Array.from(interests).map(cb => {
                const label = cb.closest('label');
                return label ? label.textContent.trim() : cb.value;
            }).join(', ');
            html += `
                <div class="confirmation-item">
                    <span class="confirmation-label">Centres d'intérêt</span>
                    <span class="confirmation-value">${interestNames}</span>
                </div>
            `;
        }

        summary.innerHTML = html || '<p style="color: var(--text-muted); text-align: center;">Aucune information à afficher</p>';
    }

    function handleSubmit(e) {
        if (!form) return;
        
        saveStepData();
        
        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        }
        
        form.submit();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
