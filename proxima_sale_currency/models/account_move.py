from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    currency_sale =fields.Char(string='Currency type',related="move_id.currency_id.name")

