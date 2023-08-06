from flask import Blueprint, render_template, redirect, url_for

from openwebpos.blueprints.pos.forms import OrderPagerForm
from openwebpos.blueprints.pos.models import OrderType, OrderPager, Order

bp = Blueprint('order', __name__, url_prefix='/order',
               template_folder='../templates')


@bp.route('/')
def index():
    """
    Displays the order page.
    """
    _orders = Order.query.all()
    return render_template('admin/order/index.html', title='Order', orders=_orders)


@bp.route('/types')
def types():
    o_types = OrderType.query.all()
    return render_template('admin/order/types.html', title='Order Types',
                           o_types=o_types)


@bp.route('/types/toggle/<int:ot_id>')
def toggle_type(ot_id):
    OrderType.query.get(ot_id).toggle()
    return redirect(url_for('.types'))


@bp.route('/pagers')
def pagers():
    o_pagers = OrderPager.query.all()
    return render_template('admin/order/pagers.html', title='Order Pagers',
                           o_pagers=o_pagers)


@bp.route('/pagers/add', methods=['GET', 'POST'])
def add_pager():
    form = OrderPagerForm()
    if form.validate_on_submit():
        op = OrderPager()
        form.populate_obj(op)
        op.save()
        return redirect(url_for('.pagers'))
    return render_template('admin/order/add_pager.html',
                           title='Add Order Pager', form=form)


@bp.route('/pagers/edit/<int:op_id>', methods=['GET', 'POST'])
def edit_pager(op_id):
    op = OrderPager.query.get(op_id)
    form = OrderPagerForm(obj=op)
    if form.validate_on_submit():
        form.populate_obj(op)
        op.save()
        return redirect(url_for('.pagers'))
    return render_template('admin/order/edit_pager.html',
                           title='Edit Order Pager', form=form)


@bp.get('/pagers/toogle/<int:op_id>')
def toggle_pager(op_id):
    OrderPager.query.get(op_id).toggle()
    return redirect(url_for('.pagers'))


@bp.get('/pagers/delete/<int:op_id>')
def delete_pager(op_id):
    OrderPager.query.get(op_id).delete()
    return redirect(url_for('.pagers'))
