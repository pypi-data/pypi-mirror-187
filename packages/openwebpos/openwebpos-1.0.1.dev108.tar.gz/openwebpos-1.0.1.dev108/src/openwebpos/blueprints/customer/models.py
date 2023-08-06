from openwebpos.extensions import db
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin


class Customer(db.Model, DateTimeMixin, CRUDMixin):
    """Customer Model"""
    __tablename__ = 'customers'
    phone = db.Column(db.String(20), nullable=True, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    has_account = db.Column(db.Boolean, nullable=False, default=False)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def format_phone(self):
        """Format phone number"""
        return '({}) {}-{}'.format(self.phone[:3], self.phone[3:6],
                                   self.phone[6:])

    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)


class CustomerProfile(db.Model, DateTimeMixin, CRUDMixin):
    """Customer Profile Model"""
    __tablename__ = 'customer_profiles'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
                            nullable=False)
    picture = db.Column(db.String(255), nullable=True, default='default.png')
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zip_code = db.Column(db.String(120))
    dob = db.Column(db.String(120))

    def __init__(self, **kwargs):
        super(CustomerProfile, self).__init__(**kwargs)
