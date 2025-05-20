from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from .models import Utilisateur
from django.core.mail import send_mail
from .models import Reservation
from .forms import ReservationForm
from .forms import CommandeForm
from .models import Commande
from django.http import HttpResponse
from .models import Stock  
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employe, Utilisateur
from .models import Contact
from django.core.mail import send_mail
from .models import Reservation
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Menu
from .models import Stock
from .models import Employe
from django.contrib import messages
from django.contrib.auth.hashers import make_password  # Pour hasher le mot de passe

from django.views.decorators.cache import never_cache

from django.contrib import admin

# Vue pour la page d'accueil
def acceuil(request):
    return render(request, 'acceuil.html')


# Vue pour la page d'accueil
def index2(request):
    menus = Menu.objects.all().order_by('nom_menu')
    categories = {
        'filter-starters': menus.filter(categorie='filter-starters'),
        'filter-salads': menus.filter(categorie='filter-salads'),
        'filter-specialty': menus.filter(categorie='filter-specialty'),
    }
    return render(request, 'index2.html', {'categories': categories})

def ajouter_invite(request):
    # Trouver l'utilisateur invité ayant le plus grand ID
    last_invite = Utilisateur.objects.filter(role="invite").order_by('-id').first()
    
    if last_invite:
        # Le prochain utilisateur invité sera invite + ID + 1
        invite_number = last_invite.id + 1
    else:
        invite_number = 1  # Si aucun utilisateur invité, commencer par invite1
    
    # Générer un nom d'utilisateur unique pour l'invité
    username = f"invite{invite_number}"
    
    # Créer un email unique pour l'invité
    email = f"invite{invite_number}@example.com"
    
    # Créer un utilisateur avec le rôle 'invite'
    utilisateur_invite = Utilisateur.objects.create_user(
        email=email,
        username=username,
        password=None,  # Pas de mot de passe requis pour l'invité
        role="invite"  # Le rôle est "invite"
    )

    # Optionnel: rediriger l'invité vers une page spécifique après la création
    return redirect('index2')  # Redirection vers la page d'index par exemple

    


def connexion(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Vérification d'abord pour l'employé
        try:
            employe = Employe.objects.get(email=email)
            if employe.statut == 'actif':
                if employe.check_password(password):
                    request.session['employe_id'] = employe.id
                    request.session['nom_utilisateur'] = employe.nom
                    return rediriger_employe(employe)
                else:
                    messages.error(request, "Mot de passe incorrect")
            else:
                messages.error(request, "Votre compte est désactivé. Contactez l'administrateur.")
            return render(request, 'connexion.html')
        except Employe.DoesNotExist:
            pass

        # Vérification pour l'utilisateur normal
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            request.session['nom_utilisateur'] = user.username
            return rediriger_utilisateur(user)
        else:
            # Vérifie si l'email existe pour afficher un message plus précis
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(username=email).exists():
                messages.error(request, "Aucun compte trouvé avec cet email")
            else:
                messages.error(request, "Mot de passe incorrect")

    return render(request, 'connexion.html')


def rediriger_employe(employe):
    if employe.fonction == "chef_cuisinier":
        return redirect('employe')  # Vue employé (chef cuisinier)
    elif employe.fonction == "serveur":
        return redirect('serveur')  # Vue serveur
    return redirect('connexion')  # Sécurité

def rediriger_utilisateur(user):
    if user.is_superuser:
        return redirect('monadmin')  # Admin Django
    elif user.role == "client":
        return redirect('index')
    elif user.role == "admin":
        return redirect('monadmin')
    else:
        return redirect('index')

def deconnexion(request):
    logout(request)
    request.session.flush()  # Supprimer toutes les sessions (y compris employé)
    return redirect('connexion')

# Protéger l'accès aux pages spécifiques
@login_required(login_url='connexion')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='connexion')
def admin_page(request):
    return render(request, 'monadmin.html')



def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('mot_de_passe')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'invite')

        # Vérification du mot de passe
        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return redirect('inscription')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('inscription')

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('inscription')

        try:
            user = Utilisateur.objects.create_user(
                email=email,
                username=username,
                password=password,
                role=role
            )
            login(request, user)
            messages.success(request, "Félicitations ! Votre inscription est réussie.")
            return redirect('connexion')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'inscription: {str(e)}")
            return redirect('inscription')

    return render(request, 'inscription.html')

def confirmation(request):
    return render(request, 'confirmation.html')



def reserver(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('numero')
        date_reservation = request.POST.get('date_reservation')
        heure_reservation = request.POST.get('heure_reservation')
        nombre_personnes = request.POST.get('nombre_personnes')
        message = request.POST.get('message')

        # Enregistrer dans la base de données
        reservation = Reservation.objects.create(
            nom=nom,
            email=email,
            telephone=telephone,
            date_reservation=date_reservation,
            heure_reservation=heure_reservation,
            nombre_personnes=nombre_personnes,
            message=message
        )

        # Envoi d'un e-mail de confirmation
        sujet = "Confirmation de votre réservation"
        contenu = f"""
        Bonjour {nom},

        Votre réservation au restaurant a été confirmée.

        📅 Date : {date_reservation}
        ⏰ Heure : {heure_reservation}
        👥 Nombre de personnes : {nombre_personnes}
        
        📞 Contact : {telephone}
        📨 Email : {email}

        Merci pour votre réservation ! À bientôt.

        L'équipe du restaurant
        """

        send_mail(
            sujet,
            contenu,
            'souadahmed@gmail.com',  # Remplace par ton adresse e-mail d’envoi
            [email],  # Destinataire
            fail_silently=False,
        )

        return render(request, 'index.html', {'success': 'Votre réservation a été enregistrée et un e-mail de confirmation a été envoyé.'})

    return render(request, 'index.html')








def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            # Enregistrer dans la base de données
            Contact.objects.create(nom=name, email=email, sujet=subject, message=message)

            # Envoyer un email de confirmation
            send_mail(
                subject="Confirmation de votre message",
                message=f"Bonjour {name},\n\nVotre message a bien été reçu.\n\nNous vous répondrons bientôt.\n\nMerci !",
                from_email="contact@votresite.com",
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'index.html', {'success': "Votre message a été envoyé avec succès !"})

    return render(request, 'index.html')


def passer_commande_invite(request):
    success_message = None  # Initialiser le message de confirmation
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        plat = request.POST.get('plat')
        quantite = request.POST.get('quantite')

        if nom and email and adresse and telephone and plat and quantite:
            # Enregistrer la commande en base de données
            commande = Commande(
                nom=nom,
                email=email,
                adresse=adresse,
                telephone=telephone,
                plat=plat,
                quantite=int(quantite)
            )
            commande.save()

            # Envoyer un e-mail de confirmation
            subject = "Confirmation de votre commande"
            message = f"""
            Bonjour {nom},

            Votre commande de {quantite} {plat}(s) a bien été enregistrée.

            📍 Adresse : {adresse}  
            📞 Téléphone : {telephone}

            Merci d'avoir commandé chez nous ! 🍽️
            """
            send_mail(subject, message, 'restaurant@example.com', [email])

            # Définir le message de succès
            success_message = "Votre commande a été enregistrée avec succès ! Un e-mail de confirmation vous a été envoyé."

    # Rendre index.html avec le message de confirmation
    return render(request, 'index2.html', {'success': success_message})

from .models import Contact

def contact_invite(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            # Enregistrer dans la base de données
            Contact.objects.create(nom=name, email=email, sujet=subject, message=message)

            # Envoyer un email de confirmation
            send_mail(
                subject="Confirmation de votre message",
                message=f"Bonjour {name},\n\nVotre message a bien été reçu.\n\nNous vous répondrons bientôt.\n\nMerci !",
                from_email="contact@votresite.com",
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'index2.html', {'success': "Votre message a été envoyé avec succès !"})

    return render(request, 'index2.html')

    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



@login_required
def menu(request):
    return render(request, 'menu.html')

@login_required
def commande(request):
    return render(request, 'commande.html')

@login_required
def employe(request):
    return render(request, 'employe.html')

@login_required
def reservation(request):
    return render(request, 'reservation.html')

def stocks(request):
    return render(request, 'stocks.html')

from django.shortcuts import render

def ajout_menu(request):
    return render(request, 'Ajoutemenu.html')  # Assurez-vous que ce template existe






def deconnexion(request):
    logout(request)
    return redirect('connexion')  # Redirige vers la page de connexion après déconnexion

from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation

# Vue pour afficher les réservations
def reservation(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation.html', {'reservations': reservations})

# Vue pour approuver une réservation
def approuver_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.approuve = True
    reservation.save()
    return redirect('reservation')  # Rediriger vers la page des réservations

# Vue pour annuler une réservation
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.annule = True
    reservation.save()
    return redirect('reservation')  # Rediriger vers la page des réservations

def tableau_bord(request):
    # Retourne la vue du tableau de bord (ajoute la logique nécessaire)
    return render(request, 'monadmin.html')

# views.py
from django.shortcuts import render
from .models import Reservation

def reservation_view(request):
    # Récupérer toutes les réservations
    reservations = Reservation.objects.all()

    # Passer les réservations au template
    return render(request, 'reservation.html', {'reservations': reservations})

from django.shortcuts import get_object_or_404, redirect
from .models import Reservation

def approuver_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id_reservation=reservation_id)
    # Mettre à jour le statut de la réservation (par exemple, en ajoutant un champ approuvé)
    reservation.status = 'APPROUVÉ'  # Tu peux ajouter ce champ dans ton modèle si nécessaire
    reservation.save()
    return redirect('reservation')  # Rediriger vers la page des réservations

def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id_reservation=reservation_id)
    # Annuler la réservation (par exemple, changer un champ de statut)
    reservation.status = 'ANNULÉ'  # Tu peux aussi ajouter un champ 'status' pour cela
    reservation.save()
    return redirect('reservation')  # Rediriger vers la page des réservations

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ma_vue(request):
    return HttpResponse("CSRF désactivé")

def employe_admin(request):
    employes = Employe.objects.all()  # Récupérer tous les employés
    return render(request, 'EmployeADMIN.html', {'employes': employes})

from django.shortcuts import render



def ajouter_employe(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        fonction = request.POST['fonction']
        salaire = request.POST['salaire']
        email = request.POST['email']
        numero = request.POST['numero']
        statut = request.POST['statut']
        password = request.POST['password']

        # Hasher le mot de passe avant de l'enregistrer
        hashed_password = make_password(password)

        # Création de l'employé
        employe = Employe(
            nom=nom,
            fonction=fonction,
            salaire=salaire,
            email=email,
            numero=numero,
            statut=statut,
            password=hashed_password  # Ajout du mot de passe haché
        )
        employe.save()

        messages.success(request, f"L'employé {nom} a été ajouté avec succès.")
        return redirect('EmployeADMIN')  # Rediriger vers la page des employés pour voir l'ajout

    return render(request, 'AjouterEmploye.html')  # Vérifie que ce fichier existe


from django.shortcuts import render, get_object_or_404, redirect
from .models import Employe
from django.contrib.auth.hashers import make_password

def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)

    if request.method == 'POST':
        employe.nom = request.POST['nom']
        employe.fonction = request.POST['fonction']
        employe.salaire = request.POST['salaire']
        employe.email = request.POST['email']
        employe.numero = request.POST['numero']
        employe.statut = request.POST['statut']
        
        # Si un mot de passe est fourni, on le hash et on le met à jour
        mot_de_passe = request.POST.get('mot_de_passe', '')
        if mot_de_passe:
            employe.mot_de_passe = make_password(mot_de_passe)
        
        employe.save()
        messages.success(request, f"L'employé {employe.nom} a été modifié avec succès.")
        return redirect('EmployeADMIN')  # Rediriger vers la page des employés

    return render(request, 'modifierEmploye.html', {'employe': employe})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Employe

def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)

    if request.method == 'POST':
        employe.delete()
        messages.success(request, f"L'employé {employe.nom} a été supprimé avec succès.")
        return redirect('EmployeADMIN')  # Rediriger après la suppression

    return render(request, 'supprimerEmploye.html', {'employe': employe})







admin.site.register(Menu)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Menu

def ajouter_menu(request):
    if request.method == 'POST':
        nom = request.POST.get('nom_menu', '').strip()
        prix = request.POST.get('prix', '').strip()
        description = request.POST.get('description', '').strip()
        categorie = request.POST.get('categorie', 'filter-specialty').strip()  # Utilisation de la valeur par défaut du modèle
        image = request.FILES.get('image')
        
        if nom and prix and description:
            try:
                menu = Menu(
                    nom_menu=nom,
                    prix=prix,
                    description=description,
                    categorie=categorie,
                    image=image
                )
                menu.save()
                messages.success(request, f"Le menu {nom} a été ajouté avec succès.")
                return redirect('menu_admin')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")
        else:
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
    
    return render(request, 'Ajoutemenu.html')

@never_cache
def menu_admin(request):
    menus = Menu.objects.all()
    return render(request, 'menu.html', {'menus': menus})

def index(request):
    menus = Menu.objects.all().order_by('nom_menu')
    categories = {
        'filter-starters': menus.filter(categorie='filter-starters'),
        'filter-salads': menus.filter(categorie='filter-salads'),
        'filter-specialty': menus.filter(categorie='filter-specialty'),
    }
    return render(request, 'index.html', {'categories': categories})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu
from django.contrib import messages

def modifier_menu(request, id_menu):
    menu = get_object_or_404(Menu, id_menu=id_menu)

    if request.method == 'POST':
        # Mise à jour des champs du menu
        menu.nom_menu = request.POST['nom_menu']
        menu.description = request.POST['description']
        menu.prix = request.POST['prix']
        
        # Si une nouvelle image est fournie, la mettre à jour
        if 'image' in request.FILES:
            menu.image = request.FILES['image']
        
        menu.save()  # Sauvegarder les modifications
        messages.success(request, f"Le menu {menu.nom_menu} a été modifié avec succès.")
        return redirect('menu_admin')  # Rediriger vers la liste des menus après la modification

    return render(request, 'modifiermenu.html', {'menu': menu, 'timestamp': now().timestamp()})

from django.utils.timezone import now

# Vue pour supprimer un menu
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from .models import Menu

def supprimer_menu(request, id_menu):
    # Utilisation de 'id_menu' au lieu de 'id'
    menu = get_object_or_404(Menu, id_menu=id_menu)

    if request.method == 'POST':
        menu.delete()
        messages.success(request, f"Le menu {menu.nom_menu} a été supprimé avec succès.")
        return redirect('menu_admin')  # Redirection vers la liste des menus après suppression

    return render(request, 'supprimemenu.html', {'menu': menu})


from django.conf import settings
from django.core.mail import send_mail
from .models import Reservation

# Fonction pour approuver la réservation
def approuver_reservation_admin(request, reservation_id):
    # Récupérer la réservation par son ID
    reservation = Reservation.objects.get(id_reservation=reservation_id)
    
    # Mettre à jour le statut de la réservation (par exemple, "Approuvé")
    reservation.status = 'Approuvé'  # Adaptez selon le champ que vous avez pour le statut
    reservation.save()

    # Contenu HTML de l'email avec une icône
    email_subject = 'Confirmation de votre réservation'
    email_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="background-color: #e0f7fa; padding: 20px; border-radius: 8px;">
                <h2 style="color: #00796b;">Votre Réservation a été Approuvée</h2>
                <p><strong>Bonjour {reservation.nom},</strong></p>
                <p>Nous avons le plaisir de vous informer que votre réservation pour le <strong>{reservation.date_reservation}</strong> à <strong>{reservation.heure_reservation}</strong> a été <span style="color: green;">approuvée</span>.</p>
                <p><strong>Nombre de personnes :</strong> {reservation.nombre_personnes}</p>
                <p style="font-size: 14px;">Nous vous remercions de choisir notre restaurant et espérons vous accueillir bientôt!</p>
                <p><img src="https://img.icons8.com/ios/50/000000/checkmark.png" alt="approuvé" width="30px" /> <span style="color: green; font-weight: bold;">Votre réservation a été confirmée.</span></p>
                <p style="font-size: 12px; color: #00796b;">Cordialement, <br>L'équipe de gestion des réservations.</p>
            </div>
        </body>
    </html>
    """

    # Envoi de l'email HTML
    send_mail(
        email_subject,
        '',
        settings.DEFAULT_FROM_EMAIL,  # Ici, settings est utilisé pour récupérer l'email d'envoi
        [reservation.email],
        fail_silently=False,
        html_message=email_message,
    )

    return redirect('reservation')  # Redirige vers la page des réservations


# Fonction pour annuler la réservation
def annuler_reservation_admin(request, reservation_id):
    # Récupérer la réservation par son ID
    reservation = Reservation.objects.get(id_reservation=reservation_id)
    
    # Mettre à jour le statut de la réservation (par exemple, "Annulé")
    reservation.status = 'Annulé'  # Adaptez selon le champ que vous avez pour le statut
    reservation.save()

    # Contenu HTML de l'email avec une icône
    email_subject = 'Annulation de votre réservation'
    email_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="background-color: #ffebee; padding: 20px; border-radius: 8px;">
                <h2 style="color: #c62828;">Votre Réservation a été Annulée</h2>
                <p><strong>Bonjour {reservation.nom},</strong></p>
                <p>Nous regrettons de vous informer que votre réservation pour le <strong>{reservation.date_reservation}</strong> à <strong>{reservation.heure_reservation}</strong> a été <span style="color: red;">annulée</span>.</p>
                <p><strong>Nombre de personnes :</strong> {reservation.nombre_personnes}</p>
                <p style="font-size: 14px;">Nous espérons vous accueillir lors de votre prochaine visite!</p>
                <p><img src="https://img.icons8.com/ios/50/000000/delete-sign.png" alt="annulé" width="30px" /> <span style="color: red; font-weight: bold;">Votre réservation a été annulée.</span></p>
                <p style="font-size: 12px; color: #c62828;">Cordialement, <br>L'équipe de gestion des réservations.</p>
            </div>
        </body>
    </html>
    """

    # Envoi de l'email HTML
    send_mail(
        email_subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [reservation.email],
        fail_silently=False,
        html_message=email_message,
    )

    return redirect('reservation')  # Redirige vers la page des réservations

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Stock

def employe_dashboard(request):
    return render(request, 'employe.html')


def serveur_dashboard(request):
    commandes = Commande.objects.filter(status__in=['Approuvé', 'En attente'])
    return render(request, 'serveur.html', {'commandes': commandes})


def commande_view(request):
    commandes = Commande.objects.all()
    return render(request, 'commandechef.html', {'commandes': commandes})

from django.shortcuts import render

def order_form(request):
    name = request.GET.get('name', '')
    price = request.GET.get('price', '')
    description = request.GET.get('description', '')

    context = {
        'name': name,
        'price': price,
        'description': description,
    }

    return render(request, 'order-form.html', context)


def AjouteStocks(request):
    return render(request, 'AjouteStocks.html')

from django.shortcuts import render
from .models import Stock

def stocks(request):
    # Pas besoin de try/except pour une opération aussi basique
    stocks = Stock.objects.all()  # Récupère TOUJOURS un QuerySet (même vide)
    return render(request, 'stocks.html', {'stocks': stocks})  # Retour garanti







from django.shortcuts import render
from .models import Stock

def fruits(request):
    stocks = Stock.objects.filter(categorie='fruits')
    return render(request, 'categories/Fruits.html', {'stocks': stocks})

def legumes(request):
    stocks = Stock.objects.filter(categorie='legumes')
    return render(request, 'legume.html', {'stocks': stocks})

def viandes(request):
    stocks = Stock.objects.filter(categorie='viandes')
    return render(request, 'viande.html', {'stocks': stocks})

def poissons(request):
    stocks = Stock.objects.filter(categorie='poissons')
    return render(request, 'poisson.html', {'stocks': stocks})

def boissons(request):
    stocks = Stock.objects.filter(categorie='boissons')
    return render(request, 'boisson.html', {'stocks': stocks})

def produits_laitiers(request):
    stocks = Stock.objects.filter(categorie='produits_laitiers')
    return render(request, 'produits.html', {'stocks': stocks})

def epices(request):
    stocks = Stock.objects.filter(categorie='epices')
    return render(request, 'categories/epices.html', {'stocks': stocks})




# Vue pour ajouter un stock en base de données
def ajoute_stock(request):
    if request.method == "POST":
        print("Données reçues :", request.POST)  # Affiche les données reçues

        categorie = request.POST.get('categorie')
        nom_produit = request.POST.get('produit')
        quantite = request.POST.get('quantite')


        try:
            quantite = int(quantite)
        except ValueError:
            return HttpResponse("Erreur : Quantité invalide", status=400)

        etat = "faible" if quantite < 15 else "suffisant"

        categories_valides = [cat[0] for cat in Stock.CATEGORIE_CHOICES]
        if categorie not in categories_valides:
            return HttpResponse("Erreur : Catégorie invalide", status=400)

        # Création de l'objet Stock
        Stock.objects.create(nom=nom_produit, quantite=quantite, categorie=categorie, etat=etat)
        return redirect('AjouteStocks')  # Redirection après succès

    return HttpResponse("Erreur lors de l'ajout du stock", status=400)


from django.shortcuts import render
from .models import Stock

# Vue pour afficher les stocks par catégorie (Fruits, Légumes, etc.)
def afficher_stocks(request, categorie):
    # Récupère les stocks filtrés par la catégorie
    stocks = Stock.objects.filter(categorie=categorie)

    # Passe les stocks à la template en fonction de la catégorie
    return render(request, f'{categorie.lower()}.html', {'stocks': stocks, 'categorie': categorie})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Commande
from django.core.exceptions import ValidationError

# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Commande

from django.shortcuts import render, redirect
from .models import Commande
from django.http import HttpResponse # pour la confirmation
from django.core.mail import send_mail #pour l'envoi de mail

from django.shortcuts import render
from django.core.mail import EmailMessage
from decimal import Decimal, InvalidOperation
import re

from .models import Commande

from django.shortcuts import render
from django.core.mail import EmailMessage
from decimal import Decimal, InvalidOperation
import re

from .models import Commande

from django.core.mail import EmailMessage
from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
import re
from datetime import datetime
from .models import Commande  # Assurez-vous que votre modèle Commande est importé
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import re
from .models import Menu, Commande
from datetime import datetime

def passer_commande(request):
    confirmation_message = None
    nom = request.GET.get('name', '')
    prix_unitaire_str = request.GET.get('price', '0')
    description = request.GET.get('description', '')
    menu_items = Menu.objects.values('nom_menu', 'prix')

    if request.method == 'POST':
        menu_name = request.POST.get('nom-menu')
        menu_price_str = request.POST.get('prix-menu')
        quantity_str = request.POST.get('quantité', '1')
        other_dish_name = request.POST.get('autre-plat', '').strip()
        other_dish_quantity_str = request.POST.get('autre-quantité-de-plat', '0')
        customer_name = request.POST.get('nom-client')
        email = request.POST.get('email')
        phone = request.POST.get('téléphone')

        menu_description_queryset = Menu.objects.filter(nom_menu=menu_name).values_list('description', flat=True)
        menu_description = menu_description_queryset.first() if menu_description_queryset.exists() else ""

        try:
            menu_unit_price = Decimal(re.sub(r'[^\d.]', '', menu_price_str))
            quantity = int(quantity_str) if quantity_str else 1
            if quantity < 1:
                raise ValueError("La quantité doit être au moins 1.")
        except (ValueError, InvalidOperation):
            confirmation_message = "Prix ou quantité invalide pour le plat principal."
            return render(request, 'order-form.html', {
                'confirmation_message': confirmation_message,
                'name': nom,
                'price': prix_unitaire_str,
                'description': description,
                'menu_items': menu_items,
            })

        other_dish_price = Decimal('0')
        other_dish_qty = 0

        if other_dish_name:
            try:
                supplement = Menu.objects.filter(nom_menu__iexact=other_dish_name).first()
                if supplement:
                    other_dish_price = supplement.prix
                    other_dish_qty = int(other_dish_quantity_str) if other_dish_quantity_str else 0
                    if other_dish_qty < 0:
                        raise ValueError("La quantité du plat supplémentaire ne peut pas être négative.")
                else:
                    confirmation_message = f"Erreur : Le plat '{other_dish_name}' n'existe pas dans notre menu."
                    return render(request, 'order-form.html', {
                        'confirmation_message': confirmation_message,
                        'name': nom,
                        'price': prix_unitaire_str,
                        'description': description,
                        'menu_items': menu_items,
                    })
            except (ValueError, InvalidOperation):
                confirmation_message = "Prix du plat supplémentaire invalide."
                return render(request, 'order-form.html', {
                    'confirmation_message': confirmation_message,
                    'name': nom,
                    'price': prix_unitaire_str,
                    'description': description,
                    'menu_items': menu_items,
                })
            except Exception as e:
                confirmation_message = f"Erreur lors de la récupération du plat supplémentaire : {str(e)}"
                return render(request, 'order-form.html', {
                    'confirmation_message': confirmation_message,
                    'name': nom,
                    'price': prix_unitaire_str,
                    'description': description,
                    'menu_items': menu_items,
                })

        total_price = (menu_unit_price * quantity) + (other_dish_price * other_dish_qty)

        commande = Commande(
            menu_name=menu_name,
            menu_price=menu_unit_price,
            menu_description=menu_description,
            quantity=quantity,
            other_dish=other_dish_name if other_dish_name else None,
            other_dish_quantity=other_dish_qty,
            menu_total_price=total_price, # Enregistrement du prix total
            customer_name=customer_name,
            email=email,
            phone=phone,
            date_commande=timezone.now()
        )

        try:
            commande.full_clean()
            commande.save()
            send_confirmation_email(
                customer_name, email, menu_name, menu_unit_price, quantity,
                other_dish_name, other_dish_qty, total_price, menu_description
            )
            confirmation_message = "Votre commande a été enregistrée avec succès ! Un email de confirmation vous a été envoyé."
        except ValidationError as e:
            confirmation_message = f"Erreur de validation : {', '.join(e.messages)}"
        except Exception as e:
            confirmation_message = f"Une erreur est survenue : {str(e)}"

    return render(request, 'order-form.html', {
        'confirmation_message': confirmation_message,
        'name': nom,
        'price': prix_unitaire_str,
        'description': description,
        'menu_items': menu_items,
    })

def send_confirmation_email(customer_name, email, menu_name, menu_price, quantity,
                             other_dish, other_dish_quantity, total_price, menu_description):
    """Envoie un email de confirmation avec le détail de la commande"""

    supplement_info = ""
    other_dish_price = Decimal('0')
    if other_dish:
        try:
            supplement = Menu.objects.get(nom_menu__iexact=other_dish)
            other_dish_price = supplement.prix
            supplement_info = f"""
            <div class="order-detail">
                <span class="detail-label">Plat supplémentaire:</span>
                <span>{other_dish_quantity} x {other_dish} ({other_dish_price} €)</span>
            </div>
            """
        except Menu.DoesNotExist:
            supplement_info = f"""
            <div class="order-detail">
                <span class="detail-label">Plat supplémentaire:</span>
                <span>{other_dish_quantity} x {other_dish} (Plat non trouvé)</span>
            </div>
            """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #f8f9fa; padding: 10px; text-align: center; }}
            .order-detail {{ margin: 10px 0; }}
            .detail-label {{ font-weight: bold; }}
            .total {{ font-size: 1.2em; font-weight: bold; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Confirmation de commande</h2>
            </div>

            <p>Bonjour {customer_name},</p>
            <p>Merci pour votre commande ! Voici les détails :</p>

            <div class="order-detail">
                <span class="detail-label">Plat principal:</span>
                <span>{quantity} x {menu_name} ({menu_price} €)</span>
            </div>

            {supplement_info}

            <div class="order-detail">
                <span class="detail-label">Description:</span>
                <span>{menu_description}</span>
            </div>

            <div class="total">
                Total de la commande: {total_price} €
            </div>

            <p>Nous vous contacterons bientôt pour la livraison.</p>
        </div>
    </body>
    </html>
    """

    email_msg = EmailMessage(
        'Confirmation de votre commande',
        html_content,
        'no-reply@votrerestaurant.com',
        [email],
    )
    email_msg.content_subtype = "html"
    try:
        email_msg.send()
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from .models import Commande

def update_commande_status(request, commande_id, new_status):
    commande = get_object_or_404(Commande, pk=commande_id)
    commande.status = new_status
    commande.save()

    # Déterminer la couleur selon le statut
    if new_status == 'Approuvé':
        color = "#4CAF50"  # Vert
        icon = "✓"
    elif new_status == 'En attente':
        color = "#FFC107"  # Orange
        icon = "⌛"
    else:  # Annulé
        color = "#F44336"  # Rouge
        icon = "✗"

    # Construction de la partie supplémentaire conditionnelle
    plat_supplementaire_html = ""
    plat_supplementaire_text = ""
    
    if commande.other_dish:
        plat_supplementaire_html = f"""
                <tr>
                    <td style="padding: 8px; font-weight: bold; border-bottom: 1px solid #ddd;">Plat supplémentaire:</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{commande.other_dish} (x{commande.other_dish_quantity})</td>
                </tr>
        """
        
        plat_supplementaire_text = f"• Plat supplémentaire: {commande.other_dish} (x{commande.other_dish_quantity})\n"

    # Construire le message HTML avec CSS intégré
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="color: {color}; font-size: 24px; text-align: center; margin-bottom: 20px;">
            {icon} Statut de votre commande #{commande.id}
        </div>
        
        <p>Bonjour {commande.customer_name},</p>
        
        <div style="background-color: {color}; color: white; padding: 10px; border-radius: 5px; text-align: center; margin: 20px 0; font-weight: bold;">
            Votre commande a été {new_status.lower()}.
        </div>
        
        <div style="background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Détails de la commande :</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; font-weight: bold; border-bottom: 1px solid #ddd;">Plat principal:</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{commande.menu_name} (x{commande.quantity})</td>
                </tr>
                {plat_supplementaire_html}
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Prix total:</td>
                    <td style="padding: 8px;">{commande.menu_total_price} fr</td>
                </tr>
            </table>
        </div>
        
        <p>{"Merci pour votre confiance !" if new_status == 'Approuvé' else 
           "Nous vous tiendrons informé." if new_status == 'En attente' else 
           "Pour toute question, n'hésitez pas à nous contacter."}</p>
        
        <div style="margin-top: 30px; font-size: 14px; color: #777; text-align: center;">
            <p>Cordialement,<br>L'équipe de votre restaurant</p>
        </div>
    </body>
    </html>
    """

    # Version texte originale
    text_message = f"""
    Bonjour {commande.customer_name},

    Votre commande #{commande.id} a été {new_status.lower()}.

    Détails de votre commande:
    {'-' * 30}
    • Plat principal: {commande.menu_name} (x{commande.quantity})
    {plat_supplementaire_text}
    • Prix total: {commande.menu_total_price} fr
    {'-' * 30}

    {
        "Merci pour votre confiance !" if new_status == 'Approuvé' else 
        "Nous vous tiendrons informé." if new_status == 'En attente' else 
        "Pour toute question, contactez-nous."
    }

    Cordialement,
    Votre service de restauration
    """

    # Version SMS
    # sms_message = (
    #     f"Commande #{commande.id} - Statut: {new_status}\n"
    #     f"Plat principal: {commande.menu_name} x{commande.quantity}\n"
    #     f"{'Plat supplémentaire: ' + commande.other_dish + ' x' + str(commande.other_dish_quantity) + '\n' if commande.other_dish else ''}"
    #     f"Total: {commande.menu_total_price:.2f} fr\n"
    #     f"{'Merci pour votre confiance!' if new_status == 'Approuvé' else 'A bientôt!'}"
    # )

    # Envoi de l'email
    send_mail(
        subject=f"Statut de votre commande #{commande.id}",
        message=text_message.strip(),
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[commande.email],
        fail_silently=False,
    )

    return redirect('commandechef')

from django.shortcuts import render
from .models import Menu

def menu_view(request):
    categories = {
        'filter-starters': Menu.objects.filter(categorie='filter-starters'),
        'filter-salads': Menu.objects.filter(categorie='filter-salads'),
        'filter-specialty': Menu.objects.filter(categorie='filter-specialty'),
    }
    return render(request, 'menu.html', {'categories': categories})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Commande

@login_required
def Suividecommande(request):
    # Récupérer l'email de l'utilisateur connecté
    user_email = request.user.email
    
    # Filtrer les commandes par email du client
    commandes = Commande.objects.filter(email__iexact=user_email).order_by('-date_commande')
    
    # Calculer les statistiques
    total_commandes = commandes.count()
    commandes_approuvees = commandes.filter(status='Approuvé').count()
    commandes_en_attente = commandes.filter(status='En attente').count()
    montant_total = commandes.aggregate(total=Sum('menu_total_price'))['total'] or 0
    
    # Préparer le contexte
    context = {
        'commandes': commandes,
        'total_commandes': total_commandes,
        'commandes_approuvees': commandes_approuvees,
        'commandes_en_attente': commandes_en_attente,
        'montant_total': montant_total,
    }
    
    return render(request, 'SuivideCommande.html', context)



from django.views.decorators.cache import never_cache

from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render
from datetime import timedelta
import json
from .models import Commande, Reservation, Employe
from django.views.decorators.cache import never_cache

@never_cache
def tableau_bord(request):
    today = timezone.now().date()

    # Statistiques principales (optimisées en une seule requête)
    stats = {
        'commandes_aujourdhui': Commande.objects.filter(date_commande__date=today).count(),
        'reservations_a_venir': Reservation.objects.filter(date_reservation__gte=today).count(),
        'employes_actifs': Employe.objects.filter(statut='actif').count(),
        'revenus_du_jour': Commande.objects.filter(
            date_commande__date=today,
            status__in=['Approuvé', 'Prête', 'Livrée']
        ).aggregate(total=Sum('menu_total_price'))['total'] or 0
    }

    # Données pour les graphiques
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    data = {
        'labels_jour': [jour.strftime('%a %d/%m') for jour in last_7_days],
        'data_commandes': [Commande.objects.filter(date_commande__date=jour).count() for jour in last_7_days],
        'data_reservations': [
            Reservation.objects.filter(heure_reservation__hour__lt=12).count(),
            Reservation.objects.filter(heure_reservation__hour__gte=12, heure_reservation__hour__lt=18).count(),
            Reservation.objects.filter(heure_reservation__hour__gte=18).count()
        ]
    }

    # Définir les couleurs du thème ici, basées sur l'image fournie
    theme_colors = {
        'background': '#f0f0f0',  # Gris clair pour le fond général
        'primary': '#8B4513',    # Marron (pour les barres du graphique principal, sidebar)
        'primary_light': '#A0522D', # Marron plus clair
        'secondary': '#D39E00',  # Or (pour les éléments secondaires, accentuation)
        'text_light': '#ffffff',       # Blanc pour le texte clair sur fond foncé
        'text_dark': '#222222', # Noir ou très foncé pour le texte sur fond clair
        'gridlines': 'rgba(0, 0, 0, 0.1)', # Gris très clair pour les lignes de grille
        'pie_chart_slices': [
            '#FFDB58',  # Jaune clair (Matin)
            '#FFB347',  # Orange clair (Midi)
            '#F4A460'   # Terre de Sienne (Soir)
        ],
        'warning': '#DC143C', # Rouge foncé pour les avertissements
        'success': '#228B22' # Vert foncé pour les succès

    }

    context = {
        **stats,
        'data_json': json.dumps(data),
        'theme_colors': theme_colors,
    }
    return render(request, 'monadmin.html', context)


from django.contrib import messages

def custom_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion')
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from django.contrib.auth.decorators import user_passes_test
from .models import AnalysePlat, AnalyseClient, PredictionStock, Menu, Stock, Commande
import json
from django.db.models import Case, When, Value, CharField 

@user_passes_test(lambda u: u.is_staff)
def run_analyses(request):
    """Exécute toutes les analyses IA"""
    try:
        # Simulation d'analyses (à remplacer par vos fonctions IA réelles)
        from random import randint, uniform
        from datetime import datetime, timedelta
        
        # 1. Analyse des plats (simulation)
        for plat in Menu.objects.all():
            AnalysePlat.objects.update_or_create(
                plat=plat,
                defaults={
                    'popularite': uniform(50, 100),
                    'profitabilite': uniform(5, 20),
                    'saison': random.choice(['été', 'hiver', 'printemps', 'automne']),
                    'heure_pointe': datetime.now().time()
                }
            )
        
        # 2. Analyse clients (simulation)
        segments = ['Fidèles', 'Occasionnels', 'Nouveaux', 'Gros consommateurs']
        for segment in segments:
            analyse, _ = AnalyseClient.objects.get_or_create(
                segment=segment,
                defaults={
                    'moyenne_depense': uniform(30, 100),
                    'frequence_visite': uniform(1, 10)
                }
            )
            # Associer 3 plats aléatoires comme préférés
            analyse.plats_preferes.set(Menu.objects.order_by('?')[:3])
        
        # 3. Prédiction stock (simulation)
        for ingredient in Stock.objects.all():
            PredictionStock.objects.update_or_create(
                ingredient=ingredient,
                defaults={
                    'quantite_predite': max(0, ingredient.quantite - randint(5, 15)),
                    'confiance': uniform(70, 95),
                    'date_prediction': timezone.now()
                }
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Analyses IA exécutées avec succès',
            'details': {
                'plats_analyses': AnalysePlat.objects.count(),
                'segments_clients': AnalyseClient.objects.count(),
                'predictions_stock': PredictionStock.objects.count()
            }
        })
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur globale: {str(e)}'
        }, status=500)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count, Q
from .models import AnalysePlat, AnalyseClient, PredictionStock, Menu, Stock
import json
from django.db.models import Case, When, Value, CharField
from django.utils import timezone

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import AnalysePlat, AnalyseClient, PredictionStock, Menu, Stock
import json
import random
from django.utils import timezone

def Analyse(request):
    try:
        # 1. Analyse des plats (Top 5) - avec génération de données si vide
        if not AnalysePlat.objects.exists():
            create_demo_plat_analysis()
            
        top_plats = AnalysePlat.objects.select_related('plat').order_by('-popularite')[:5]
        plat_names = [p.plat.nom_menu for p in top_plats]
        plat_popularity = [p.popularite for p in top_plats]
        
        # 2. Prédictions de stock
        predictions = PredictionStock.objects.select_related('ingredient').all()
        critical_count = predictions.filter(
            quantite_predite__lt=10
        ).count() 
        warning_count = predictions.filter(quantite_predite__lt=20, quantite_predite__gte=10).count()
        good_count = predictions.filter(quantite_predite__gte=20).count()
        
        # 3. Segments clients (avec génération de données si vide)
        if not AnalyseClient.objects.exists():
            create_demo_segments()
        segments = AnalyseClient.objects.all()
        
        # 4. Calcul de la confiance moyenne
        avg_confidence = predictions.aggregate(avg_conf=Avg('confiance'))['avg_conf'] or 0
        
        context = {
            'analyses_plats': AnalysePlat.objects.select_related('plat').order_by('-popularite'),
            'average_confidence': round(avg_confidence * 100, 1),
            'critical_stock_count': critical_count,
            'predictions_stock': predictions,
            'warning_stock_count': warning_count,
            'good_stock_count': good_count,
            'segments_clients': segments,
            'plat_names': json.dumps(plat_names),
            'plat_popularity': json.dumps(plat_popularity),
            'error': None
        }
        print(f" {critical_count}")
        print(f"{predictions.filter(quantite_predite__lt=10)}")
        
        return render(request, 'analyses.html', context)
        return render(request, 'analyses.html', context)
        
    except Exception as e:
        return render(request, 'analyses.html', {
            'error': str(e),
            'segments_clients': [],
            'analyses_plats': [],
            'predictions_stock': []
        })

def create_demo_plat_analysis():
    """Crée des analyses de plats de démonstration"""
    from random import uniform
    saisons = ['été', 'hiver', 'printemps', 'automne']
    
    for plat in Menu.objects.all():
        AnalysePlat.objects.create(
            plat=plat,
            popularite=uniform(50, 100),  # Entre 50% et 100%
            profitabilite=uniform(5, 20),  # Entre 5 et 20 francs
            saison=random.choice(saisons),
            heure_pointe=timezone.now().time()
        )

def create_demo_segments():
    """Crée des segments clients de démonstration"""
    segments_data = [
        {'segment': 'Clients fidèles', 'moyenne_depense': 85.50, 'frequence_visite': 4.2},
        {'segment': 'Clients occasionnels', 'moyenne_depense': 45.30, 'frequence_visite': 1.5},
        {'segment': 'Grands consommateurs', 'moyenne_depense': 120.75, 'frequence_visite': 3.8},
    ]
    
    menu_items = list(Menu.objects.all())
    
    for data in segments_data:
        segment = AnalyseClient.objects.create(
            segment=data['segment'],
            moyenne_depense=data['moyenne_depense'],
            frequence_visite=data['frequence_visite']
        )
        if menu_items:
            segment.plats_preferes.set(random.sample(menu_items, min(3, len(menu_items))))

@require_POST
@csrf_exempt
def refresh_stock_data(request):
    """Actualise les données de stock via AJAX"""
    try:
        # Simulation de mise à jour des prédictions
        from random import randint, uniform
        for prediction in PredictionStock.objects.all():
            prediction.quantite_predite = max(0, prediction.ingredient.quantite - randint(1, 10))
            prediction.confiance = uniform(80, 95)
            prediction.save()
        
        predictions = PredictionStock.objects.all()
        return JsonResponse({
            'status': 'success',
            'stock_status': {
                'critical': predictions.filter(quantite_predite__lt=10).count(),
                'warning': predictions.filter(quantite_predite__lt=20, quantite_predite__gte=10).count(),
                'good': predictions.filter(quantite_predite__gte=20).count(),
            },
            'average_confidence': predictions.aggregate(avg=Avg('confiance'))['avg'] or 0
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
@csrf_exempt
def commander_ingredient(request):
    """Gère les commandes d'ingrédients"""
    try:
        data = json.loads(request.body)
        ingredient_id = data.get('ingredient_id')
        quantity = data.get('quantity', 10)  # Valeur par défaut
        
        if not ingredient_id:
            raise ValueError("ID d'ingrédient manquant")
            
        stock = Stock.objects.get(pk=ingredient_id)
        stock.quantite += quantity
        stock.save()
        
        # Met à jour la prédiction
        prediction = PredictionStock.objects.get(ingredient=stock)
        prediction.quantite_predite += quantity
        prediction.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Stock de {stock.nom} mis à jour (+{quantity})',
            'new_quantity': stock.quantite,
            'new_prediction': prediction.quantite_predite
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def plat_detail(request, plat_id):
    """Détail d'un plat avec analyse"""
    plat = get_object_or_404(Menu, pk=plat_id)
    analyse = AnalysePlat.objects.filter(plat=plat).first()
    
    return render(request, 'plat_detail.html', {
        'plat': plat,
        'analyse': analyse,
        'stock_status': Stock.objects.filter(
            id__in=plat.ingredients.values_list('id', flat=True)
        ).annotate(
            status=Case(
                When(predictionstock__quantite_predite__lt=10, then=Value('critical')),
                When(predictionstock__quantite_predite__lt=20, then=Value('warning')),
                default=Value('good'),
                output_field=CharField()
            )
        )
    })