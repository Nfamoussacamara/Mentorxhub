"""
Commande Django pour créer les matières initiales dans la base de données
"""
from django.core.management.base import BaseCommand
from mentoring.models import Subject


class Command(BaseCommand):
    help = 'Crée les matières initiales dans la base de données'

    def handle(self, *args, **options):
        subjects_data = [
            {'name': 'Développement Web', 'description': 'HTML, CSS, JavaScript, frameworks web'},
            {'name': 'Développement Mobile', 'description': 'iOS, Android, React Native, Flutter'},
            {'name': 'Data Science', 'description': 'Analyse de données, machine learning, statistiques'},
            {'name': 'Intelligence Artificielle', 'description': 'Machine Learning, Deep Learning, NLP'},
            {'name': 'Cybersécurité', 'description': 'Sécurité informatique, éthique du hacking'},
            {'name': 'DevOps', 'description': 'Docker, Kubernetes, CI/CD, cloud computing'},
            {'name': 'Base de données', 'description': 'SQL, NoSQL, optimisation, administration'},
            {'name': 'Programmation Python', 'description': 'Python, frameworks, bibliothèques'},
            {'name': 'Programmation Java', 'description': 'Java, Spring, JEE'},
            {'name': 'Programmation JavaScript', 'description': 'JavaScript, Node.js, TypeScript'},
            {'name': 'Programmation C/C++', 'description': 'C, C++, programmation système'},
            {'name': 'Programmation Go', 'description': 'Go, développement backend'},
            {'name': 'Programmation Rust', 'description': 'Rust, programmation système sécurisée'},
            {'name': 'UI/UX Design', 'description': 'Design d\'interface, expérience utilisateur'},
            {'name': 'Marketing Digital', 'description': 'SEO, SEM, réseaux sociaux, e-commerce'},
            {'name': 'Gestion de Projet', 'description': 'Agile, Scrum, gestion d\'équipe'},
            {'name': 'Blockchain', 'description': 'Cryptomonnaies, smart contracts, Web3'},
            {'name': 'Cloud Computing', 'description': 'AWS, Azure, GCP, infrastructure cloud'},
            {'name': 'Architecture Logicielle', 'description': 'Design patterns, architecture, clean code'},
            {'name': 'Test & QA', 'description': 'Tests unitaires, intégration, automatisation'},
        ]

        created_count = 0
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults={'description': subject_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Matière créée: {subject.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Matière déjà existante: {subject.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n{created_count} nouvelle(s) matière(s) créée(s). '
                f'Total: {Subject.objects.count()} matières dans la base de données.'
            )
        )
