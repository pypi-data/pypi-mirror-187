from flask import Blueprint, render_template, redirect, url_for

from ..forms import USBPrinterForm, NetworkPrinterForm
from ..models import USBPrinter, NetworkPrinter

bp = Blueprint('printer', __name__, template_folder='../templates',
               url_prefix='/printer')


@bp.route('/')
def index():
    """
    Displays the printers page.
    """
    return render_template('admin/printer/index.html', title='Printers')


@bp.route('/usb', methods=['GET', 'POST'])
def usb_view():
    """USB printer view."""
    printers = USBPrinter.query.all()
    return render_template('admin/printer/usb.html', title='USB Printers',
                           printers=printers)


@bp.route('/usb/add', methods=['GET', 'POST'])
def usb_add():
    """USB printer add view."""
    form = USBPrinterForm()
    form.set_choices()
    if form.validate_on_submit():
        printer = USBPrinter()
        form.populate_obj(printer)
        printer.save()
        return redirect(url_for('.usb_view'))
    return render_template('admin/printer/usb_add.html',
                           title='Add USB Printer', form=form)


@bp.route('/usb/edit/<int:p_id>', methods=['GET', 'POST'])
def usb_edit(p_id):
    """USB printer edit view."""
    printer = USBPrinter.query.get_or_404(p_id)
    form = USBPrinterForm(obj=printer)
    form.set_choices()
    if form.validate_on_submit():
        form.populate_obj(printer)
        printer.update()
        return redirect(url_for('.usb_view'))
    return render_template('admin/printer/usb_edit.html',
                           title='Edit USB Printer', form=form)


@bp.route('/usb/delete/<int:p_id>', methods=['GET', 'POST'])
def usb_delete(p_id):
    """USB printer delete view."""
    printer = USBPrinter.query.get_or_404(p_id)
    printer.delete()
    return redirect(url_for('.usb_view'))


@bp.get('/usb/toggle/<int:p_id>')
def usb_toggle(p_id):
    """USB printer toggle view."""
    printer = USBPrinter.query.get_or_404(p_id)
    printer.toggle()
    return redirect(url_for('.usb_view'))


@bp.get('/network')
def network_view():
    """Network printer view."""
    printers = NetworkPrinter.query.all()
    return render_template('admin/printer/network.html',
                           title='Network Printers', printers=printers)


@bp.route('/network/add', methods=['GET', 'POST'])
def network_add():
    """Network printer add view."""
    form = NetworkPrinterForm()
    form.set_choices()
    if form.validate_on_submit():
        printer = NetworkPrinter()
        form.populate_obj(printer)
        printer.save()
        return redirect(url_for('.network_view'))
    return render_template('admin/printer/network_add.html',
                           title='Add Network Printer', form=form)


@bp.route('/network/edit/<int:p_id>', methods=['GET', 'POST'])
def network_edit(p_id):
    """Network printer edit view."""
    printer = NetworkPrinter.query.get_or_404(p_id)
    form = NetworkPrinterForm(obj=printer)
    form.set_choices()
    if form.validate_on_submit():
        form.populate_obj(printer)
        printer.update()
        return redirect(url_for('.network_view'))
    return render_template('admin/printer/network_edit.html',
                           title='Edit Network Printer', form=form)


@bp.route('/network/delete/<int:p_id>', methods=['GET', 'POST'])
def network_delete(p_id):
    """Network printer delete view."""
    printer = NetworkPrinter.query.get_or_404(p_id)
    printer.delete()
    return redirect(url_for('.network_view'))


@bp.get('/network/toggle/<int:p_id>')
def network_toggle(p_id):
    """Network printer toggle view."""
    printer = NetworkPrinter.query.get_or_404(p_id)
    printer.toggle()
    return redirect(url_for('.network_view'))
