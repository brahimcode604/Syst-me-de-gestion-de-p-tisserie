# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BakeryOrder(models.Model):
    _name = 'bakery.order'
    _description = 'Commande Patisserie'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc'

    name = fields.Char(string='Reference', readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    date_order = fields.Datetime(string='Date de commande', default=fields.Datetime.now)
    date_delivery = fields.Date(string='Date de livraison souhaitee')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmee'),
        ('done', 'Livree'),
        ('cancelled', 'Annulee'),
    ], string='Etat', default='draft', tracking=True)
    order_line_ids = fields.One2many('bakery.order.line', 'order_id', string='Lignes')
    amount_total = fields.Float(string='Total (MAD)', compute='_compute_amount_total', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('order_line_ids.subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('subtotal'))


class BakeryOrderLine(models.Model):
    _name = 'bakery.order.line'
    _description = 'Ligne de Commande Patisserie'

    order_id = fields.Many2one('bakery.order', required=True, ondelete='cascade')
    product_id = fields.Many2one('bakery.product', string='Produit', required=True)
    quantity = fields.Float(string='Quantite', default=1.0)
    unit_price = fields.Float(string='Prix unitaire (MAD)')
    subtotal = fields.Float(string='Sous-total (MAD)', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price