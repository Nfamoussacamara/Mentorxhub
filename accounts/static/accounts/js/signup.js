// Sélection visuelle du rôle
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.role-option input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.querySelectorAll('.role-option').forEach(option => {
                option.classList.remove('selected');
            });
            this.closest('.role-option').classList.add('selected');
        });
    });
}); 