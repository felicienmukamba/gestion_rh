from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import (
    Employe, Conge, Presence, Annonce, Avantage, Prime, Role,
    FicheDePaie, FichePaiePrime, FichePaieAvantage,
    Utilisateur
)
from .forms import (
    EmployeForm, CongeForm, PresenceForm, AnnonceForm, AvantageForm, PrimeForm,
    FicheDePaieForm, RoleForm, UtilisateurCreationForm, UtilisateurUpdateForm
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import transaction

# --- Mixins de Permissions pour Admin et RH ---
# A adapter selon vos besoins précis
# Supposons que l'Admin a le rôle 'Admin' et que le RH a le rôle 'RH'
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role and self.request.user.role.nom_role == 'Admin'

class RhRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role and self.request.user.role.nom_role == 'RH'

# Combine les deux pour les vues accessibles aux deux rôles
class AdminOrRhRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        is_admin = self.request.user.is_authenticated and self.request.user.role and self.request.user.role.nom_role == 'Admin'
        is_rh = self.request.user.is_authenticated and self.request.user.role and self.request.user.role.nom_role == 'RH'
        return is_admin or is_rh

# ==============================================
# Vues pour le modèle Employe (Gérées par le RH)
# ==============================================

class EmployeListView(AdminOrRhRequiredMixin, ListView):
    model = Employe
    template_name = 'rh/employe_list.html'
    context_object_name = 'employes'

class EmployeDetailView(AdminOrRhRequiredMixin, DetailView):
    model = Employe
    template_name = 'rh/employe_detail.html'
    context_object_name = 'employe'

class EmployeCreateView(AdminOrRhRequiredMixin, CreateView):
    model = Employe
    form_class = EmployeForm
    template_name = 'rh/employe_form.html'
    success_url = reverse_lazy('employe_list')

    # Vous devrez gérer la création de l'objet Utilisateur associé ici
    # ou créer une vue plus complexe pour gérer les deux en même temps.

class EmployeUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = Employe
    form_class = EmployeForm
    template_name = 'rh/employe_form.html'
    success_url = reverse_lazy('employe_list')

class EmployeDeleteView(AdminOrRhRequiredMixin, DeleteView):
    model = Employe
    template_name = 'rh/employe_confirm_delete.html'
    success_url = reverse_lazy('employe_list')

# ==================================================
# Vues pour le modèle Conge (Demandé par l'Employé)
# ==================================================

# Vues pour l'employé pour faire sa demande
class CongeDemandeListView(LoginRequiredMixin, ListView):
    model = Conge
    template_name = 'employe/conge_demande_list.html'
    context_object_name = 'conges_demandes'

    def get_queryset(self):
        # Ne montrer que les congés de l'utilisateur connecté
        return Conge.objects.filter(employe__utilisateur=self.request.user)

class CongeDemandeCreateView(LoginRequiredMixin, CreateView):
    model = Conge
    form_class = CongeForm
    template_name = 'employe/conge_demande_form.html'
    success_url = reverse_lazy('conge_demande_list')

    def form_valid(self, form):
        # Assigner l'employé connecté automatiquement
        form.instance.employe = self.request.user.employe
        # Le statut est 'DEMANDE' par défaut dans le modèle, ce qui est correct
        messages.success(self.request, "Votre demande de congé a été soumise avec succès.")
        return super().form_valid(form)
    
# Vues pour le RH pour gérer les congés
class CongeGestionListView(AdminOrRhRequiredMixin, ListView):
    model = Conge
    template_name = 'rh/conge_gestion_list.html'
    context_object_name = 'conges'

class CongeGestionUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = Conge
    form_class = CongeForm
    template_name = 'rh/conge_gestion_form.html'
    success_url = reverse_lazy('conge_gestion_list')

# =====================================================
# Vues pour le modèle Presence (Gérées par le RH/Admin)
# =====================================================
# Le diagramme parle de "Pointer", ce qui est un peu différent de "Gérer".
# "Pointer" (pour l'employé) peut être une vue simple qui enregistre l'heure d'arrivée/départ.
# "Gérer les présences" (pour le RH) est une vue CRUD classique.

class PresenceListView(AdminOrRhRequiredMixin, ListView):
    model = Presence
    template_name = 'rh/presence_list.html'
    context_object_name = 'presences'

class PresenceCreateView(AdminOrRhRequiredMixin, CreateView):
    model = Presence
    form_class = PresenceForm
    template_name = 'rh/presence_form.html'
    success_url = reverse_lazy('presence_list')

class PresenceUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = Presence
    form_class = PresenceForm
    template_name = 'rh/presence_form.html'
    success_url = reverse_lazy('presence_list')

class PresenceDeleteView(AdminOrRhRequiredMixin, DeleteView):
    model = Presence
    template_name = 'rh/presence_confirm_delete.html'
    success_url = reverse_lazy('presence_list')

# =====================================================
# Vues pour le modèle FicheDePaie (Gérées par le RH)
# =====================================================

class FicheDePaieListView(AdminOrRhRequiredMixin, ListView):
    model = FicheDePaie
    template_name = 'rh/fiche_paie_list.html'
    context_object_name = 'fiches_paie'

class FicheDePaieCreateView(AdminOrRhRequiredMixin, CreateView):
    model = FicheDePaie
    form_class = FicheDePaieForm
    template_name = 'rh/fiche_paie_form.html'
    success_url = reverse_lazy('fiche_paie_list')

class FicheDePaieDetailView(AdminOrRhRequiredMixin, DetailView):
    model = FicheDePaie
    template_name = 'rh/fiche_paie_detail.html'
    context_object_name = 'fiche_paie'

class FicheDePaieUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = FicheDePaie
    form_class = FicheDePaieForm
    template_name = 'rh/fiche_paie_form.html'
    success_url = reverse_lazy('fiche_paie_list')

class FicheDePaieDeleteView(AdminOrRhRequiredMixin, DeleteView):
    model = FicheDePaie
    template_name = 'rh/fiche_paie_confirm_delete.html'
    success_url = reverse_lazy('fiche_paie_list')

# ==============================================================
# Vues pour le modèle Formation (Gérées par le RH)
# ==============================================================
# Le diagramme montre que l'employé "Participe" et "Suit", tandis que le RH "Gère".
# Gérer implique le CRUD sur le modèle Formation.
# Participer/Suivre implique le CRUD sur le modèle ParticipationFormation.

class FormationListView(AdminOrRhRequiredMixin, ListView):
    model = Annonce
    template_name = 'rh/formation_list.html'
    context_object_name = 'formations'

class FormationCreateView(AdminOrRhRequiredMixin, CreateView):
    model = Annonce
    # Vous n'avez pas de formulaire pour Formation, il faudrait le créer
    # form_class = FormationForm
    template_name = 'rh/formation_form.html'
    success_url = reverse_lazy('formation_list')

class FormationUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = Annonce
    # form_class = FormationForm
    template_name = 'rh/formation_form.html'
    success_url = reverse_lazy('formation_list')

class FormationDeleteView(AdminOrRhRequiredMixin, DeleteView):
    model = Annonce
    template_name = 'rh/formation_confirm_delete.html'
    success_url = reverse_lazy('formation_list')

# =====================================================
# Vues pour les Annonces (Gérées par l'Admin/RH)
# =====================================================

class AnnonceListView(LoginRequiredMixin, ListView):
    model = Annonce
    template_name = 'annoncelist.html'
    context_object_name = 'annonces'

class AnnonceCreateView(AdminOrRhRequiredMixin, CreateView):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'annonce_form.html'
    success_url = reverse_lazy('annonce_list')

class AnnonceDetailView(LoginRequiredMixin, DetailView):
    model = Annonce
    template_name = 'annonce_detail.html'
    context_object_name = 'annonce'

class AnnonceUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'annonce_form.html'
    success_url = reverse_lazy('annonce_list')

class AnnonceDeleteView(AdminOrRhRequiredMixin, DeleteView):
    model = Annonce
    template_name = 'annonce_confirm_delete.html'
    success_url = reverse_lazy('annonce_list')

# ==============================================================
# Vues pour les Avantages et Primes (Gérées par le RH)
# ==============================================================

class AvantageListView(AdminOrRhRequiredMixin, ListView):
    model = Avantage
    template_name = 'rh/avantage_list.html'
    context_object_name = 'avantages'

class AvantageCreateView(AdminOrRhRequiredMixin, CreateView):
    model = Avantage
    form_class = AvantageForm
    template_name = 'rh/avantage_form.html'
    success_url = reverse_lazy('avantage_list')

class AvantageUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = Avantage
    form_class = AvantageForm
    template_name = 'rh/avantage_form.html'
    success_url = reverse_lazy('avantage_list')

class AvantageDeleteView(AdminOrRhRequiredMixin, DeleteView):
    model = Avantage
    template_name = 'rh/avantage_confirm_delete.html'
    success_url = reverse_lazy('avantage_list')

class PrimeListView(AdminOrRhRequiredMixin, ListView):
    model = Prime
    template_name = 'rh/prime_list.html'
    context_object_name = 'primes'

class PrimeCreateView(AdminOrRhRequiredMixin, CreateView):
    model = Prime
    form_class = PrimeForm
    template_name = 'rh/prime_form.html'
    success_url = reverse_lazy('prime_list')

class PrimeUpdateView(AdminOrRhRequiredMixin, UpdateView):
    model = Prime
    form_class = PrimeForm
    template_name = 'rh/prime_form.html'
    success_url = reverse_lazy('prime_list')

class PrimeDeleteView(AdminOrRhRequiredMixin, DeleteView):
    model = Prime
    template_name = 'rh/prime_confirm_delete.html'
    success_url = reverse_lazy('prime_list')

# =====================================================
# Vues pour les Rôles et Utilisateurs (Gérées par l'Admin)
# =====================================================

class RoleListView(AdminRequiredMixin, ListView):
    model = Role
    template_name = 'admin/role_list.html'
    context_object_name = 'roles'

class RoleCreateView(AdminRequiredMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'admin/role_form.html'
    success_url = reverse_lazy('role_list')

class RoleUpdateView(AdminRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'admin/role_form.html'
    success_url = reverse_lazy('role_list')

class RoleDeleteView(AdminRequiredMixin, DeleteView):
    model = Role
    template_name = 'admin/role_confirm_delete.html'
    success_url = reverse_lazy('role_list')

class UtilisateurListView(AdminRequiredMixin, ListView):
    model = Utilisateur
    template_name = 'admin/utilisateur_list.html'
    context_object_name = 'utilisateurs'

class UtilisateurDetailView(AdminRequiredMixin, DetailView):
    model = Utilisateur
    template_name = 'admin/utilisateur_detail.html'
    context_object_name = 'utilisateur'

class UtilisateurCreateView(AdminRequiredMixin, CreateView):
    model = Utilisateur
    form_class = UtilisateurCreationForm
    template_name = 'admin/utilisateur_form.html'
    success_url = reverse_lazy('utilisateur_list')

    @transaction.atomic
    def form_valid(self, form):
        # Créer l'utilisateur
        user = form.save()
        # Créer l'employé associé si le rôle le nécessite
        if user.role and user.role.nom_role == 'Employe':
            Employe.objects.create(utilisateur=user)
        messages.success(self.request, "Utilisateur créé avec succès.")
        return redirect(self.get_success_url())

class UtilisateurUpdateView(AdminRequiredMixin, UpdateView):
    model = Utilisateur
    form_class = UtilisateurUpdateForm
    template_name = 'admin/utilisateur_form.html'
    success_url = reverse_lazy('utilisateur_list')

class UtilisateurDeleteView(AdminRequiredMixin, DeleteView):
    model = Utilisateur
    template_name = 'admin/utilisateur_confirm_delete.html'
    success_url = reverse_lazy('utilisateur_list')