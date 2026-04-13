# -*- coding: utf-8 -*-
{
    'name': 'Bakery Management - Systeme de Gestion de Patisserie',
    'version': '17.0.0.9.0',
    'category': 'Industries',
    'summary': "Gestion complete d'une patisserie : stock, produits, commandes, facturation & tableau de bord",
    'description': '''
        Module de gestion de patisserie pour Odoo 17.

        Fonctionnalites :
        - Gestion des ingredients et du stock (alertes seuil minimum)
        - Catalogue de produits avec recettes et calcul du cout
        - Commandes clients avec workflow complet (5 etapes)
        - Facturation integree (account.move) avec suivi du paiement
        - Extension fiche client (historique, total depense)
        - Tableau de bord analytique en temps reel (OWL)
        - Securite par roles (Administrateur / Employe)
    ''',
    'author': 'Bakery Management',
    'website': '',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
        'views/ingredient_views.xml',
        'views/product_views.xml',
        'views/order_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'bakery_management/static/src/xml/bakery_dashboard.xml',
            'bakery_management/static/src/css/bakery_dashboard.css',
            'bakery_management/static/src/js/bakery_dashboard.js',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}