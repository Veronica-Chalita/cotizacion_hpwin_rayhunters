# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    currency_rate = fields.Float(string='Quotation Currency Rate', compute='_get_currency_rate', store=False)
    multi_currency = fields.Boolean(string='Enable Multi Currency', default=False)
   
    @api.depends('date_order', 'company_id', 'currency_id')
    def _get_currency_rate(self):
        for order in self:
            order_currency = order.currency_id or order.company_id.currency_id
            order['currency_rate'] = self.env['res.currency']._get_conversion_rate(order_currency,order.company_id.currency_id,order.company_id, order.date_order)

    @api.model
    def _prepare_invoice(self):
        res = super(SaleOrder,self)._prepare_invoice()
        if self.multi_currency == False:
            res.update({'currency_id':self.currency_id})
        else:
            res.update({'currency_id':self.company_id.currency_id})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    unitprice_mxn = fields.Float('Unit Price MXN', compute='_compute_price_mxn')

    @api.depends('price_unit','order_id.currency_rate','order_id.multi_currency')
    def _compute_price_mxn(self):
        for order_line in self:
            if order_line.order_id.multi_currency == True:
                order_line['unitprice_mxn'] = order_line.price_unit * order_line.order_id.currency_rate
            else:
                order_line['unitprice_mxn'] = order_line.price_unit

    @api.model
    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'price_unit': self.unitprice_mxn})
        return res  
