from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from openwebpos.blueprints.billing.models import PaymentMethod
from openwebpos.blueprints.user.decorators import role_require, \
    permission_require
from .company_views import bp as company_bp
from .menu_views import bp as menu_bp
from .order_views import bp as order_bp
from .printer_views import bp as printer_bp
from .user_views import bp as user_bp
from ..models import Company

admin = Blueprint('admin', __name__, template_folder='../templates',
                  url_prefix='/admin')

admin.register_blueprint(printer_bp)
admin.register_blueprint(menu_bp)
admin.register_blueprint(order_bp)
admin.register_blueprint(user_bp)
admin.register_blueprint(company_bp)


@admin.before_request
@login_required
@role_require('Administrator')
@permission_require('view_admin')
def before_request():
    """
    Protects all the admin endpoints.
    """
    pass


@admin.route('/')
def index():
    """
    Admin dashboard.
    """
    _company = Company.query.first()
    return render_template('admin/index.html', title='Admin', company=_company)


@admin.route('/billing')
def billing():
    """
    Displays the billing page.
    """
    return render_template('admin/billing.html', title='Billing')


@admin.route('/billing/payment_methods')
def payment_methods():
    """
    Displays all the payment methods.
    """
    _payment_methods = PaymentMethod.query.all()
    return render_template('admin/payment_methods.html',
                           title='Payment Methods',
                           payment_methods=_payment_methods)


@admin.get('/billing/payment_method/toggle/<int:payment_method_id>')
def toggle_payment_method(payment_method_id):
    """
    Toggles the payment method. (Enables/Disables)

    Args:
        payment_method_id: The payment method id.

    Returns:
        The payment methods page.
    """
    _payment_method = PaymentMethod.query.get(payment_method_id)
    _payment_method.toggle()
    return redirect(url_for('admin.payment_methods'))


@admin.route('/company/toggle/twilio')
def toggle_twilio():
    """
    Toggles the twilio. (Enables/Disables)

    Returns:
        The company page.
    """
    _company = Company.query.first()
    _company.toggle_twilio()
    return redirect(url_for('admin.company'))

