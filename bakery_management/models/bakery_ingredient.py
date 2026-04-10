# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BakeryIngredient(models.Model):
    _name = 'bakery.ingredient'
    _description = 'Ingredient de Patisserie'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nom de l'ingredient", required=True, tracking=True)
    category = fields.Selection([
        ('flour', 'Farine & Cereales'),
        ('sugar', 'Sucre & Edulcorants'),
        ('butter', 'Beurre & Matieres grasses'),
        ('eggs', 'Oeufs'),
        ('dairy', 'Produits laitiers'),
        ('other', 'Autre'),
    ], string='Categorie', required=True, default='other')
    unit_of_measure = fields.Selection([
        ('kg', 'Kilogramme (kg)'),
        ('g', 'Gramme (g)'),
        ('L', 'Litre (L)'),
        ('piece', 'Piece'),
    ], string='Unite de mesure', required=True, default='kg')
    quantity_on_hand = fields.Float(string='Quantite en stock')
    active = fields.Boolean(string='Actif', default=True)
    notes = fields.Text(string='Notes')