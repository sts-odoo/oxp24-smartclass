# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.base.tests.common import TransactionCase


class TestSubscriptionCustom(TransactionCase):

    def test_subscription_custom(self):
        self.parent_subscription = self.env['sale.subscription'].create({
            'partner_id': self.env.ref('base.partner_demo_portal').id,
            'template_id': self.env.ref('sale_subscription.monthly_subscription').id,
            'recurring_invoice_line_ids': [(0, False, {
                'product_id': self.env.ref('sale_subscription.product_office_cleaning').id,
                'name': self.env.ref('sale_subscription.product_office_cleaning').name,
                'quantity': 2,
                'uom_id': self.env.ref('uom.product_uom_categ_unit').id,
                'price_unit': 55,
            })],
            })

        self.assertEqual(self.parent_subscription.child_recurring_total, 0.00)
        self.assertEqual(self.parent_subscription.amount_at_start, 0.00)

        self.child_subscription = self.env['sale.subscription'].create({
            'partner_id': self.env.ref('base.partner_demo_portal').id,
            'parent_id': self.parent_subscription.id,
            'template_id': self.env.ref('sale_subscription.monthly_subscription').id,
            'recurring_invoice_line_ids': [(0, False, {
                'product_id': self.env.ref('sale_subscription.product_office_cleaning').id,
                'name': self.env.ref('sale_subscription.product_office_cleaning').name,
                'quantity': 2,
                'uom_id': self.env.ref('uom.product_uom_categ_unit').id,
                'price_unit': 33,
            })],
            })

        self.parent_subscription.start_subscription()
        self.child_subscription.start_subscription()
        self.assertEqual(self.parent_subscription.amount_at_start, 110.0)
        self.assertEqual(self.child_subscription.amount_at_start, 66.0)
