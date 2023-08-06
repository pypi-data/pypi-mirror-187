from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from .forms import LoginForm
from .models import User, UserActivity

user = Blueprint('user', __name__, template_folder='templates',
                 url_prefix='/user/')


@user.before_request
def before_request():
    pass


@user.get('/login')
def login():
    """
    Login page.

    Returns:
        Rendered the login page.(user/login.html)
    """
    # redirect to the index page if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pos.index'))
    form = LoginForm()
    return render_template('user/login.html', form=form, title='Login')


@user.post('/login')
def login_post():
    """
    Handle the POST request for the login form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        _user = User.query.filter_by(username=form.username.data).first_or_404()
        _user_activity = UserActivity.query.filter_by(user_id=_user.id).first_or_404()
        # check if the user exists and if the password is correct
        if _user is None or not _user.check_password(form.password.data):
            flash('Invalid username or password', 'red')
            return redirect(url_for('user.login'))
        # Check if the user has an activity record if not create one
        if _user_activity is None:
            user_agent = request.headers.get('User-Agent')
            referrer = request.referrer
            _user_activity = UserActivity(user_id=_user.id,
                                          user_agent=user_agent,
                                          referrer=referrer)
            _user_activity.save()

        # Log the user in and redirect to the index page
        login_user(_user, remember=False)

        # Update the user activity
        _user_activity.update_activity(request.remote_addr, _user.id)

        # Redirect to the next page if it is set
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('pos.index')
        return redirect(next_page)
    return redirect(url_for('pos.index'))


@user.get('/logout')
@login_required
def logout():
    """
    Handle the logout request.

    Returns:
        Redirect to the login page.(user/login.html)
    """
    # Logout the user.
    logout_user()
    flash('You have been logged out.', 'green')
    return redirect(url_for('user.login'))
