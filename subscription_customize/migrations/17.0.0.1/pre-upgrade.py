import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    _logger.info('creating column from previous version')
    util.create_column(cr, 'sale_order', 'parent_id', 'integer')
    util.create_column(cr, 'sale_order', 'child_recurring_total', 'double precision')
    util.create_column(cr, 'sale_order', 'amount_at_start', 'double precision')
    _logger.info('creating column from previous version')

    cr.execute('''
        UPDATE sale_order
            SET parent_id = sale_subscription.parent_id,
                child_recurring_total = sale_subscription.child_recurring_total,
                amount_at_start = sale_subscription.amount_at_start
            FROM sale_subscription
            WHERE sale_subscription.new_sale_order_id = sale_order.id
    ''')
    _logger.info('finished')
