import usb
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from openwebpos.blueprints.admin.models import Company
from openwebpos.blueprints.billing.forms import PaymentAmountForm
from openwebpos.blueprints.billing.models import PaymentMethod, Payment, Invoice
from openwebpos.blueprints.customer.forms import PhoneSearchForm
from openwebpos.blueprints.customer.models import Customer
from openwebpos.blueprints.user.decorators import role_require
from openwebpos.utils.money import dollars_to_cents
from openwebpos.utils.printers import kitchen_receipt, customer_receipt
from openwebpos.utils.twilio import send_message
from .forms import QuantityForm, AddItemToOrderForm
from .models import (
    MenuType, MenuCategory, MenuItem, OrderType, Order, OrderItem,
    MenuItemIngredient, OrderItemOption, Ingredient, MenuItemAddon, OrderPager,
    OrderSection)

pos = Blueprint('pos', __name__, template_folder='templates', url_prefix='/pos')


@pos.before_request
@login_required
@role_require('Administrator', 'Manager', 'Cashier')
def before_request():
    """
    Protects all the pos endpoints.
    """
    pass


def send_text_message(order_id, to_number, message):
    """
    Sends a text receipt to the customer.
    """
    import os
    from twilio.rest import Client

    _order = Order.query.get(order_id)

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    number = os.environ.get('TWILIO_NUMBER')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'{message}\nYour order number is {_order.order_number}\nSubTotal: ${_order.subtotal}\nTax: ${_order.tax_total}\nTotal: ${_order.total}',
        from_=number,
        to=to_number
    )

    print(message.sid)


@pos.route('/text/<phone_number>/<int:order_id>/<message>')
def text(phone_number, order_id=None, message=None):
    """
    Sends a text message to the customer.

    Args:
        phone_number (str): The phone number to send the message to.
        order_id (int): The order id to send the message for.
        message (str): The message to send to the customer.

    Returns:
        Redirects to the order page.

    Examples:
        >>> text('+15555555555', 1, 'Your order is ready!')
    """
    if message is None:
        # TODO: Add a default message.
        message = 'Thank you for your order!'
    if order_id is None:
        # TODO: Add a default order id.
        order_id = 1
    send_text_message(order_id, phone_number, message)
    return 'sent'


@pos.get('/print/<int:order_id>/<string:receipt_type>')
def print_receipt(order_id, receipt_type):
    """
    Prints a test receipt.
    """
    _order = Order.query.get(order_id)
    active_twilio = Company.query.first().active_twilio
    if receipt_type == 'kitchen':
        if _order.is_printed():
            _order.update_print_count()
        else:
            _order.set_printed()
            _order.update_print_count()
            if active_twilio:
                if _order.has_customer() and _order.order_type.name == 'Phone':
                    send_message(order_id, _order.customer.phone_number,
                                 'Your order is ready!')
        kitchen_receipt(order_id, 'usb', 1)
    elif receipt_type == 'customer':
        customer_receipt(order_id, 'usb', 1)
        _order.update_print_count()
    return redirect(url_for('pos.index'))


@pos.route('/')
def index():
    """
    POS index page.

    Returns:
        The POS index page.(pos/index.html)
    """
    active_order_types = OrderType.query.filter_by(active=True).all()
    active_orders = Order.query.filter_by(active=True).all()
    pagers = OrderPager.query.filter_by(active=True, in_use=False).all()
    if active_orders:
        # Check if there is an active order.
        return render_template('pos/active_orders.html', title='Active Orders',
                               active_orders=active_orders, pagers=pagers,
                               order_types=active_order_types)
    return render_template('pos/index.html', title='POS',
                           order_types=active_order_types, pagers=pagers)


@pos.route('/usb-printers')
def usb_printers():
    """
    USB Printers page.

    Returns:
        The USB Printers page.(pos/usb_printers.html)
    """
    printers = usb.core.find(idVendor=0x0fe6, idProduct=0x811e, find_all=True)
    for printer in printers:
        print(printer)
    return 'ok'


@pos.route('/create/<int:order_type_id>')
def create_order(order_type_id):
    """
    Creates a new order.

    Args:
        order_type_id (int): The order type id.

    Returns:
        Redirects to the POS index page.(pos/order.html)
    """
    order_type = OrderType.query.get(order_type_id)
    _order = Order(order_type=order_type, user_id=current_user.id)
    _order.save()
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.route('/create/order_section/<int:order_id>')
def create_order_section(order_id):
    """
    Creates a new order section.

    Args:
        order_id (int): The order id.

    Returns:
        Redirects to the POS order page.(pos/order.html)
    """
    _order = Order.query.get(order_id)
    _order_section = OrderSection.query.filter_by(order_id=order_id)[-1]
    print(_order_section)
    if _order_section.has_items():
        _order.create_order_section()
    else:
        flash(
            'You must add items to the section before creating a new section.',
            'red')
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.get('/create/<int:order_type_id>/<int:order_pager_id>')
def create_order_with_pager(order_type_id, order_pager_id):
    """
    Creates a new order with a pager.

    Args:
        order_type_id (int): The order type id.
        order_pager_id (int): The order pager id.

    Returns:
        Redirects to the POS order page.(pos/order.html)
    """
    order_type = OrderType.query.get(order_type_id)
    order_pager = OrderPager.query.get(order_pager_id)
    _order = Order(order_type=order_type, order_pager=order_pager,
                   user_id=current_user.id)
    _order.save()
    order_pager.toggle_in_use()
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.route('/order/<int:order_id>')
def order(order_id):
    """
    Displays the order page.

    Args:
        order_id (int): The order id.

    Returns:
        The order page.(pos/order.html)
    """
    _order = Order.query.get(order_id)
    _order_sections = OrderSection.query.filter_by(order_id=_order.id).all()
    _last_order_section = _order_sections[-1]
    _menu_types = MenuType.query.filter_by(active=True).all()
    _menu_categories = MenuCategory.query.filter_by(active=True).all()
    _order_items = OrderItem.query.filter_by(order_id=_order.id).all()
    _menu_item_ingredients = MenuItemIngredient.query.all()
    _menu_item_addons = MenuItemAddon.query.all()
    _ingredients = Ingredient.query.all()
    order_number = _order.order_number
    form = QuantityForm()
    phone_search_form = PhoneSearchForm()
    return render_template('pos/order.html', title='Order', order=_order,
                           menu_types=_menu_types, order_items=_order_items,
                           menu_item_ingredients=_menu_item_ingredients,
                           ingredients=_ingredients, form=form,
                           phone_search_form=phone_search_form,
                           menu_item_addons=_menu_item_addons,
                           order_sections=_order_sections,
                           last_order_section=_last_order_section,
                           menu_categories=_menu_categories, order_number=order_number)


@pos.route('<int:order_item_id>/item-ingredients/<int:item_id>')
def item_ingredients_view(item_id, order_item_id):
    _menu_item_ingredients = MenuItemIngredient.query.all()
    _ingredients = []
    option_type = request.args.get('option_type')
    for item_ingredient in _menu_item_ingredients:
        if item_ingredient.menu_item_id == item_id:
            _ingredients.append(item_ingredient.ingredient)
    option_color = ''
    if option_type == 'NO':
        option_color = 'red darken-1'
    elif option_type == 'Extra':
        option_color = 'green darken-1'
    return render_template('pos/item_ingredients.html', title='Item Ingredients', ingredients=_ingredients,
                           order_item_id=order_item_id, option_type=option_type, option_color=option_color)


@pos.route('/<int:order_item_id>/item-addons/<int:item_id>')
def item_addons_view(item_id, order_item_id):
    _menu_item_addons = MenuItemAddon.query.all()
    _addons = []
    option_type = request.args.get('option_type')
    for item_addon in _menu_item_addons:
        if item_addon.menu_item_id == item_id:
            _addons.append(item_addon.ingredient)
    option_color = ''
    if option_type == 'NO':
        option_color = 'red darken-1'
    elif option_type == 'Extra':
        option_color = 'green darken-1'
    return render_template('pos/item_addons.html', title='Item Addons', addons=_addons, item_id=item_id,
                           order_item_id=order_item_id, option_type=option_type, option_color=option_color)


@pos.get('/order/<int:order_id>/toggle')
def toggle_order(order_id):
    """
    Toggles the active status of an order.

    Args:
        order_id (int): The order id.

    Returns:
        Redirects to the POS index page.(pos/index.html)
    """
    _order = Order.query.get(order_id)
    if _order.order_pager:
        _order.order_pager.toggle_in_use()
    _order.toggle()

    return redirect(url_for('pos.index'))


@pos.get('/order/<int:order_id>/delete')
def delete_order(order_id):
    """
    Deletes an order.

    Args:
        order_id (int): The order id.

    Returns:
        Redirects to the POS index page.(pos/index.html)
    """
    _order = Order.query.get(order_id)
    _order_pager = OrderPager.query.get(_order.order_pager_id)
    if _order_pager:
        _order_pager.toggle_in_use()
    _order.delete()
    return redirect(url_for('pos.index'))


# @pos.route('/order/<int:order_id>/<int:menu_type_id>')
# def order_menu_type(order_id, menu_type_id):
#     """
#     Displays the order page for a specific menu type.
#
#     Args:
#         order_id (int): The order id.
#         menu_type_id (int): The menu type id.
#
#     Returns:
#         The order menu type page. (order_menu_type.html)
#     """
#     _order = Order.query.get(order_id)
#     _menu_type = MenuType.query.get(menu_type_id)
#     _menu_categories = MenuCategory.query.filter_by(
#         menu_type_id=menu_type_id, active=True).all()
#     return render_template('pos/order_menu_type.html', title='Order',
#                            order=_order, menu_type=_menu_type,
#                            menu_categories=_menu_categories)


# @pos.route('/order/<int:order_id>/<int:menu_type_id>/<int:menu_category_id>')
# def order_menu_category(order_id, menu_type_id, menu_category_id):
#     """
#     Displays the order page for a specific menu category.
#
#     Args:
#         order_id (int): The order id.
#         menu_type_id (int): The menu type id.
#         menu_category_id (int): The menu category id.
#
#     Returns:
#         The order menu category page. (order_menu_category.html)
#     """
#     _order = Order.query.get(order_id)
#     _menu_type = MenuType.query.get(menu_type_id)
#     _menu_category = MenuCategory.query.get(menu_category_id)
#     _menu_items = MenuItem.query.filter_by(
#         menu_category_id=menu_category_id, active=True).all()
#     form = QuantityForm()
#     return render_template('pos/order_menu_category.html', title='Order',
#                            order=_order, menu_type=_menu_type,
#                            menu_category=_menu_category, menu_items=_menu_items,
#                            form=form)


@pos.route('/<string:order_number>/<string:category_slug>/items', methods=['GET', 'POST'])
def menu_items(category_slug, order_number):
    """
    Displays the menu items for a specific menu category.

    Args:
        category_slug (str): The menu category id.
        order_number (str): The order number.

    Returns:
        The menu items page. (menu_items.html)
    """

    _order = Order.query.filter_by(order_number=order_number).first()
    category_id = MenuCategory.query.filter_by(slug=category_slug).first().id
    _menu_items = MenuItem.query.filter_by(menu_category_id=category_id, active=True).all()
    _order_sections = OrderSection.query.filter_by(order_id=_order.id).all()
    _last_order_section = _order_sections[-1]
    form = AddItemToOrderForm()
    if form.validate_on_submit():
        item_id = form.menu_item_id.data
        ordered_quantity = form.quantity.data
        ordered_item = OrderItem(order_id=_order.id, menu_item_id=item_id, quantity=ordered_quantity,
                                 order_section_id=_last_order_section.id)
        ordered_item.save()
        _order.update_totals()
        return redirect(url_for('pos.order', order_id=_order.id))
    return render_template('pos/menu_items.html', title='Menu Items',
                           menu_items=_menu_items, order_number=order_number, form=form)


# @pos.post('/order/add_item/<int:order_id>/<int:menu_item_id>')
# def order_add_item(order_id, menu_item_id):
#     """
#     Adds an item to an order.
#
#     Args:
#         order_id (int): The order id.
#         menu_item_id (int): The menu item id.
#
#     Returns:
#         Redirects to the order page.(pos/order.html)
#     """
#     _order = Order.query.get(order_id)
#     _menu_item = MenuItem.query.get(menu_item_id)
#     _order_sections = OrderSection.query.filter_by(order_id=_order.id).all()
#     _last_order_section = _order_sections[-1]
#     form = QuantityForm()
#     if form.validate_on_submit():
#         _order_item = OrderItem(order_id=order_id, menu_item_id=_menu_item.id,
#                                 quantity=form.quantity.data,
#                                 order_section_id=_last_order_section.id)
#         _order_item.save()
#         _order.update_totals()
#     return redirect(url_for('pos.order', order_id=_order.id))


@pos.post('/order/update_quantity/<int:order_item_id>')
def update_quantity(order_item_id):
    """
    Updates an item in an order.

    Args:
        order_item_id (int): The order item id.

    Returns:
        Redirects to the order page.(pos/order.html)
    """
    _order_item = OrderItem.query.get(order_item_id)
    form = QuantityForm()
    if form.validate_on_submit():
        _order_item.update_quantity(form.quantity.data)
        _order_item.order.update_totals()
    return redirect(url_for('pos.order', order_id=_order_item.order_id))


@pos.get('/order/remove_item/<int:order_item_id>')
def order_remove_item(order_item_id):
    """
    Removes an item from an order.

    Args:
        order_item_id (int): The order item id.

    Returns:
        Redirects to the order page.(pos/order.html)
    """
    _order_item = OrderItem.query.get(order_item_id)
    _order_item_section = OrderSection.query.filter_by(
        order_id=_order_item.order_id).all()
    _order = Order.query.get(_order_item.order_id)
    _order_item.delete()
    _order.update_totals()
    for section in _order_item_section:
        if not section.has_items() and not section.last_section():
            section.delete()
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.route(
    '/order/add_order_item_option/<int:order_item_id>/<int:ingredient_id>/<string:option_type>/<string:option_price>')
def order_add_order_item_option(order_item_id, ingredient_id, option_type,
                                option_price):
    """
    Adds an option to an order item.

    Args:
        order_item_id (int): The order item id.
        ingredient_id (int): The menu item ingredient id.
        option_type (str): The option type.
        option_price (str): The option price.

    Returns:
        Redirects to the order page.(pos/order.html)
    """
    _order_item = OrderItem.query.get(order_item_id)
    _order = Order.query.get(_order_item.order_id)
    _order_item_option = OrderItemOption(
        order_id=_order.id, order_item_id=_order_item.id,
        ingredient_id=ingredient_id, option_type=option_type,
        price=option_price)
    _order_item_option.save()
    _order_item.update_totals()
    _order.update_totals()
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.post('/order/add_customer/<int:order_id>')
def order_add_customer(order_id):
    """
    Adds a customer to an order.

    Args:
        order_id (int): The order id.

    Returns:
        Redirects to the order page.(pos/order.html)
    """
    _order = Order.query.get(order_id)
    form = PhoneSearchForm()
    if form.validate_on_submit():
        _customer = Customer.query.filter_by(phone=form.phone.data).first()
        if _customer:
            _order.customer_id = _customer.id
            _order.update()
        else:
            _customer = Customer(phone=form.phone.data)
            _customer.save()
            _order.customer_id = _customer.id
            _order.update()
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.get('/invoice/order/<int:order_id>')
def invoice_order(order_id):
    """
    Invoice an order.

    Args:
        order_id (int): The order id.

    Returns:
        Redirects to the invoice page.(pos/invoice.html)
    """
    _order = Order.query.get(order_id)
    active_twilio = Company.query.first().active_twilio

    if not _order.has_items():
        return redirect(url_for('pos.order', order_id=_order.id))

    # Check if the order has already been invoiced.
    if _order.is_invoiced():
        return redirect(url_for('.invoice', invoice_id=_order.invoice.id))

    _invoice = Invoice(order_id=_order.id, tax=_order.tax_total,
                       subtotal=_order.subtotal, total=_order.total,
                       due=_order.total)
    _invoice.save()
    _order.set_invoiced()
    if not _order.is_printed():
        kitchen_receipt(_order.id, 'usb', 1)
        _order.set_printed()
        if active_twilio:
            if _order.customer_id and _order.order_type.name == 'Phone':
                order_created_message = f'Your order has been created.\n Your order total is $ {_order.total}\n\n For faster service, please pay online at https://www.ourwebsite.com/pay/{_order.order_number}'
                send_message(order_id, _order.customer.phone,
                             message=order_created_message)
    return redirect(url_for('.invoice', invoice_id=_invoice.id))


@pos.route('/invoice/<int:invoice_id>')
def invoice(invoice_id):
    """
    Displays an invoice.

    Args:
        invoice_id (int): The invoice id.

    Returns:
        The invoice page. (invoice.html)
    """
    _invoice = Invoice.query.get(invoice_id)
    _payment_methods = PaymentMethod.query.filter_by(active=True).all()
    _payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    form = PaymentAmountForm()
    return render_template('pos/invoice.html', title='Invoice', form=form,
                           invoice=_invoice, payment_methods=_payment_methods,
                           payments=_payments)


@pos.post('/payment/<int:invoice_id>')
def payment(invoice_id):
    """
    Adds a payment to an invoice.

    Args:
        invoice_id (int): The invoice id.

    Returns:
        Redirects to the invoice page.(pos/invoice.html)
    """
    _invoice = Invoice.query.get(invoice_id)
    form = PaymentAmountForm()
    payment_method_id = request.form.get('payment_method_id')
    if form.validate_on_submit():
        _payment = Payment(invoice_id=invoice_id,
                           amount=dollars_to_cents(form.amount.data),
                           payment_method_id=payment_method_id)
        _payment.save()
        _payment.update_invoice_due()
        if _invoice.due <= 0:
            customer_receipt(_invoice.id, p_type='usb', p_id=1)
            if _invoice.order.customer_id and _invoice.order.order_type.name == 'Phone':
                order_paid_message = f'Your order has been paid.\n here is your digital receipt https://www.mywebsite.com/receipts/{_invoice.receipt_number}\n\n Thank you for your business!'
                send_message(_invoice.order.id, _invoice.order.customer.phone,
                             message=order_paid_message)
    return redirect(url_for('pos.invoice', invoice_id=invoice_id))


@pos.post('/order/pay/<int:order_id>/<int:payment_method_id>')
def order_pay_method(order_id, payment_method_id):
    """
    Pays an order with a payment method.

    Args:
        order_id (int): The order id.
        payment_method_id (int): The payment method id.

    Returns:
        Redirects to the order page.(pos/order.html)
    """
    _order = Order.query.get(order_id)
    _payment_method = PaymentMethod.query.get(payment_method_id)
    form = PaymentAmountForm()
    if form.validate_on_submit():
        _payment = Payment(invoice_id=order_id,
                           payment_method_id=_payment_method.id,
                           amount=form.amount.data)
        _payment.save()
        _order.update_totals()
        if _payment.amount >= _order.total:
            _order.set_paid()
            order_total = _order.subtotal + _order.tax_total
            _invoice = Invoice(order_id=_order.id, tax=_order.tax_total,
                               subtotal=_order.subtotal, total=order_total)
            _invoice.save()
            return redirect(url_for('pos.order', order_id=_order.id))
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.get('/open_register')
def open_register():
    """
    Opens the register.

    Returns:
        Redirects to the register page.(pos/register.html)
    """
    open_register()
    return redirect(url_for('pos.index'))
