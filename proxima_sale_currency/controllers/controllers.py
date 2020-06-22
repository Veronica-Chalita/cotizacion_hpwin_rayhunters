# -*- coding: utf-8 -*-
# from odoo import http


# class ProximaSaleCurrency(http.Controller):
#     @http.route('/proxima_sale_currency/proxima_sale_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proxima_sale_currency/proxima_sale_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('proxima_sale_currency.listing', {
#             'root': '/proxima_sale_currency/proxima_sale_currency',
#             'objects': http.request.env['proxima_sale_currency.proxima_sale_currency'].search([]),
#         })

#     @http.route('/proxima_sale_currency/proxima_sale_currency/objects/<model("proxima_sale_currency.proxima_sale_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proxima_sale_currency.object', {
#             'object': obj
#         })
