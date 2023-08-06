from openwebpos.extensions import db
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin


class Company(DateTimeMixin, db.Model, CRUDMixin):
    """Company model"""
    __tablename__ = "company"
    name = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=True, default='default.png')
    active_twilio = db.Column(db.Boolean, default=False)
    branches = db.relationship('Branch', backref='company', lazy='dynamic',
                               cascade="all, delete-orphan")

    @staticmethod
    def insert_default_company():
        """Insert default company"""
        company = Company(name='OpenWebPOS')
        company.save()

    def toggle_twilio(self):
        """Toggle twilio"""
        self.active_twilio = not self.active_twilio
        self.update()

    def twilio_active(self):
        """Check if twilio is active"""
        return self.active_twilio

    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)


class Branch(DateTimeMixin, db.Model, CRUDMixin):
    """Branch model"""
    __tablename__ = "branch"
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    fax = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    taxes = db.relationship('TaxRate', backref='branch', lazy='dynamic')
    usb_printers = db.relationship('USBPrinter', backref='branch',
                                   lazy='dynamic')
    network_printers = db.relationship('NetworkPrinter', backref='branch',
                                       lazy='dynamic')
    users = db.relationship('User', backref='branch', lazy='dynamic')

    @staticmethod
    def insert_default_branch():
        """Insert default branch"""
        company_location = Branch(company_id=1,
                                  name='Main Branch',
                                  address='1234 Main St',
                                  city='Fort Worth',
                                  state='TX',
                                  zip_code='76164',
                                  country='USA',
                                  phone='8171234567')
        company_location.save()

    def toggle(self):
        """Toggle active status."""
        if not self.last_branch():
            self.active = not self.active
            self.update()

    def last_branch(self):
        """Check if this is the last branch."""
        return Branch.query.count() == 1

    def __init__(self, **kwargs):
        super(Branch, self).__init__(**kwargs)


class USBPrinter(db.Model, DateTimeMixin, CRUDMixin):
    """USB Printer model"""
    __tablename__ = "usb_printers"
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'),
                          nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    idVendor = db.Column(db.String(255), nullable=False)
    idProduct = db.Column(db.String(255), nullable=False)
    timeout = db.Column(db.Integer, nullable=False, default=0)
    in_endpoint = db.Column(db.String(255), nullable=False)
    out_endpoint = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        self.update()

    def is_active(self):
        """Check if printer is active."""
        return self.active

    def __init__(self, **kwargs):
        super(USBPrinter, self).__init__(**kwargs)
        if self.timeout is None:
            self.timeout = 0


class NetworkPrinter(db.Model, DateTimeMixin, CRUDMixin):
    """Network Printer model"""
    __tablename__ = "network_printers"
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'),
                          nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    host = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=9100)
    timeout = db.Column(db.Integer, nullable=False, default=60)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        self.update()

    def is_active(self):
        """Check if printer is active."""
        return self.active

    def __init__(self, **kwargs):
        super(NetworkPrinter, self).__init__(**kwargs)


class TaxRate(DateTimeMixin, db.Model, CRUDMixin):
    """Tax rate model"""
    __tablename__ = "tax_rates"
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('branch.id'),
                          nullable=False)
    name = db.Column(db.String(255), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, **kwargs):
        super(TaxRate, self).__init__(**kwargs)
