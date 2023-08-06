from openwebpos.extensions import db
from openwebpos.utils import gen_order_number
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin


class PaymentMethod(db.Model, DateTimeMixin, CRUDMixin):
    """Payment Method Model"""
    __tablename__ = 'payment_methods'
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    payments = db.relationship('Payment', backref='payment_method',
                               lazy='dynamic')

    @staticmethod
    def insert_default_payment_methods():
        """
        Insert default payment methods into the database.
        """
        payment_methods = [
            {'name': 'Cash', 'description': 'Cash payment'},
            {'name': 'Credit Card', 'description': 'Credit card payment'},
            {'name': 'Coupon', 'description': 'Coupon payment'},
            {'name': 'Gift Card', 'description': 'Gift card payment'},
        ]

        for payment_method in payment_methods:
            payment_method = PaymentMethod(**payment_method)
            payment_method.save()

    def toggle(self):
        """ Toggle active status """
        self.active = not self.active
        self.update()

    def __init__(self, **kwargs):
        super(PaymentMethod, self).__init__(**kwargs)


class Payment(db.Model, DateTimeMixin, CRUDMixin):
    """Payment Model"""
    __tablename__ = 'payments'
    payment_method_id = db.Column(db.Integer,
                                  db.ForeignKey('payment_methods.id'),
                                  nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    change = db.Column(db.Integer, nullable=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'),
                           nullable=False)

    def update_invoice_due(self):
        """Update the invoice due amount."""
        invoice = Invoice.query.get(self.invoice_id)
        invoice.due = invoice.due - self.amount
        invoice.update_payment_status()
        invoice.update()

    def __init__(self, **kwargs):
        super(Payment, self).__init__(**kwargs)
        invoice_total = Invoice.query.get(self.invoice_id).total
        invoice_due = Invoice.query.filter_by(id=self.invoice_id).first().due

        invoice_due_dollars = invoice_due / 100

        if invoice_due_dollars < invoice_total:  # invoice is overpaid
            change = invoice_due_dollars * -1
            self.change = change * 100
            print("change: ", change)

        print("invoice_due_dollars: ", invoice_due_dollars)

        # change = self.amount - invoice_total
        # if change > 0:
        #     self.change = change
        # else:
        #     self.change = 0.0


class Invoice(db.Model, DateTimeMixin, CRUDMixin):
    """Invoice Model"""
    __tablename__ = 'invoices'

    receipt_number = db.Column(db.String(100), nullable=False, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    tax = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    due = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(100), nullable=False, default='unpaid')
    payments = db.relationship('Payment', backref='invoice', lazy='dynamic')

    def update_due(self):
        """Update the due amount of the invoice"""
        self.due = self.total - sum([p.amount for p in self.payments])
        self.update_payment_status()

    def update_payment_status(self):
        """Update the payment status of the invoice"""
        if self.due <= 0:
            self.payment_status = 'paid'
        elif self.due < self.total:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'

    def __init__(self, **kwargs):
        super(Invoice, self).__init__(**kwargs)
        self.receipt_number = gen_order_number()
