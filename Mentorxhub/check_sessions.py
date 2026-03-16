import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorxhub.settings')
django.setup()

from mentoring.models import MentoringSession

# Compter les sessions
total = MentoringSession.objects.count()
print(f"📊 Total de sessions dans la base : {total}")

# Sessions disponibles (ouvertes)
available = MentoringSession.objects.filter(status='available', student__isnull=True)
print(f"\n🟢 Sessions disponibles (ouvertes) : {available.count()}")
for session in available[:5]:
    print(f"  • ID {session.id}: {session.title}")
    print(f"    Date: {session.date} {session.start_time}-{session.end_time}")
    print(f"    Mentor: {session.mentor.user.get_full_name()}")
    print()

# Toutes les sessions
print("\n📋 Toutes les sessions :")
all_sessions = MentoringSession.objects.all()[:10]
for session in all_sessions:
    student_name = session.student.user.get_full_name() if session.student else "Aucun (session ouverte)"
    print(f"  • ID {session.id}: {session.title}")
    print(f"    Status: {session.get_status_display()}")
    print(f"    Étudiant: {student_name}")
    print()

if total == 0:
    print("❌ Aucune session dans la base de données.")
    print("💡 Créez une session en tant que mentor sur /mentoring/mentor/sessions/create-available/")
