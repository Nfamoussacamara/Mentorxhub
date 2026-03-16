from .auth import CustomLoginView, SignUpView, CustomLogoutView
from .onboarding.role import RoleSelectionView
from .profile import ProfileDisplayView, ProfileEditView

# Alias pour compatibilité
ProfileView = ProfileDisplayView
