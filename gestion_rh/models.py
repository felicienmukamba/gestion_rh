from django.db import models
from django.contrib.auth.models import AbstractUser

# On peut étendre le modèle User de base ou en créer un complètement séparé.
# Pour la simplicité et la robustesse, on va lier notre Employe au User de Django.

class Role(models.Model):
    nom_role = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom_role

class Utilisateur(AbstractUser):
    # AbstractUser contient déjà username, password, email, etc.
    # On ajoute juste la liaison vers le rôle.
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

class Employe(models.Model):
    # Liaison One-to-One avec le modèle Utilisateur pour l'authentification
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    service = models.CharField(max_length=100) # Pourrait être une ForeignKey vers un modèle Departement
    poste = models.CharField(max_length=100)   # Pourrait être une ForeignKey vers un modèle Poste
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    date_embauche = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"

class Conge(models.Model):
    STATUT_CHOICES = [
        ('DEMANDE', 'Demandé'),
        ('VALIDE', 'Validé'),
        ('REFUSE', 'Refusé'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField()
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='DEMANDE')

    def __str__(self):
        return f"Congé pour {self.employe} du {self.date_debut} au {self.date_fin}"

class Formation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    duree_heures = models.IntegerField()
    participants = models.ManyToManyField(Employe, through='ParticipationFormation')

    def __str__(self):
        return self.titre

class ParticipationFormation(models.Model):
    STATUT_CHOICES = [
        ('INSCRIT', 'Inscrit'),
        ('TERMINE', 'Terminé'),
        ('ANNULE', 'Annulé'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    date_inscription = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='INSCRIT')
    resultat = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('employe', 'formation')

# ... (Les modèles Role, Utilisateur, Employe, Conge, Formation, ParticipationFormation existent déjà) ...

class JourneeTravail(models.Model):
    """Représente une journée de travail spécifique."""
    date_journee = models.DateField(unique=True, help_text="Date de la journée de travail")

    def __str__(self):
        return self.date_journee.strftime('%Y-%m-%d')

class Presence(models.Model):
    """Enregistre les heures d'arrivée et de départ d'un employé pour une journée."""
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='presences')
    journee = models.ForeignKey(JourneeTravail, on_delete=models.CASCADE, related_name='presences_jour')
    heure_arrivee = models.TimeField()
    heure_depart = models.TimeField(null=True, blank=True)

    class Meta:
        # Un employé ne peut avoir qu'un enregistrement de présence par jour.
        # Si un employé peut pointer plusieurs fois par jour (ex: pause déjeuner),
        # il faudrait retirer cette contrainte et adapter la logique.
        unique_together = ('employe', 'journee')

    def __str__(self):
        return f"Présence de {self.employe} le {self.journee.date_journee}"

class Annonce(models.Model):
    """Modèle pour les annonces internes."""
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='annonces')

    def __str__(self):
        return self.titre

# --- Modèles pour la Fiche de Paie ---

class Avantage(models.Model):
    """Définit un type d'avantage social (ex: assurance maladie, tickets restaurant)."""
    nom_avantage = models.CharField(max_length=150)
    montant_avantage = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_avantage} - {self.montant_avantage}"

class Prime(models.Model):
    """Définit un type de prime (ex: prime de rendement, 13ème mois)."""
    nom_prime = models.CharField(max_length=150)
    # Le montant peut être fixe ou calculé, on le stockera dans la liaison avec la fiche de paie.
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nom_prime

class FicheDePaie(models.Model):
    """Le document central de la paie pour un employé pour un mois donné."""
    STATUT_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('VALIDE', 'Validée'),
        ('EMISE', 'Émise'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='fiches_de_paie')
    mois = models.IntegerField(help_text="Le mois de la paie (1-12)")
    annee = models.IntegerField(help_text="L'année de la paie")
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='BROUILLON')
    salaire_brut = models.DecimalField(max_digits=10, decimal_places=2)
    total_primes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_avantages = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cotisations_sociales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impot_sur_revenu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salaire_net = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Pour lier les primes et avantages spécifiques à CETTE fiche de paie
    avantages = models.ManyToManyField(Avantage, through='FichePaieAvantage')
    primes = models.ManyToManyField(Prime, through='FichePaiePrime')

    class Meta:
        unique_together = ('employe', 'mois', 'annee') # Une seule fiche de paie par employé par mois/année

    def __str__(self):
        return f"Fiche de paie pour {self.employe} - {self.mois}/{self.annee}"

# Modèles intermédiaires pour stocker le montant spécifique au moment de la paie
class FichePaieAvantage(models.Model):
    fiche_de_paie = models.ForeignKey(FicheDePaie, on_delete=models.CASCADE)
    avantage = models.ForeignKey(Avantage, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2, help_text="Montant de l'avantage pour ce mois spécifique")

    class Meta:
        unique_together = ('fiche_de_paie', 'avantage')

class FichePaiePrime(models.Model):
    fiche_de_paie = models.ForeignKey(FicheDePaie, on_delete=models.CASCADE)
    prime = models.ForeignKey(Prime, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2, help_text="Montant de la prime pour ce mois spécifique")

    class Meta:
        unique_together = ('fiche_de_paie', 'prime')