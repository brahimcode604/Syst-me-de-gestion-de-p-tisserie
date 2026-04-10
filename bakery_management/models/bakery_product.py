# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BakeryProduct(models.Model):
    _name = 'bakery.product'
    _description = 'Produit de Patisserie'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom du produit', required=True, tracking=True)
    description = fields.Text(string='Description')
    category = fields.Selection([
        ('cake', 'Gateau'),
        ('pastry', 'Viennoiserie'),
        ('bread', 'Pain & Boulangerie'),
        ('tart', 'Tarte'),
        ('cookie', 'Biscuit & Cookie'),
        ('other', 'Autre'),
    ], string='Categorie', required=True, default='cake')
    sale_price = fields.Float(string='Prix de vente (MAD)', required=True)
    image_1920 = fields.Image(string='Image du produit', max_width=1920, max_height=1920)
    active = fields.Boolean(string='Actif', default=True)