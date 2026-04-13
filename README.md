# Systeme de Gestion de Patisserie - Module Odoo 17

[![Odoo 17](https://img.shields.io/badge/Odoo-17.0-875A7B)]()
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)]()

Module Odoo complet pour la gestion d'une patisserie : ingredients, produits avec recettes, commandes clients, facturation integree et tableau de bord analytique.

## Fonctionnalites

### Gestion du Stock (Ingredients)
- Catalogue d'ingredients avec categories
- Suivi de la quantite en stock + seuil minimum
- Alertes automatiques (stock faible / vide)

### Catalogue Produits & Recettes
- Fiches produit avec image, categorie, prix de vente
- Recettes integrees : calcul automatique du cout de revient
- Calcul de la marge commerciale

### Commandes Clients
- Workflow complet en 5 etapes
- Reference auto-generee (CMD/2025/00001)
- Vue Kanban groupee par etat

### Facturation (account.move)
- Bouton Creer la facture depuis la commande
- Suivi du statut de facturation

### Tableau de Bord (OWL)
- KPIs en temps reel
- Commandes recentes et alertes stock

## Installation

1. Copier bakery_management/ dans addons/
2. Redemarrer Odoo
3. Installer depuis Applications

## Prerequis

- Odoo 17.0
- Modules : base, mail, account, stock