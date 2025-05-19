import os
import django
import random
from datetime import datetime, timedelta, time
from django.utils import timezone
from faker import Faker

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'montutoreT.settings')
django.setup()

# Import des modèles
from monprojet.models import (
    Menu, Reservation, Commande, Contact, Stock, 
    Utilisateur, Employe, AnalysePlat, AnalyseClient, PredictionStock
)
from django.db.models import Count

fake = Faker('fr_FR')

def generate_analyses():
    """Génère les analyses IA basées sur les données existantes"""
    
    # 1. Analyses des plats (basées sur les commandes existantes)
    print("Génération des analyses de plats...")
    
    # Ne pas regénérer si des analyses existent déjà
    if AnalysePlat.objects.count() == 0:
        popular_menus = Commande.objects.values('menu_name').annotate(count=Count('id')).order_by('-count')
        
        for item in popular_menus:
            menu = Menu.objects.filter(nom_menu=item['menu_name']).first()
            if menu:
                AnalysePlat.objects.create(
                    plat=menu,
                    popularite=min(0.95, item['count'] / Commande.objects.count() * 5),
                    profitabilite=random.uniform(0.4, 0.98),
                    saison=random.choice(["été", "hiver", "printemps", "automne", "toute saison"]),
                    heure_pointe=time(hour=random.randint(12, 14)) if random.random() > 0.5 else time(hour=random.randint(19, 21)),
                )

    # 2. Segments clients (basés sur les réservations/commandes)
    print("Génération des segments clients...")
    if AnalyseClient.objects.count() == 0:
        segments = ["Clients occasionnels", "Clients réguliers", "Clients VIP", "Nouveaux clients", "Clients du déjeuner"]
        menus = list(Menu.objects.all())
        
        for segment in segments:
            analyse = AnalyseClient.objects.create(
                segment=segment,
                moyenne_depense=random.uniform(10, 50),
                frequence_visite=random.uniform(0.2, 4),
            )
            
            # Sélectionner des plats populaires
            nb_plats = min(5, len(menus))
            plats_preferes = random.sample(menus, nb_plats)
            analyse.plats_preferes.set(plats_preferes)

    # 3. Prédictions de stock (IA)
    print("Génération des prédictions de stock...")
    # Supprimer seulement les anciennes prédictions
    PredictionStock.objects.all().delete()
    
    stocks = Stock.objects.all()
    for stock in stocks:
        # Modèle de prédiction simplifié (à remplacer par votre vraie IA)
        quantite_predite = max(0, stock.quantite + random.randint(-15, 20))
        
        PredictionStock.objects.create(
            ingredient=stock,
            quantite_predite=quantite_predite,
            confiance=random.uniform(0.7, 0.95),
        )

def main():
    print("Début du traitement des données existantes...")
    
    # Vérification des données existantes
    print(f"Données actuelles:")
    print(f"- Menus: {Menu.objects.count()}")
    print(f"- Réservations: {Reservation.objects.count()}")
    print(f"- Commandes: {Commande.objects.count()}")
    print(f"- Stocks: {Stock.objects.count()}")
    
    # Génération des analyses IA seulement
    generate_analyses()
    
    print("Traitement terminé avec succès!")
    print(f"Résultats:")
    print(f"- Analyses Plat: {AnalysePlat.objects.count()}")
    print(f"- Analyses Client: {AnalyseClient.objects.count()}")
    print(f"- Prédictions Stock: {PredictionStock.objects.count()}")

if __name__ == "__main__":
    main()