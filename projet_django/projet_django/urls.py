# ACCUEIL
# Redirige vers les applications


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('WacStaff/', include('WacStaff.urls')),  # délègue à l'app
    path('auth/', include('django.contrib.auth.urls')),  # Pour les vues d'authentification intégrées
]
