# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.base.tests.common import TransactionCase


class TestSubscriptionCustom(TransactionCase):

    def test_subscription_custom(self):
        self.parent_subscription = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.partner_demo_portal').id,
            'plan_id': self.env.ref('sale_subscription.subscription_plan_month').id,
            'order_line': [(0, False, {
                'product_id': self.env.ref('sale_subscription.product_office_cleaning').id,
                'name': self.env.ref('sale_subscription.product_office_cleaning').name,
                'product_uom_qty': 2,
                'product_uom': self.env.ref('uom.product_uom_categ_unit').id,
                'price_unit': 55,
            })],
            })

        self.assertEqual(self.parent_subscription.child_recurring_total, 0.00)
        self.assertEqual(self.parent_subscription.amount_at_start, 0.00)

        self.child_subscription = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.partner_demo_portal').id,
            'parent_id': self.parent_subscription.id,
            'plan_id': self.env.ref('sale_subscription.subscription_plan_month').id,
            'order_line': [(0, False, {
                'product_id': self.env.ref('sale_subscription.product_office_cleaning').id,
                'name': self.env.ref('sale_subscription.product_office_cleaning').name,
                'product_uom_qty': 2,
                'product_uom': self.env.ref('uom.product_uom_categ_unit').id,
                'price_unit': 33,
            })],
            })

        self.parent_subscription.action_confirm()
        self.child_subscription.action_confirm()
        self.assertEqual(self.parent_subscription.amount_at_start, 110.0)
        self.assertEqual(self.child_subscription.amount_at_start, 66.0)
