# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2012 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

import unittest

from stoqlib.domain.account import Account
from stoqlib.gui.editors.accounteditor import AccountEditor
from stoqlib.gui.uitestutils import GUITest


class TestAccountEditor(GUITest):
    def testCreate(self):
        editor = AccountEditor(self.trans)

        # Model
        self.assertTrue(isinstance(editor.model, Account))

        # FIXME: In the long run this should be moved into the domain,
        #        Like Domain.create_empty() or so
        self.assertEquals(editor.model.account_type, Account.TYPE_CASH)
        self.assertEquals(editor.model.description, '')

        self.check_editor(editor, 'editor-account-create')

        editor.description.update('Updated description')

        self.check_editor(editor, 'editor-account-create-can-confirm')

    def testShow(self):
        account = self.create_account()
        editor = AccountEditor(self.trans, account)

        self.check_editor(editor, 'editor-account-show')


if __name__ == '__main__':
    from stoqlib.api import api
    c = api.prepare_test()
    unittest.main()
