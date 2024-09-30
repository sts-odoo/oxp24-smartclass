from odoo import api, fields, models

TEETH = [
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('21', '21'),
            ('22', '22'),
            ('23', '23'),
            ('24', '24'),
            ('25', '25'),
            ('26', '26'),
            ('27', '27'),
            ('28', '28'),
            ('31', '31'),
            ('32', '32'),
            ('33', '33'),
            ('34', '34'),
            ('35', '35'),
            ('36', '36'),
            ('37', '37'),
            ('38', '38'),
            ('41', '41'),
            ('42', '42'),
            ('43', '43'),
            ('44', '44'),
            ('45', '45'),
            ('46', '46'),
            ('47', '47'),
            ('48', '48'),
    ]
POSITION = [
        ('outside', 'Outside'),
        ('top', 'Top'),
        ('inside', 'Inside'),
    ]


class Patient(models.Model):
    _description = "Patient"
    _inherit = "res.partner"

    intervention_ids = fields.One2many('sale.order.line', 'partner_id', domain=[('product_id.type', '=', 'dental')])
    is_patient = fields.Boolean('Is Patient', compute='_compute_is_patient', store=True, readonly=False)

    @api.depends('intervention_ids')
    def _compute_is_patient(self):
        for partner in self:
            partner.is_patient = len(partner.intervention_ids) > 0


class Intervention(models.Model):
    _description = "Intervention"
    _inherit = "sale.order.line"

    partner_id = fields.Many2one(related='order_id.partner_id', string='Patient')
    dental_tooth = fields.Selection(TEETH)
    dental_position = fields.Selection(POSITION)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[
        ('dental', 'Dental Care'),
    ], ondelete={'dental': 'set service'})
    dental_care_type = fields.Selection([
        ('part', 'Part of the Tooth'),
        ('tooth', 'Whole Tooth'),
        ('mouth', 'Mouth'),
    ])

    @api.onchange('type')
    def _onchange_type_event_booth(self):
        if self.type == 'dental':
            self.invoice_policy = 'order'
