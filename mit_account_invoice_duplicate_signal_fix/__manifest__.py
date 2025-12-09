# -*- coding: utf-8 -*-
# Copyright 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MIT Account Invoice Duplicate Signal Fix',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Prevent duplicate invoice creation signals for nested returns',
    'description': """
MIT Account Invoice Duplicate Signal Fix
=========================================

This module fixes an issue where processing a "return of a return" Transfer
Request creates duplicate invoicing signals.

Problem:
--------
When processing nested returns (a return of a return TR), the invoice creation
logic can be triggered multiple times, causing duplicate mt_invoice_created
signals to be posted for the same invoice.

Solution:
---------
This module overrides the _creation_subtype method in account.move to check
if an invoice already has a message with the mt_invoice_created subtype before
returning it. If a duplicate is detected, it returns None to prevent the
duplicate signal from being posted.

Technical Details:
------------------
- Inherits from account.move model
- Overrides _creation_subtype method
- Checks for existing messages with mt_invoice_created subtype
- Prevents duplicate signals while maintaining normal invoice creation behavior
    """,
    'author': 'Open Source Integrators',
    'website': 'https://www.opensourceintegrators.com',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
