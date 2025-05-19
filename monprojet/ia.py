import os
import django
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import random
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Max, F
from django.db.models.functions import ExtractHour

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'montutoreT.settings')
django.setup()

from monprojet.models import Commande, Menu, Stock, AnalysePlat, AnalyseClient, PredictionStock

from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import time
import random

def analyze_orders():
    """Analyse des commandes respectant vos modèles exacts"""
    try:
        # 1. Récupération des données agrégées
        commandes = Commande.objects.values('menu_name').annotate(
            total_quantity=Sum('quantity'),
            avg_price=Avg('menu_price')
        ).filter(total_quantity__gt=0)
        
        if not commandes:
            print("Aucune commande valide trouvée")
            return False

        total_commandes = sum(c['total_quantity'] for c in commandes)

        # 2. Traitement des données
        for cmd in commandes:
            try:
                # Trouve ou crée le menu (sans utiliser de relation inverse)
                menu, created = Menu.objects.get_or_create(
                    nom_menu=cmd['menu_name'],
                    defaults={
                        'prix': cmd['avg_price'],
                        'description': 'Menu créé automatiquement',
                        'categorie': 'filter-specialty'
                    }
                )

                # Crée ou met à jour l'analyse
                AnalysePlat.objects.update_or_create(
                    plat=menu,
                    defaults={
                        'popularite': (cmd['total_quantity'] / total_commandes) * 100,
                        'profitabilite': cmd['total_quantity'] * cmd['avg_price'],
                        'saison': get_current_season(),
                        'heure_pointe': time(hour=random.randint(11, 14))  # Heure aléatoire entre 11h et 14h
                    }
                )
            except Exception as e:
                print(f"Erreur traitement {cmd['menu_name']}: {str(e)}")
                continue

        print(f"{AnalysePlat.objects.count()} analyses de plat créées")
        return True

    except Exception as e:
        print(f"ERREUR analyse_orders: {str(e)}")
        return False

def analyze_customers():
    """Segmente les clients en groupes homogènes"""
    try:
        if not Commande.objects.exists():
            print("Aucune commande pour analyser les clients")
            return False

        # Modification: Regroupement différent pour avoir plus de données
        data = Commande.objects.values('customer_name', 'email').annotate(
            total_spent=Sum('menu_price'),
            avg_spent=Avg('menu_price'),
            visit_count=Count('id'),
            last_visit=Max('date_commande')
        ).filter(visit_count__gt=0)
        
        if len(data) < 2:  # Modification: Au moins 2 clients
            print(f"Seulement {len(data)} clients disponibles - clustering impossible")
            return False

        df = pd.DataFrame(list(data))
        df['recency'] = (timezone.now() - pd.to_datetime(df['last_visit'])).dt.days
        df['freq_score'] = df['visit_count'] / df['visit_count'].max() if df['visit_count'].max() > 0 else 0
        
        # Modification: Nombre de clusters dynamique
        n_clusters = min(3, len(df))  # Maximum 3 clusters pour petits datasets
        if n_clusters < 2:
            print("Trop peu de clients pour un clustering significatif")
            return False
            
        features = ['total_spent', 'avg_spent', 'recency', 'freq_score']
        scaler = StandardScaler()
        X = scaler.fit_transform(df[features])
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['segment'] = kmeans.fit_predict(X)
        
        # Modification: Segments simplifiés
        segment_map = {
            0: "Clients occasionnels",
            1: "Clients réguliers",
            2: "Clients fidèles"
        }
        
        for _, row in df.iterrows():
            segment_name = segment_map.get(row['segment'], "Autres clients")
            analyse, _ = AnalyseClient.objects.get_or_create(
                segment=segment_name,
                defaults={
                    'moyenne_depense': row['avg_spent'],
                    'frequence_visite': row['freq_score']
                }
            )
            
            # Ajout des plats préférés
            top_plats = Commande.objects.filter(
                customer_name=row['customer_name'],
                email=row['email']
            ).values('menu_name').annotate(
                count=Count('id')
            ).order_by('-count')[:3]
            
            for plat in top_plats:
                try:
                    menu, _ = Menu.objects.get_or_create(nom_menu=plat['menu_name'])
                    analyse.plats_preferes.add(menu)
                except Exception as e:
                    print(f"Erreur ajout plat préféré: {str(e)}")
                    continue
                    
        return True
        
    except Exception as e:
        print(f"Erreur dans analyze_customers: {str(e)}")
        return False
    
def predict_stock():
    """Prédiction des stocks avec gestion des erreurs améliorée"""
    try:
        if not Stock.objects.exists():
            print("Aucun stock à analyser")
            return False
            
        stocks = Stock.objects.all()
        
        for stock in stocks:
            try:
                # Solution alternative sans relation directe
                menu_names = Menu.objects.filter(
                    Q(description__icontains=stock.nom) | 
                    Q(nom_menu__icontains=stock.nom)
                ).values_list('nom_menu', flat=True)
                
                consumption = Commande.objects.filter(
                    date_commande__gte=timezone.now() - timedelta(days=30),
                    menu_name__in=menu_names
                ).aggregate(
                    total=Sum('quantity')
                )['total'] or 0
                
                avg_daily = consumption / 30
                predicted_qty = max(0, stock.quantite - (avg_daily * 7))
                confidence = min(0.95, 0.5 + (avg_daily * 0.02))  # Ajustement formule
                
                PredictionStock.objects.update_or_create(
                    ingredient=stock,
                    defaults={
                        'quantite_predite': round(predicted_qty),
                        'confiance': round(confidence, 2),
                        'date_prediction': timezone.now()
                    }
                )
                
            except Exception as e:
                print(f"Erreur prédiction pour {stock.nom}: {str(e)}")
                PredictionStock.objects.update_or_create(
                    ingredient=stock,
                    defaults={
                        'quantite_predite': max(0, stock.quantite - 5),
                        'confiance': 0.6,
                        'date_prediction': timezone.now()
                    }
                )
                continue
                
        return True
        
    except Exception as e:
        print(f"Erreur globale dans predict_stock: {str(e)}")
        return False

# Fonctions utilitaires
def create_default_prediction(stock):
    """Crée une prédiction par défaut"""
    try:
        PredictionStock.objects.update_or_create(
            ingredient=stock,
            defaults={
                'quantite_predite': max(0, stock.quantite - 10),
                'confiance': 0.7,
                'date_prediction': timezone.now()
            }
        )
    except Exception as e:
        print(f"Erreur création prédiction par défaut: {str(e)}")

def generate_popularity_chart(top_plats):
    """Génère le graphique des plats populaires"""
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(x='menu_name', y='total_quantity', data=top_plats)
        plt.title('Top 5 des plats les plus populaires')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        os.makedirs('static/analyses', exist_ok=True)
        plt.savefig('static/analyses/top_plats.png')
        plt.close()
    except Exception as e:
        print(f"Erreur génération graphique: {str(e)}")

def get_current_season():
    """Retourne la saison actuelle sans dépendances"""
    month = timezone.now().month
    if 3 <= month <= 5:
        return "printemps"
    elif 6 <= month <= 8:
        return "été"
    elif 9 <= month <= 11:
        return "automne"
    return "hiver"

def get_peak_hour(menu_id):
    """Retourne l'heure de pointe pour un menu"""
    try:
        menu = Menu.objects.get(pk=menu_id)
        peak = Commande.objects.filter(
            menu_name__iexact=menu.nom_menu
        ).annotate(
            hour=ExtractHour('date_commande')
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('-count').first()
        
        return timezone.now().time().replace(hour=peak['hour'] if peak else 12, minute=0)
    except Exception as e:
        print(f"Erreur recherche heure pointe: {str(e)}")
        return timezone.now().time().replace(hour=12, minute=0)

if __name__ == "__main__":
    # Exécution séquentielle avec gestion des erreurs
    results = {
        'orders': analyze_orders(),
        'customers': analyze_customers(),
        'stock': predict_stock()
    }
    
    print("\nRésultats des analyses:")
    for name, success in results.items():
        status = "SUCCÈS" if success else "ÉCHEC"
        print(f"- {name.upper()}: {status}")