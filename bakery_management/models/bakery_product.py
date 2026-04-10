# TODO: ajouter tests unitaires pour le calcul du cout
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BakeryProduct(models.Model):
    _name = 'bakery.product'
    _description = 'Produit de Pâtisserie'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'category, name'

    # ─── Champs principaux ───────────────────────────────────────────────────

    name = fields.Char(
        string='Nom du produit',
        required=True,
        tracking=True,
    )
    description = fields.Text(string='Description')
    category = fields.Selection([
        ('cake',      'Gâteau'),
        ('pastry',    'Viennoiserie'),
        ('bread',     'Pain & Boulangerie'),
        ('tart',      'Tarte'),
        ('cookie',    'Biscuit & Cookie'),
        ('chocolate', 'Chocolat & Confiserie'),
        ('drink',     'Boisson'),
        ('other',     'Autre'),
    ], string='Catégorie', required=True, default='cake', tracking=True)

    # ─── Tarification ────────────────────────────────────────────────────────

    sale_price = fields.Float(
        string='Prix de vente (MAD)',
        digits=(16, 2),
        required=True,
        tracking=True,
    )
    cost_price = fields.Float(
        string='Coût de revient (MAD)',
        compute='_compute_cost_price',
        store=True,
        digits=(16, 2),
    )
    margin = fields.Float(
        string='Marge (%)',
        compute='_compute_margin',
        store=True,
        digits=(16, 1),
    )

    # ─── Médias & infos ──────────────────────────────────────────────────────

    image_1920 = fields.Image(
        string='Image du produit',
        max_width=1920,
        max_height=1920,
    )
    preparation_time = fields.Float(
        string='Temps de préparation (h)',
        digits=(16, 2),
    )
    active = fields.Boolean(string='Actif', default=True)

    # ─── Recette ─────────────────────────────────────────────────────────────

    recipe_line_ids = fields.One2many(
        'bakery.recipe.line',
        'product_id',
        string='Recette — Ingrédients',
    )

    # ─── Statistiques ────────────────────────────────────────────────────────

    order_count = fields.Integer(
        string='Nb commandes',
        compute='_compute_order_count',
    )

    # ─── Computed ────────────────────────────────────────────────────────────

    @api.depends('recipe_line_ids.subtotal')
    def _compute_cost_price(self):
        for rec in self:
            rec.cost_price = sum(rec.recipe_line_ids.mapped('subtotal'))

    @api.depends('sale_price', 'cost_price')
    def _compute_margin(self):
        for rec in self:
            rec.margin = (
                ((rec.sale_price - rec.cost_price) / rec.sale_price) * 100
                if rec.sale_price > 0 else 0.0
            )

    def _compute_order_count(self):
        for rec in self:
            lines = self.env['bakery.order.line'].search(
                [('product_id', '=', rec.id)]
            )
            rec.order_count = len(lines.mapped('order_id'))

    # ─── Actions ─────────────────────────────────────────────────────────────

    def action_view_orders(self):
        lines = self.env['bakery.order.line'].search(
            [('product_id', '=', self.id)]
        )
        order_ids = lines.mapped('order_id').ids
        return {
            'name': f'Commandes — {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'bakery.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', order_ids)],
        }


class BakeryRecipeLine(models.Model):
    _name = 'bakery.recipe.line'
    _description = 'Ligne de Recette'

    product_id = fields.Many2one(
        'bakery.product',
        string='Produit',
        required=True,
        ondelete='cascade',
    )
    ingredient_id = fields.Many2one(
        'bakery.ingredient',
        string='Ingrédient',
        required=True,
    )
    quantity = fields.Float(
        string='Quantité',
        required=True,
        digits=(16, 3),
        default=1.0,
    )
    unit_of_measure = fields.Selection(
        related='ingredient_id.unit_of_measure',
        string='Unité',
        readonly=True,
    )
    subtotal = fields.Float(
        string='Coût (MAD)',
        compute='_compute_subtotal',
        store=True,
        digits=(16, 2),
    )

    @api.depends('quantity', 'ingredient_id.cost_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.ingredient_id.cost_price
