# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class BakeryOrder(models.Model):
    _name = 'bakery.order'
    _description = 'Commande Pâtisserie'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc'

    # ─── Identification ──────────────────────────────────────────────────────

    name = fields.Char(
        string='Référence',
        readonly=True,
        copy=False,
        default='/',
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        tracking=True,
    )

    # ─── Dates ───────────────────────────────────────────────────────────────

    date_order = fields.Datetime(
        string='Date de commande',
        default=fields.Datetime.now,
        required=True,
        tracking=True,
    )
    date_delivery = fields.Date(
        string='Date de livraison souhaitée',
        tracking=True,
    )

    # ─── Workflow ────────────────────────────────────────────────────────────

    state = fields.Selection([
        ('draft',      'Brouillon'),
        ('confirmed',  'Confirmée'),
        ('production', 'En production'),
        ('ready',      'Prête'),
        ('done',       'Livrée'),
        ('cancelled',  'Annulée'),
    ], string='État', default='draft', tracking=True, copy=False)

    # ─── Lignes ──────────────────────────────────────────────────────────────

    order_line_ids = fields.One2many(
        'bakery.order.line',
        'order_id',
        string='Lignes de commande',
        copy=True,
    )
    amount_total = fields.Float(
        string='Total (MAD)',
        compute='_compute_amount_total',
        store=True,
        digits=(16, 2),
        tracking=True,
    )
    notes = fields.Text(string='Notes / Instructions spéciales')
    active = fields.Boolean(string='Actif', default=True)

    # ─── Facturation (account.move) ──────────────────────────────────────────

    invoice_ids = fields.Many2many(
        'account.move',
        'bakery_order_invoice_rel',
        'order_id',
        'invoice_id',
        string='Factures',
        copy=False,
    )
    invoice_count = fields.Integer(
        string='Nb factures',
        compute='_compute_invoice_count',
    )
    invoice_status = fields.Selection([
        ('not_invoiced', 'Non facturée'),
        ('partial',      'Partiellement facturée'),
        ('invoiced',     'Facturée & Payée'),
    ], string='Statut facturation', compute='_compute_invoice_status', store=True)

    # ─── Computed ────────────────────────────────────────────────────────────

    @api.depends('order_line_ids.subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('subtotal'))

    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    @api.depends('invoice_ids', 'invoice_ids.state', 'invoice_ids.payment_state')
    def _compute_invoice_status(self):
        for order in self:
            invoices = order.invoice_ids.filtered(lambda i: i.state != 'cancel')
            if not invoices:
                order.invoice_status = 'not_invoiced'
            elif all(
                inv.payment_state in ('paid', 'in_payment') for inv in invoices
            ):
                order.invoice_status = 'invoiced'
            else:
                order.invoice_status = 'partial'

    # ─── Workflow Actions ─────────────────────────────────────────────────────

    def action_confirm(self):
        for order in self:
            if not order.order_line_ids:
                raise ValidationError(
                    "Impossible de confirmer une commande sans produits."
                )
            if order.name == '/':
                order.name = (
                    self.env['ir.sequence'].next_by_code('bakery.order') or '/'
                )
            order.state = 'confirmed'
            order.message_post(body=_("✅ Commande confirmée."))

    def action_start_production(self):
        for order in self:
            order.state = 'production'
            order.message_post(body=_("🏭 Mise en production démarrée."))

    def action_ready(self):
        for order in self:
            order.state = 'ready'
            order.message_post(body=_("✨ Commande prête pour la livraison."))

    def action_done(self):
        for order in self:
            order.state = 'done'
            order.message_post(body=_("🚀 Commande livrée au client."))

    def action_cancel(self):
        for order in self:
            if order.state == 'done':
                raise UserError(
                    "Impossible d'annuler une commande déjà livrée."
                )
            order.state = 'cancelled'
            order.message_post(body=_("❌ Commande annulée."))

    def action_draft(self):
        for order in self:
            if order.state == 'cancelled':
                order.state = 'draft'
                order.message_post(body=_("↩ Commande remise en brouillon."))

    # ─── Facturation ─────────────────────────────────────────────────────────

    def action_create_invoice(self):
        """Crée une facture client (account.move) liée à cette commande."""
        self.ensure_one()
        if not self.order_line_ids:
            raise UserError(
                "Impossible de facturer une commande sans lignes de produits."
            )

        invoice_lines = []
        for line in self.order_line_ids:
            invoice_lines.append((0, 0, {
                'name': line.product_id.name,
                'quantity': line.quantity,
                'price_unit': line.unit_price,
            }))

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
            'narration': f"Facture pour la commande {self.name}",
            'ref': self.name,
        }

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_ids = [(4, invoice.id)]
        self.message_post(
            body=_(f"💰 Facture <b>{invoice.name or 'Brouillon'}</b> créée.")
        )

        return {
            'name': _('Facture'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_invoices(self):
        """Ouvre toutes les factures liées à cette commande."""
        self.ensure_one()
        return {
            'name': _(f'Factures — {self.name}'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
        }


# ─── Ligne de Commande ───────────────────────────────────────────────────────

class BakeryOrderLine(models.Model):
    _name = 'bakery.order.line'
    _description = 'Ligne de Commande Pâtisserie'

    order_id = fields.Many2one(
        'bakery.order',
        string='Commande',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'bakery.product',
        string='Produit',
        required=True,
    )
    quantity = fields.Float(
        string='Quantité',
        required=True,
        default=1.0,
        digits=(16, 2),
    )
    unit_price = fields.Float(
        string='Prix unitaire (MAD)',
        digits=(16, 2),
    )
    subtotal = fields.Float(
        string='Sous-total (MAD)',
        compute='_compute_subtotal',
        store=True,
        digits=(16, 2),
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.sale_price

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price
