# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2007 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Outc., or visit: http://www.gnu.org/.
##
## Author(s):   Johan Dahlin          <jdahlin@async.com.br>
##
##
""" Dialog for adding simple payments """


import datetime

from kiwi.datatypes import currency, ValidationError

from stoqlib.domain.interfaces import IInPayment, IOutPayment
from stoqlib.domain.payment.category import PaymentCategory
from stoqlib.domain.payment.group import PaymentGroup
from stoqlib.domain.payment.payment import Payment
from stoqlib.domain.person import PersonAdaptToClient, PersonAdaptToSupplier
from stoqlib.gui.editors.baseeditor import BaseEditor
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext


class BasePaymentAddition(BaseEditor):
    gladefile = "BasePaymentAddition"
    model_type = Payment
    title = _(u"Payment")
    proxy_widgets = ['value',
                     'description',
                     'due_date',
                     'category']

    def __init__(self, conn, model=None):
        """ A base class for additional payments

        @param conn: a database connection
        @param model: a L{stoqlib.domain.payment.payment.Payment} object or None

        """
        BaseEditor.__init__(self, conn, model)

    #
    # BaseEditor hooks
    #

    def create_model(self, trans):
        group = PaymentGroup(connection=trans)
        return Payment(open_date=datetime.date.today(),
                       description='',
                       value=currency(0),
                       base_value=currency(0),
                       due_date=None,
                       method=None,
                       group=group,
                       till=None,
                       category=None,
                       destination=None,
                       connection=trans)

    def on_due_date__activate(self, date):
        self.confirm()

    def setup_proxies(self):
        categories = PaymentCategory.select(
            connection=self.trans).orderBy('name')
        if categories:
            self.category.prefill([(c.name, c) for c in categories])
        else:
            self.category.set_sensitive(False)

        self.populate_person()
        self.add_proxy(self.model, BasePaymentAddition.proxy_widgets)

    def validate_confirm(self):
        # FIXME: the kiwi view should export it's state and it shoul
        #        be used by default
        return bool(self.model.description and self.model.due_date and
                    self.model.value)

    def on_confirm(self):
        self.model.set_pending()
        self.model.base_value = self.model.value
        person = self.person.get_selected()
        print person
        if person is not None:
            setattr(self.model.group,
                    self.person_attribute,
                    person.person)
        return self.model

    #
    # Kiwi Callbacks
    #

    def on_value__validate(self, widget, newvalue):
        if newvalue is None or newvalue <= 0:
            return ValidationError(_(u"The value must be greater than zero."))


class InPaymentAdditionDialog(BasePaymentAddition):
    person_attribute = 'payer'
    def __init__(self, conn, model=None):
        """ This dialog is responsible to create additional payments with
        IInPayment facet.

        @param conn: a database connection
        @param model: a L{stoqlib.domain.payment.payment.Payment} object
                      or None
        """
        BasePaymentAddition.__init__(self, conn, model)
        self.model.addFacet(IInPayment, connection=self.conn)
        self.person_label.set_label(_("Payer:"))

    def populate_person(self):
        clients = PersonAdaptToClient.get_active_clients(self.trans)
        if clients:
            self.person.prefill(sorted([(c.person.name, c)
                                        for c in clients]))
        else:
            self.person.set_sensitive(False)


class OutPaymentAdditionDialog(BasePaymentAddition):
    person_attribute = 'recipient'
    def __init__(self, conn, model=None):
        """ This dialog is responsible to create additional payments with
        IOutPayment facet.

        @param conn: a database connection
        @param model: a L{stoqlib.domain.payment.payment.Payment} object
                      or None
        """
        BasePaymentAddition.__init__(self, conn, model)
        self.model.addFacet(IOutPayment, connection=self.conn)
        self.person_label.set_label(_("Recipient:"))

    def populate_person(self):
        suppliers = PersonAdaptToSupplier.get_active_suppliers(self.trans)
        if suppliers:
            self.person.prefill(sorted([(s.person.name, s)
                                        for s in suppliers]))
        else:
            self.person.set_sensitive(False)
