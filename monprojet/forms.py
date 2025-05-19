from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from monprojet.models import Utilisateur
from .models import Reservation


class InscriptionForm(UserCreationForm):
    date_naissance = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password1', 'password2']

class ConnexionForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")




class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'email', 'telephone', 'date_reservation', 'heure_reservation', 'nombre_personnes', 'message']
from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = [
            'menu_name',
            'menu_price',
            'menu_description',
            'quantity',
            'other_dish',
            'other_dish_quantity',
            'customer_name',
            'email',
            'phone',
        ]
        widgets = {
            'menu_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'menu_price': forms.TextInput(attrs={'readonly': 'readonly'}),
            'menu_description': forms.Textarea(attrs={'readonly': 'readonly'}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'other_dish': forms.TextInput(attrs={'placeholder': 'Nom du plat supplémentaire'}),
            'other_dish_quantity': forms.NumberInput(attrs={'min': 1}),
            'phone': forms.TextInput(attrs={'required': 'required'}),
        }
        labels = {
            'menu_name': 'Nom du Plat',
            'menu_price': 'Prix',
            'menu_description': 'Description',
            'quantity': 'Quantité',
            'other_dish': 'Autre plat souhaité',
            'other_dish_quantity': 'Quantité pour ce plat supplémentaire',
            'customer_name': 'Votre Nom',
            'email': 'Email',
            'phone': 'Numéro de téléphone',
        }
    
# forms.py
from django import forms
from .models import Employe

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom', 'fonction', 'salaire', 'email', 'numero', 'statut']


from django import forms
from .models import Menu  # Assurez-vous d'importer le modèle Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu  # Utilisation du modèle Menu
        fields = ['nom_menu', 'description', 'prix', 'image']  # Champs du formulaire
