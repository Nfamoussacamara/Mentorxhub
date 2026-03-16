from django.http import JsonResponse
from django.views import View
from .models import MentorProfile

class MentorListAPIView(View):
    def get(self, request):
        mentors = MentorProfile.objects.select_related('user').filter(user__is_active=True)
        data = []
        for mentor in mentors:
            data.append({
                'id': mentor.id,
                'name': mentor.user.get_full_name(),
                'email': mentor.user.email,
                'expertise': mentor.expertise,
                'bio': mentor.user.bio if mentor.user.bio else '',
                'years_of_experience': mentor.years_of_experience,
                'hourly_rate': float(mentor.hourly_rate),
                'languages': mentor.languages,
                'rating': float(mentor.rating),
                'total_sessions': mentor.total_sessions,
                'is_available': mentor.is_available,
                'profile_picture': mentor.user.profile_picture.url if mentor.user.profile_picture else '',
                'linkedin_profile': mentor.linkedin_profile,
                'github_profile': mentor.github_profile,
                'website': mentor.website,
            })
        return JsonResponse(data, safe=False)
