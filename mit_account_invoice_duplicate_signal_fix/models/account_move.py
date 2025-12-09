# -*- coding: utf-8 -*-
# Copyright 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _creation_subtype(self):
        """
        Override to prevent duplicate invoice creation signals when processing
        nested returns (return of a return Transfer Requests).

        When processing a return of a return TR, the invoice creation logic
        can be triggered multiple times, causing duplicate mt_invoice_created
        signals. This method checks if the invoice already has a message with
        the mt_invoice_created subtype before returning it, preventing duplicate
        signals.

        Returns:
            mail.message.subtype or None: The creation subtype if it should be
            posted, or None to prevent duplicate signals.
        """
        # Call parent method first to get the default behavior
        result = super()._creation_subtype()
        
        # Only apply the fix for customer invoices and receipts
        if self.move_type in ('out_invoice', 'out_receipt'):
            invoice_created_subtype = self.env.ref('account.mt_invoice_created')
            
            # If result is the invoice created subtype, check for duplicates
            if result == invoice_created_subtype:
                # Only check for duplicates if the invoice already exists in the database
                # This prevents duplicate signals when _creation_subtype is called
                # multiple times for the same invoice (e.g., during nested returns)
                if self.id:
                    # Invoice exists, check if it already has the creation subtype message
                    existing_message = self.message_ids.filtered(
                        lambda m: m.subtype_id == invoice_created_subtype
                    )
                    if existing_message:
                        # Invoice already has creation signal, return None to prevent duplicate
                        return None
            
            return invoice_created_subtype
        
        return result
