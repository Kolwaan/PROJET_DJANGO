# Lancer avec : python manage.py test WacStaff

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Collaborateur, Restaurant, Fonction, Affectation


# ═══════════════════════════════════════════════════════════════
# HELPERS — création des objets de test réutilisables
# Équivalent des fixtures pytest, mais en méthodes setUp()
# ═══════════════════════════════════════════════════════════════

# Crée un collaborateur simple (non-admin par défaut).
def make_collaborateur(email='collab@test.fr', nom='Dupont', prenom='Jean',
                        password='pass123', admin=False, superuser=False):
    if superuser:
        return Collaborateur.objects.create_superuser(
            email=email, nom=nom, prenom=prenom, password=password
        )
    user = Collaborateur.objects.create_user(
        email=email, nom=nom, prenom=prenom, password=password
    )
    user.admin = admin
    user.save()
    return user


def make_restaurant(nom='WacDo Marseille', adresse='1 rue de la Cannebière',
                    codePostal='13001', ville='Marseille'):
    return Restaurant.objects.create(nom=nom, adresse=adresse,
                                     codePostal=codePostal, ville=ville)


def make_fonction(intitule='Caissier'):
    return Fonction.objects.create(intitulePoste=intitule)


def make_affectation(collaborateur, restaurant, poste, fin=None):
    return Affectation.objects.create(
        collaborateur=collaborateur,
        restaurant=restaurant,
        poste=poste,
        fin=fin,
    )


# ═══════════════════════════════════════════════════════════════
# 1. MODÈLES
# ═══════════════════════════════════════════════════════════════

# Vérifie les comportements du modèle Collaborateur (AbstractBaseUser).
class CollaborateurModelTest(TestCase):

    def test_create_user_hash_password(self):
        # Le mot de passe doit être hashé, jamais stocké en clair.
        user = make_collaborateur()
        self.assertNotEqual(user.password, 'pass123')
        self.assertTrue(user.check_password('pass123'))

    def test_is_staff_reflete_admin(self):
        # is_staff est une property branchée sur le champ admin.
        user = make_collaborateur(admin=False)
        self.assertFalse(user.is_staff)
        user.admin = True
        user.save()
        self.assertTrue(user.is_staff)

    def test_create_superuser(self):
        # create_superuser doit positionner admin=True et is_superuser=True.
        su = make_collaborateur(email='su@test.fr', superuser=True)
        self.assertTrue(su.admin)
        self.assertTrue(su.is_superuser)
        self.assertTrue(su.is_staff)  # via la property

    def test_str(self):
        user = make_collaborateur(nom='Martin', prenom='Sophie')
        self.assertEqual(str(user), 'Sophie Martin')

    # Deux collaborateurs avec le même email doivent lever une erreur.
    def test_email_unique(self):
        make_collaborateur(email='doublon@test.fr')
        with self.assertRaises(Exception):
            make_collaborateur(email='doublon@test.fr')


# Vérifie la logique des affectations (active vs terminée).
class AffectationModelTest(TestCase):

    def setUp(self):
        self.collab = make_collaborateur()
        self.resto = make_restaurant()
        self.poste = make_fonction()

    # Une affectation sans date de fin est considérée active.
    def test_affectation_active_fin_null(self):
        aff = make_affectation(self.collab, self.resto, self.poste, fin=None)
        self.assertIsNone(aff.fin)

    # Une affectation avec date de fin est terminée.
    def test_affectation_terminee(self):
        aff = make_affectation(self.collab, self.resto, self.poste,
                               fin=timezone.now())
        self.assertIsNotNone(aff.fin)

    def test_str(self):
        aff = make_affectation(self.collab, self.resto, self.poste)
        self.assertIn('Jean Dupont', str(aff))
        self.assertIn('WacDo Marseille', str(aff))


# ═══════════════════════════════════════════════════════════════
# 2. AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════

# Vérifie le login/logout et les redirections pour les non-connectés.
class AuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_collaborateur(email='login@test.fr', password='secret')

    # Un login valide redirige vers home.
    def test_login_succes(self):
        response = self.client.post(reverse('login'), {
            'email': 'login@test.fr',
            'password': 'secret',
        })
        self.assertRedirects(response, reverse('home'))

    # Un mauvais mot de passe doit afficher une erreur sur le formulaire.
    def test_login_mauvais_mdp(self):
        response = self.client.post(reverse('login'), {
            'email': 'login@test.fr',
            'password': 'mauvais',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    # Après logout, on est redirigé vers login.
    def test_logout_redirige(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    # Un utilisateur non connecté est redirigé vers login.
    def test_home_redirige_si_non_connecte(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")


# ═══════════════════════════════════════════════════════════════
# 3. CONTRÔLE D'ACCÈS (RBAC)
# Un collaborateur simple ne peut pas créer/modifier/supprimer
# ═══════════════════════════════════════════════════════════════

# Vérifie que les vues de création/modification/suppression
# sont réservées aux admins (is_staff).
class RBACTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.simple_user = make_collaborateur(email='simple@test.fr', admin=False)
        self.admin_user = make_collaborateur(email='admin@test.fr', admin=True)
        self.resto = make_restaurant()
        self.fonction = make_fonction()

    # Un non-admin est redirigé avec un message d'erreur.
    def test_simple_user_ne_peut_pas_creer_restaurant(self):
        self.client.force_login(self.simple_user)
        response = self.client.post(reverse('restaurant_create'), {
            'nom': 'Nouveau Resto',
            'adresse': '10 rue Test',
            'codePostal': '75001',
            'ville': 'Paris',
        })
        # Redirigé vers la liste
        self.assertRedirects(response, reverse('restaurant_list'))
        # Le resto n'a pas été créé
        self.assertFalse(Restaurant.objects.filter(nom='Nouveau Resto').exists())

    # Un admin peut créer un restaurant.
    def test_admin_peut_creer_restaurant(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('restaurant_create'), {
            'nom': 'Nouveau Resto',
            'adresse': '10 rue Test',
            'codePostal': '75001',
            'ville': 'Paris',
        })
        self.assertRedirects(response, reverse('restaurant_list'))
        self.assertTrue(Restaurant.objects.filter(nom='Nouveau Resto').exists())

    # Un non-admin ne peut pas supprimer une fonction.
    def test_simple_user_ne_peut_pas_supprimer_fonction(self):
        self.client.force_login(self.simple_user)
        self.client.post(reverse('fonction_delete', kwargs={'pk': self.fonction.pk}))
        # La fonction existe toujours
        self.assertTrue(Fonction.objects.filter(pk=self.fonction.pk).exists())

    # Un admin peut supprimer une fonction sans affectation.
    def test_admin_peut_supprimer_fonction(self):
        self.client.force_login(self.admin_user)
        self.client.post(reverse('fonction_delete', kwargs={'pk': self.fonction.pk}))
        self.assertFalse(Fonction.objects.filter(pk=self.fonction.pk).exists())

    # Une fonction liée à une affectation ne doit pas pouvoir être supprimée
    # (PROTECT au niveau du modèle).
    def test_admin_ne_peut_pas_supprimer_fonction_utilisee(self):
        collab = make_collaborateur(email='c2@test.fr')
        make_affectation(collab, self.resto, self.fonction)
        self.client.force_login(self.admin_user)
        self.client.post(reverse('fonction_delete', kwargs={'pk': self.fonction.pk}))
        # La fonction doit toujours exister (PROTECT)
        self.assertTrue(Fonction.objects.filter(pk=self.fonction.pk).exists())


# ═══════════════════════════════════════════════════════════════
# 4. FILTRE "NON AFFECTÉS" (la logique qui avait un bug)
# ═══════════════════════════════════════════════════════════════

# Teste le filtre collaborateurs non affectés :
# - sans aucune affectation
# - avec affectation terminée (fin non null)
# - avec affectation active (fin null) → NE doit PAS apparaître
class FiltreNonAffectesTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = make_collaborateur(email='admin@test.fr', admin=True)
        self.client.force_login(self.admin)

        self.resto = make_restaurant()
        self.poste = make_fonction()

        # Collab sans affectation
        self.sans_aff = make_collaborateur(email='sans@test.fr', nom='SansAff', prenom='X')

        # Collab avec affectation terminée
        self.aff_terminee = make_collaborateur(email='termine@test.fr', nom='Termine', prenom='X')
        make_affectation(self.aff_terminee, self.resto, self.poste, fin=timezone.now())

        # Collab avec affectation active
        self.aff_active = make_collaborateur(email='actif@test.fr', nom='Actif', prenom='X')
        make_affectation(self.aff_active, self.resto, self.poste, fin=None)

    # Le collab avec affectation active ne doit PAS apparaître dans les non-affectés.
    def test_filtre_exclut_affectes_actifs(self):
        response = self.client.get(reverse('collaborateur_list'), {'non_affectes': '1'})
        self.assertEqual(response.status_code, 200)
        collabs = list(response.context['collaborateurs'])
        self.assertNotIn(self.aff_active, collabs)

    # Le collab sans affectation doit apparaître.
    def test_filtre_inclut_sans_affectation(self):
        response = self.client.get(reverse('collaborateur_list'), {'non_affectes': '1'})
        collabs = list(response.context['collaborateurs'])
        self.assertIn(self.sans_aff, collabs)

    # Le collab avec affectation terminée doit apparaître.
    def test_filtre_inclut_affectation_terminee(self):
        response = self.client.get(reverse('collaborateur_list'), {'non_affectes': '1'})
        collabs = list(response.context['collaborateurs'])
        self.assertIn(self.aff_terminee, collabs)


# ═══════════════════════════════════════════════════════════════
# 5. FORMULAIRES
# ═══════════════════════════════════════════════════════════════

# Vérifie les validations du formulaire de création de collaborateur.
class CollaborateurCreationFormTest(TestCase):

    # Deux mots de passe différents doivent invalider le formulaire.
    def test_mots_de_passe_differents(self):
        from .forms import CollaborateurCreationForm
        form = CollaborateurCreationForm(data={
            'nom': 'Test', 'prenom': 'User',
            'email': 'u@test.fr',
            'password1': 'abc123', 'password2': 'different',
        })
        self.assertFalse(form.is_valid())

    # Le champ admin ne doit pas être présent pour un admin non-superuser.
    def test_champ_admin_absent_pour_non_superuser(self):
        from .forms import CollaborateurCreationForm
        form = CollaborateurCreationForm(superuser=False)
        self.assertNotIn('admin', form.fields)

    # Le champ admin doit être présent pour un superuser.
    def test_champ_admin_present_pour_superuser(self):
        from .forms import CollaborateurCreationForm
        form = CollaborateurCreationForm(superuser=True)
        self.assertIn('admin', form.fields)