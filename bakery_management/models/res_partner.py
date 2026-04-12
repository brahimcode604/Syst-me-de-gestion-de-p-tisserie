# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ─── Champs Pâtisserie ───────────────────────────────────────────────────

    is_bakery_customer = fields.Boolean(
        string='Client Pâtisserie',
        default=False,
        help='Cochez si ce contact est un client de la pâtisserie.',
    )
    bakery_order_ids = fields.One2many(
        'bakery.order',
        'partner_id',
        string='Commandes Pâtisserie',
    )
    bakery_order_count = fields.Integer(
        string='Nb commandes',
        compute='_compute_bakery_stats',
        store=True,
    )
    bakery_total_spent = fields.Float(
        string='Total dépensé (MAD)',
        compute='_compute_bakery_stats',
        store=True,
        digits=(16, 2),
    )

    # ─── Computed ────────────────────────────────────────────────────────────

    @api.depends(
        'bakery_order_ids',
        'bakery_order_ids.amount_total',
        'bakery_order_ids.state',
    )
    def _compute_bakery_stats(self):
        for partner in self:
            orders = partner.bakery_order_ids.filtered(
                lambda o: o.state not in ('cancelled',)
            )
            partner.bakery_order_count = len(orders)
            partner.bakery_total_spent = sum(orders.mapped('amount_total'))

    # ─── Actions ─────────────────────────────────────────────────────────────

    def action_view_bakery_orders(self):
        return {
            'name': f'Commandes de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'bakery.order',
            'view_mode': 'list,kanban,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
