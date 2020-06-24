from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    currency_rate = fields.Float(string='Quotation Currency Rate',compute='_get_currency_rate',store=False)
    multi_currency = fields.Boolean(string="Enable Multi Currency",default=False)
   
    @api.depends('date_order','company_id','currency_id')
    def _get_currency_rate(self):
        currency_usd = self.env.ref('base.USD')
        for order in self:
            order_currency = order.currency_id or order.company_id.currency_id
            order['currency_rate'] = self.env['res.currency']._get_conversion_rate(currency_usd,order_currency,order.company_id, order.date_order)
    
    @api.model
    def _prepare_invoice(self):
        res = super(SaleOrder,self)._prepare_invoice()
        company_currency = self.env.ref('base.main_company').currency_id
        if self.multi_currency == False:
            res.update({'currency_id':self.currency_id})
        else:
            res.update({'currency_id':company_currency})
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    unitprice_mxn = fields.Float("Unit Price MXN",compute='_compute_price_mxn')

    @api.depends('price_unit','order_id.state','order_id.currency_rate','order_id.multi_currency')
    def _compute_price_mxn(self):
        for order_line in self:
            if order_line.order_id.state in ['draft','sent','sale','cancel']:
                if order_line.order_id.multi_currency == True:
                    order_line['unitprice_mxn'] = order_line.price_unit * order_line.order_id.currency_rate
                else:
                    order_line['unitprice_mxn'] = order_line.price_unit

    @api.model
    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'price_unit': self.unitprice_mxn})
        return res  
