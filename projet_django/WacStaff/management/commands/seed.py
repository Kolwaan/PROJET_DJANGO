# python manage.py seed

from django.core.management.base import BaseCommand
from django.utils import timezone
from WacStaff.models import Restaurant, Fonction, Collaborateur, Affectation


class Command(BaseCommand):
    help = 'Remplit la base de données avec les données initiales'

    def handle(self, *args, **kwargs):
        self.stdout.write('Suppression des données existantes...')
        # On supprime dans l'ordre pour respecter les contraintes FK
        Affectation.objects.all().delete()
        Collaborateur.objects.all().delete()
        Fonction.objects.all().delete()
        Restaurant.objects.all().delete()

        # ─── RESTAURANTS ───────────────────────────────
        self.stdout.write('Création des restaurants...')
        restaurants_data = [
            {'nom': 'WacDo Marseille Vieux-Port', 'adresse': '1 Quai du Port',                                    'codePostal': '13002',     'ville': 'Marseille'},
            {'nom': 'WacDo Lune Sud',             'adresse': 'Base Lunaire Alpha - Crater Copernic - Secteur Sud','codePostal': 'LUNA-4021', 'ville': 'Copernic City'},
            {'nom': 'WacDo Mars',                 'adresse': 'Dôme habitable 7 - Plaine de Chryse Planitia',      'codePostal': 'MARS-X007', 'ville': 'Colonie Chryse'},
        ]
        restaurants = {}
        for data in restaurants_data:
            r = Restaurant.objects.create(**data)
            restaurants[r.nom] = r
        self.stdout.write(self.style.SUCCESS(f'  {len(restaurants)} restaurants créés'))

        # ─── FONCTIONS ─────────────────────────────────
        self.stdout.write('Création des fonctions...')
        fonctions_data = [
            'Superviseur de préparation',
            'Agent de préparation',
            "Agent d'accueil",
            'Responsable de restaurant',
        ]
        fonctions = {}
        for intitule in fonctions_data:
            f = Fonction.objects.create(intitulePoste=intitule)
            fonctions[intitule] = f
        self.stdout.write(self.style.SUCCESS(f'  {len(fonctions)} fonctions créées'))

        # ─── COLLABORATEURS ────────────────────────────
        self.stdout.write('Création des collaborateurs...')
        collaborateurs_data = [
            {'nom': 'Doe',    'prenom': 'Mike', 'email': 'mikedoe@test.com',  'password': 'test123', 'admin': False, 'is_superuser': False},
            {'nom': 'Grey',   'prenom': 'Jin',  'email': 'jingrey@test.com',  'password': 'test123', 'admin': False, 'is_superuser': False},
            {'nom': 'Wiz',    'prenom': 'Lou',  'email': 'louwiz@test.com',   'password': 'test123', 'admin': False, 'is_superuser': False},
            {'nom': 'Boss',   'prenom': 'For',  'email': 'boss@test.com',     'password': 'test123', 'admin': True,  'is_superuser': True},
            {'nom': 'Jon',    'prenom': 'Deuf', 'email': 'deuf@test.com',     'password': 'test123', 'admin': True,  'is_superuser': False},
            {'nom': 'Lechat', 'prenom': 'Jean', 'email': 'lechat@test.com',   'password': 'test123', 'admin': False, 'is_superuser': False},
        ]
        collaborateurs = {}
        for data in collaborateurs_data:
            password = data.pop('password')
            is_superuser = data.pop('is_superuser')
            if is_superuser:
                collab = Collaborateur.objects.create_superuser(password=password, **data)
            else:
                collab = Collaborateur(**data)
                collab.set_password(password)
                collab.save()
            collaborateurs[f"{data['prenom']} {data['nom']}"] = collab
        self.stdout.write(self.style.SUCCESS(f'  {len(collaborateurs)} collaborateurs créés'))

        # ─── AFFECTATIONS ──────────────────────────────
        self.stdout.write('Création des affectations...')
        affectations_data = [
            {
                'collaborateur': collaborateurs['Mike Doe'],
                'restaurant':    restaurants['WacDo Marseille Vieux-Port'],
                'poste':         fonctions['Superviseur de préparation'],
                'fin':           None,  # en cours
            },
            {
                'collaborateur': collaborateurs['Jin Grey'],
                'restaurant':    restaurants['WacDo Mars'],
                'poste':         fonctions['Superviseur de préparation'],
                'fin':           None,  # en cours
            },
            {
                'collaborateur': collaborateurs['Jean Lechat'],
                'restaurant':    restaurants['WacDo Lune Sud'],
                'poste':         fonctions['Responsable de restaurant'],
                'fin':           timezone.datetime(2025, 3, 15, tzinfo=timezone.utc),  # terminée
            },
            {
                'collaborateur': collaborateurs['Jean Lechat'],
                'restaurant':    restaurants['WacDo Mars'],
                'poste':         fonctions['Responsable de restaurant'],
                'fin':           None,  # en cours
            },
        ]
        for data in affectations_data:
            Affectation.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'  {len(affectations_data)} affectations créées'))

        self.stdout.write(self.style.SUCCESS('\nSeed terminé avec succès !'))
        self.stdout.write('  Superuser : boss@test.com / test123')