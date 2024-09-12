# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import ValidationError


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    parent_id = fields.Many2one('sale.subscription', string="Parent subscription")
    child_ids = fields.One2many('sale.subscription', 'parent_id', string="Child subscriptions")
    child_recurring_total = fields.Monetary('Total recurring amount from child', compute='_compute_child_amount', store=True, readonly=True)
    amount_at_start = fields.Monetary('Amount at start up')

    def start_subscription(self):
        self.ensure_one()
        res = super(SaleSubscription, self).start_subscription()
        self.amount_at_start = self.recurring_total
        return res

    @api.depends('child_ids.recurring_total')
    def _compute_child_amount(self):
        for rec in self:
            rec.child_recurring_total = sum(rec.child_ids.mapped('recurring_total'))
