# -*- coding: utf-8 -*-
{
    'name': 'Bakery Management — Système de Gestion de Pâtisserie',
    'version': '17.0.1.0.0',
    'category': 'Industries',
    'summary': 'Gestion complète d\'une pâtisserie : stock, produits, commandes, facturation & tableau de bord',
    'description': """
        Module de gestion de pâtisserie pour Odoo 17.

        Fonctionnalités :
        ─────────────────
        ✔ Gestion des ingrédients et du stock (alertes seuil minimum)
        ✔ Catalogue de produits avec recettes et calcul du coût
        ✔ Commandes clients avec workflow complet (5 étapes)
        ✔ Facturation intégrée (account.move) avec suivi du paiement
        ✔ Extension fiche client (historique, total dépensé)
        ✔ Tableau de bord analytique en temps réel (OWL)
        ✔ Sécurité par rôles (Administrateur / Employé)
    """,
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
