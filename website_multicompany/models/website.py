##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import logging
from odoo import models, tools
from odoo.http import request

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _frontend_pre_dispatch(cls):
        super()._frontend_pre_dispatch()
        user = request.env.user
        website = request.env['website'].get_current_website()

        if user.id != website._get_cached('user_id'):
            users_company_ids = website._get_cached_companies()
            request.update_context(
                allowed_company_ids=users_company_ids,
            )
        request.website = website.with_context(request.context)

class Website(models.Model):

    _inherit = 'website'
        
    @tools.ormcache('self.env.uid')
    def _get_cached_companies(self):
        return self.env.user.company_ids.ids

