# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2011 Async Open Source
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

import gtk

from kiwi.python import Settable
from stoqlib.domain.account import Account
from stoqlib.gui.accounttree import AccountTree
from stoqlib.gui.editors.baseeditor import BaseEditor

class AccountEditor(BaseEditor):
    """ Account Editor """
    gladefile = "AccountEditor"
    proxy_widgets = ['description', 'code']
    size = (400, 300)
    model_type = Account

    def __init__(self, conn, model=None, parent_account=None):
        self.existing = model is not None
        self.parent_account = conn.get(parent_account)
        BaseEditor.__init__(self, conn, model)

    #
    # BaseEditor hooks
    #

    def create_model(self, conn):
        return Account(description="",
                       connection=conn)

    def _setup_widgets(self):
        self.parent_accounts = AccountTree(with_code=False)
        self.parent_accounts.set_headers_visible(False)
        self.table.attach(self.parent_accounts, 1, 2, 2, 3)
        model = self.model if not self.existing else None
        self.parent_accounts.insert_initial(self.conn, ignore=model)
        if self.parent_account:
            self.parent_accounts.select(self.parent_account)
        self.parent_accounts.show()

    def setup_proxies(self):
        self._setup_widgets()
        self.add_proxy(self.model, AccountEditor.proxy_widgets)

    def validate_confirm(self):
        if not self.model.description:
            return False
        account = self.parent_accounts.get_selected()
        if not account:
            return True
        return account.kind == 'account'

    def on_confirm(self):
        new_parent = self.parent_accounts.get_selected()
        if new_parent != self.model:
            self.model.parent = self.parent_accounts.get_selected()
        return self.model

    def on_description__activate(self, entry):
        self.confirm()

    def on_code__activate(self, entry):
        self.confirm()
