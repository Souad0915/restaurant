from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.utils.crypto import get_random_string  # Ajout de l'importation de la fonction
from django.db import IntegrityError
from django.utils import timezone

import random
import string

class Menu(models.Model):
    CATEGORIE_CHOICES = [
        ('filter-starters', 'Entrées'),
        ('filter-salads', 'Salades'),
        ('filter-specialty', 'Spécialités'),
    ]
    
    id_menu = models.AutoField(primary_key=True)
    nom_menu = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='filter-specialty')

    def __str__(self):
        return self.nom_menu


# Table Reservation
from django.db import models

class Reservation(models.Model):
    id_reservation = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    date_reservation = models.DateField(default=timezone.now)
    heure_reservation = models.TimeField(default=timezone.now)
    nombre_personnes = models.IntegerField()
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Réservation de {self.nom} le {self.date_reservation} à {self.heure_reservation}"

# models.py

from django.db import models

from django.db import models
from django.utils import timezone
from .models import Menu  # Assure-toi que le modèle Menu est importé
from django.db import models
from django.utils import timezone

class Commande(models.Model):
    # Choix pour le statut de la commande
    STATUS_EN_ATTENTE = 'En attente'
    STATUS_APPROUVE = 'Approuvé'
    STATUS_PREPARATION = 'En préparation'
    STATUS_PRETE = 'Prête'
    STATUS_LIVREE = 'Livrée'
    STATUS_ANNULEE = 'Annulée'
    
    STATUS_CHOICES = [
        (STATUS_EN_ATTENTE, 'En attente'),
        (STATUS_APPROUVE, 'Approuvé'),
        (STATUS_PREPARATION, 'En préparation'),
        (STATUS_PRETE, 'Prête'),
        (STATUS_LIVREE, 'Livrée'),
        (STATUS_ANNULEE, 'Annulée'),
    ]

    # Informations sur le menu
    menu_name = models.CharField(max_length=255, verbose_name="Nom du menu")
    menu_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Prix unitaire"
    )
    menu_description = models.TextField(blank=True, null=True, verbose_name="Description")
    quantity = models.IntegerField(verbose_name="Quantité")
    
    # Autres plats
    other_dish = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Autre plat"
    )
    other_dish_quantity = models.IntegerField(
        default=0,
        verbose_name="Quantité autre plat"
    )
    
    # Prix total
    menu_total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Prix total"
    )
    
    # Informations client
    customer_name = models.CharField(
        max_length=255, 
        verbose_name="Nom du client"
    )
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(
        max_length=20, 
        verbose_name="Téléphone"
    )
    
    # Date et statut
    date_commande = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Date de commande"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_EN_ATTENTE,
        verbose_name="Statut"
    )

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_commande']  # Tri par date décroissante par défaut

    def __str__(self):
        return f"Commande #{self.id} - {self.customer_name} ({self.status})"

    def save(self, *args, **kwargs):
        # Vous pouvez ajouter ici une logique avant la sauvegarde si nécessaire
        super().save(*args, **kwargs)
    
from django.db import models

class Contact(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    sujet = models.CharField(max_length=255)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet}"

from django.db import models

class Stock(models.Model):
    CATEGORIE_CHOICES = [
        ('fruits', 'Fruits'),
        ('legumes', 'Légumes'),
        ('viandes', 'Viandes'),
        ('poissons', 'Poissons'),
        ('boissons', 'Boissons'),
        ('produits_laitiers', 'Produits Laitiers'),
        ('epices', 'Épices'),
    ]
    
    # Ajout des choix pour l'état
    ETAT_CHOICES = [
        ('faible', 'Faible (stock < 15)'),
        ('suffisant', 'Suffisant (stock ≥ 15)'),
    ]

    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    quantite = models.IntegerField()
    # Ajout du champ etat
    etat = models.CharField(
        max_length=20,
        choices=ETAT_CHOICES,
        default='suffisant'  # Valeur par défaut
    )

    def save(self, *args, **kwargs):
        """Met à jour automatiquement l'état avant chaque sauvegarde"""
        self.etat = 'faible' if self.quantite < 15 else 'suffisant'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.quantite} unités - {self.get_etat_display()})"





# Fonction pour générer un mot de passe aléatoire
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))




from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, username, password=None, role="client", **extra_fields):
        if not email and role != "invite":
            raise ValueError("L'email est requis")
        if not username and role != "invite":
            raise ValueError("Le nom d'utilisateur est requis")
        
        # Validation du mot de passe
        if password and len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role, **extra_fields)
        
        if password:
            user.set_password(password)  # Hachage automatique
        else:
            if role != "invite":
                raise ValueError("Le mot de passe est requis pour cet utilisateur.")
        
        user.save(using=self._db)
        return user

    def create_invite_user(self):
        """Crée un utilisateur invité avec un nom unique"""
        last_invite = Utilisateur.objects.filter(role="invite").order_by('-id').first()
        invite_number = last_invite.id + 1 if last_invite else 1
        username = f"invite{invite_number}"
        email = f"invite{invite_number}@example.com"

        try:
            return self.create_user(email=email, username=username, role="invite", password=None)
        except IntegrityError:
            return self.create_invite_user()

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('invite', 'Invité'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    objects = UtilisateurManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email if self.email else f"Invite-{self.username}"

    def save(self, *args, **kwargs):
        # Validation du mot de passe pour les non-invités
        if not self.password and self.role != "invite":
            raise ValidationError("Un mot de passe est requis")
        super().save(*args, **kwargs)

from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models

class EmployeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email doit être fourni.')
        
        # Validation du mot de passe
        if password and len(password) < 8:
            raise ValueError('Le mot de passe doit contenir au moins 8 caractères')
            
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Employe(AbstractBaseUser, PermissionsMixin):
    FONCTION_CHOICES = [
        ('serveur', 'Serveur'),
        ('chef_cuisinier', 'Chef Cuisinier'),
    ]

    nom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100, choices=FONCTION_CHOICES, default='serveur')
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(unique=True)
    numero = models.CharField(max_length=15)
    statut = models.CharField(max_length=10, choices=[('actif', 'Actif'), ('inactif', 'Inactif')], default='actif')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']

    objects = EmployeManager()

    # Gestion des permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name='groupes',
        blank=True,
        related_name="employe_groups",
        related_query_name="employe",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissions utilisateur',
        blank=True,
        related_name="employe_permissions",
        related_query_name="employe",
    )

    def __str__(self):
        return f"{self.nom} ({self.fonction})"

    def save(self, *args, **kwargs):
        # Validation du mot de passe
        if hasattr(self, 'password') and len(self.password) < 8:
            raise ValidationError("Le mot de passe employé doit contenir au moins 8 caractères")
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_superuser


class AnalysePlat(models.Model):
    plat = models.ForeignKey(Menu, on_delete=models.CASCADE)
    popularite = models.FloatField()
    profitabilite = models.FloatField()
    saison = models.CharField(max_length=50)
    heure_pointe = models.TimeField()

class AnalyseClient(models.Model):
    segment = models.CharField(max_length=100)
    moyenne_depense = models.FloatField()
    frequence_visite = models.FloatField()
    plats_preferes = models.ManyToManyField(Menu)

class PredictionStock(models.Model):
    ingredient = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantite_predite = models.IntegerField()
    confiance = models.FloatField()
    date_prediction = models.DateTimeField(auto_now_add=True)