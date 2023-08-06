from escpos import printer
from flask_login import current_user

from openwebpos.blueprints.admin.models import Company, Branch, NetworkPrinter, \
    USBPrinter
from openwebpos.blueprints.billing.models import Invoice, Payment
from openwebpos.blueprints.pos.models import OrderItem, OrderItemOption, \
    OrderSection, Order
from .money import cents_to_dollars


def test_printer():
    """
    Prints a test receipt.

    Returns:
        escpos.printer.Dummy: A dummy printer object.
    """
    p = printer.Dummy()
    return p


def network_printer(p_id):
    """
    Returns a network printer object.

    Args:
        p_id (int): The id of the printer to use.

    Returns:
        escpos.printer.Network: A network printer object.
    """
    try:
        np = NetworkPrinter.query.get(p_id)
        p = printer.Network(host=np.host, port=np.port, timeout=np.timeout)
    except Exception as e:
        print(e)
        p = printer.Dummy()
    return p


def usb_printer(p_id):
    """
    Returns a USB printer object.

    Args:
        p_id (int): The id of the printer to use.

    Returns:
        escpos.printer.Usb: A USB printer object.
    """
    try:
        usb_p = USBPrinter.query.get(p_id)
        p_vid = int(usb_p.idVendor, 16)
        usb_pid = int(usb_p.idProduct, 16)
        usb_timeout = usb_p.timeout
        usb_in_ep = int(usb_p.in_endpoint, 16)
        usb_out_ep = int(usb_p.out_endpoint, 16)
        p = printer.Usb(p_vid, usb_pid, timeout=usb_timeout, in_ep=usb_in_ep,
                        out_ep=usb_out_ep)
    except Exception as e:
        print(e)
        p = printer.Dummy()
    return p


def kitchen_receipt(order_id, p_type, p_id):
    """
    Prints a kitchen receipt for the given invoice id.

    Args:
        order_id (int): The id of the order to print.
        p_type (str): The type of printer to use. (network, usb, dummy)
        p_id (int): The id of the printer to use.

    Returns:
        None
    """

    purchases = []
    options = []
    receipt_width = 24

    # invoice = Invoice.query.get(invoice_id)
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    order_sections = OrderSection.query.filter_by(order_id=order_id).all()
    order = Order.query.filter_by(id=order_id).first()
    order_type = order.order_type.name

    if p_type == 'network':
        p = network_printer(p_id)
    elif p_type == 'usb':
        p = usb_printer(p_id)
    else:
        p = test_printer()

    if order_type == 'Dine In':
        if order.order_pager_id is not None:
            message = order.order_pager.short_name
        else:
            message = 'Dine In'
    else:
        message = order_type

    receipt_content = [
        'Kitchen'.center(receipt_width),
    ]

    order_divider = '-' * (receipt_width - 5)

    for order_section in order_sections:
        for order_item in order_items:
            if order_item.menu_item.menu_category.menu_type.name != 'Drink':
                if order_item.order_section_id == order_section.id:
                    item_options = []
                    item_addons = []

                    item_category = order_item.menu_item.menu_category.name
                    item_name = order_item.menu_item.name
                    item_quantity = order_item.quantity
                    section_id = order_item.order_section_id
                    if order_item.has_order_item_options or order_item.has_order_item_addons:
                        order_item_options = OrderItemOption.query.filter_by(
                            order_item_id=order_item.id).all()
                        for option in order_item_options:
                            ingredient_name = option.ingredient.name
                            option_type = option.option_type
                            item_options.append(
                                f'{option_type}: {ingredient_name}')
                    purchases.append(
                        (
                            item_category, item_name, item_quantity,
                            item_options,
                            item_addons, section_id))

    # order sections
    for order_section in order_sections:
        for purchase in purchases:
            if purchase[5] == order_section.id:
                line_item = f'{purchase[2]}x {purchase[0]} {purchase[1]}'
                if purchase[3] or purchase[4]:
                    for option in purchase[3]:
                        line_item += f'\n     {option}'
                    for addon in purchase[4]:
                        line_item += f'\n     {addon}'
                line = line_item.ljust(receipt_width)
                receipt_content.append(line)
        receipt_content.append(order_divider.center(receipt_width))

    # message
    receipt_content.append(message.center(receipt_width))
    # order number
    receipt_content.append(
        f'O#: {order.order_number[-6:]}'.center(receipt_width))

    if order.customer_id is not None:
        # customer phone
        c_phone = order.customer.phone
        receipt_content.append(
            f'C: ({c_phone[0:3]}) {c_phone[3:6]}-{c_phone[6:10]}'.center(
                receipt_width))

    p.set(height=3, width=3, font='b', text_type='B')
    p.text("\n".join(receipt_content))
    p.cut()
    p.close()


def customer_receipt(invoice_id, p_type, p_id):
    """
    Prints a customer receipt for the given invoice id.

    Args:
        invoice_id (int): The id of the invoice to print.
        p_type (str): The type of printer to use. (network, usb, dummy)
        p_id (int): The id of the printer to use.

    Returns:
        None
    """
    if p_type == 'network':
        p = network_printer(p_id)
    elif p_type == 'usb':
        p = usb_printer(p_id)
    else:
        p = test_printer()
    cu = current_user
    branch_id = cu.branch_id
    _branch = Branch.query.get(branch_id)
    invoice = Invoice.query.get(invoice_id)
    _company = Company.query.first()
    _invoice_due = invoice.due
    if _invoice_due <= 0:
        _invoice_due = 0
    _payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    _company_name = _company.name
    _company_address = _branch.address
    _company_city = _branch.city
    _company_state = _branch.state
    _company_zip = _branch.zip_code
    _company_phone = _branch.phone
    _company_email = _branch.email
    _order_date = Invoice.query.filter_by(
        id=invoice_id).first_or_404().created_at

    price = 0
    quantity = 0
    receipt_subtotal = 0
    purchases = []
    options = []
    receipt_width = 48

    shop_name = _company_name.title().center(receipt_width)
    shop_address = f'{_company_address}\n{_company_city}, {_company_state} {_company_zip}\n{_company_phone}'
    shop_address = shop_address.splitlines()
    order_date = f'{_order_date.strftime("%m/%d/%Y %I:%M %p")}'
    receipt_message = 'Thank you for your business!\nPlease come again!'
    receipt_message = receipt_message.splitlines()
    tax_percentage = invoice.order.tax_rate
    receipt_content = [
        shop_name,
        shop_address[0].center(receipt_width),
        shop_address[1].center(receipt_width),
        shop_address[2].center(receipt_width),
        '\n',
    ]

    order_items = OrderItem.query.filter_by(order_id=invoice.order_id).all()
    order_itme_options = OrderItemOption.query.filter_by(
        order_id=invoice.order_id).all()
    for order_item in order_items:
        order_item_id = order_item.id
        name = order_item.menu_item.menu_category.name + ' - ' + order_item.menu_item.name
        quantity = order_item.quantity
        price = cents_to_dollars(order_item.menu_item.price)
        total = cents_to_dollars(order_item.total)
        receipt_subtotal += price * quantity
        purchases.append((order_item_id, name, quantity, price, total), )

    for order_item_option in order_itme_options:
        order_item_id = order_item_option.order_item_id
        option_type = order_item_option.option_type
        ingredient_name = order_item_option.ingredient.name
        option_price = order_item_option.price
        options.append(
            (order_item_id, option_type, ingredient_name, option_price), )

    for order_item_id, name, quantity, price, total in purchases:
        line_subtotal = '$' + str(round(total, 2))
        purchase_line = f'{name}'.ljust(receipt_width - len(line_subtotal), '.')
        purchase_line += line_subtotal
        if type(quantity) is int and quantity >= 1:
            purchase_line += f'     {quantity} @ {price} /ea'
        if order_item_id in [option[0] for option in options]:
            for option in options:
                if order_item_id == option[0]:
                    purchase_line += f'\n     {option[1]}: {option[2]} @ {option[3]} /ea'
        receipt_content.append(purchase_line)

    receipt_subtotal = str(round(receipt_subtotal, 2))
    receipt_tax = str(round(float(receipt_subtotal) * 0.0825, 2))
    receipt_total = str(round(float(receipt_subtotal) + float(receipt_tax), 2))

    receipt_content.append('\n')
    receipt_content.append('    Subtotal: '.rjust(
        receipt_width - len(receipt_subtotal) - 1) + '$' + receipt_subtotal)
    receipt_content.append(f'    Tax ({tax_percentage})%: '.rjust(
        receipt_width - len(receipt_tax) - 2) + '$' + receipt_tax)
    receipt_content.append('    Total: '.rjust(
        receipt_width - len(receipt_total) - 1) + '$' + receipt_total)

    for payment in _payments:
        receipt_content.append('    Payment Method: '.rjust(
            receipt_width - len(
                receipt_total) - 2) + payment.payment_method.name)
        receipt_content.append('    Payment Amount: '.rjust(
            receipt_width - len(receipt_total) - 2) + '$' + str(
            cents_to_dollars(payment.amount)))
        if payment.change > 0:
            receipt_content.append('    Change: '.rjust(
                receipt_width - len(receipt_total) - 2) + '$' + str(
                payment.change))
        if _invoice_due > 0:
            receipt_content.append('    Due: '.rjust(
                receipt_width - len(receipt_total) - 2) + '$' + str(
                _invoice_due))

    receipt_content.append('\n'.ljust(receipt_width, '*'))
    receipt_content.append(receipt_message[0].center(receipt_width))
    receipt_content.append(receipt_message[1].center(receipt_width))
    receipt_content.append(f'{order_date}'.center(receipt_width))

    p.set(height=1, width=1)
    p.text("\n".join(receipt_content))
    p.cut()
    p.cashdraw(2)
    p.close()
