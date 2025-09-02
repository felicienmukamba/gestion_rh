from django import forms
from .models import (
    Employe, Conge, Presence, Annonce, FicheDePaie, Avantage, Prime, 
    JourneeTravail, Role, Utilisateur
)

# ==============================================
# Formulaires de base (création/édition simple)
# ==============================================

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        # On exclut le champ 'utilisateur' car il doit être géré séparément
        # lors de la création d'un compte.
        exclude = ['utilisateur'] 
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'poste': forms.TextInput(attrs={'class': 'form-control'}),
            'salaire_base': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['employe', 'date_debut', 'date_fin', 'motif', 'statut']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'employe': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['employe', 'journee', 'heure_arrivee', 'heure_depart']
        widgets = {
            'heure_arrivee': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_depart': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'employe': forms.Select(attrs={'class': 'form-select'}),
            'journee': forms.Select(attrs={'class': 'form-select'}),
        }

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'contenu', 'auteur']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'auteur': forms.Select(attrs={'class': 'form-select'}),
        }

class AvantageForm(forms.ModelForm):
    class Meta:
        model = Avantage
        fields = '__all__'
        widgets = {
            'nom_avantage': forms.TextInput(attrs={'class': 'form-control'}),
            'montant_avantage': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class PrimeForm(forms.ModelForm):
    class Meta:
        model = Prime
        fields = '__all__'
        widgets = {
            'nom_prime': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['nom_role']
        widgets = {
            'nom_role': forms.TextInput(attrs={'class': 'form-control'}),
        }

# =========================================================
# Formulaires plus complexes (ex: Fiche de paie, Utilisateur)
# =========================================================

class FicheDePaieForm(forms.ModelForm):
    class Meta:
        model = FicheDePaie
        # Les champs ManyToMany (primes, avantages) et les totaux calculés 
        # sont gérés dans la vue, pas directement dans le formulaire de base.
        fields = ['employe', 'mois', 'annee', 'statut', 'salaire_brut', 'cotisations_sociales', 'impot_sur_revenu']
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-select'}),
            'mois': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'annee': forms.NumberInput(attrs={'class': 'form-control', 'min': 2020}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'salaire_brut': forms.NumberInput(attrs={'class': 'form-control'}),
            'cotisations_sociales': forms.NumberInput(attrs={'class': 'form-control'}),
            'impot_sur_revenu': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UtilisateurCreationForm(forms.ModelForm):
    """Formulaire pour créer un nouvel utilisateur avec mot de passe."""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Sauvegarde l'utilisateur et hache le mot de passe
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UtilisateurUpdateForm(forms.ModelForm):
    """Formulaire pour modifier un utilisateur existant (sans changer le mdp directement)."""
    role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }