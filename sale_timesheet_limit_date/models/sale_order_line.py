# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models
from odoo.osv import expression

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_compute_delivered_quantity_domain(self):
        _logger.info("TS PATH | sale_timesheet_limit_date | sale.order.line | _timesheet_compute_delivered_quantity_domain")
        domain = super()._timesheet_compute_delivered_quantity_domain()
        order = self.mapped('order_id')
        if order.timesheet_limit_date:
            domain = expression.AND([
                domain,
                [('date', '<=', order.timesheet_limit_date)]]
            )
        return domain

    @api.depends('order_id.timesheet_limit_date')
    @api.multi
    def _compute_qty_delivered(self):
        """Group lines by sale order to allow application of 'per order'
         domain above"""
        _logger.info("TS PATH | sale_timesheet_limit_date | sale.order.line | _compute_qty_delivered")
        orders = self.mapped('order_id')
        lines_groups = [
            self.filtered(lambda sol: sol.order_id.id == o.id) for o in orders
        ]
        for item in lines_groups:
            super(SaleOrderLine, item)._compute_qty_delivered()
