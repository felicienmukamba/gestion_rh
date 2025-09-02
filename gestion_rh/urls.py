# mon_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URLs pour les employés
    path('employes/', views.EmployeListView.as_view(), name='employe_list'),
    path('employes/<int:pk>/', views.EmployeDetailView.as_view(), name='employe_detail'),
    path('employes/creer/', views.EmployeCreateView.as_view(), name='employe_create'),
    path('employes/<int:pk>/modifier/', views.EmployeUpdateView.as_view(), name='employe_update'),
    path('employes/<int:pk>/supprimer/', views.EmployeDeleteView.as_view(), name='employe_delete'),

    # URLs pour les congés (côté RH)
    path('rh/conges/', views.CongeGestionListView.as_view(), name='conge_gestion_list'),
    path('rh/conges/<int:pk>/modifier/', views.CongeGestionUpdateView.as_view(), name='conge_gestion_update'),

    # URLs pour les congés (côté employé)
    path('employe/conges/', views.CongeDemandeListView.as_view(), name='conge_demande_list'),
    path('employe/conges/demander/', views.CongeDemandeCreateView.as_view(), name='conge_demande_create'),

    # URLs pour les présences
    path('presences/', views.PresenceListView.as_view(), name='presence_list'),
    path('presences/creer/', views.PresenceCreateView.as_view(), name='presence_create'),
    path('presences/<int:pk>/modifier/', views.PresenceUpdateView.as_view(), name='presence_update'),
    path('presences/<int:pk>/supprimer/', views.PresenceDeleteView.as_view(), name='presence_delete'),

    # URLs pour les fiches de paie (côté RH)
    path('rh/fiches-paie/', views.FicheDePaieListView.as_view(), name='fiche_paie_list'),
    path('rh/fiches-paie/creer/', views.FicheDePaieCreateView.as_view(), name='fiche_paie_create'),
    path('rh/fiches-paie/<int:pk>/', views.FicheDePaieDetailView.as_view(), name='fiche_paie_detail'),
    path('rh/fiches-paie/<int:pk>/modifier/', views.FicheDePaieUpdateView.as_view(), name='fiche_paie_update'),
    path('rh/fiches-paie/<int:pk>/supprimer/', views.FicheDePaieDeleteView.as_view(), name='fiche_paie_delete'),
    
    # Ajouter ici les URLs pour Formations, Annonces, Avantages, Primes, Rôles, Utilisateurs)
    path('roles/', views.RoleListView.as_view(), name='role_list'),
    path('roles/creer/', views.RoleCreateView.as_view(), name='role_create'),
    path('roles/<int:pk>/modifier/', views.RoleUpdateView.as_view(), name='role_update'),
    path('roles/<int:pk>/supprimer/', views.RoleDeleteView.as_view(), name='role_delete'),
    path('utilisateurs/', views.UtilisateurListView.as_view(), name='utilisateur_list'),
    path('utilisateurs/creer/', views.UtilisateurCreateView.as_view(), name='utilisateur_create'),
    path('utilisateurs/<int:pk>/modifier/', views.UtilisateurUpdateView.as_view(), name='utilisateur_update'),
    path('utilisateurs/<int:pk>/supprimer/', views.UtilisateurDeleteView.as_view(), name='utilisateur_delete'), 
    
    
    # Exemple pour les annonces
    path('annonces/', views.AnnonceListView.as_view(), name='annonce_list'),
    path('annonces/creer/', views.AnnonceCreateView.as_view(), name='annonce_create'),
]