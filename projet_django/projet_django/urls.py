# ACCUEIL
# Redirige vers les applications


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('WacStaff.urls'))  # délègue à l'app
]
