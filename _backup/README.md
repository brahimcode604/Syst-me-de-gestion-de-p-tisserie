# 🍰 Système de Gestion de Pâtisserie — Module Odoo 17

[![Odoo 17](https://img.shields.io/badge/Odoo-17.0-875A7B?style=flat-square&logo=odoo)](https://www.odoo.com)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/lgpl-3.0)

Module Odoo complet pour la **gestion d'une pâtisserie** : ingrédients, produits avec recettes, commandes clients, facturation intégrée et tableau de bord analytique en temps réel.

---

## ✨ Fonctionnalités

### 🧂 Gestion du Stock (Ingrédients)
- Catalogue d'ingrédients avec catégories (farine, sucre, chocolat…)
- Suivi de la quantité en stock + seuil minimum
- Alertes automatiques (stock faible / vide) avec badges colorés
- Calcul automatique de la valeur du stock
- Vues : Liste, Formulaire, Kanban

### 🎂 Catalogue Produits & Recettes
- Fiches produit avec image, catégorie, prix de vente
- **Recettes intégrées** : liaison ingrédients → calcul automatique du coût de revient
- Calcul de la **marge commerciale** en temps réel
- Vue Kanban visuelle avec images des produits

### 📋 Commandes Clients
- Workflow complet en **5 étapes** :
  `Brouillon → Confirmée → En production → Prête → Livrée`
- Référence auto-générée (`CMD/2025/00001`)
- Vue Kanban groupée par état
- Notes / instructions spéciales par commande

### 💰 Facturation (account.move)
- Bouton **"Créer la facture"** directement depuis la commande
- Suivi du statut de facturation (Non facturée / Partielle / Payée)
- Lien direct vers les factures Odoo native
- Compteur de factures sur la fiche commande

### 👥 Gestion des Clients
- Extension de la fiche `res.partner`
- Onglet **Pâtisserie** avec historique des commandes
- Statistiques : nombre de commandes, total dépensé
- Badge rapide sur la fiche client

### 📊 Tableau de Bord Analytique (OWL)
- KPIs en temps réel :
  - Commandes aujourd'hui
  - Chiffre d'affaires du mois
  - Commandes en cours
  - Commandes du mois
  - Alertes de stock
- Liste des commandes récentes (cliquables)
- Liste des ingrédients en alerte stock
- Actions rapides en un clic

### 🔒 Sécurité par Rôles
| Rôle | Accès |
|---|---|
| **Employé** | Lecture stock, création/modification commandes, lecture produits |
| **Administrateur** | Accès complet + configuration + facturation |

---

## 📁 Structure du Module

```
bakery_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── bakery_ingredient.py    # Stock / Ingrédients
│   ├── bakery_product.py       # Produits & Recettes
│   ├── bakery_order.py         # Commandes + Facturation
│   └── res_partner.py          # Clients (extension)
├── security/
│   ├── security.xml            # Groupes : Admin & Employé
│   └── ir.model.access.csv     # Droits d'accès CRUD
├── views/
│   ├── dashboard_views.xml     # Action dashboard OWL
│   ├── menu_views.xml          # Menus + Actions
│   ├── ingredient_views.xml    # Vues Stock
│   ├── product_views.xml       # Vues Produits
│   ├── order_views.xml         # Vues Commandes
│   └── res_partner_views.xml   # Vues Clients
├── data/
│   └── sequences.xml           # Séquence CMD/YYYY/NNNNN
└── static/
    ├── description/
    │   └── icon.png
    └── src/
        ├── js/bakery_dashboard.js
        ├── xml/bakery_dashboard.xml
        └── css/bakery_dashboard.css
```

---

## 🚀 Installation

### Prérequis
- **Odoo 17.0**
- Modules Odoo requis : `base`, `mail`, `account`, `stock`

### Étapes
1. Copier le dossier `bakery_management/` dans votre répertoire `addons/`
2. Redémarrer Odoo :
   ```bash
   ./odoo-bin -c odoo.conf
   ```
3. Aller dans **Paramètres → Applications → Mettre à jour la liste**
4. Rechercher **"Bakery Management"** et cliquer **Installer**

### Installation via ligne de commande
```bash
# Nouvelle installation
./odoo-bin -d votre_base -i bakery_management --stop-after-init

# Mise à jour
./odoo-bin -d votre_base -u bakery_management --stop-after-init
```

---

## 🗂 Modèles de Données

| Modèle | Description |
|---|---|
| `bakery.ingredient` | Ingrédients avec suivi de stock |
| `bakery.product` | Produits de pâtisserie |
| `bakery.recipe.line` | Lignes de recette (ingrédient × quantité) |
| `bakery.order` | Commandes clients |
| `bakery.order.line` | Lignes de commande (produit × quantité) |
| `res.partner` (extension) | Champs pâtisserie sur les clients |

---

## 📱 Menus & Navigation

```
🍰 Pâtisserie
├── 📊 Tableau de bord
├── 📋 Commandes
│   └── Toutes les commandes
├── 🎂 Catalogue
│   └── Produits & Recettes
├── 🧂 Stock
│   ├── Ingrédients
│   └── ⚠️ Alertes Stock
└── 👥 Clients
```

---

## 📄 Licence

Ce module est distribué sous licence **LGPL-3**.
