from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from openwebpos.blueprints.user.forms import UserProfileForm, AddUserForm
from openwebpos.blueprints.user.models import User, UserActivity, UserProfile

bp = Blueprint('user', __name__, url_prefix='/user', template_folder='../templates')


@bp.route('/list', methods=['GET', 'POST'])
def list_view():
    """
    Display a list of users
    """
    _users = User.query.all()
    form = AddUserForm()
    form.set_choices()
    if form.validate_on_submit():
        is_staff = False
        if form.role.data <= 6:
            is_staff = True
        _user = User(username=form.username.data,
                     email=form.email.data,
                     role_id=form.role.data, staff=is_staff)
        _user.set_password(form.password.data)
        _user.save()
        flash('User added successfully', 'success')
        return redirect(url_for('.list_view'))
    return render_template('admin/user/list.html', title='Users', users=_users, form=form)


@bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile_view(user_id):
    user = User.query.get_or_404(user_id)
    _user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    form = UserProfileForm(obj=_user_profile)
    if form.validate_on_submit():
        update_profile = UserProfile(user_id=user_id)
        form.populate_obj(update_profile)
        if _user_profile:
            update_profile.update()
        update_profile.save()
    return render_template('admin/user/profile.html', title='Use Profile',
                           user=user, form=form)


@bp.route('/activity/<int:user_id>')
def activity_view(user_id):
    """
    Displays the activity log for a user
    """
    user = User.query.get(user_id)
    user_activities = UserActivity.query.filter_by(user_id=user_id).all()
    return render_template('admin/user/activity.html', title='User Activity',
                           user=user, user_activities=user_activities)


@bp.route('/delete/<int:user_id>')
def delete_view(user_id):
    """
    Delete a user
    """
    # Check if more than one admin user exists
    _user = User.query.get(user_id)
    _admin_users = User.query.filter_by(role_id=1).all()
    if len(_admin_users) == 1 and _user.role_id == 1:
        flash('Cannot delete the last admin user', 'danger')

    # Check if user is logged in
    elif _user.id == current_user.id:
        flash('Cannot delete the currently logged in user', 'danger')

    # Check if user has any orders associated with them and prevent deletion
    elif _user.orders:
        flash('Cannot delete user with orders', 'danger')
        flash('Making user inactive instead', 'info')
        _user.make_inactive()

    else:
        _user.delete()
        flash('User deleted successfully', 'success')

    return redirect(url_for('admin.user.list_view'))


@bp.route('/toggle/<int:user_id>/active')
def toggle_active_view(user_id):
    """
    Toggle a user between active and inactive

    Params:
        user_id: The id of the user to toggle
    """
    _user = User.query.get_or_404(user_id)
    if not _user.query.count() == 1:
        _user.toggle_active()
        flash('User activated successfully', 'success')
    else:
        flash('Cannot deactivate the last user', 'danger')
    return redirect(url_for('.list_view'))


@bp.route('/toggle/<int:user_id>/staff')
def toggle_staff_view(user_id):
    """
    Toggle a user between staff and not staff

    Params:
        user_id: The id of the user to toggle
    """
    _user = User.query.get_or_404(user_id)
    if _user.is_last_staff():
        flash('Cannot deactivate the last staff member', 'danger')
    else:
        _user.toggle_staff()
        flash('User staff status toggled successfully', 'success')
    return redirect(url_for('.list_view'))
