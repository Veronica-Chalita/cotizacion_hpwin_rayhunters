from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    currency_rate = fields.Float(string='Quotation Currency Rate',compute='_get_currency_rate',store=False)
    multi_currency = fields.Boolean(string="Enable Multi Currency",default=False)
   
    @api.depends('date_order')
    def _get_currency_rate(self):
        currency_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
        currency_value = self.env['res.currency.rate'].search([('currency_id','=',currency_id),('name','=',self.date_order)]).rate
        for record in self:
            if currency_value:
                record.currency_rate = 1/currency_value
    
    # @api.model
    # def _prepare_invoice(self):
    #     res = super(SaleOrder,self)._prepare_invoice()
    #     company_currency = self.env.ref('base.main_company').currency_id
    #     res.update({'currency_id':company_currency})
    #     return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    unitprice_mxn = fields.Float("Unit Price MXN",compute='_compute_price_mxn')

    @api.depends('price_unit','order_id.state')
    def _compute_price_mxn(self):
        for line in self:
            if line.order_id.state in ['draft','sent','sale','cancel']:
                if line.order_id.multi_currency == True:
                    line.unitprice_mxn = line.price_unit * line.order_id.currency_rate
                else:
                    if line.order_id.currency_id.id == 2:
                        line.unitprice_mxn = line.price_unit
                    else:
                        line.unitprice_mxn = line.unitprice_mxn

    @api.model
    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'price_unit': self.unitprice_mxn})
        return res  
