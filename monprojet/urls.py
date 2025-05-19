from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('tableau_bord/', views.tableau_bord, name='tableau_bord'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('menu/ajout/', views.ajout_menu, name='Ajoutemenu'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('index/', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('admin_dashboard/', views.admin_page, name='monadmin'),
    path('commander/', views.passer_commande, name='passer_commande'),
    path('inscription/', views.inscription, name='inscription'),
    path('ajouter_invite/', views.ajouter_invite, name='ajouter_invite'),
    path('reserver/', views.reserver, name='reserver'),
    path('contact/', views.contact, name='contact'),
    path('passer_commande_invite/', views.passer_commande_invite, name='passer_commande_invite'),
    path('contact_invite/', views.contact_invite, name='contact_invite'),
    path('menu/', views.menu, name="menu"),
    path('stocks/', views.stocks, name='stocks'),
    path('commande/', views.commande, name='commande'),
    path('reservation/approuver/<int:reservation_id>/', views.approuver_reservation, name='approuver_reservation'),
    path('reservation/annuler/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
    path('employes/', views.employe_admin, name='EmployeADMIN'),
    path('ajouter-employe/', views.ajouter_employe, name='ajouter_employe'),
    path('modifier_employe/<int:id>/', views.modifier_employe, name='modifierEmploye'),
    path('supprimer_employe/<int:id>/', views.supprimer_employe, name='supprimerEmploye'),
    path("ajouter-menu/", views.ajouter_menu, name="ajouter_menu"),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('modifier-menu/<int:id_menu>/', views.modifier_menu, name='modifier_menu'),
    path('supprimer-menu/<int:id_menu>/', views.supprimer_menu, name='supprimer_menu'),
    path('approuver_reservation_admin/<int:reservation_id>/', views.approuver_reservation_admin, name='approuver_reservation_admin'),
    path('annuler_reservation_admin/<int:reservation_id>/', views.annuler_reservation_admin, name='annuler_reservation_admin'),
    path('employe/', views.employe_dashboard, name='employe'),
    path('serveur/', views.serveur_dashboard, name='serveur'),
    path('commandechef/', views.commande_view, name='commandechef'),
    path('AjouteStocks/', views.AjouteStocks, name='AjouteStocks'),
    path('order-form/', views.order_form, name='order_form'),
    path('ajoute_stock/', views.ajoute_stock, name='ajoute_stock'),
    path('stocks/', views.stocks, name='stocks'),
    path('stocks/<str:categorie>/', views.afficher_stocks, name='stocks_par_categorie'),
    # Catégories de stocks
    path('stocks/fruits/', views.fruits, name='fruits'),
    path('legumes/', views.legumes, name='legumes'),
    path('viandes/', views.viandes, name='viandes'),
    path('poissons/', views.poissons, name='poissons'),
    path('boissons/', views.boissons, name='boissons'),
    path('produits-laitiers/', views.produits_laitiers, name='produits_laitiers'),
    path('stocks/epices/', views.epices, name='epices'),
    path('update_commande_status/<int:commande_id>/<str:new_status>/', views.update_commande_status, name='update_commande_status'),
    path('menu_view/', views.menu_view, name='menu_view'),
    path('Suividecommande/', views.Suividecommande, name='Suividecommande'),
    path('logout/', views.custom_logout, name='logout'),
    path('tableau_bord/', views.tableau_bord, name='tableau_bord'),
    path('run_analyses', views.run_analyses, name='run_analyses'),
    # urls.py
    path('api/commander-ingredient/', views.commander_ingredient, name='commander_ingredient'), 
    path('analyse/refresh-stock/', views.refresh_stock_data, name='refresh_stock_data'),
    path('plat/<int:plat_id>/', views.plat_detail, name='plat_detail'),
    path('Analyse', views.Analyse, name='Analyse'),
    path('', views.acceuil, name='acceuil'),  # Page d'accueil
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
# Pour servir les fichiers statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


