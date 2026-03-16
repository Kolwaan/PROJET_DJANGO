"""
Commande de seed pour WacStaff.
Lance avec : python manage.py seed

Recrée les données initiales :
- 3 restaurants
- 4 fonctions
- 3 collaborateurs
"""

from django.core.management.base import BaseCommand
from WacStaff.models import Restaurant, Fonction, Collaborateur


class Command(BaseCommand):
    help = 'Remplit la base de données avec les données initiales'

    def handle(self, *args, **kwargs):
        self.stdout.write('Suppression des données existantes...')
        # On supprime dans l'ordre pour respecter les contraintes FK
        Collaborateur.objects.all().delete()
        Fonction.objects.all().delete()
        Restaurant.objects.all().delete()

        # ─── RESTAURANTS ───────────────────────────────
        self.stdout.write('Création des restaurants...')
        restaurants = [
            {'nom': 'WacDo Marseille Vieux-Port', 'adresse': '1 Quai du Port',                              'codePostal': '13002',    'ville': 'Marseille'},
            {'nom': 'WacDo Lune Sud',             'adresse': 'Base Lunaire Alpha - Crater Copernic - Secteur Sud', 'codePostal': 'LUNA-4021', 'ville': 'Copernic City'},
            {'nom': 'WacDo Mars',                 'adresse': 'Dôme habitable 7 - Plaine de Chryse Planitia','codePostal': 'MARS-X007', 'ville': 'Colonie Chryse'},
        ]
        for data in restaurants:
            Restaurant.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'  {len(restaurants)} restaurants créés'))

        # ─── FONCTIONS ─────────────────────────────────
        self.stdout.write('Création des fonctions...')
        fonctions = [
            'Superviseur de préparation',
            'Agent de préparation',
            "Agent d'accueil",
            'Administrateur',
        ]
        for intitule in fonctions:
            Fonction.objects.create(intitulePoste=intitule)
        self.stdout.write(self.style.SUCCESS(f'  {len(fonctions)} fonctions créées'))

        # ─── COLLABORATEURS ────────────────────────────
        self.stdout.write('Création des collaborateurs...')
        collaborateurs = [
            {'nom': 'Doe',  'prenom': 'Mike', 'email': 'mikedoe@test.com', 'password': 'test123', 'admin': False},
            {'nom': 'Grey', 'prenom': 'Jin',  'email': 'jingrey@test.com', 'password': 'test123', 'admin': False},
            {'nom': 'Wiz',  'prenom': 'Lou',  'email': 'louwiz@test.com',  'password': 'test123', 'admin': False},
        ]
        for data in collaborateurs:
            password = data.pop('password')
            collab = Collaborateur(**data)
            collab.set_password(password)  # hashage du mot de passe
            collab.save()
        self.stdout.write(self.style.SUCCESS(f'  {len(collaborateurs)} collaborateurs créés'))

        self.stdout.write(self.style.SUCCESS('\nSeed terminé avec succès !'))
        self.stdout.write('Note : le superuser admin doit être créé séparément avec "python manage.py createsuperuser"')
