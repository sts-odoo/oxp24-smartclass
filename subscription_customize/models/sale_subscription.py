# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    parent_id = fields.Many2one('sale.order', string="Parent subscription", domain=[('is_subscription', '=', True)])
    child_ids = fields.One2many('sale.order', 'parent_id', string="Child subscriptions")
    child_recurring_total = fields.Monetary('Total recurring amount from child', compute='_compute_child_amount', store=True, readonly=True)
    amount_at_start = fields.Monetary('Amount at start up')

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
            if rec.is_subscription:
                rec.amount_at_start = rec.recurring_total
        return res

    @api.depends('child_ids.recurring_total')
    def _compute_child_amount(self):
        for rec in self:
            rec.child_recurring_total = sum(rec.child_ids.mapped('recurring_total'))
