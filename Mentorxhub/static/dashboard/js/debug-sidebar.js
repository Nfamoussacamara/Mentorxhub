/**
 * Script de débogage pour la sidebar
 * Ajouter ce script temporairement pour comprendre l'état au chargement
 */

console.log('=== DEBUG SIDEBAR ===');
console.log('sessionStorage.sidebarWidth:', sessionStorage.getItem('sidebarWidth'));
console.log('sessionStorage.sidebarCollapsed:', sessionStorage.getItem('sidebarCollapsed'));
console.log('localStorage.sidebarWidth:', localStorage.getItem('sidebarWidth'));
console.log('localStorage.sidebarCollapsed:', localStorage.getItem('sidebarCollapsed'));

const sidebar = document.getElementById('dashboard-sidebar');
if (sidebar) {
    console.log('Sidebar width actuelle:', sidebar.offsetWidth);
    console.log('Sidebar style.width:', sidebar.style.width);
    console.log('Sidebar classes:', sidebar.className);
    console.log('Sidebar classList contains collapsed:', sidebar.classList.contains('collapsed'));
}

// Nettoyer tout le storage
function resetSidebar() {
    sessionStorage.removeItem('sidebarWidth');
    sessionStorage.removeItem('sidebarCollapsed');
    localStorage.removeItem('sidebarWidth');
    localStorage.removeItem('sidebarCollapsed');
    console.log('✓ Storage nettoyé. Rechargez la page.');
}

// Exposer la fonction globalement
window.resetSidebar = resetSidebar;
console.log('Pour réinitialiser la sidebar, tapez: resetSidebar()');
