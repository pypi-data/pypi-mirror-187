from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, \
    IntegerField
from wtforms.validators import DataRequired, ValidationError, IPAddress, URL, \
    Email, Length

from openwebpos.blueprints.admin.models import Branch


class CompanyForm(FlaskForm):
    """
    Form for admin to add or edit a company

    Extends:
        FlaskForm

    Variables:
        name {StringField} -- Name of the company
        logo {FileField} -- Logo of the company
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit a company

    Example:
        >>> form = CompanyForm()
    """
    name = StringField('Company Name', validators=[DataRequired()])
    logo = FileField('Company Logo')
    submit = SubmitField('Save')


class CompanyBranchForm(FlaskForm):
    """
    Form for admin to add or edit a company branch

    Extends:
        FlaskForm

    Variables:
        name {StringField} -- Name of the company branch
        address {StringField} -- Address of the company branch
        city {StringField} -- City of the company branch
        state {StringField} -- State of the company branch
        zip_code {StringField} -- Zip code of the company branch
        country {StringField} -- Country of the company branch
        phone {StringField} -- Phone number of the company branch
        fax {StringField} -- Fax number of the company branch
        email {StringField} -- Email of the company branch
        website {StringField} -- Website of the company branch
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit a company branch

    Example:
        >>> form = CompanyBranchForm()
    """
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = IntegerField('Zip Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    fax = StringField('Fax')
    email = StringField('Email', validators=[Email()])
    website = StringField('Website', validators=[URL()])
    submit = SubmitField('Save')

    # def validate_name(self, name):
    #     company = Branch.query.filter_by(name=name.data).first()
    #     if company is not None:
    #         raise ValidationError('Please use a different company name.')


class PrinterForm(FlaskForm):
    """
    Form for admin to add or edit a printer

    Extends:
        FlaskForm

    Variables:
        branch {SelectField} -- Branch of the printer
        url {StringField} -- URL of the printer
        name {StringField} -- Name of the printer
        ip_address {StringField} -- IP address of the printer
        port {StringField} -- Port of the printer
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit a printer

    Example:
        >>> form = PrinterForm()
    """
    branch = SelectField('Branch', coerce=int, validators=[DataRequired()])
    url = StringField('Webhook URL')
    name = StringField('Name', validators=[DataRequired()])
    ip_address = StringField('IP Address',
                             validators=[DataRequired(), IPAddress()])
    port = IntegerField('Port', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_name(self, name):
        """Validate name."""
        printer = Branch.query.filter_by(name=name.data).first()
        if printer is not None:
            raise ValidationError('Please use a different printer name.')

    def set_choices(self):
        """Set choices for branch."""
        self.branch.choices = [(branch.id, branch.name)
                               for branch in Branch.query.all()]


class BranchDefaultPrinterForm(FlaskForm):
    """
    Form for admin to set default printer for a branch

    Extends:
        FlaskForm

    Variables:
        branch {SelectField} -- Branch of the printer
        printer {SelectField} -- Printer to set as default
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to set default printer for a branch

    Example:
        >>> form = BranchDefaultPrinterForm()
    """
    branch = SelectField('Branch', coerce=int, validators=[DataRequired()])
    printer = SelectField('Printer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def set_choices(self):
        """Set choices for branch and printer."""
        self.branch.choices = [(branch.id, branch.name)
                               for branch in Branch.query.all()]
        self.printer.choices = [(printer.id, printer.name)
                                for printer in Branch.query.all()]


class USBPrinterForm(FlaskForm):
    """
    Form for admin to add or edit a USB printer

    Extends:
        FlaskForm

    Variables:
        branch_id {SelectField} -- Branch of the printer
        name {StringField} -- Name of the printer
        idVendor {StringField} -- idVendor of the printer
        idProduct {StringField} -- idProduct of the printer
        timeout {IntegerField} -- Timeout of the printer
        in_ep {StringField} -- in_ep of the printer
        out_ep {StringField} -- out_ep of the printer
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit a USB printer

    Example:
        >>> form = USBPrinterForm()
    """
    branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    idVendor = StringField('idVendor', validators=[DataRequired()])
    idProduct = StringField('idProduct', validators=[DataRequired()])
    timeout = IntegerField('Timeout', default=0)
    in_endpoint = StringField('In Endpoint')
    out_endpoint = StringField('Out Endpoint')
    submit = SubmitField('Save')

    def validate_name(self, name):
        """Validate name."""
        printer = Branch.query.filter_by(name=name.data).first()
        if printer is not None:
            raise ValidationError('Please use a different printer name.')

    def set_choices(self):
        """Set choices for branch."""
        self.branch_id.choices = [(branch.id, branch.name) for branch in
                                  Branch.query.all()]


class NetworkPrinterForm(FlaskForm):
    """
    Form for admin to add or edit a network printer

    Extends:
        FlaskForm

    Variables:
        branch_id {SelectField} -- Branch of the printer
        name {StringField} -- Name of the printer
        ip_address {StringField} -- IP address of the printer
        port {StringField} -- Port of the printer
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit a network printer

    Example:
        >>> form = NetworkPrinterForm()
    """
    branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    host = StringField('IP Address', validators=[DataRequired(), IPAddress()])
    port = IntegerField('Port', validators=[DataRequired()], default=9100)
    timeout = IntegerField('Timeout', default=60)
    submit = SubmitField('Save')

    def validate_name(self, name):
        """Validate name."""
        printer = Branch.query.filter_by(name=name.data).first()
        if printer is not None:
            raise ValidationError('Please use a different printer name.')

    def set_choices(self):
        """Set choices for branch."""
        self.branch_id.choices = [(branch.id, branch.name) for branch in
                                  Branch.query.all()]


class TwilioForm(FlaskForm):
    """
    Form for admin to add or edit Twilio credentials

    Extends:
        FlaskForm

    Variables:
        account_sid {StringField} -- Account SID
        auth_token {StringField} -- Auth token
        phone_number {StringField} -- Phone number
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit Twilio credentials

    Example:
        >>> form = TwilioForm()
    """
    pm = "Phone number must be in the format +1XXXXXXXXXX"
    account_sid = StringField('Account SID', validators=[DataRequired()])
    auth_token = StringField('Auth Token', validators=[DataRequired()])
    phone_number = StringField('Phone Number',
                               validators=[DataRequired(),
                                           Length(min=12, max=15, message=pm)])
    submit = SubmitField('Save')
