# DÉCIDE QUOI AFFICHER

from django.shortcuts import render

def home(request):                  # La fonction home est une vue. Elle reçoit une requête HTTP (ici GET)
                                    # et renvoie une réponse.
                                        
    return render(request, "home.html") # va chercher le HTML et le retourne
                                        # request : la requête du navigateur
                                        # home.html : le template


