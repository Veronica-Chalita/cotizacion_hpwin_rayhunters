from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    currency_sale =fields.Char(string='Currency',related="company_currency_id.name")

