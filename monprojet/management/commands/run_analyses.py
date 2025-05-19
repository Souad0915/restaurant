from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from models import AnalysePlat, AnalyseClient, PredictionStock, Menu
from ia import analyze_orders, analyze_customers, predict_stock
import json
from math import Avg

def run_analyses(request):
    if request.user.is_staff:
        try:
            # Exécuter les analyses IA
            analyze_orders()
            analyze_customers()
            predict_stock()
            
            return HttpResponse("Analyses IA exécutées avec succès!")
        except Exception as e:
            return HttpResponse(f"Erreur lors des analyses IA: {str(e)}", status=500)
    return HttpResponse("Accès refusé", status=403)

def Analyse(request):
    try:
        # Récupérer les 5 plats les plus populaires
        top_plats = AnalysePlat.objects.order_by('-popularite')[:5]
        
        context = {
            'analyses_plats': AnalysePlat.objects.order_by('-popularite'),
            'segments_clients': AnalyseClient.objects.all(),
            'predictions_stock': PredictionStock.objects.all().select_related('ingredient'),
            'plat_names': [p.plat.nom_menu for p in top_plats],
            'plat_popularity': [p.popularite for p in top_plats],
            'critical_stock_count': PredictionStock.objects.filter(quantite_predite__lt=10).count(),
            'warning_stock_count': PredictionStock.objects.filter(quantite_predite__lt=20, quantite_predite__gte=10).count(),
            'good_stock_count': PredictionStock.objects.filter(quantite_predite__gte=20).count(),
            'average_confidence': PredictionStock.objects.aggregate(Avg('confiance'))['confiance__avg'] * 100 
                               if PredictionStock.objects.exists() else 0,
        }
        return render(request, 'analyses.html', context)
    except Exception as e:
        return render(request, 'analyses.html', {'error': str(e)})