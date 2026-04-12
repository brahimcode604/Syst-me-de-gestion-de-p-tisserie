# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BakeryIngredient(models.Model):
    _name = 'bakery.ingredient'
    _description = 'Ingrédient de Pâtisserie'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'category, name'
    _rec_name = 'name'

    # ─── Champs principaux ───────────────────────────────────────────────────

    name = fields.Char(
        string='Nom de l\'ingrédient',
        required=True,
        tracking=True,
    )
    category = fields.Selection([
        ('flour',     'Farine & Céréales'),
        ('sugar',     'Sucre & Édulcorants'),
        ('butter',    'Beurre & Matières grasses'),
        ('eggs',      'Œufs'),
        ('dairy',     'Produits laitiers'),
        ('fruit',     'Fruits & Confitures'),
        ('chocolate', 'Chocolat & Cacao'),
        ('spice',     'Épices & Arômes'),
        ('leavening', 'Levures & Levains'),
        ('other',     'Autre'),
    ], string='Catégorie', required=True, default='other', tracking=True)

    unit_of_measure = fields.Selection([
        ('kg',      'Kilogramme (kg)'),
        ('g',       'Gramme (g)'),
        ('L',       'Litre (L)'),
        ('mL',      'Millilitre (mL)'),
        ('piece',   'Pièce'),
        ('package', 'Sachet / Paquet'),
    ], string='Unité de mesure', required=True, default='kg')

    # ─── Stock ───────────────────────────────────────────────────────────────

    quantity_on_hand = fields.Float(
        string='Quantité en stock',
        digits=(16, 3),
        tracking=True,
    )
    minimum_quantity = fields.Float(
        string='Seuil minimum',
        digits=(16, 3),
        help='Alerte déclenchée si le stock descend en dessous de cette valeur.',
    )

    # ─── Tarification ────────────────────────────────────────────────────────

    cost_price = fields.Float(
        string='Prix unitaire (MAD)',
        digits=(16, 2),
        tracking=True,
    )
    stock_value = fields.Float(
        string='Valeur du stock (MAD)',
        compute='_compute_stock_value',
        store=True,
        digits=(16, 2),
    )

    # ─── Relations ───────────────────────────────────────────────────────────

    supplier_id = fields.Many2one(
        'res.partner',
        string='Fournisseur principal',
        domain=[('supplier_rank', '>', 0)],
    )

    # ─── Statut & divers ─────────────────────────────────────────────────────

    stock_status = fields.Selection([
        ('ok',    'Stock OK'),
        ('low',   'Stock Faible'),
        ('empty', 'Stock Vide'),
    ], string='État du stock', compute='_compute_stock_status', store=True)

    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Actif', default=True)

    # ─── Computed ────────────────────────────────────────────────────────────

    @api.depends('quantity_on_hand', 'minimum_quantity')
    def _compute_stock_status(self):
        for rec in self:
            if rec.quantity_on_hand <= 0:
                rec.stock_status = 'empty'
            elif rec.quantity_on_hand < rec.minimum_quantity:
                rec.stock_status = 'low'
            else:
                rec.stock_status = 'ok'

    @api.depends('quantity_on_hand', 'cost_price')
    def _compute_stock_value(self):
        for rec in self:
            rec.stock_value = rec.quantity_on_hand * rec.cost_price

    # ─── Contraintes ─────────────────────────────────────────────────────────

    @api.constrains('quantity_on_hand')
    def _check_quantity(self):
        for rec in self:
            if rec.quantity_on_hand < 0:
                raise ValidationError(
                    f"La quantité de '{rec.name}' ne peut pas être négative."
                )

    # ─── Actions ─────────────────────────────────────────────────────────────

    def action_add_stock(self):
        """Ouvre le formulaire pour ajouter du stock."""
        return {
            'name': f'Modifier le stock : {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'bakery.ingredient',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def name_get(self):
        result = []
        for rec in self:
            label = f"{rec.name} ({rec.quantity_on_hand} {rec.unit_of_measure})"
            result.append((rec.id, label))
        return result
