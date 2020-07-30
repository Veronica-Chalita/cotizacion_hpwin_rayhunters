# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    currency_rate = fields.Float(string='Quotation Currency Rate', compute='_get_currency_rate', store=False)
    multi_currency = fields.Boolean(string='Enable Multi Currency', default=False)
    
    @api.depends('date_order', 'company_id', 'currency_id', 'company_id.currency_id')
    def _get_currency_rate(self):
        for order in self:
            order_currency = order.currency_id or order.company_id.currency_id
            order.currency_rate = self.env['res.currency']._get_conversion_rate(order_currency, order.company_id.currency_id, order.company_id, order.date_order)

    @api.model
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.multi_currency:
            res.update({'currency_id':self.company_id.currency_id})
        else:
            res.update({'currency_id':self.currency_id})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    unitprice_mxn = fields.Float(string='Unit Price MXN', compute='_compute_price_mxn')
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_amount_mxn', readonly=True, store=True)

    @api.depends('price_unit', 'order_id.currency_rate', 'order_id.multi_currency')
    def _compute_price_mxn(self):
        for order_line in self:
            if order_line.order_id.multi_currency:
                order_line.unitprice_mxn = order_line.price_unit * order_line.order_id.currency_rate
            else:
                order_line.unitprice_mxn = order_line.price_unit

    @api.depends('unitprice_mxn', 'product_uom_qty', 'order_id.multi_currency', 'price_unit', 'tax_id', 'discount')
    def _compute_amount_mxn(self):
        for line in self:
            if line.order_id.multi_currency:
                price = line.unitprice_mxn * (1 - (line.discount or 0.0) / 100.0)
            else:
                price = line.unitprice_mxn * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
    
    @api.onchange('product_id', 'price_unit', 'tax_id', 'discount', 'product_uom_qty')
    def _onchange_line_mxn(self):
        for line in self:
            if line.order_id.multi_currency:
                 line._compute_amount_mxn()
            return

    @api.model
    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'price_unit': self.unitprice_mxn})
        return res  